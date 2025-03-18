
from fractions import Fraction
from queue import Queue
import sys
from threading import Thread
import threading
import time
from typing import List

import av
import cv2
from loguru import logger
import numpy as np
from handlers.avatar.liteavatar.algo.audio2signal_speed_limiter import Audio2SignalSpeedLimiter
from handlers.avatar.liteavatar.algo.base_algo_adapter import BaseAlgoAdapter
from handlers.avatar.liteavatar.media.speech_audio_processor import SpeechAudioProcessor
from handlers.avatar.liteavatar.avatar_output_handler import AvatarOutputHandler
from handlers.avatar.liteavatar.media.video_audio_aligner import VideoAudioAligner
from handlers.avatar.liteavatar.model.algo_model import (
    AvatarInitOption, AudioResult, AudioSlice, AvatarStatus, MouthResult, SignalResult, VideoResult)
from handlers.avatar.liteavatar.model.audio_input import SpeechAudio
from src.utils.interval_counter import IntervalCounter


class AvatarProcessor:
    def __init__(self,
                 algo_adapter: BaseAlgoAdapter,
                 init_option: AvatarInitOption):
        
        ## TODO remove debugger logger
        logger.remove()
        logger.add(sys.stdout, level='INFO')

        logger.info("init avatar processor {}", init_option)
        self._output_handlers: List[AvatarOutputHandler] = []
        self._algo_adapter = algo_adapter
        self._init_option = init_option
        self._audio_slice_queue: Queue = None
        self._signal_queue: Queue = None
        self._mouth_img_queue: Queue = None
        self._speech_audio_processor: SpeechAudioProcessor = None

        # running context
        self._session_running = False
        self._audio2signal_thread: Thread = None
        self._signal2img_thread: Thread = None
        self._mouth2full_thread: Thread = None
        self._global_frame_count = 0
        self._current_audio_pts = 0     # in ms
        self._current_video_pts = 0
        self._last_speech_ended = True
        self._current_speech_id = ""
        self._session_start_time = 0
        self._callback_avatar_status: AvatarStatus = None

        # other helpers
        self._audio2signal_speed_limiter = None
        self._video_audio_aligner = None

        # statistic counter
        self._audio2signal_counter = IntervalCounter("generate signal")
        self._callback_counter = IntervalCounter("avatar callback")

        # for debug
        self._debug_mode = init_option.debug

        self._init_algo()

    def start(self):
        self._session_running = True
        self._callback_start()
        self._reset_processor_status()
        self._start_threads()
        self._session_start_time = time.time()

    def stop(self):
        logger.info("stop avatar processor, totol session time {:.3f}",
                    time.time() - self._session_start_time)
        self._session_running = False
        self._callback_stop()
        if self._signal2img_thread is not None:
            self._signal2img_thread.join()
        if self._audio2signal_thread is not None:
            self._audio2signal_thread.join()
        if self._mouth2full_thread is not None:
            self._mouth2full_thread.join()
        logger.info("avatar processor stopped")

    def add_audio(self, speech_audio: SpeechAudio):
        audio_slices = self._speech_audio_processor.get_speech_audio_slice(speech_audio)
        for audio_slice in audio_slices:
            self._audio_slice_queue.put(audio_slice)

    def clear_output_handlers(self):
        self._output_handlers.clear()

    def register_output_handler(self,
                                avatar_output_handler: AvatarOutputHandler):
        self._output_handlers.append(avatar_output_handler)

    def interrupt(self):
        """
        clear input audio
        """
        if self._audio_slice_queue is not None:
            self._audio_slice_queue.queue.clear()

    def _audio2signal_loop(self):
        """
        generate signal for signal2img
        """
        logger.info("audio2signal loop started")
        speech_id = ""
        audio_slice = None
        self._audio2signal_speed_limiter.start()
        target_round_time = 0.9
        while self._session_running:
            start_time = time.time()
            try:
                audio_slice: AudioSlice = self._audio_slice_queue.get(timeout=0.1)
                target_round_time = audio_slice.get_audio_duration() - 0.1
            except Exception:
                continue

            speech_id = audio_slice.speech_id
            if speech_id != self._current_speech_id:
                self._last_speech_ended = False
                self._current_speech_id = speech_id
            if audio_slice.end_of_speech:
                self._last_speech_ended = True

            logger.info("audio2signal input audio durtaion {}", audio_slice.get_audio_duration())
            signal_vals = self._algo_adapter.audio2signal(audio_slice)
            avatar_status = AvatarStatus.SPEAKING

            # remove front padding audio and relative frames
            front_padding_duration = audio_slice.front_padding_duration
            target_round_time = audio_slice.get_audio_duration() - front_padding_duration - 0.1
            padding_frame_count = int(front_padding_duration * self._init_option.video_frame_rate)
            signal_vals = signal_vals[padding_frame_count:]
            padding_audio_count = int(front_padding_duration) * self._init_option.audio_sample_rate * 2
            audio_slice.play_audio_data = audio_slice.play_audio_data[padding_audio_count:]

            audio_slice.play_audio_data = self._video_audio_aligner.get_speech_level_algined_audio(
                audio_slice.play_audio_data, audio_slice.play_audio_sample_rate, len(signal_vals),
                audio_slice.speech_id, audio_slice.end_of_speech)

            for i, signal in enumerate(signal_vals):
                end_of_speech = audio_slice.end_of_speech and i == len(signal_vals) - 1
                middle_result = SignalResult(
                    speech_id=speech_id,
                    end_of_speech=end_of_speech,
                    middle_data=signal,
                    frame_id=i,
                    global_frame_id=self._global_frame_count,
                    avatar_status=avatar_status,
                    audio_slice=audio_slice if i == 0 else None
                )
                self._audio2signal_counter.add()
                self._signal_queue.put_nowait(middle_result)
            cost = time.time() - start_time
            sleep_time = target_round_time - cost
            if sleep_time > 0:
                time.sleep(sleep_time)
        logger.info("audio2signal loop stopped")

    def _signal2img_loop(self):
        """
        generate image and do callbacks
        """
        logger.info("signal2img loop started")
        start_time = -1
        timestamp = 0
        
        # delay start to ensure no extra audio and video generated
        time.sleep(0.5)
        
        while self._session_running:
            if self._signal_queue.empty():
                # generate idle
                signal_val = self._algo_adapter.get_idle_signal(1)[0]
                avatar_status = AvatarStatus.LISTENING if self._last_speech_ended else AvatarStatus.SPEAKING
                signal = SignalResult(
                    speech_id=self._current_speech_id,
                    end_of_speech=False,
                    middle_data=signal_val,
                    frame_id=0,
                    avatar_status=avatar_status,
                    audio_slice=self._get_idle_audio_slice(1)
                )
            else:
                signal: SignalResult = self._signal_queue.get_nowait()

            out_image, bg_frame_id = self._algo_adapter.signal2img(signal.middle_data, signal.avatar_status)
            # create mouth result
            mouth_result = MouthResult(
                speech_id=signal.speech_id,
                mouth_image=out_image,
                bg_frame_id=bg_frame_id,
                end_of_speech=signal.end_of_speech,
                avatar_status=signal.avatar_status,
                audio_slice=signal.audio_slice,
                global_frame_id=self._global_frame_count
            )
            
            self._global_frame_count += 1

            self._mouth_img_queue.put(mouth_result)

            if start_time == -1:
                start_time = time.time()
                timestamp = 0
            else:
                timestamp += 1 / self._init_option.video_frame_rate
                wait = start_time + timestamp - time.time()
                if wait > 0:
                    time.sleep(wait)

        logger.info("signal2img loop ended")

    def _mouth2full_loop(self):
        logger.info("combine img loop started")
        while self._session_running:
            try:
                mouth_reusult: MouthResult = self._mouth_img_queue.get(timeout=0.1)
            except Exception:
                continue
            image = mouth_reusult.mouth_image
            bg_frame_id = mouth_reusult.bg_frame_id
            full_img = self._algo_adapter.mouth2full(image, bg_frame_id)
            
            if mouth_reusult.audio_slice is not None:
                # create audio result
                audio_data = mouth_reusult.audio_slice.play_audio_data
                audio_frame = av.AudioFrame.from_ndarray(
                    np.frombuffer(audio_data, dtype=np.int16).reshape(1, -1),
                    format="s16",
                    layout="mono"
                )
                audio_time_base = Fraction(1, self._init_option.audio_sample_rate)
                audio_frame.time_base = audio_time_base
                audio_frame.pts = self._current_audio_pts
                audio_frame.sample_rate = mouth_reusult.audio_slice.play_audio_sample_rate
                self._current_audio_pts += len(audio_data) // 2

                audio_result = AudioResult(
                    audio_frame=audio_frame,
                    speech_id=mouth_reusult.audio_slice.speech_id
                )
                self._callback_audio(audio_result)
                logger.debug("create audio with duration {:.3f}s, status: {}",
                             mouth_reusult.audio_slice.get_audio_duration(), mouth_reusult.avatar_status)
            # create video result
            if self._debug_mode:
                full_img = cv2.putText(
                    full_img, f"{mouth_reusult.avatar_status} {mouth_reusult.global_frame_id}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            full_img = cv2.flip(full_img, 1)
            video_frame = av.VideoFrame.from_ndarray(full_img, format="bgr24")
            video_frame.time_base = Fraction(1, self._init_option.video_frame_rate)
            video_frame.pts = self._current_video_pts
            self._current_video_pts += 1

            image_result = VideoResult(
                video_frame=video_frame,
                speech_id=mouth_reusult.speech_id,
                avatar_status=mouth_reusult.avatar_status,
                end_of_speech=mouth_reusult.end_of_speech,
                bg_frame_id=bg_frame_id
            )

            self._callback_image(image_result)
            
            if self._callback_avatar_status != image_result.avatar_status and self._callback_avatar_status is not None:
                self._callback_avatar_status_changed(mouth_reusult.speech_id, image_result.avatar_status)
            self._callback_avatar_status = image_result.avatar_status
            
        logger.info("combine img loop ended")

    def _reset_processor_status(self):
        self._audio_slice_queue = Queue()
        self._signal_queue = Queue()
        self._mouth_img_queue = Queue()
        algo_config = self._algo_adapter.get_algo_config()
        self._speech_audio_processor = SpeechAudioProcessor(
            self._init_option.audio_sample_rate,
            algo_config.input_audio_sample_rate,
            algo_config.input_audio_slice_duration,
            enable_fast_mode=self._init_option.enable_fast_mode
        )
        self._audio2signal_speed_limiter = Audio2SignalSpeedLimiter(self._init_option.video_frame_rate)
        self._video_audio_aligner = VideoAudioAligner(self._init_option.video_frame_rate)

    def _init_algo(self):
        logger.info("init algo")
        self._algo_adapter.init(self._init_option)

    def _start_threads(self):
        self._audio2signal_thread = threading.Thread(target=self._audio2signal_loop)
        self._audio2signal_thread.start()
        self._signal2img_thread = threading.Thread(target=self._signal2img_loop)
        self._signal2img_thread.start()
        self._mouth2full_thread = threading.Thread(target=self._mouth2full_loop)
        self._mouth2full_thread.start()

    def _callback_image(self, image_result: VideoResult):
        self._callback_counter.add_property("callback_image")
        if self._session_running:
            for output_handler in self._output_handlers:
                output_handler.on_video(image_result)

    def _callback_audio(self, audio_result: AudioResult):
        audio_frame = audio_result.audio_frame
        self._callback_counter.add_property("callback_audio", audio_frame.samples / audio_frame.sample_rate)
        if self._session_running:
            for output_handler in self._output_handlers:
                output_handler.on_audio(audio_result)

    def _callback_start(self):
        for output_handler in self._output_handlers:
            output_handler.on_start(self._init_option)

    def _callback_stop(self):
        for output_handler in self._output_handlers:
            output_handler.on_stop()

    def _callback_avatar_status_changed(self, speech_id, avatar_status: AvatarStatus):
        for output_handler in self._output_handlers:
            output_handler.on_avatar_status_change(speech_id, avatar_status)
            
    def _get_idle_audio_slice(self, idle_frame_count):
        speech_id = "" if self._last_speech_ended else self._current_speech_id
        # generate silence audio
        frame_rate = self._init_option.video_frame_rate
        play_audio_sample_rate = self._init_option.audio_sample_rate
        idle_duration_seconds = idle_frame_count / frame_rate
        idle_data_length = int(2 * idle_duration_seconds * play_audio_sample_rate)
        idle_audio_data = bytes(idle_data_length)
        idle_audio_slice = AudioSlice(
            speech_id=speech_id,
            play_audio_data=idle_audio_data,
            play_audio_sample_rate=play_audio_sample_rate,
            algo_audio_data=None,
            algo_audio_sample_rate=0,
            end_of_speech=False
        )
        return idle_audio_slice
