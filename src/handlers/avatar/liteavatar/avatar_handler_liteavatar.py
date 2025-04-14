from abc import ABC
import asyncio
from typing import cast, Optional, Dict
from enum import Enum
import threading
import time

import numpy as np
from loguru import logger
from pydantic import BaseModel, Field
import torch.multiprocessing as mp

from handlers.avatar.liteavatar.avatar_output_handler import AvatarOutputHandler
from handlers.avatar.liteavatar.avatar_processor import AvatarProcessor
from handlers.avatar.liteavatar.avatar_processor_factory import AvatarProcessorFactory, AvatarAlgoType
from handlers.avatar.liteavatar.model.algo_model import AvatarInitOption, AudioResult, VideoResult, AvatarStatus
from handlers.avatar.liteavatar.model.audio_input import SpeechAudio
from chat_engine.common.engine_channel_type import EngineChannelType
from chat_engine.common.handler_base import HandlerBase, HandlerDetail, HandlerBaseInfo, HandlerDataInfo
from chat_engine.common.chat_data_type import ChatDataType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext, SharedStates
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from utils.interval_counter import IntervalCounter


class Tts2FaceEvent(Enum):
    START = 1001
    STOP = 1002

    LISTENING_TO_SPEAKING = 2001
    SPEAKING_TO_LISTENING = 2002


class Tts2FaceConfigModel(HandlerBaseConfigModel, BaseModel):
    avatar_name: str = Field(default="sample_data")
    debug: bool = Field(default=False)
    fps: int = Field(default=25)
    enable_fast_mode: bool = Field(default=False)
    use_gpu: bool = Field(default=True)


class Tts2FaceOutputHandler(AvatarOutputHandler):
    def __init__(self, audio_output_queue, video_output_queue,
                 event_out_queue):
        self.audio_output_queue = audio_output_queue
        self.video_output_queue = video_output_queue
        self.evnet_out_queue = event_out_queue
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
            self.evnet_out_queue.put_nowait(Tts2FaceEvent.SPEAKING_TO_LISTENING)
 

class AvatarProcessorWrapper:
    def __init__(self,
                 ):
        self.event_in_queue: Optional[mp.Queue] = None
        self.event_out_queu: Optional[mp.Queue] = None
        self.audio_in_queue: Optional[mp.Queue] = None
        self.audio_out_queue: Optional[mp.Queue] = None
        self.video_out_queue: Optional[mp.Queue] = None
        self.io_queues = []
        self.processor: Optional[AvatarProcessor] = None
        self.session_running = False
        self.audio_input_thread = None

    def start_avatar(self,
                     handler_root: str,
                     config: Tts2FaceConfigModel,
                     event_in_queue,
                     event_out_queue,
                     audio_in_queue,
                     audio_out_queue,
                     video_out_queue):
        self.event_in_queue = event_in_queue
        self.event_out_queue = event_out_queue
        self.audio_in_queue = audio_in_queue
        self.audio_out_queue = audio_out_queue
        self.video_out_queue = video_out_queue
        self.io_queues = [
            event_in_queue,
            event_out_queue,
            audio_in_queue,
            audio_out_queue,
            video_out_queue
        ]

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


class HandlerTts2FaceContext(HandlerContext):
    def __init__(self,
                 session_id: str,
                 event_in_queue,
                 audio_out_queue,
                 video_out_queue,
                 event_out_queue,
                 rtc_audio_queue,
                 rtc_video_queue,
                 shared_status):
        super().__init__(session_id)
        self.result_handler: Optional[Tts2FaceOutputHandler] = None
        self.event_in_queue: mp.Queue = event_in_queue
        self.audio_out_queue: mp.Queue = audio_out_queue
        self.video_out_queue: mp.Queue = video_out_queue
        self.event_out_queue: mp.Queue = event_out_queue
        self.rtc_audio_queue: asyncio.Queue = rtc_audio_queue
        self.rtc_video_queue: asyncio.Queue = rtc_video_queue
        self.shared_state: SharedStates = shared_status
        
        self.media_out_thread: threading.Thread = None
        self.event_out_thread: threading.Thread = None

        self.loop_running = True
        self.media_out_thread = threading.Thread(target=self._media_out_loop)
        self.media_out_thread.start()
        self.event_out_thread = threading.Thread(target=self._event_out_loop)
        self.event_out_thread.start()

    def _media_out_loop(self):
        while self.loop_running:
            no_output = True
            # get audio
            if self.audio_out_queue.qsize() > 0:
                no_output = False
                try:
                    audio = self.audio_out_queue.get_nowait()
                    self.rtc_audio_queue.put_nowait(audio)
                    no_output = False
                except Exception:
                    pass
            # get video
            if self.video_out_queue.qsize() > 0:
                no_output = False
                try:
                    video = self.video_out_queue.get_nowait()
                    self.rtc_video_queue.put_nowait(video)
                    no_output = False
                except Exception:
                    pass
            if no_output:
                time.sleep(0.05)
                continue
        logger.info("media out loop exit")

    def _event_out_loop(self):
        while self.loop_running:
            try:
                event: Tts2FaceEvent = self.event_out_queue.get(timeout=0.1)
                logger.info("receive output event: {}", event)
                if event == Tts2FaceEvent.SPEAKING_TO_LISTENING:
                    self.shared_state.enable_vad = True
            except Exception:
                continue
        logger.info("event out loop exit")
    
    def clear(self):
        logger.info("clear tts2face context")
        self.loop_running = False
        self.event_in_queue.put_nowait(Tts2FaceEvent.STOP)
        self.media_out_thread.join()
        self.event_out_thread.join()


