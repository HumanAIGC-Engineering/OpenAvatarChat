from loguru import logger
import torch.multiprocessing as mp
import threading
import time
from typing import Optional
from enum import Enum
import os

import sysconfig

cudnn_path = os.path.join(sysconfig.get_path("purelib"), "nvidia", "cudnn", "lib")
logger.info("cudnn_path: {}", cudnn_path)
os.environ["LD_LIBRARY_PATH"] = f"{cudnn_path}:{os.environ['LD_LIBRARY_PATH']}"


from handlers.avatar.liteavatar.avatar_output_handler import AvatarOutputHandler
from handlers.avatar.liteavatar.avatar_processor import AvatarProcessor
from handlers.avatar.liteavatar.avatar_processor_factory import AvatarProcessorFactory, AvatarAlgoType
from handlers.avatar.liteavatar.model.algo_model import AvatarInitOption, AudioResult, VideoResult, AvatarStatus
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


class Tts2FaceEvent(Enum):
    START = 1001
    STOP = 1002

    LISTENING_TO_SPEAKING = 2001
    SPEAKING_TO_LISTENING = 2002

class Tts2FaceOutputHandler(AvatarOutputHandler):
    def __init__(self, audio_output_queue, video_output_queue,
                 event_out_queue):
        self.audio_output_queue = audio_output_queue
        self.video_output_queue = video_output_queue
        self.event_out_queue = event_out_queue
        self._video_producer_counter = IntervalCounter("video_producer")

    def on_start(self, init_option: AvatarInitOption):
        logger.info("on algo processor start")

    def on_stop(self):
        logger.info("on algo processor stop")

    def on_audio(self, audio_result: AudioResult):
        audio_frame = audio_result.audio_frame
        audio_data = audio_frame.to_ndarray()
        self.audio_output_queue.put_nowait(audio_data)

    def on_video(self, video_result: VideoResult):
        self._video_producer_counter.add()
        video_frame = video_result.video_frame
        data = video_frame.to_ndarray(format="bgr24")
        self.video_output_queue.put_nowait(data)

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
        self._avatar_process = mp.Process(target=self.start_avatar, args=[handler_root, config])
        self._avatar_process.start()
    
    
    def get_status(self):
        return self.worker_status
    
    def recruit(self):
        self.worker_status = WorkerStatus.BUSY
    
    def release(self):
        self.worker_status = WorkerStatus.IDLE

    def start_avatar(self,
                     handler_root: str,
                     config: Tts2FaceConfigModel):

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
        # start event input loop
        event_in_loop = threading.Thread(target=self._event_input_loop)
        event_in_loop.start()
        
        # keep process alive
        while True:
            time.sleep(1)
    
    def _event_input_loop(self):
        while True:
            event: Tts2FaceEvent = self.event_in_queue.get()
            logger.info("receive event: {}", event)
            if event == Tts2FaceEvent.START:
                self.session_running = True
                result_hanler = Tts2FaceOutputHandler(
                    audio_output_queue=self.audio_out_queue,
                    video_output_queue=self.video_out_queue,
                    event_out_queue=self.event_out_queue,
                )
                self.processor.register_output_handler(result_hanler)
                self.processor.start()
                self.audio_input_thread = threading.Thread(target=self._audio_input_loop)
                self.audio_input_thread.start()

            elif event == Tts2FaceEvent.STOP:
                self.session_running = False
                self.processor.stop()
                self.processor.clear_output_handlers()
                self.audio_input_thread.join()
                self.audio_input_thread = None
                self._clear_mp_queues()
                self.context = None
    
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
                q.get()
    
    def destroy(self):
        """terminate avatar process when object is destroyed"""
        try:
            if self._avatar_process is not None:
                if self._avatar_process.is_alive():
                    logger.info("Terminating avatar process in destructor")
                    self._avatar_process.terminate()
                    self._avatar_process.join(timeout=5)
                    if self._avatar_process.is_alive():
                        logger.warning("Avatar process still alive after terminate, killing it")
                        self._avatar_process.kill()
                        self._avatar_process.join()
                logger.info("Avatar process terminated successfully")
        except Exception as e:
            logger.error(f"Error during avatar process cleanup: {e}")