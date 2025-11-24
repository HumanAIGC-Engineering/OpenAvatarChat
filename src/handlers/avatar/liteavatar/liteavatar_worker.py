from loguru import logger
import torch.multiprocessing as mp
import threading
import time
from typing import Optional
from enum import Enum
import os
import numpy as np
from multiprocessing import shared_memory

import sysconfig

cudnn_path = os.path.join(sysconfig.get_path("purelib"), "nvidia", "cudnn", "lib")
logger.info("cudnn_path: {}", cudnn_path)
os.environ["LD_LIBRARY_PATH"] = f"{cudnn_path}:{os.environ.get('LD_LIBRARY_PATH', '')}"


from handlers.avatar.liteavatar.avatar_output_handler import AvatarOutputHandler
from handlers.avatar.liteavatar.avatar_processor import AvatarProcessor
from handlers.avatar.liteavatar.avatar_processor_factory import AvatarProcessorFactory, AvatarAlgoType
from handlers.avatar.liteavatar.model.algo_model import AvatarInitOption, AudioResult, VideoResult, AvatarStatus
from handlers.avatar.liteavatar.shared_memory_buffer_pool import SharedMemoryBufferPool, SharedMemoryDataPacket
from engine_utils.interval_counter import IntervalCounter
from chat_engine.common.handler_base import HandlerBaseConfigModel
from pydantic import BaseModel, Field


mp.set_start_method('spawn', force=True)


class Tts2FaceConfigModel(HandlerBaseConfigModel, BaseModel):
    avatar_name: str = Field(default="sample_data")
    debug: bool = Field(default=False)
    fps: int = Field(default=25)
    enable_fast_mode: bool = Field(default=False)
    use_gpu: bool = Field(default=True)
    stop_ack_timeout: float = Field(default=5.0)


class Tts2FaceEvent(Enum):
    START = 1001
    STOP = 1002

    LISTENING_TO_SPEAKING = 2001
    SPEAKING_TO_LISTENING = 2002

class Tts2FaceOutputHandler(AvatarOutputHandler):
    def __init__(self, audio_output_queue, video_output_queue,
                 event_out_queue, shm_pool: SharedMemoryBufferPool):
        self.audio_output_queue = audio_output_queue
        self.video_output_queue = video_output_queue
        self.event_out_queue = event_out_queue
        self.shm_pool = shm_pool
        self._video_producer_counter = IntervalCounter("video_producer")

    def on_start(self, init_option: AvatarInitOption):
        logger.info("on algo processor start")

    def on_stop(self):
        logger.info("on algo processor stop")

    def on_audio(self, audio_result: AudioResult):
        audio_frame = audio_result.audio_frame
        audio_data = audio_frame.to_ndarray()
        
        try:
            # Acquire buffer from pool
            buf_idx, shm_name, buf_size = self.shm_pool.acquire_audio_buffer()
            
            # Write to shared memory
            shm = shared_memory.SharedMemory(name=shm_name)
            np_buffer = np.ndarray(audio_data.shape, dtype=audio_data.dtype, buffer=shm.buf)
            np_buffer[:] = audio_data
            
            # Create packet and send
            packet = SharedMemoryDataPacket(
                buffer_index=buf_idx,
                shm_name=shm_name,
                data_size=audio_data.nbytes,
                shape=audio_data.shape,
                dtype=str(audio_data.dtype),
                buffer_type='audio'
            )
            self.audio_output_queue.put_nowait(packet)
            shm.close()  # Don't unlink, just close this process's reference
            
        except Exception as e:
            logger.error(f"Error sending audio via shared memory: {e}")

    def on_video(self, video_result: VideoResult):
        self._video_producer_counter.add()
        video_frame = video_result.video_frame
        video_data = video_frame.to_ndarray(format="bgr24")
        
        try:
            # Acquire buffer from pool
            buf_idx, shm_name, buf_size = self.shm_pool.acquire_video_buffer()
            
            # Write to shared memory
            shm = shared_memory.SharedMemory(name=shm_name)
            np_buffer = np.ndarray(video_data.shape, dtype=video_data.dtype, buffer=shm.buf)
            np_buffer[:] = video_data
            
            # Create packet and send
            packet = SharedMemoryDataPacket(
                buffer_index=buf_idx,
                shm_name=shm_name,
                data_size=video_data.nbytes,
                shape=video_data.shape,
                dtype=str(video_data.dtype),
                buffer_type='video'
            )
            self.video_output_queue.put_nowait(packet)
            shm.close()  # Don't unlink, just close this process's reference
            
        except Exception as e:
            logger.error(f"Error sending video via shared memory: {e}")

    def on_avatar_status_change(self, speech_id, avatar_status: AvatarStatus):
        logger.info(f"Avatar status changed: {speech_id} {avatar_status}")
        if avatar_status.value == AvatarStatus.LISTENING.value:
            self.event_out_queue.put_nowait(Tts2FaceEvent.SPEAKING_TO_LISTENING)
 

