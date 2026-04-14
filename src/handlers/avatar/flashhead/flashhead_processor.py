"""
FlashHead streaming processor for per-session audio buffering and inference.

Wraps the FlashHead pipeline and maintains per-session state including:
- Audio sliding-window buffer (deque)
- Pipeline motion-frame latents for temporal continuity
- Frame-rate metronome (frame collector) for constant output
- Audio-video synchronization via paired output queue
- Interrupt support for duplex mode
"""
import queue
import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import torch
from loguru import logger


@dataclass
class FlashHeadProcessorCallbacks:
    """Callback functions bridging processor output to the engine."""
    on_video_frame: Optional[Callable[[np.ndarray], None]] = None
    on_audio_frame: Optional[Callable[[np.ndarray], None]] = None
    on_speech_end: Optional[Callable[[str], None]] = None


@dataclass
class FrameQueueItem:
    """A single output item pairing a video frame with its audio segment."""
    video_frame: Optional[np.ndarray]    # BGR uint8, (H, W, 3) or None (end marker)
    audio_segment: Optional[np.ndarray]  # float32 at original SR, or None
    speech_id: Optional[str]
    end_of_speech: bool


class FlashHeadProcessor:
    """Per-session streaming processor for FlashHead avatar.

    Each processor instance maintains its own audio buffer and pipeline session
    state.  The heavy model weights (DiT, VAE, wav2vec2) are shared via the
    pipeline object; only lightweight per-session tensors are duplicated.

    Architecture (similar to MuseTalk):
    - add_audio() receives TTS audio, buffers, and triggers pipeline inference
    - Inference results are placed into _output_queue as (video, audio) pairs
    - _frame_collector_worker thread runs at constant FPS, drains queue, emits
      speaking frames or idle frames when queue is empty
    """

    def __init__(
        self,
        pipeline,
        infer_params: dict,
        output_audio_sample_rate: int = 24000,
        idle_noise_amplitude: float = 0.003,
        callbacks: Optional[FlashHeadProcessorCallbacks] = None,
    ):
        self.pipeline = pipeline
        self.infer_params = infer_params
        self.callbacks = callbacks
        self._idle_noise_amplitude = idle_noise_amplitude
        self._breath_phase = 0.0

        # Key inference parameters
        self.sample_rate: int = infer_params["sample_rate"]        # 16000
        self.tgt_fps: int = infer_params["tgt_fps"]                # 25
        self.frame_num: int = infer_params["frame_num"]            # 33
        self.motion_frames_num: int = infer_params["motion_frames_num"]
        self.cached_audio_duration: int = infer_params["cached_audio_duration"]  # 8

        self.slice_len: int = self.frame_num - self.motion_frames_num  # 24 for lite
        self.audio_slice_samples: int = self.slice_len * self.sample_rate // self.tgt_fps

        # Original audio output parameters
        self._output_sr: int = output_audio_sample_rate
        self._original_audio_per_frame: int = self._output_sr // self.tgt_fps  # 960 at 24kHz/25fps
        self._original_audio_slice_samples: int = self.slice_len * self._output_sr // self.tgt_fps

        # Streaming audio buffer (sliding window of cached_audio_duration seconds)
        cached_audio_length = self.sample_rate * self.cached_audio_duration
        self.audio_end_idx: int = self.cached_audio_duration * self.tgt_fps
        self.audio_start_idx: int = self.audio_end_idx - self.frame_num

        init_audio = self._make_ambient_noise(cached_audio_length)
        self._audio_deque = deque(init_audio.tolist(), maxlen=cached_audio_length)
        self._pending_audio = np.array([], dtype=np.float32)
        self._pending_original_audio = np.array([], dtype=np.float32)

        # Per-session pipeline state (save/restore for multi-session)
        self._initial_latent_1slice = pipeline.ref_img_latent[:, :1].clone()
        self._latent_motion_frames = self._initial_latent_1slice.clone()

        # Thread safety
        self._lock = threading.Lock()
        self._interrupted = False
        self._speaking = False           # True while TTS audio is being processed
        self._speech_start_pending = False  # Signal to reset deque on first speech chunk
        self._inference_lock = threading.Lock()  # Serializes pipeline access (speech vs idle)

        # Current speech tracking
        self._current_speech_id: Optional[str] = None

        # --- Frame collector architecture ---
        self._output_queue: queue.Queue[FrameQueueItem] = queue.Queue()

        # Pre-compute static idle frame as fallback (BGR uint8)
        self._idle_frame = self._make_idle_frame(pipeline)

        # Threads (started after callbacks are set)
        self._stop_event = threading.Event()
        self._collector_thread: Optional[threading.Thread] = None
        self._idle_thread: Optional[threading.Thread] = None

    def _make_idle_frame(self, pipeline) -> np.ndarray:
        """Convert pipeline's reference image tensor to BGR uint8 numpy array."""
        ref = pipeline.original_color_reference  # (1, C, 1, H, W), range [-1, 1]
        rgb = ((ref[0, :, 0].permute(1, 2, 0) + 1) / 2 * 255).clamp(0, 255).byte().cpu().numpy()
        bgr = rgb[:, :, ::-1].copy()
        logger.info(f"FlashHead: idle frame prepared, shape={bgr.shape}")
        return bgr

    def set_callbacks(self, callbacks: Optional[FlashHeadProcessorCallbacks]):
        self.callbacks = callbacks

    def start(self):
        """Start the frame collector and idle inference threads. Call after callbacks are set."""
        if self._collector_thread is not None and self._collector_thread.is_alive():
            return
        self._stop_event.clear()
        self._collector_thread = threading.Thread(
            target=self._frame_collector_worker, daemon=True, name="FlashHead-FrameCollector",
        )
        self._idle_thread = threading.Thread(
            target=self._idle_inference_worker, daemon=True, name="FlashHead-IdleInference",
        )
        self._collector_thread.start()
        self._idle_thread.start()
        logger.info("FlashHead: frame collector and idle inference threads started")

    def add_audio(self, audio_data_16k: np.ndarray, original_audio: np.ndarray,
                  speech_id: str, end_of_speech: bool):
        """Add audio samples and trigger inference when enough data.

        Args:
            audio_data_16k: float32 numpy array at 16kHz (for pipeline inference).
            original_audio: float32 numpy array at output_audio_sample_rate (for client playback).
            speech_id: Unique identifier for the current TTS stream.
            end_of_speech: True if this is the last audio chunk for the speech.
        """
        with self._lock:
            if self._interrupted:
                return
            was_speaking = self._speaking
            self._current_speech_id = speech_id
            self._speaking = True

        if not was_speaking:
            self._speech_start_pending = True
            # Drain idle frames from queue so speech frames play immediately
            drained = 0
            temp = []
            while not self._output_queue.empty():
                try:
                    item = self._output_queue.get_nowait()
                    if item.speech_id is not None:
                        temp.append(item)
                    else:
                        drained += 1
                except queue.Empty:
                    break
            for item in temp:
                self._output_queue.put(item)
            if drained:
                logger.info(f"FlashHead: drained {drained} idle frames on speech start")

        # Append to pending buffers
        self._pending_audio = np.concatenate([self._pending_audio, audio_data_16k])
        self._pending_original_audio = np.concatenate([self._pending_original_audio, original_audio])

        logger.info(
            f"FlashHead add_audio: speech_id={speech_id}, end={end_of_speech}, "
            f"16k={len(audio_data_16k)}, pending={len(self._pending_audio)}, "
            f"need={self.audio_slice_samples}"
        )

        # Process full slices
        while len(self._pending_audio) >= self.audio_slice_samples:
            if self._interrupted:
                return

            chunk_16k = self._pending_audio[:self.audio_slice_samples]
            self._pending_audio = self._pending_audio[self.audio_slice_samples:]

            # Take corresponding original audio slice
            orig_take = min(self._original_audio_slice_samples, len(self._pending_original_audio))
            chunk_orig = self._pending_original_audio[:orig_take]
            self._pending_original_audio = self._pending_original_audio[orig_take:]

            self._process_chunk(chunk_16k, chunk_orig, speech_id, end_of_speech=False)

        # On end of speech, flush remaining audio (pad with zeros if needed)
        if end_of_speech:
            if len(self._pending_audio) > 0 and not self._interrupted:
                pad_16k = self.audio_slice_samples - len(self._pending_audio)
                if pad_16k > 0:
                    self._pending_audio = np.concatenate([
                        self._pending_audio,
                        np.zeros(pad_16k, dtype=np.float32),
                    ])
                # Pad original audio proportionally
                orig_needed = self._original_audio_slice_samples
                orig_available = len(self._pending_original_audio)
                if orig_available < orig_needed:
                    self._pending_original_audio = np.concatenate([
                        self._pending_original_audio,
                        np.zeros(orig_needed - orig_available, dtype=np.float32),
                    ])
                chunk_orig = self._pending_original_audio[:orig_needed]

                self._process_chunk(
                    self._pending_audio[:self.audio_slice_samples],
                    chunk_orig, speech_id, end_of_speech=True,
                )
                self._pending_audio = np.array([], dtype=np.float32)
                self._pending_original_audio = np.array([], dtype=np.float32)
            elif not self._interrupted:
                # No pending audio left but speech ended -- queue an end marker
                self._output_queue.put(FrameQueueItem(
                    video_frame=None, audio_segment=None,
                    speech_id=speech_id, end_of_speech=True,
                ))
            # Speech fully processed, allow idle inference to resume
            with self._lock:
                self._speaking = False

    def _process_chunk(self, audio_chunk_16k: np.ndarray, original_audio: np.ndarray,
                       speech_id: str, end_of_speech: bool):
        """Run one inference chunk through the FlashHead pipeline and enqueue results."""
        lock_start = time.monotonic()
        self._inference_lock.acquire()
        lock_wait = time.monotonic() - lock_start
        if lock_wait > 0.05:
            logger.info(
                f"FlashHead: speech inference waited {lock_wait*1000:.0f}ms "
                f"for _inference_lock (idle inference may have been running)"
            )
        try:
            t_start = time.monotonic()

            # On idle→speech transition, flush the audio deque so that
            # residual idle noise does not contaminate the speech embedding.
            if self._speech_start_pending:
                self._speech_start_pending = False
                cached_audio_length = self.sample_rate * self.cached_audio_duration
                self._audio_deque = deque(
                    [0.0] * cached_audio_length, maxlen=cached_audio_length,
                )
                logger.info("FlashHead: audio deque reset on speech start")

            # Update sliding window buffer
            self._audio_deque.extend(audio_chunk_16k.tolist())
            audio_array = np.array(self._audio_deque)

            # Restore per-session latent state
            self.pipeline.latent_motion_frames = self._latent_motion_frames.clone()

            # Extract audio embedding
            audio_embedding = self._get_audio_embedding(audio_array)

            # Run diffusion + VAE decode
            sample_frames = self._run_pipeline(audio_embedding)

            # Save updated latent motion frames for next chunk
            self._latent_motion_frames = self.pipeline.latent_motion_frames.clone()

            # Trim motion frames (first motion_frames_num frames are overlap)
            video_frames = sample_frames[self.motion_frames_num:]

            dur_ms = (time.monotonic() - t_start) * 1000
            logger.info(
                f"FlashHead chunk inference done: {video_frames.shape[0]} frames in {dur_ms:.1f}ms "
                f"({video_frames.shape[0] / (dur_ms / 1000):.1f} FPS)"
            )
        finally:
            self._inference_lock.release()

        # Convert to numpy uint8 and enqueue (video, audio) pairs
        frames_np = video_frames.cpu().numpy().astype(np.uint8)
        n_frames = frames_np.shape[0]
        spf = self._original_audio_per_frame  # samples per frame at original SR

        for i in range(n_frames):
            if self._interrupted:
                return

            # RGB -> BGR for fastrtc
            frame_bgr = frames_np[i][:, :, ::-1].copy()

            # Slice corresponding original audio segment
            audio_start = i * spf
            audio_end = min((i + 1) * spf, len(original_audio))
            if audio_start < len(original_audio):
                audio_seg = original_audio[audio_start:audio_end]
            else:
                audio_seg = None

            is_last = (i == n_frames - 1) and end_of_speech

            self._output_queue.put(FrameQueueItem(
                video_frame=frame_bgr,
                audio_segment=audio_seg,
                speech_id=speech_id,
                end_of_speech=is_last,
            ))

    def _idle_inference_worker(self):
        """Background thread: generates idle animation frames with silent audio.

        When the output queue is running low and no TTS speech is active,
        feeds silent audio through the pipeline to generate frames with
        natural micro-movements (breathing, subtle head motion).
        """
        # Keep a small buffer (half a slice) to avoid starving the frame
        # collector, but don't over-fill — that would block speech inference
        # by holding _inference_lock when speech audio arrives.
        IDLE_THRESHOLD = max(self.slice_len // 2, 6)
        logger.info(f"FlashHead idle inference worker started (threshold={IDLE_THRESHOLD})")

        while not self._stop_event.is_set():
            need_idle = (
                self._output_queue.qsize() < IDLE_THRESHOLD
                and not self._speaking
            )
            if not need_idle:
                self._stop_event.wait(timeout=0.1)
                continue

            self._generate_idle_chunk()

        logger.info("FlashHead idle inference worker stopped")

    def _make_ambient_noise(self, n_samples: int) -> np.ndarray:
        """Generate breathing-patterned noise for idle animation.

        Produces amplitude-modulated noise with a ~4-second breathing cycle.
        The periodic energy variation gives wav2vec2 richer temporal structure
        than flat white noise, which may help drive subtle head motion.
        Phase is tracked across calls for cross-chunk continuity.
        """
        if self._idle_noise_amplitude <= 0:
            return np.zeros(n_samples, dtype=np.float32)

        sr = self.sample_rate
        t = np.arange(n_samples, dtype=np.float32) / sr

        # ~15 breaths/min ≈ 0.25 Hz (one full cycle every 4 seconds)
        breath_freq = 0.25
        phase = self._breath_phase
        raw_envelope = np.sin(2 * np.pi * breath_freq * t + phase)
        envelope = np.clip(raw_envelope, 0.0, 1.0) ** 0.5

        self._breath_phase = phase + 2 * np.pi * breath_freq * n_samples / sr

        noise = np.random.randn(n_samples).astype(np.float32)

        # Gentle low-pass via moving average to soften harsh high frequencies
        kernel_size = max(1, sr // 2000)  # ~8 taps at 16 kHz
        kernel = np.ones(kernel_size, dtype=np.float32) / kernel_size
        noise = np.convolve(noise, kernel, mode="same")

        return (noise * envelope * self._idle_noise_amplitude).astype(np.float32)

    def _generate_idle_chunk(self):
        """Run one inference chunk with ambient-noise audio for idle animation.

        Uses the pipeline's generator in its natural advancing sequence
        (no re-seeding) to avoid directional noise bias accumulation.
        """
        silent_16k = self._make_ambient_noise(self.audio_slice_samples)

        with self._inference_lock:
            if self._speaking or self._stop_event.is_set():
                return

            t_start = time.monotonic()

            self._audio_deque.extend(silent_16k.tolist())
            audio_array = np.array(self._audio_deque)

            self.pipeline.latent_motion_frames = self._latent_motion_frames.clone()

            audio_embedding = self._get_audio_embedding(audio_array)
            sample_frames = self._run_pipeline(audio_embedding)

            self._latent_motion_frames = self.pipeline.latent_motion_frames.clone()

            video_frames = sample_frames[self.motion_frames_num:]

            dur_ms = (time.monotonic() - t_start) * 1000
            logger.debug(
                f"FlashHead idle chunk: {video_frames.shape[0]} frames in {dur_ms:.1f}ms"
            )

        frames_np = video_frames.cpu().numpy().astype(np.uint8)
        for i in range(frames_np.shape[0]):
            if self._speaking or self._stop_event.is_set():
                return
            frame_bgr = frames_np[i][:, :, ::-1].copy()
            self._output_queue.put(FrameQueueItem(
                video_frame=frame_bgr,
                audio_segment=None,
                speech_id=None,
                end_of_speech=False,
            ))

    def _frame_collector_worker(self):
        """Frame-rate metronome: strictly outputs one frame per 1/fps second.

        When speaking frames are available in the queue, emits them with
        synchronized audio. Otherwise emits the static idle (reference) frame
        as fallback (the idle inference thread generates animated idle frames).
        """
        fps = self.tgt_fps
        frame_interval = 1.0 / fps
        start_time = time.perf_counter()
        frame_id = 0

        logger.info(f"FlashHead frame collector started: fps={fps}")

        while not self._stop_event.is_set():
            # --- Precise timing (absolute reference, no cumulative drift) ---
            target_time = start_time + frame_id * frame_interval
            now = time.perf_counter()
            sleep_time = target_time - now
            if sleep_time > 0.002:
                time.sleep(sleep_time - 0.001)  # Coarse wait
            while time.perf_counter() < target_time:
                pass  # Spin wait for sub-ms accuracy

            # --- Try to get a speaking frame (non-blocking) ---
            item: Optional[FrameQueueItem] = None
            try:
                item = self._output_queue.get_nowait()
            except queue.Empty:
                pass

            # Discard stale *speech* frames on interrupt; idle frames (speech_id=None) pass through
            if self._interrupted and item is not None and item.speech_id is not None:
                item = None

            # --- Emit ---
            if self.callbacks is None:
                frame_id += 1
                continue

            if item is not None and item.video_frame is not None:
                # Speaking frame
                if self.callbacks.on_video_frame:
                    self.callbacks.on_video_frame(item.video_frame)
                if item.audio_segment is not None and len(item.audio_segment) > 0:
                    if self.callbacks.on_audio_frame:
                        self.callbacks.on_audio_frame(item.audio_segment)
                if item.end_of_speech:
                    if self.callbacks.on_speech_end:
                        self.callbacks.on_speech_end(item.speech_id)
            else:
                # Idle frame: emit video AND silent audio so the RTC
                # audio/video PTS advance at the same rate.  Without
                # this, video runs ahead because idle frames had no
                # paired audio and emit() would block.
                if self.callbacks.on_video_frame:
                    self.callbacks.on_video_frame(self._idle_frame)
                if self.callbacks.on_audio_frame:
                    self.callbacks.on_audio_frame(
                        np.zeros(self._original_audio_per_frame, dtype=np.float32)
                    )
                # Pure end marker (no video but need to close stream)
                if item is not None and item.end_of_speech:
                    if self.callbacks.on_speech_end:
                        self.callbacks.on_speech_end(item.speech_id)

            frame_id += 1

        logger.info("FlashHead frame collector stopped")

    def _get_audio_embedding(self, audio_array: np.ndarray):
        """Extract wav2vec2 audio embedding with windowed sampling."""
        audio_embedding = self.pipeline.preprocess_audio(
            audio_array, sr=self.sample_rate, fps=self.tgt_fps,
        )

        indices = (torch.arange(2 * 2 + 1) - 2) * 1
        center_indices = (
            torch.arange(self.audio_start_idx, self.audio_end_idx, 1).unsqueeze(1)
            + indices.unsqueeze(0)
        )
        center_indices = torch.clamp(center_indices, min=0, max=self.audio_end_idx - 1)

        audio_embedding = audio_embedding[center_indices][None, ...].contiguous()
        return audio_embedding

    def _run_pipeline(self, audio_embedding):
        """Run the pipeline's generate() and return video frames as uint8 tensor."""
        audio_embedding = audio_embedding.to(self.pipeline.device)
        sample = self.pipeline.generate(audio_embedding)
        # Convert from [-1, 1] to [0, 255] uint8: (T, H, W, C)
        sample_frames = (((sample + 1) / 2).permute(1, 2, 3, 0).clip(0, 1) * 255).contiguous()
        return sample_frames

    def interrupt(self):
        """Interrupt current inference and clear all audio state.

        Resets the audio sliding-window buffer so that subsequent idle inference
        generates clean idle frames without residual speech mouth movements.
        """
        logger.info("FlashHeadProcessor: interrupt requested")
        with self._lock:
            self._interrupted = True
            self._speaking = False
            self._current_speech_id = None
        self._speech_start_pending = False

        # Clear pending audio
        self._pending_audio = np.array([], dtype=np.float32)
        self._pending_original_audio = np.array([], dtype=np.float32)

        # Reset audio deque to silence so idle inference won't produce
        # frames driven by residual speech audio.
        cached_audio_length = self.sample_rate * self.cached_audio_duration
        self._audio_deque = deque(
            [0.0] * cached_audio_length, maxlen=cached_audio_length,
        )

        # Drain output queue
        while not self._output_queue.empty():
            try:
                self._output_queue.get_nowait()
            except queue.Empty:
                break

    def reset_interrupt(self):
        """Allow new audio processing after an interrupt."""
        with self._lock:
            self._interrupted = False

    def reset_session(self):
        """Fully reset session state (motion frames, audio buffer) to initial."""
        logger.info("FlashHeadProcessor: resetting session state")
        with self._lock:
            self._interrupted = False
            self._current_speech_id = None
            self._speaking = False
        self._speech_start_pending = False
        self._pending_audio = np.array([], dtype=np.float32)
        self._pending_original_audio = np.array([], dtype=np.float32)
        self._breath_phase = 0.0
        cached_audio_length = self.sample_rate * self.cached_audio_duration
        init_audio = self._make_ambient_noise(cached_audio_length)
        self._audio_deque = deque(init_audio.tolist(), maxlen=cached_audio_length)
        self._latent_motion_frames = self._initial_latent_1slice.clone()

    def stop(self):
        """Cleanup when session ends."""
        self._stop_event.set()
        self.interrupt()
        if self._idle_thread is not None and self._idle_thread.is_alive():
            self._idle_thread.join(timeout=3)
        if self._collector_thread is not None and self._collector_thread.is_alive():
            self._collector_thread.join(timeout=3)
