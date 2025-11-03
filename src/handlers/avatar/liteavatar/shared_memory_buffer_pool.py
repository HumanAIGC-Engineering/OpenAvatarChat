"""
SharedMemory Buffer Pool for cross-process audio/video data transmission.

This module provides a buffer pool management system using multiprocessing.shared_memory
to safely transfer large audio and video data between processes without triggering
PyTorch's automatic shared memory mechanism that can cause Bus errors.
"""

import atexit
import weakref
from dataclasses import dataclass
from multiprocessing import Queue, shared_memory
import multiprocessing as mp
from typing import List, Tuple, Optional
from loguru import logger
import uuid


@dataclass
class SharedMemoryDataPacket:
    """
    Metadata packet for shared memory data transmission.
    This is sent through multiprocessing.Queue instead of the actual data.
    """
    buffer_index: int       # Index in the buffer pool
    shm_name: str          # Shared memory name
    data_size: int         # Actual data size in bytes
    shape: Tuple[int, ...]  # numpy array shape
    dtype: str             # numpy dtype as string
    buffer_type: str       # 'audio' or 'video'


class SharedMemoryBufferPool:
    """
    Manages two separate buffer pools for audio and video data transmission
    between processes using shared memory.
    
    Features:
    - Pre-allocated fixed-size buffers for audio and video
    - Thread-safe buffer acquisition and release
    - Automatic cleanup on exit using atexit and weakref
    - Handles variable-size data within maximum buffer size
    """
    
    def __init__(self, 
                 audio_pool_size: int,
                 video_pool_size: int,
                 max_audio_size: int,
                 max_video_size: int,
                 create_mode: bool = True,
                 shm_names: Optional[dict] = None,
                 audio_available_queue=None,
                 video_available_queue=None):
        """
        Initialize the buffer pool.
        
        Args:
            audio_pool_size: Number of audio buffers to pre-allocate
            video_pool_size: Number of video buffers to pre-allocate
            max_audio_size: Maximum size in bytes for each audio buffer
            max_video_size: Maximum size in bytes for each video buffer
            create_mode: If True, create new shared memory. If False, attach to existing.
            shm_names: Dictionary with 'audio' and 'video' lists of shared memory names (for attach mode)
        """
        self.audio_pool_size = audio_pool_size
        self.video_pool_size = video_pool_size
        self.max_audio_size = max_audio_size
        self.max_video_size = max_video_size
        self.create_mode = create_mode
        
        # Storage for SharedMemory objects
        self.audio_buffers: List[Optional[shared_memory.SharedMemory]] = []
        self.video_buffers: List[Optional[shared_memory.SharedMemory]] = []
        
        # Queues to track available buffer indices (shared across processes)
        if audio_available_queue is not None:
            self.audio_available = audio_available_queue
        else:
            self.audio_available = mp.Queue()
        
        if video_available_queue is not None:
            self.video_available = video_available_queue
        else:
            self.video_available = mp.Queue()
        
        # Track if cleanup has been registered
        self._cleanup_registered = False
        self._is_cleaned_up = False
        
        if create_mode:
            self._init_audio_pool()
            self._init_video_pool()
        else:
            if shm_names is None:
                raise ValueError("shm_names must be provided in attach mode")
            self._attach_audio_pool(shm_names.get('audio', []))
            self._attach_video_pool(shm_names.get('video', []))
        
        if create_mode:
            self._register_cleanup()
        
        logger.info(
            f"SharedMemoryBufferPool {'created' if create_mode else 'attached'}: "
            f"audio={audio_pool_size}x{max_audio_size/1024:.1f}KB, "
            f"video={video_pool_size}x{max_video_size/1024/1024:.1f}MB"
        )
    
    def _init_audio_pool(self):
        """Initialize the audio buffer pool."""
        logger.info(f"Initializing audio buffer pool with {self.audio_pool_size} buffers")
        for i in range(self.audio_pool_size):
            try:
                # Create unique name for shared memory
                shm_name = f"audio_buf_{uuid.uuid4().hex[:16]}"
                shm = shared_memory.SharedMemory(
                    name=shm_name,
                    create=True,
                    size=self.max_audio_size
                )
                self.audio_buffers.append(shm)
                self.audio_available.put(i)
                logger.debug(f"Created audio buffer {i}: {shm_name}")
            except Exception as e:
                logger.error(f"Failed to create audio buffer {i}: {e}")
                self.audio_buffers.append(None)
    
    def _init_video_pool(self):
        """Initialize the video buffer pool."""
        logger.info(f"Initializing video buffer pool with {self.video_pool_size} buffers")
        for i in range(self.video_pool_size):
            try:
                # Create unique name for shared memory
                shm_name = f"video_buf_{uuid.uuid4().hex[:16]}"
                shm = shared_memory.SharedMemory(
                    name=shm_name,
                    create=True,
                    size=self.max_video_size
                )
                self.video_buffers.append(shm)
                self.video_available.put(i)
                logger.debug(f"Created video buffer {i}: {shm_name}")
            except Exception as e:
                logger.error(f"Failed to create video buffer {i}: {e}")
                self.video_buffers.append(None)
    
    def _attach_audio_pool(self, shm_names: List[str]):
        """Attach to existing audio buffer pool."""
        logger.info(f"Attaching to audio buffer pool with {len(shm_names)} buffers")
        for i, shm_name in enumerate(shm_names):
            try:
                shm = shared_memory.SharedMemory(name=shm_name, create=False)
                self.audio_buffers.append(shm)
                logger.debug(f"Attached to audio buffer {i}: {shm_name}")
            except Exception as e:
                logger.error(f"Failed to attach to audio buffer {i} ({shm_name}): {e}")
                self.audio_buffers.append(None)
        logger.info(f"Audio attached: {len(self.audio_buffers)} buffers, queue: {self.audio_available.qsize()}")
    
    def _attach_video_pool(self, shm_names: List[str]):
        """Attach to existing video buffer pool."""
        logger.info(f"Attaching to video buffer pool with {len(shm_names)} buffers")
        for i, shm_name in enumerate(shm_names):
            try:
                shm = shared_memory.SharedMemory(name=shm_name, create=False)
                self.video_buffers.append(shm)
                logger.debug(f"Attached to video buffer {i}: {shm_name}")
            except Exception as e:
                logger.error(f"Failed to attach to video buffer {i} ({shm_name}): {e}")
                self.video_buffers.append(None)
    
    def get_shm_names(self) -> dict:
        """
        Get the names of all shared memory buffers.
        Used to pass to child processes for attachment.
        
        Returns:
            Dictionary with 'audio' and 'video' lists of shared memory names
        """
        audio_names = [shm.name if shm is not None else None for shm in self.audio_buffers]
        video_names = [shm.name if shm is not None else None for shm in self.video_buffers]
        return {
            'audio': audio_names,
            'video': video_names
        }
    
    def acquire_audio_buffer(self, timeout: Optional[float] = 5.0) -> Tuple[int, str, int]:
        """
        Acquire an available audio buffer from the pool.
        
        Args:
            timeout: Maximum time to wait for an available buffer (seconds)
            
        Returns:
            Tuple of (buffer_index, shm_name, buffer_size)
            
        Raises:
            TimeoutError: If no buffer becomes available within timeout
            RuntimeError: If buffer pool is not initialized
        """
        if self._is_cleaned_up:
            raise RuntimeError("Buffer pool has been cleaned up")
        
        logger.debug(f"Attempting to acquire audio buffer, queue size: {self.audio_available.qsize()}")
        try:
            index = self.audio_available.get(timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to acquire audio buffer: {e}, queue size: {self.audio_available.qsize()}")
            raise TimeoutError(f"No audio buffer available within {timeout}s") from e
        
        shm = self.audio_buffers[index]
        if shm is None:
            logger.error(f"Audio buffer {index} is None")
            raise RuntimeError(f"Audio buffer {index} is not initialized")
        
        return index, shm.name, self.max_audio_size
    
    def acquire_video_buffer(self, timeout: Optional[float] = 5.0) -> Tuple[int, str, int]:
        """
        Acquire an available video buffer from the pool.
        
        Args:
            timeout: Maximum time to wait for an available buffer (seconds)
            
        Returns:
            Tuple of (buffer_index, shm_name, buffer_size)
            
        Raises:
            TimeoutError: If no buffer becomes available within timeout
            RuntimeError: If buffer pool is not initialized
        """
        if self._is_cleaned_up:
            raise RuntimeError("Buffer pool has been cleaned up")
        
        try:
            index = self.video_available.get(timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to acquire video buffer: {e}")
            raise TimeoutError(f"No video buffer available within {timeout}s") from e
        
        shm = self.video_buffers[index]
        if shm is None:
            logger.error(f"Video buffer {index} is None")
            raise RuntimeError(f"Video buffer {index} is not initialized")
        
        return index, shm.name, self.max_video_size
    
    def release_audio_buffer(self, index: int):
        """
        Release an audio buffer back to the pool.
        
        Args:
            index: Buffer index to release
        """
        if index < 0 or index >= len(self.audio_buffers):
            logger.error(f"Invalid audio buffer index: {index}")
            return
        
        if self.audio_buffers[index] is not None:
            self.audio_available.put(index)
            logger.debug(f"Released audio buffer {index}")
        else:
            logger.warning(f"Attempted to release None audio buffer {index}")
    
    def release_video_buffer(self, index: int):
        """
        Release a video buffer back to the pool.
        
        Args:
            index: Buffer index to release
        """
        if index < 0 or index >= len(self.video_buffers):
            logger.error(f"Invalid video buffer index: {index}")
            return
        
        if self.video_buffers[index] is not None:
            self.video_available.put(index)
            logger.debug(f"Released video buffer {index}")
        else:
            logger.warning(f"Attempted to release None video buffer {index}")
    
    def cleanup(self):
        """
        Clean up all shared memory buffers.
        Create mode: closes and unlinks. Attach mode: only closes.
        """
        if self._is_cleaned_up:
            return
        
        self._is_cleaned_up = True
        logger.info(f"Cleaning up buffer pool (create_mode={self.create_mode})")
        
        # Clean up audio buffers
        for i, shm in enumerate(self.audio_buffers):
            if shm is not None:
                try:
                    shm.close()
                    if self.create_mode:
                        shm.unlink()
                    logger.debug(f"Cleaned up audio buffer {i}: {shm.name}")
                except Exception as e:
                    logger.warning(f"Error cleaning up audio buffer {i}: {e}")
        
        # Clean up video buffers
        for i, shm in enumerate(self.video_buffers):
            if shm is not None:
                try:
                    shm.close()
                    if self.create_mode:
                        shm.unlink()
                    logger.debug(f"Cleaned up video buffer {i}: {shm.name}")
                except Exception as e:
                    logger.warning(f"Error cleaning up video buffer {i}: {e}")
        
        self.audio_buffers.clear()
        self.video_buffers.clear()
        logger.info("SharedMemoryBufferPool cleanup complete")
    
    def _register_cleanup(self):
        """Register cleanup handlers for normal and abnormal exit."""
        if self._cleanup_registered:
            return
        
        self._cleanup_registered = True
        
        if self.create_mode:
            atexit.register(self.cleanup)
            logger.debug("Registered atexit cleanup (create_mode)")
        else:
            # Attach mode: use weakref.finalize for cleanup
            weakref.finalize(self, self._cleanup_callback, 
                            self.audio_buffers, self.video_buffers, self.create_mode)
            logger.debug("Registered weakref cleanup (attach_mode)")
    
    @staticmethod
    def _cleanup_callback(audio_buffers: List, video_buffers: List, create_mode: bool):
        """Static cleanup callback for weakref.finalize."""
        logger.info(f"Weakref cleanup (create_mode={create_mode})")
        
        for i, shm in enumerate(audio_buffers):
            if shm is not None:
                try:
                    shm.close()
                    if create_mode:
                        shm.unlink()
                except Exception as e:
                    logger.warning(f"Weakref cleanup audio buffer {i} error: {e}")
        
        for i, shm in enumerate(video_buffers):
            if shm is not None:
                try:
                    shm.close()
                    if create_mode:
                        shm.unlink()
                except Exception as e:
                    logger.warning(f"Weakref cleanup video buffer {i} error: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except Exception as e:
            logger.error(f"Error in __del__: {e}")