class HandlerTts2Face(HandlerBase, ABC):

    TARGET_FPS = 25
    
    def __init__(self):
        super().__init__()
        self.processor_wrapper: Optional[AvatarProcessorWrapper] = None
        self.processor = None
        self.io_queues = None
        self.context = None
        self.input_loop_thread = None
        self.event_loop_thread = None
        self.session_running = False
        self.managerInstance = mp.Manager()

        self.event_in_queue =self.managerInstance.Queue()
        self.event_out_queue = self.managerInstance.Queue()
        self.audio_in_queue = self.managerInstance.Queue()
        self.audio_out_queue = self.managerInstance.Queue()
        self.video_out_queue = self.managerInstance.Queue()
   
        self.shared_state: SharedStates = None
        
        self.rtc_audio_queue: asyncio.Queue = None
        self.rtc_video_queue: asyncio.Queue = None
        
        self.event_out_thread = None
        self.media_out_thread = None

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=Tts2FaceConfigModel,
            load_priority=-999,
        )
    
    def load(self,
             engine_config: ChatEngineConfigModel,
             handler_config: Optional[Tts2FaceConfigModel] = None):
        self.processor_wrapper = AvatarProcessorWrapper()
        # start process
        self._avatar_process = mp.Process(target=self.processor_wrapper.start_avatar,
                                          args=[
                                              self.handler_root,
                                              handler_config,
                                              self.event_in_queue,
                                              self.event_out_queue,
                                              self.audio_in_queue,
                                              self.audio_out_queue,
                                              self.video_out_queue
                                          ])
        self._avatar_process.start()
    
    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[Tts2FaceConfigModel] = None) -> HandlerContext:
        self.shared_state = session_context.shared_states
        
        self.rtc_audio_queue = session_context.output_queues.get(EngineChannelType.AUDIO)
        self.rtc_video_queue = session_context.output_queues.get(EngineChannelType.VIDEO)
        
        self.event_in_queue.put_nowait(Tts2FaceEvent.START)

        return HandlerTts2FaceContext("session",
                                      self.event_in_queue,
                                      self.audio_out_queue,
                                      self.video_out_queue,
                                      self.event_out_queue,
                                      self.rtc_audio_queue,
                                      self.rtc_video_queue,
                                      self.shared_state)
    
    def start_context(self, session_context, handler_context):
        pass

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        inputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
            )
        }
        outputs = {}
        return HandlerDetail(
            inputs=inputs, outputs=outputs,
        )

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        if inputs.type != ChatDataType.AVATAR_AUDIO:
            return
        context = cast(HandlerTts2FaceContext, context)
        speech_id = inputs.data.get_meta("speech_id")
        speech_end = inputs.data.get_meta("avatar_speech_end", False)
        audio_entry = inputs.data.get_main_definition_entry()
        audio_array = inputs.data.get_main_data()
        if audio_array is not None:
            if audio_array.dtype != np.int16:
                audio_array = (audio_array * 32767).astype(np.int16)
        else:
            audio_array = np.zeros([512], dtype=np.int16)
        #logger.info(f's2v: {audio_array.shape} type {type(audio_array)}')
        #logger.info(f'sample_rate {audio_entry.sample_rate}' )
        speech_audio = SpeechAudio(
            speech_id=speech_id,
            end_of_speech=speech_end,
            audio_data=audio_array.tobytes(),
            sample_rate=audio_entry.sample_rate,
        )
        self.audio_in_queue.put(speech_audio)

    def destroy_context(self, context: HandlerContext):
        if isinstance(context, HandlerTts2FaceContext):
            context.clear()


if __name__ == "__main__":
    s2v_handler = HandlerTts2Face()
    mp.spawn
    s2v_process = mp.Process(target=s2v_handler.start)
    s2v_process.start()
