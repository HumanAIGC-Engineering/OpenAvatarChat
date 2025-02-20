import enum
import math
import os
from abc import ABC
from typing import cast, Dict, Optional, Tuple

import numpy as np
from loguru import logger
from pydantic import BaseModel, Field

from chat_engine.common.handler_base import HandlerBase, HandlerDetail, HandlerDataInfo, HandlerBaseInfo
from chat_engine.common.chat_data_type import ChatDataType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry
from utils.directory_info import DirectoryInfo
from utils.general_slicer import SliceContext, slice_data


class SileroVADConfigModel(HandlerBaseConfigModel, BaseModel):
    speaking_threshold: float = Field(default=0.5)
    start_delay: int = Field(default=2048)
    end_delay: int = Field(default=5000)
    buffer_look_back: int = Field(default=1024)
    speech_padding: int = Field(default=512)


class SpeakingStatus(enum.Enum):
    PRE_START = enum.auto()
    START = enum.auto()
    END = enum.auto()


class HumanAudioVADContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: SileroVADConfigModel = SileroVADConfigModel()
        self.speaking_status = SpeakingStatus.END

        self.clip_size = 512

        self.audio_history = []
        self.history_length_limit = 0

        self.speech_length: int = 0
        self.silence_length: int = 0

        self.shared_states = None

        self.model_state: Optional[np.ndarray] = None
        self.slice_context: Optional[SliceContext] = None

        self.speech_id: int = 0

    def reset(self):
        self.audio_history.clear()
        self.speech_length = 0
        self.silence_length = 0
        self.slice_context.flush()

    def _update_status_on_pre_start(self, clip: np.ndarray):
        if self.speech_length >= self.config.start_delay:
            self.speaking_status = SpeakingStatus.START
            sample_num_to_fetch = self.config.buffer_look_back + self.config.start_delay
            slice_num_to_fetch = math.ceil(sample_num_to_fetch / self.clip_size)
            output_audio = np.concatenate(self.audio_history[-slice_num_to_fetch:], axis=0)
            output_audio = np.concatenate(
                [np.zeros(self.config.speech_padding, dtype=clip.dtype), output_audio], axis=0)
            self.speech_id += 1
            logger.info("Start of human speech")
            return output_audio, {"human_speech_start": True}
        else:
            if self.silence_length > 0:
                logger.info("Back to not started status")
                self.speaking_status = SpeakingStatus.END
            return None, {}

    def _update_status_on_start(self, clip: np.ndarray):
        if self.silence_length >= self.config.end_delay:
            self.speaking_status = SpeakingStatus.END
            output_audio = np.concatenate(
                [np.zeros(self.config.speech_padding, dtype=clip.dtype), clip], axis=0)
            logger.info("End of human speech")
            return output_audio, {"human_speech_end": True}
        else:
            return clip, {}

    def _update_status_on_end(self, _clip: np.ndarray):
        if self.speech_length > 0:
            logger.info("Pre start of new human speech")
            self.speaking_status = SpeakingStatus.PRE_START
        return None, {}

    def _append_to_history(self, clip: np.ndarray):
        self.audio_history.append(clip)
        while 0 < self.history_length_limit < len(self.audio_history):
            self.audio_history.pop(0)

    def update_status(self, speech_prob: float, clip: np.ndarray) -> Tuple[Optional[np.ndarray], Dict]:
        self._append_to_history(clip)
        if speech_prob > self.config.speaking_threshold:
            self.speech_length += self.clip_size
            self.silence_length = 0
        else:
            self.silence_length += self.clip_size
            self.speech_length = 0
        if self.speaking_status == SpeakingStatus.PRE_START:
            return self._update_status_on_pre_start(clip)
        elif self.speaking_status == SpeakingStatus.START:
            return self._update_status_on_start(clip)
        elif self.speaking_status == SpeakingStatus.END:
            return self._update_status_on_end(clip)


class HandlerAudioVAD(HandlerBase, ABC):
    def __init__(self):
        super().__init__()
        self.model = None

    def get_handler_info(self):
        return HandlerBaseInfo(
            name="SileroVad",
            config_model=SileroVADConfigModel
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config = None):
        import onnxruntime
        model_name = "silero_vad.onnx"
        model_path = os.path.join(DirectoryInfo.get_src_dir(),
                                  "third_party", "silero_vad",
                                  "src", "silero_vad", "data",
                                  model_name)
        options = onnxruntime.SessionOptions()
        options.inter_op_num_threads = 1
        options.intra_op_num_threads = 1
        options.log_severity_level = 4
        self.model = onnxruntime.InferenceSession(model_path,
                                                  providers=["CPUExecutionProvider"],
                                                  sess_options=options)

    def create_context(self, session_context: SessionContext, handler_config = None) -> HandlerContext:
        context = HumanAudioVADContext(session_context.session_info.session_id)
        context.shared_states = session_context.shared_states
        if isinstance(handler_config, SileroVADConfigModel):
            context.config = handler_config
        context.model_state = np.zeros((2, 1, 128), dtype=np.float32)
        context.slice_context = SliceContext.create_numpy_slice_context(
            slice_size=context.clip_size,
            slice_axis=0,
        )
        context.history_length_limit = math.ceil((context.config.start_delay + context.config.buffer_look_back)
                                                 / context.clip_size)
        return context

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_audio_entry("human_audio", 1, 16000))

        inputs = {
            ChatDataType.MIC_AUDIO: HandlerDataInfo(
                type=ChatDataType.MIC_AUDIO
            )
        }
        outputs = {ChatDataType.HUMAN_AUDIO: HandlerDataInfo(
                type=ChatDataType.HUMAN_AUDIO,
                definition=definition
            )
        }
        return HandlerDetail(
            inputs=inputs,
            outputs=outputs,
        )

    def _inference(self, context: HumanAudioVADContext, clip: np.ndarray, sr: int=16000):
        clip = clip.squeeze()
        if clip.ndim != 1:
            logger.warning("Input audio should be 1-dim array")
            return 0
        clip = np.expand_dims(clip, axis=0)
        inputs = {
            "input": clip,
            "sr": np.array([sr], dtype=np.int64),
            "state": context.model_state
        }
        prob, state = self.model.run(None, inputs)
        context.model_state = state
        return prob[0][0]

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        context = cast(HumanAudioVADContext, context)
        output_definition = output_definitions.get(ChatDataType.HUMAN_AUDIO).definition
        if not context.shared_states.enable_vad:
            return
        if inputs.type != ChatDataType.MIC_AUDIO:
            return

        audio = inputs.data.get_main_data()
        if audio is None:
            return
        audio = audio.squeeze()

        if audio.dtype != np.float32:
            audio = audio.astype(np.float32) / 32767

        for clip in slice_data(context.slice_context, audio):
            speech_prob = self._inference(context, clip)
            audio_clip, flags = context.update_status(speech_prob, clip)
            # FIXME this is a hack to disable VAD after human speech end,
            #  but it should be handled by client or downstream handlers
            human_speech_end = flags.get("human_speech_end", False)
            speech_id = f"speech-{context.session_id}-{context.speech_id}"
            if human_speech_end:
                context.shared_states.enable_vad = False
                context.reset()
            if audio_clip is not None:
                output = DataBundle(output_definition)
                output.set_main_data(np.expand_dims(audio_clip, axis=0))
                for flag_name, flag_value in flags.items():
                    output.add_meta(flag_name, flag_value)
                output.add_meta("speech_id", speech_id)
                yield output

    def destroy_context(self, context: HandlerContext):
        pass
