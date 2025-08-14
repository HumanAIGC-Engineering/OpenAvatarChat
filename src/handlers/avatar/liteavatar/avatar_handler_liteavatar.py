from abc import ABC
from typing import cast, Optional, Dict

import numpy as np
from loguru import logger
import torch.multiprocessing as mp

from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundleEntry, \
    VariableSize
from handlers.avatar.liteavatar.model.audio_input import SpeechAudio
from chat_engine.common.handler_base import HandlerBase, HandlerDetail, HandlerBaseInfo, HandlerDataInfo, \
    ChatDataConsumeMode
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext, SharedStates
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel
from handlers.avatar.liteavatar.liteavatar_worker import Tts2FaceConfigModel
from handlers.avatar.liteavatar.liteavatar_handler_context import HandlerTts2FaceContext
from handlers.avatar.liteavatar.liteavatar_worker_manager import LiteAvatarWorkerManager


class HandlerTts2Face(HandlerBase, ABC):

    TARGET_FPS = 25
    
    def __init__(self):
        super().__init__()
        self.lite_avatar_worker_manager: Optional[LiteAvatarWorkerManager] = None
        
        self.output_data_definitions: Dict[ChatDataType, DataBundleDefinition] = {}

        self.shared_state: SharedStates = None
        
    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=Tts2FaceConfigModel,
            load_priority=-999,
        )
    
    def load(self,
             engine_config: ChatEngineConfigModel,
             handler_config: Optional[Tts2FaceConfigModel] = None):

        audio_output_definition = DataBundleDefinition()
        audio_output_definition.add_entry(DataBundleEntry.create_audio_entry(
            "avatar_audio",
            1,
            24000,
        ))
        audio_output_definition.lockdown()
        self.output_data_definitions[ChatDataType.AVATAR_AUDIO] = audio_output_definition

        video_output_definition = DataBundleDefinition()
        video_output_definition.add_entry(DataBundleEntry.create_framed_entry(
            "avatar_video",
            [VariableSize(), VariableSize(), VariableSize(), 3],
            0,
            30
        ))
        video_output_definition.lockdown()
        self.output_data_definitions[ChatDataType.AVATAR_VIDEO] = video_output_definition
        self.lite_avatar_worker_manager = LiteAvatarWorkerManager(
            handler_config.concurrent_limit, self.handler_root, handler_config)
    
    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[Tts2FaceConfigModel] = None) -> HandlerContext:
        self.shared_state = session_context.shared_states
        
        assert self.lite_avatar_worker_manager is not None
        
        worker = self.lite_avatar_worker_manager.start_worker()
        if worker is None:
            raise Exception("No available lite avatar worker")

        context = HandlerTts2FaceContext("session", worker, self.shared_state)
        context.output_data_definitions = self.output_data_definitions
        return context

    def start_context(self, session_context, handler_context):
        pass

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        context = cast(HandlerTts2FaceContext, context)
        inputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                input_consume_mode=ChatDataConsumeMode.ONCE,
            )
        }
        outputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                definition=context.output_data_definitions[ChatDataType.AVATAR_AUDIO],
            ),
            ChatDataType.AVATAR_VIDEO: HandlerDataInfo(
                type=ChatDataType.AVATAR_VIDEO,
                definition=context.output_data_definitions[ChatDataType.AVATAR_VIDEO],
            ),
        }
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
        context.lite_avatar_worker.audio_in_queue.put(speech_audio)

    def destroy_context(self, context: HandlerContext):
        if isinstance(context, HandlerTts2FaceContext):
            logger.info("destroy context with session id: {}", context.session_id)
            context.clear()
    
    def destroy(self):
        if self.lite_avatar_worker_manager is not None:
            self.lite_avatar_worker_manager.destroy()
            self.lite_avatar_worker_manager = None


if __name__ == "__main__":
    s2v_handler = HandlerTts2Face()
    mp.spawn
    s2v_process = mp.Process(target=s2v_handler.start)
    s2v_process.start()
