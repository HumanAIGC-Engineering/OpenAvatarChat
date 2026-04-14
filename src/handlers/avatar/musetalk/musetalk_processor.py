import queue
import threading
import time
from queue import Empty, Queue
from threading import Thread
from typing import Optional

import librosa
import numpy as np
import torch
from loguru import logger

from handlers.avatar.musetalk.musetalk_data_models import (
    MuseTalkAvatarStatus, MuseTalkSpeechAudio, MuseTalkProcessorCallbacks,
    AudioQueueItem, WhisperQueueItem, UNetQueueItem, ComposeQueueItem,
)
from handlers.avatar.musetalk.musetalk_algo import MuseTalkAlgoV15
from handlers.avatar.musetalk.musetalk_config import AvatarMuseTalkConfig

class AvatarMuseTalkProcessor:
    """MuseTalk processor responsible for audio-to-video conversion (multi-threaded queue structure)."""
    
    def __init__(self, avatar: MuseTalkAlgoV15, config: AvatarMuseTalkConfig):
        # --- Core references ---
        self._avatar: MuseTalkAlgoV15 = avatar                             # Shared GPU algorithm instance
        self._config: AvatarMuseTalkConfig = config                        # Configuration
        self._algo_audio_sample_rate: int = config.algo_audio_sample_rate  # Internal sample rate for Whisper
        self._output_audio_sample_rate: int = config.output_audio_sample_rate  # Output audio sample rate
        self._callbacks: Optional[MuseTalkProcessorCallbacks] = None       # Output callbacks

        # --- Queues ---
        self._audio_queue: Queue = Queue()                                 # AudioQueueItem
        self._whisper_queue: Queue = Queue()                               # WhisperQueueItem
        self._unet_queue: Queue = Queue()                                  # UNetQueueItem (multi_thread_inference mode only)
        self._frame_id_queue: Queue = Queue()                              # int (backpressure queue: Frame Collector → Frame Generator)
        self._compose_queue: Queue = Queue()                               # ComposeQueueItem
        self._output_queue: Queue = Queue()                                # ComposeQueueItem (with frame field set)

        # --- Threads ---
        self._feature_thread: Optional[Thread] = None                      # Feature Extractor Worker
        self._frame_gen_thread: Optional[Thread] = None                    # Frame Generator (single-thread mode)
        self._frame_gen_unet_thread: Optional[Thread] = None               # UNet Worker (multi-thread mode)
        self._frame_gen_vae_thread: Optional[Thread] = None                # VAE Worker (multi-thread mode)
        self._compose_thread: Optional[Thread] = None                      # Compose Worker
        self._frame_collect_thread: Optional[Thread] = None                # Frame Collector Worker

        # --- State ---
        self._stop_event: threading.Event = threading.Event()              # Stop signal
        self._session_running: bool = False                                # Whether the processor is running
        self._interrupted: threading.Event = threading.Event()             # Interrupt flag
        self._generation_id: int = 0                                       # Monotonically increasing counter (distinguishes stale vs fresh data)
        self._generation_lock: threading.Lock = threading.Lock()           # Protects _generation_id
        self._frame_id_lock: threading.Lock = threading.Lock()             # Protects queue clear operations

        # --- Debug statistics ---
        self._first_add_audio_time: Optional[float] = None                 # Timestamp of the first add_audio call
        self._audio_duration_sum: float = 0.0                              # Cumulative audio duration

    def set_callbacks(self, callbacks: MuseTalkProcessorCallbacks):
        self._callbacks = callbacks

    def _reset_runtime_state(self):
        """Reset all per-session runtime state for pool reuse."""
        self._interrupted.clear()
        self._first_add_audio_time = None
        self._audio_duration_sum = 0.0
        self._clear_queues()

    def start(self):
        """Start the processor and all worker threads."""
        # --- Guard: prevent double-start ---
        if self._session_running:
            logger.error("Processor already running. session_running=True")
            return

        # --- Reset per-session state and mark running ---
        self._reset_runtime_state()
        self._session_running = True
        self._stop_event.clear()

        try:
            # --- Create worker threads ---
            # multi_thread_inference=True  → 5 threads: Feature + UNet + VAE + Compose + Collector
            # multi_thread_inference=False → 4 threads: Feature + FrameGen(UNet+VAE) + Compose + Collector
            self._feature_thread = threading.Thread(target=self._feature_extractor_worker)
            if self._config.multi_thread_inference:
                self._frame_gen_unet_thread = threading.Thread(target=self._frame_generator_unet_worker)
                self._frame_gen_vae_thread = threading.Thread(target=self._frame_generator_vae_worker)
            else:
                self._frame_gen_thread = threading.Thread(target=self._frame_generator_worker)
            self._frame_collect_thread = threading.Thread(target=self._frame_collector_worker)
            self._compose_thread = threading.Thread(target=self._compose_worker)

            # --- Start all threads ---
            self._feature_thread.start()
            if self._config.multi_thread_inference:
                self._frame_gen_unet_thread.start()
                self._frame_gen_vae_thread.start()
            else:
                self._frame_gen_thread.start()
            self._frame_collect_thread.start()
            self._compose_thread.start()
            logger.info(f"MuseProcessor started (multi_thread_inference={self._config.multi_thread_inference}).")
        except Exception as e:
            # Rollback state on failure so stop() won't be confused
            logger.opt(exception=True).error(f"Exception during thread start: {e}")
            self._session_running = False
            self._stop_event.set()
            raise

    def stop(self):
        """Stop the processor and all worker threads."""
        # --- Guard: prevent double-stop ---
        if not self._session_running:
            logger.warning("Processor not running. Skip stop.")
            return

        # --- Signal all workers to exit ---
        self._session_running = False
        self._stop_event.set()

        # --- Join all threads (timeout=5s each) ---
        threads = [
            (self._feature_thread, "Feature"),
            (self._frame_gen_thread, "Frame generator"),
            (self._frame_gen_unet_thread, "Frame generator UNet"),
            (self._frame_gen_vae_thread, "Frame generator VAE"),
            (self._frame_collect_thread, "Frame collector"),
            (self._compose_thread, "Compose"),
        ]
        for thread, name in threads:
            if thread is not None:
                thread.join(timeout=5)
                if thread.is_alive():
                    logger.error(f"{name} thread did not exit in time.")

        # --- Cleanup ---
        self._clear_queues()
        # Reset thread references to allow clean restart via start()
        self._feature_thread = None
        self._frame_gen_thread = None
        self._frame_gen_unet_thread = None
        self._frame_gen_vae_thread = None
        self._frame_collect_thread = None
        self._compose_thread = None
        logger.info(f"MuseProcessor stopped.")

    def add_audio(self, speech_audio: MuseTalkSpeechAudio):
        """
        Add an audio segment to the processing queue. The segment length must not exceed 1 second.
        """
        # --- Format conversion: bytes/ndarray → float32 ndarray ---
        audio_data = speech_audio.audio_data
        if isinstance(audio_data, bytes):
            audio_data = np.frombuffer(audio_data, dtype=np.float32)
        elif isinstance(audio_data, np.ndarray):
            audio_data = audio_data.astype(np.float32)
        else:
            logger.error(f"audio_data must be bytes or np.ndarray, got {type(audio_data)}")
            return

        # --- Input validation ---
        if len(audio_data) == 0:
            logger.error(f"Input audio is empty, speech_id={speech_audio.speech_id}")
            return
        if len(audio_data) > self._output_audio_sample_rate:  # Must not exceed 1 second
            logger.error(f"Audio segment too long: {len(audio_data)} > {self._output_audio_sample_rate}, speech_id={speech_audio.speech_id}")
            return
        if speech_audio.sample_rate != self._output_audio_sample_rate:
            logger.error(
                f"Sample rate mismatch: expected {self._output_audio_sample_rate}, "
                f"got {speech_audio.sample_rate}, speech_id={speech_audio.speech_id}"
            )
            return

        # --- Audio lag detection: warn if TTS feeds audio slower than real-time ---
        now = time.time()
        if self._first_add_audio_time is None:
            self._first_add_audio_time = now
        audio_duration = len(audio_data) / speech_audio.sample_rate
        self._audio_duration_sum += audio_duration
        total_interval = now - self._first_add_audio_time
        if self._audio_duration_sum < total_interval:
            logger.warning(
                f"[AUDIO_LAG] speech_id={speech_audio.speech_id}, "
                f"cumulative_audio={self._audio_duration_sum:.3f}s, wall_clock={total_interval:.3f}s, "
                f"lag={total_interval - self._audio_duration_sum:.3f}s"
            )
        elif self._config.debug:
            logger.info(
                f"[add_audio] speech_id={speech_audio.speech_id}, end_of_speech={speech_audio.end_of_speech}, "
                f"audio_duration={audio_duration:.3f}s, cumulative_audio={self._audio_duration_sum:.3f}s, "
                f"wall_clock={total_interval:.3f}s"
            )
        if speech_audio.end_of_speech:
            if self._config.debug:
                logger.info(f"[add_audio] speech_id={speech_audio.speech_id} end_of_speech, cumulative_audio={self._audio_duration_sum:.3f}s, wall_clock={total_interval:.3f}s")
            self._audio_duration_sum = 0.0
            self._first_add_audio_time = None

        # --- Enqueue with generation_id tagging ---
        with self._generation_lock:
            gen_id = self._generation_id
        try:
            self._audio_queue.put(AudioQueueItem(
                audio_data=audio_data,
                speech_id=speech_audio.speech_id,
                end_of_speech=speech_audio.end_of_speech,
                generation_id=gen_id,
            ), timeout=1)
        except queue.Full:
            logger.opt(exception=True).error(f"Audio queue full, dropping audio segment, speech_id={speech_audio.speech_id}")
            return
        # Only clear _interrupted if no concurrent interrupt() changed the generation_id
        with self._generation_lock:
            if self._generation_id == gen_id:
                self._interrupted.clear()

    def _feature_extractor_worker(self):
        """Worker thread for extracting audio features."""
        # --- CUDA warmup: ensure GPU context is allocated in this thread ---
        if torch.cuda.is_available():
            t0 = time.time()
            warmup_sr = 16000
            dummy_audio = np.zeros(warmup_sr, dtype=np.float32)
            self._avatar.extract_whisper_feature(dummy_audio, warmup_sr)
            torch.cuda.synchronize()
            t1 = time.time()
            logger.info(f"[THREAD_WARMUP] _feature_extractor_worker thread id: {threading.get_ident()} whisper feature warmup done, time: {(t1-t0)*1000:.1f} ms")

        while not self._stop_event.is_set():
            try:
                t_start = time.time()
                item: AudioQueueItem = self._audio_queue.get(timeout=1)

                # Discard stale data from a previous generation (interrupted speech)
                if item.generation_id != self._generation_id:
                    continue

                audio_data = item.audio_data
                speech_id = item.speech_id
                end_of_speech = item.end_of_speech
                fps = self._config.fps

                # --- Resample: output_audio_sample_rate → algo_audio_sample_rate (e.g. 24kHz → 16kHz) ---
                segment = librosa.resample(audio_data, orig_sr=self._output_audio_sample_rate, target_sr=self._algo_audio_sample_rate)

                # --- Pad to exactly 1 second (algo_audio_sample_rate samples) for Whisper ---
                target_len = self._algo_audio_sample_rate
                if len(segment) > target_len:
                    logger.error(f"Segment too long: {len(segment)} > {target_len}, speech_id={speech_id}")
                    raise ValueError(f"Segment too long: {len(segment)} > {target_len}")
                if len(segment) < target_len:
                    segment = np.pad(segment, (0, target_len - len(segment)), mode='constant')

                # --- Extract Whisper features (GPU, via _inference_lock) ---
                t0 = time.time()
                whisper_chunks = self._avatar.extract_whisper_feature(segment, self._algo_audio_sample_rate)
                t1 = time.time()

                # --- Frame alignment: split audio into per-frame segments ---
                # Config guarantees output_audio_sample_rate % fps == 0, so
                # samples_per_frame is exact and every frame gets a fixed-length segment.
                orig_audio_len = len(audio_data)
                samples_per_frame = self._output_audio_sample_rate // fps
                num_frames = int(np.ceil(orig_audio_len / samples_per_frame))
                whisper_chunks = whisper_chunks[:num_frames]

                # Pad tail so the last frame is also exactly samples_per_frame long
                target_audio_len = num_frames * samples_per_frame
                if orig_audio_len < target_audio_len:
                    audio_data = np.pad(audio_data, (0, target_audio_len - orig_audio_len), mode='constant')

                num_chunks = len(whisper_chunks)
                if self._interrupted.is_set():
                    continue

                # --- Dispatch per-frame WhisperQueueItems ---
                for i in range(num_chunks):
                    if self._interrupted.is_set():
                        break
                    whisper_chunk = whisper_chunks[i:i+1]
                    audio_segment = audio_data[i * samples_per_frame : (i + 1) * samples_per_frame]
                    is_last_chunk = (i == num_chunks - 1)
                    self._whisper_queue.put(WhisperQueueItem(
                        whisper_chunks=whisper_chunk,
                        speech_id=speech_id,
                        end_of_speech=end_of_speech and is_last_chunk,
                        audio_data=audio_segment,
                    ), timeout=1)

                t_end = time.time()
                if self._config.debug:
                    logger.info(f"[FEATURE_WORKER] speech_id={speech_id}, total_time={(t_end-t_start)*1000:.1f}ms, num_chunks={num_chunks}, orig_audio_len={orig_audio_len}, end_of_speech={end_of_speech}")
            except queue.Empty:
                continue
            except Exception as e:
                logger.opt(exception=True).error(f"Exception in _feature_extractor_worker: {e}")
                continue

    def _collect_batch(self):
        """Collect a full batch from _whisper_queue with padding. Returns None on stop/interrupt.

        Returns:
            tuple: (whisper_batch, batch_audio, batch_speech_id, batch_end_of_speech, valid_num, frame_ids)
                   or None if stopped/interrupted.
        """
        batch_size = self._config.batch_size
        orig_samples_per_frame = int(self._output_audio_sample_rate / self._config.fps)
        max_speaking_buffer = batch_size * 5                       # Backpressure threshold for _output_queue
        batch_chunks = []
        batch_audio = []
        batch_speech_id = []
        batch_end_of_speech = []

        while not self._stop_event.is_set():
            # --- Interrupt: discard partial batch and wait ---
            if self._interrupted.is_set():
                batch_chunks.clear()
                batch_audio.clear()
                batch_speech_id.clear()
                batch_end_of_speech.clear()
                time.sleep(0.01)
                continue

            # --- Backpressure: pause when _output_queue is too deep ---
            while self._output_queue.qsize() > max_speaking_buffer and not self._stop_event.is_set():
                if self._config.debug:
                    logger.info(f"[FRAME_GEN] output buffer full, waiting... output_queue_size={self._output_queue.qsize()}, max_speaking_buffer={max_speaking_buffer}")
                time.sleep(0.01)

            try:
                item: WhisperQueueItem = self._whisper_queue.get(timeout=1)
                # Re-check interrupt after blocking get (data may be stale)
                if self._interrupted.is_set():
                    batch_chunks.clear()
                    batch_audio.clear()
                    batch_speech_id.clear()
                    batch_end_of_speech.clear()
                    continue

                batch_chunks.append(item.whisper_chunks)
                batch_audio.append(item.audio_data)
                batch_speech_id.append(item.speech_id)
                batch_end_of_speech.append(item.end_of_speech)

                # Submit batch when full OR on end_of_speech (don't delay speech_end signal)
                if len(batch_chunks) == batch_size or item.end_of_speech:
                    valid_num = len(batch_chunks)

                    # --- Pad incomplete batch with zeros to reach batch_size ---
                    if valid_num < batch_size:
                        logger.warning(f"[FRAME_GEN] valid_num < batch_size, valid_num={valid_num}, batch_size={batch_size}")
                        pad_num = batch_size - valid_num
                        pad_shape = list(batch_chunks[0].shape)
                        if isinstance(batch_chunks[0], torch.Tensor):
                            pad_chunks = [torch.zeros(pad_shape, dtype=batch_chunks[0].dtype, device=batch_chunks[0].device) for _ in range(pad_num)]
                        else:
                            pad_chunks = [np.zeros(pad_shape, dtype=batch_chunks[0].dtype) for _ in range(pad_num)]
                        batch_chunks.extend(pad_chunks)
                        batch_audio.extend([np.zeros(orig_samples_per_frame, dtype=np.float32) for _ in range(pad_num)])
                        batch_speech_id.extend([batch_speech_id[-1]] * pad_num)
                        batch_end_of_speech.extend([False] * pad_num)

                    # --- Concatenate whisper chunks into a batch tensor ---
                    if isinstance(batch_chunks[0], torch.Tensor):
                        whisper_batch = torch.cat(batch_chunks, dim=0)
                    else:
                        whisper_batch = np.concatenate(batch_chunks, axis=0)

                    # --- Acquire frame_ids from Frame Collector (backpressure: blocks until Collector allocates) ---
                    frame_ids = []
                    for _ in range(batch_size):
                        while not self._stop_event.is_set():
                            if self._interrupted.is_set():
                                return None
                            try:
                                frame_ids.append(self._frame_id_queue.get(timeout=0.5))
                                break
                            except Empty:
                                continue
                    if self._stop_event.is_set():
                        return None
                    return (whisper_batch, batch_audio, batch_speech_id, batch_end_of_speech, valid_num, frame_ids)
            except queue.Empty:
                time.sleep(0.01)
                continue
        return None

    def _frame_generator_unet_worker(self):
        """UNet-only stage (multi_thread_inference=True): collect batch -> UNet -> _unet_queue."""
        batch_size = self._config.batch_size

        # --- CUDA warmup ---
        if torch.cuda.is_available():
            t0 = time.time()
            dummy_whisper = torch.zeros(batch_size, 50, 384, device=self._avatar.device, dtype=self._avatar.weight_dtype)
            self._avatar.generate_frames_unet(dummy_whisper, 0, batch_size)
            torch.cuda.synchronize()
            t1 = time.time()
            logger.info(f"[THREAD_WARMUP] _frame_generator_unet_worker thread id: {threading.get_ident()} warmup done, time: {(t1-t0)*1000:.1f} ms")

        while not self._stop_event.is_set():
            # --- Collect batch (blocks until batch_size chunks or end_of_speech) ---
            result = self._collect_batch()
            if result is None:
                continue
            whisper_batch, batch_audio, batch_speech_id, batch_end_of_speech, valid_num, frame_ids = result

            # --- UNet inference (GPU, via _inference_lock) ---
            batch_start_time = time.time()
            try:
                pred_latents, idx_list = self._avatar.generate_frames_unet(whisper_batch, frame_ids[0], batch_size)
            except Exception as e:
                # Fallback: zero latents to keep pipeline flowing (will produce black face)
                logger.opt(exception=True).error(f"[GEN_FRAME_ERROR] frame_id={frame_ids[0]}, speech_id={batch_speech_id[0]}, error: {e}")
                pred_latents = torch.zeros((batch_size, 4, 32, 32), dtype=self._avatar.unet.model.dtype, device=self._avatar.device)
                idx_list = [frame_ids[0] + i for i in range(batch_size)]
            if self._config.debug:
                logger.info(f"[FRAME_GEN] UNet batch: speech_id={batch_speech_id[0]}, batch_size={batch_size}, time={(time.time() - batch_start_time)*1000:.1f}ms")
            if self._interrupted.is_set():
                continue

            # --- Enqueue entire batch as a single UNetQueueItem for VAE worker ---
            self._unet_queue.put(UNetQueueItem(
                pred_latents=pred_latents,
                speech_id=batch_speech_id,
                avatar_status=MuseTalkAvatarStatus.SPEAKING,
                end_of_speech=batch_end_of_speech,
                audio_data=batch_audio,
                valid_num=valid_num,
                idx_list=idx_list,
                timestamp=time.time(),
            ))

    def _frame_generator_vae_worker(self):
        """VAE decode stage (multi_thread_inference=True): _unet_queue -> VAE -> _compose_queue."""
        batch_size = self._config.batch_size

        # --- CUDA warmup ---
        if torch.cuda.is_available():
            t0 = time.time()
            dummy_latents = torch.zeros(batch_size, 4, 32, 32, device=self._avatar.device, dtype=self._avatar.weight_dtype)
            idx_list = [i for i in range(batch_size)]
            self._avatar.generate_frames_vae(dummy_latents, idx_list, batch_size)
            torch.cuda.synchronize()
            t1 = time.time()
            logger.info(f"[THREAD_WARMUP] _frame_generator_vae_worker thread id: {threading.get_ident()} warmup done, time: {(t1-t0)*1000:.1f} ms")

        while not self._stop_event.is_set():
            if self._interrupted.is_set():
                time.sleep(0.01)
                continue
            try:
                item: UNetQueueItem = self._unet_queue.get(timeout=1)
                if self._interrupted.is_set():
                    continue

                # --- VAE decode: pred_latents → face crops (GPU, via _inference_lock) ---
                cur_batch = item.pred_latents.shape[0]
                batch_start_time = time.time()
                try:
                    recon_idx_list = self._avatar.generate_frames_vae(item.pred_latents, item.idx_list, cur_batch)
                except Exception as e:
                    # Fallback: zero face crops
                    logger.opt(exception=True).error(f"[GEN_FRAME_ERROR] frame_id={item.idx_list[0]}, speech_id={item.speech_id[0] if isinstance(item.speech_id, list) else item.speech_id}, error: {e}")
                    recon_idx_list = [(np.zeros((256, 256, 3), dtype=np.uint8), item.idx_list[0] + i) for i in range(cur_batch)]
                if self._config.debug:
                    logger.info(f"[FRAME_GEN] VAE batch: batch_size={cur_batch}, time={(time.time() - batch_start_time)*1000:.1f}ms")
                if self._interrupted.is_set():
                    continue

                # --- Split batch into per-frame ComposeQueueItems (only valid_num, skip padding) ---
                for i in range(item.valid_num):
                    if self._interrupted.is_set():
                        break
                    recon, idx = recon_idx_list[i]
                    self._compose_queue.put(ComposeQueueItem(
                        recon=recon, idx=idx,
                        speech_id=item.speech_id[i],
                        avatar_status=MuseTalkAvatarStatus.SPEAKING,
                        end_of_speech=item.end_of_speech[i],
                        audio_segment=item.audio_data[i],
                        frame_id=idx, timestamp=time.time(),
                    ))
            except queue.Empty:
                continue

    def _frame_generator_worker(self):
        """Single-thread inference (multi_thread_inference=False): collect batch -> UNet+VAE -> _compose_queue."""
        batch_size = self._config.batch_size

        # --- CUDA warmup ---
        if torch.cuda.is_available():
            t0 = time.time()
            dummy_whisper = torch.zeros(batch_size, 50, 384, device=self._avatar.device, dtype=self._avatar.weight_dtype)
            self._avatar.generate_frames(dummy_whisper, 0, batch_size)
            torch.cuda.synchronize()
            t1 = time.time()
            logger.info(f"[THREAD_WARMUP] _frame_generator_worker thread id: {threading.get_ident()} warmup done, time: {(t1-t0)*1000:.1f} ms")

        while not self._stop_event.is_set():
            # --- Collect batch ---
            result = self._collect_batch()
            if result is None:
                continue
            whisper_batch, batch_audio, batch_speech_id, batch_end_of_speech, valid_num, frame_ids = result

            # --- UNet + VAE combined inference (GPU, via _inference_lock) ---
            batch_start_time = time.time()
            try:
                recon_idx_list = self._avatar.generate_frames(whisper_batch, frame_ids[0], batch_size)
            except Exception as e:
                # Fallback: zero face crops
                logger.opt(exception=True).error(f"[GEN_FRAME_ERROR] frame_id={frame_ids[0]}, speech_id={batch_speech_id[0]}, error: {e}")
                recon_idx_list = [(np.zeros((256, 256, 3), dtype=np.uint8), frame_ids[0] + i) for i in range(batch_size)]
            if self._config.debug:
                logger.info(f"[FRAME_GEN] Full batch: speech_id={batch_speech_id[0]}, batch_size={batch_size}, time={(time.time() - batch_start_time)*1000:.1f}ms")
            if self._interrupted.is_set():
                continue

            # --- Split batch into per-frame ComposeQueueItems (only valid_num, skip padding) ---
            for i in range(valid_num):
                if self._interrupted.is_set():
                    break
                recon, idx = recon_idx_list[i]
                self._compose_queue.put(ComposeQueueItem(
                    recon=recon, idx=idx,
                    speech_id=batch_speech_id[i],
                    avatar_status=MuseTalkAvatarStatus.SPEAKING,
                    end_of_speech=batch_end_of_speech[i],
                    audio_segment=batch_audio[i],
                    frame_id=idx, timestamp=time.time(),
                ))

    def _compose_worker(self):
        """Compose face crop onto full frame (CPU, no _inference_lock): _compose_queue -> _output_queue."""
        while not self._stop_event.is_set():
            try:
                item: ComposeQueueItem = self._compose_queue.get(timeout=0.1)
                if self._interrupted.is_set():
                    continue
                frame = self._avatar.res2combined(item.recon, item.idx)
                item.frame = frame
                self._output_queue.put(item)
            except queue.Empty:
                continue

    def _frame_collector_worker(self):
        """Frame-rate metronome: strictly outputs one frame per 1/fps second.
        Also allocates frame_ids to control inference backpressure.
        """
        fps = self._config.fps
        frame_interval = 1.0 / fps                                 # Seconds per frame
        start_time = time.perf_counter()                           # Absolute reference for drift-free timing
        local_frame_id = 0
        last_active_speech_id = None
        last_speaking = False
        last_end_of_speech = False
        current_speech_id = None
        max_frame_id_buffer = self._config.batch_size * 3          # Max frame_ids to pre-allocate

        while not self._stop_event.is_set():
            # --- Precise timing: absolute time avoids cumulative drift ---
            target_time = start_time + local_frame_id * frame_interval
            now = time.perf_counter()
            sleep_time = target_time - now
            if sleep_time > 0.002:
                time.sleep(sleep_time - 0.001)                     # Coarse wait (leave 1ms margin)
            while time.perf_counter() < target_time:               # Spin wait for sub-ms accuracy
                pass
            t_frame_start = time.perf_counter()

            # --- Allocate frame_id (backpressure: inference thread blocks until Collector allocates) ---
            if not self._interrupted.is_set() and self._frame_id_queue.qsize() < max_frame_id_buffer:
                self._frame_id_queue.put(local_frame_id)

            # --- Try to get a speaking frame (non-blocking) ---
            output_item: Optional[ComposeQueueItem] = None
            try:
                output_item = self._output_queue.get_nowait()
            except queue.Empty:
                pass
            if output_item is not None and self._interrupted.is_set():
                output_item = None                                 # Discard stale frame on interrupt

            # --- Decide output: speaking frame vs idle frame ---
            if output_item is not None:
                frame = output_item.frame
                speech_id = output_item.speech_id
                avatar_status = output_item.avatar_status
                end_of_speech = output_item.end_of_speech
                frame_timestamp = output_item.timestamp
                audio_segment = output_item.audio_segment
            else:
                frame = self._avatar.generate_idle_frame(local_frame_id)
                speech_id = last_active_speech_id
                avatar_status = MuseTalkAvatarStatus.LISTENING
                end_of_speech = False
                frame_timestamp = time.time()
                audio_segment = None

            is_idle = (output_item is None)
            is_speaking = (avatar_status == MuseTalkAvatarStatus.SPEAKING)
            is_end_of_speech = bool(end_of_speech)

            # --- Logging: speaking START/END transitions and idle insertion ---
            if self._config.debug:
                if is_speaking:
                    if speech_id != current_speech_id:
                        logger.info(f"[SPEAKING_FRAME][START] frame_id={local_frame_id}, speech_id={speech_id}, status={avatar_status}, end_of_speech={end_of_speech}, video_timestamp={frame_timestamp}")
                        current_speech_id = speech_id
                    if is_end_of_speech:
                        logger.info(f"[SPEAKING_FRAME][END] frame_id={local_frame_id}, speech_id={speech_id}, status={avatar_status}, end_of_speech={end_of_speech}, video_timestamp={frame_timestamp}")
                        current_speech_id = None
                    if not is_end_of_speech and (speech_id == current_speech_id):
                        logger.info(f"[SPEAKING_FRAME] frame_id={local_frame_id}, speech_id={speech_id}, status={avatar_status}, end_of_speech={end_of_speech}, video_timestamp={frame_timestamp}")
                elif is_idle and last_speaking:
                    if last_end_of_speech:
                        logger.info(f"[IDLE_FRAME] Start after speaking: frame_id={local_frame_id}, status={avatar_status}")
                    else:
                        logger.warning(f"[IDLE_FRAME] Inserted idle during speaking: frame_id={local_frame_id}")
            else:
                if is_speaking and speech_id != current_speech_id:
                    logger.info(f"[SPEAKING_FRAME] Start: frame_id={local_frame_id}, speech_id={speech_id}")
                    current_speech_id = speech_id
                if is_speaking and is_end_of_speech:
                    logger.info(f"[SPEAKING_FRAME] End: frame_id={local_frame_id}, speech_id={speech_id}, end_of_speech=True")
                    current_speech_id = None
                if is_idle and last_speaking:
                    if last_end_of_speech:
                        logger.info(f"[IDLE_FRAME] Start after speaking: frame_id={local_frame_id}")
                    else:
                        logger.warning(f"[IDLE_FRAME] Inserted idle during speaking: frame_id={local_frame_id}")

            # --- Output callbacks: video (every frame), audio (speaking only), speech_end ---
            self._notify_video(frame)
            audio_len = len(audio_segment) if audio_segment is not None else 0
            if audio_segment is not None and audio_len > 0:
                audio_np = np.asarray(audio_segment, dtype=np.float32)
                if audio_np.ndim == 1:
                    audio_np = audio_np[np.newaxis, :]             # Ensure shape [1, N] for mono audio
                self._notify_audio(audio_np)
            if end_of_speech:
                logger.info(f"Status change: SPEAKING -> LISTENING, speech_id={speech_id}")
                self._notify_speech_end(speech_id)

            # --- Per-frame profiling (debug only) ---
            t_frame_end = time.perf_counter()
            if self._config.debug and (t_frame_end - t_frame_start > frame_interval):
                logger.warning(f"[PROFILE] frame_id={local_frame_id} total={t_frame_end-t_frame_start:.4f}s (>{frame_interval:.4f}s)")

            # --- Update state for next iteration ---
            if is_speaking:
                last_active_speech_id = speech_id
            local_frame_id += 1
            last_speaking = is_speaking
            last_end_of_speech = is_end_of_speech

    # --- Callback dispatchers (called from worker threads) ---

    def _notify_audio(self, audio_data: np.ndarray):
        if self._callbacks and self._callbacks.on_audio_frame:
            try:
                self._callbacks.on_audio_frame(audio_data)
            except Exception as e:
                logger.opt(exception=True).error(f"Exception in _notify_audio: {e}")

    def _notify_video(self, frame: np.ndarray):
        if self._callbacks and self._callbacks.on_video_frame:
            try:
                self._callbacks.on_video_frame(frame)
            except Exception as e:
                logger.opt(exception=True).error(f"Exception in _notify_video: {e}")

    def _notify_speech_end(self, speech_id: str):
        if self._callbacks and self._callbacks.on_speech_end:
            try:
                self._callbacks.on_speech_end(speech_id)
            except Exception as e:
                logger.opt(exception=True).error(f"Exception in _notify_speech_end: {e}")

    # --- Interrupt and queue management ---

    def interrupt(self):
        """Interrupt current speech: set interrupt flag and clear all intermediate queues.
        Pipeline: _audio_queue -> _whisper_queue -> [_unet_queue] -> _frame_id_queue -> _compose_queue -> _output_queue
        """
        logger.info("MuseTalk processor interrupt: setting interrupted flag and clearing all queues")
        # 1. Increment generation_id to invalidate all enqueued data
        with self._generation_lock:
            self._generation_id += 1
        # 2. Set interrupt flag for fast worker skip/sleep
        self._interrupted.set()
        # 3. Drain all pipeline queues
        with self._frame_id_lock:
            for q in [self._audio_queue, self._whisper_queue, self._unet_queue, self._frame_id_queue, self._compose_queue, self._output_queue]:
                while not q.empty():
                    try:
                        q.get_nowait()
                    except Exception:
                        break
        # 4. Reset debug statistics
        self._audio_duration_sum = 0.0
        self._first_add_audio_time = None
        logger.info("MuseTalk processor interrupt: done")

    def _clear_queues(self):
        """Drain all pipeline queues. Used by _reset_runtime_state() and stop()."""
        with self._frame_id_lock:
            for q in [self._audio_queue, self._whisper_queue, self._unet_queue, self._frame_id_queue, self._compose_queue, self._output_queue]:
                while not q.empty():
                    try:
                        q.get_nowait()
                    except Exception as e:
                        logger.opt(exception=True).warning(f"Exception in _clear_queues: {e}")
                        pass
