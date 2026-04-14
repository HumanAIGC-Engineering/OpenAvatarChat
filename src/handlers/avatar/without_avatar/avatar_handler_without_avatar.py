from typing import Dict, Optional, cast
from uuid import uuid4

import numpy as np
from pydantic import BaseModel, Field

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.common.handler_base import HandlerBase
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel, ChatEngineConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundleEntry, DataBundle
from chat_engine.data_models.internal.handler_definition_data import HandlerBaseInfo, HandlerDetail, HandlerDataInfo, \
    ChatDataConsumeMode
from chat_engine.data_models.chat_stream_config import ChatStreamConfig


# ARKit 52 blendshape channel names
ARKIT_CHANNELS = [
    "browDownLeft", "browDownRight", "browInnerUp", "browOuterUpLeft", "browOuterUpRight",
    "cheekPuff", "cheekSquintLeft", "cheekSquintRight",
    "eyeBlinkLeft", "eyeBlinkRight", "eyeLookDownLeft", "eyeLookDownRight",
    "eyeLookInLeft", "eyeLookInRight", "eyeLookOutLeft", "eyeLookOutRight",
    "eyeLookUpLeft", "eyeLookUpRight", "eyeSquintLeft", "eyeSquintRight",
    "eyeWideLeft", "eyeWideRight",
    "jawForward", "jawLeft", "jawOpen", "jawRight",
    "mouthClose", "mouthDimpleLeft", "mouthDimpleRight", "mouthFrownLeft", "mouthFrownRight",
    "mouthFunnel", "mouthLeft", "mouthLowerDownLeft", "mouthLowerDownRight",
    "mouthPressLeft", "mouthPressRight", "mouthPucker", "mouthRight",
    "mouthRollLower", "mouthRollUpper", "mouthShrugLower", "mouthShrugUpper",
    "mouthSmileLeft", "mouthSmileRight", "mouthStretchLeft", "mouthStretchRight",
    "mouthUpperUpLeft", "mouthUpperUpRight",
    "noseSneerLeft", "noseSneerRight", "tongueOut"
]


class AvatarEmptyConfig(HandlerBaseConfigModel, BaseModel):
    audio_sample_rate: int = Field(default=24000)
    motion_frame_rate: int = Field(default=30)


class AvatarEmptyContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[AvatarEmptyConfig] = None


class HandlerAvatarEmpty(HandlerBase):
    """
    A passthrough avatar handler that converts AVATAR_AUDIO to AVATAR_MOTION_DATA
    without any actual avatar processing. It generates empty/zero motion data
    while passing through the audio data.
    """

    def __init__(self):
        super().__init__()

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=AvatarEmptyConfig
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        if not isinstance(handler_config, AvatarEmptyConfig):
            handler_config = AvatarEmptyConfig()
        # No model to load for empty handler

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        if not isinstance(handler_config, AvatarEmptyConfig):
            handler_config = AvatarEmptyConfig()
        context = AvatarEmptyContext(session_context.session_info.session_id)
        context.config = handler_config
        return context

    def get_handler_detail(self, session_context: SessionContext, context: HandlerContext) -> HandlerDetail:
        context = cast(AvatarEmptyContext, context)
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_framed_entry(
            name="arkit_face",
            shape=[1, 52],
            time_axis=0,
            sample_rate=context.config.motion_frame_rate,
            channel_axis=1,
            channel_names=ARKIT_CHANNELS
        ))
        definition.add_entry(DataBundleEntry.create_audio_entry(
            name="avatar_audio",
            channel_num=1,
            sample_rate=context.config.audio_sample_rate,
        ))
        inputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                input_consume_mode=ChatDataConsumeMode.ONCE,
            )
        }
        outputs = {
            ChatDataType.AVATAR_MOTION_DATA: HandlerDataInfo(
                type=ChatDataType.AVATAR_MOTION_DATA,
                definition=definition
            )
        }
        return HandlerDetail(
            inputs=inputs,
            outputs=outputs
        )

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        output_definition = output_definitions.get(ChatDataType.AVATAR_MOTION_DATA).definition
        context = cast(AvatarEmptyContext, context)

        is_last = inputs.is_last_data
        speech_text = inputs.data.get_meta("avatar_speech_text")

        audio = inputs.data.get_main_data()
        audio_data = audio.squeeze()

        audio_duration = len(audio_data) / context.config.audio_sample_rate
        num_frames = max(1, int(audio_duration * context.config.motion_frame_rate))

        arkit_data = np.zeros([num_frames, 52], dtype=np.float32)

        output = DataBundle(output_definition)
        output.set_main_data(arkit_data)
        output.set_data("avatar_audio", audio_data[np.newaxis, ...])
        streamer = context.data_submitter.get_streamer(ChatDataType.AVATAR_MOTION_DATA)
        stream_key = streamer.current_stream.identity.stream_key_str if streamer.current_stream is not None else None
        if stream_key is None:
            stream = streamer.new_stream(sources=[inputs.stream_id], name="without_avatar", config=ChatStreamConfig(cancelable=True))
            stream_key = stream.stream_key_str
        output.add_meta("stream_key", stream_key)
        if speech_text is not None:
            output.add_meta("avatar_speech_text", speech_text)

        context.submit_data(output, finish_stream=is_last)

    def destroy_context(self, context: HandlerContext):
        pass