class WorkerStatus(Enum):
    IDLE = 1001
    BUSY = 1002
 

class LiteAvatarWorker:
    def __init__(self,
                 handler_root: str,
                 config: Tts2FaceConfigModel):
        self.event_in_queue = mp.Queue()
        self.event_out_queue = mp.Queue()
        self.audio_in_queue = mp.Queue()
        self.audio_out_queue = mp.Queue()
        self.video_out_queue = mp.Queue()
        self.io_queues = [
            self.event_in_queue,
            self.event_out_queue,
            self.audio_in_queue,
            self.audio_out_queue,
            self.video_out_queue
        ]
        self.processor: Optional[AvatarProcessor] = None
        self.session_running = False
        self.audio_input_thread = None
        self.worker_status = WorkerStatus.IDLE
        self._handler_root = handler_root
        self._config = config

        # Event synchronization: stop acknowledgement
        self._stop_ack_event = mp.Event()
        self._stop_ack_event.clear()
        self.stop_ack_timeout = getattr(config, "stop_ack_timeout", 5.0)

        # Initialize shared memory buffer pool
        # Calculate maximum buffer sizes
        self.max_audio_size = 24000 * 2 * 1  # sample_rate * bytes_per_sample * max_seconds (1秒)
        self.max_video_size = 1920 * 1080 * 3  # max_width * max_height * channels
        self.audio_pool_size = 10
        self.video_pool_size = 10
        
        self._init_shared_memory_pool()
        self._start_avatar_process()

    def __getstate__(self):
        """Exclude shm_pool from serialization to child process."""
        state = self.__dict__.copy()
        state['shm_pool'] = None
        return state
    
    def __setstate__(self, state):
        """Restore state in child process."""
        self.__dict__.update(state)
    
    def get_status(self):
        return self.worker_status
    
    def recruit(self):
        """Acquire worker for a new session"""
        # Ensure process is still alive
        if self._avatar_process is not None and not self._avatar_process.is_alive():
            raise RuntimeError("Avatar process is not alive")

        self.worker_status = WorkerStatus.BUSY
        logger.info("Avatar worker recruited for new session")
    
    def release(self):
        """Release worker and wait for session to stop"""
        logger.info("Releasing avatar worker for next session")

        # Wait for stop acknowledgement with configurable timeout
        if not self._stop_ack_event.wait(timeout=self.stop_ack_timeout):
            logger.error(
                f"Stop acknowledgement timeout after {self.stop_ack_timeout}s, restarting avatar worker"
            )
            self._restart_avatar_process()
        else:
            logger.info("Stop acknowledgement received")
            self._stop_ack_event.clear()

        self.worker_status = WorkerStatus.IDLE
        logger.info("Avatar worker released and ready for next session")

    def start_avatar(self,
                     handler_root: str,
                     config: Tts2FaceConfigModel,
                     shm_names: dict,
                     audio_pool_size: int,
                     video_pool_size: int,
                     max_audio_size: int,
                     max_video_size: int,
                     audio_available_queue,
                     video_available_queue):

        try:
            # Attach to shared memory created by parent process
            self.shm_pool = SharedMemoryBufferPool(
                audio_pool_size=audio_pool_size,
                video_pool_size=video_pool_size,
                max_audio_size=max_audio_size,
                max_video_size=max_video_size,
                create_mode=False,
                shm_names=shm_names,
                audio_available_queue=audio_available_queue,
                video_available_queue=video_available_queue
            )
            logger.info("Child process attached to shared memory buffer pool")

            self.processor = AvatarProcessorFactory.create_avatar_processor(
                handler_root,
                AvatarAlgoType.TTS2FACE_CPU,
                AvatarInitOption(
                    audio_sample_rate=24000,
                    video_frame_rate=config.fps,
                    avatar_name=config.avatar_name,
                    debug=config.debug,
                    enable_fast_mode=config.enable_fast_mode,
                    use_gpu=config.use_gpu
                )
            )
            logger.info("Avatar process is ready")
            
            # Start event input loop
            event_in_loop = threading.Thread(target=self._event_input_loop)
            event_in_loop.start()
            
            # Keep process alive
            while True:
                time.sleep(1)
        except Exception as e:
            logger.error(f"Error in avatar process: {e}")
        finally:
            if hasattr(self, 'shm_pool') and self.shm_pool is not None:
                self.shm_pool.cleanup()
    
    def _event_input_loop(self):
        while True:
            event: Tts2FaceEvent = self.event_in_queue.get()
            logger.info("receive event: {}", event)
            if event == Tts2FaceEvent.START:
                # Start a new session only when none is active
                if not self.session_running:
                    self.session_running = True
                    result_hanler = Tts2FaceOutputHandler(
                        audio_output_queue=self.audio_out_queue,
                        video_output_queue=self.video_out_queue,
                        event_out_queue=self.event_out_queue,
                        shm_pool=self.shm_pool,
                    )
                    self.processor.register_output_handler(result_hanler)
                    self.processor.start()
                    self.audio_input_thread = threading.Thread(target=self._audio_input_loop)
                    self.audio_input_thread.start()
                    logger.info("Avatar session started")
                else:
                    logger.warning("Received START event but session is already active, ignoring")

            elif event == Tts2FaceEvent.STOP:
                # Stop session only when one is active
                if self.session_running:
                    self.session_running = False
                    
                    if self.processor is not None:
                        self.processor.stop()
                        self.processor.clear_output_handlers()
                    if self.audio_input_thread is not None:
                        self.audio_input_thread.join()
                        self.audio_input_thread = None
                    self._clear_mp_queues()
                    self.context = None
                    logger.info("Avatar session stopped")
                    # Signal stop acknowledgement
                    self._stop_ack_event.set()
                else:
                    logger.warning("Received STOP event but no active session, ignoring")
    
    def _audio_input_loop(self):
        while self.session_running:
            try:
                speech_audio = self.audio_in_queue.get(timeout=0.1)
                self.processor.add_audio(speech_audio)
            except Exception:
                continue

    def _clear_mp_queues(self):
        for q in self.io_queues:
            while not q.empty():
                item = q.get()
                try:
                    if q is self.audio_out_queue and isinstance(item, SharedMemoryDataPacket):
                        if self.shm_pool is not None:
                            self.shm_pool.release_audio_buffer(item.buffer_index)
                    elif q is self.video_out_queue and isinstance(item, SharedMemoryDataPacket):
                        if self.shm_pool is not None:
                            self.shm_pool.release_video_buffer(item.buffer_index)
                except Exception as release_error:
                    logger.error("Failed to release buffer while clearing queue: {}", release_error)
    
    def destroy(self):
        """Terminate avatar process and cleanup resources."""
        try:
            if self._avatar_process is not None:
                if self._avatar_process.is_alive():
                    self._avatar_process.terminate()
                    self._avatar_process.join(timeout=5)
                    if self._avatar_process.is_alive():
                        logger.warning("Force killing avatar process")
                        self._avatar_process.kill()
                        self._avatar_process.join()
                self._avatar_process = None
            
            if hasattr(self, 'shm_pool') and self.shm_pool is not None:
                self.shm_pool.cleanup()
                self.shm_pool = None
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def _init_shared_memory_pool(self):
        self.shm_pool = SharedMemoryBufferPool(
            audio_pool_size=self.audio_pool_size,
            video_pool_size=self.video_pool_size,
            max_audio_size=self.max_audio_size,
            max_video_size=self.max_video_size,
            create_mode=True
        )

    def _start_avatar_process(self):
        shm_names = self.shm_pool.get_shm_names()
        audio_available_queue = self.shm_pool.audio_available
        video_available_queue = self.shm_pool.video_available

        self._avatar_process = mp.Process(
            target=self.start_avatar,
            args=[self._handler_root, self._config, shm_names, self.audio_pool_size,
                  self.video_pool_size, self.max_audio_size, self.max_video_size,
                  audio_available_queue, video_available_queue]
        )
        self._avatar_process.start()

    def _restart_avatar_process(self):
        logger.info("Restarting avatar worker process")
        self.destroy()
        self._init_shared_memory_pool()
        self._start_avatar_process()
        self._stop_ack_event.clear()