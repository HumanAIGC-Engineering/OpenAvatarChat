import os
import time
from abc import ABC
from typing import Optional, cast, Dict

import librosa
import numpy as np
# noinspection PyPackageRequirements
import torch
from loguru import logger
from pydantic import BaseModel, Field
from transformers import AutoModel, AutoTokenizer

from chat_engine.common.handler_base import HandlerBase, HandlerDetail, HandlerBaseInfo, HandlerDataInfo
from chat_engine.common.chat_data_type import ChatDataType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry
from utils.directory_info import DirectoryInfo
from utils.general_slicer import SliceContext, slice_data


class MiniCPMConfig(HandlerBaseConfigModel, BaseModel):
    model_name: str = Field(default="MiniCPM-o-2_6")
    voice_prompt: str = Field(default="你是一个AI助手。你能接受视频，音频和文本输入并输出语音和文本。模仿输入音频中的声音特征。")
    assistant_prompt: str = Field(default="作为助手，你将使用这种声音风格说话。")


class MiniCPMContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config = None
        self.local_session_id = 0

        self.dump_audio = True
        self.audio_dump_file = None
        if self.dump_audio:
            dump_file_path = os.path.join(DirectoryInfo.get_project_dir(),
                                          f"dump_talk_audio.pcm")
            self.audio_dump_file = open(dump_file_path, "wb")

        self.sys_msg = None

        self.audio_prefill_length = 16000
        self.audio_prefill_cache = []
        self.audio_prefill_cached_length = 0

        self.audio_prefill_slice_context = SliceContext.create_numpy_slice_context(
            slice_size=16000,
            slice_axis=0,
        )


class HandlerS2SMiniCPM(HandlerBase, ABC):

    def __init__(self):
        super().__init__()
        self.device='cuda:0'
        self.model = None
        self.tokenizer = None
        self.module_path = os.path.join(DirectoryInfo.get_src_dir(), "third_party", "MiniCPM-o")
        self.ref_audio = None
        self.created_session_num = 0

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            name="S2S_MiniCPM",
            config_model=MiniCPMConfig,
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        model_name = "MiniCPM-o-2_6"
        if isinstance(handler_config, MiniCPMConfig):
            model_name = handler_config.model_name
        project_dir = DirectoryInfo.get_project_dir()
        model_path = os.path.join(project_dir, engine_config.model_root, model_name)
        if model_name == "MiniCPM-o-2_6-int4":
            # noinspection PyUnresolvedReferences
            from auto_gptq import AutoGPTQForCausalLM
            self.model = AutoGPTQForCausalLM.from_quantized(
                model_path,
                torch_dtype=torch.bfloat16,
                device=self.device,
                trust_remote_code=True,
                disable_exllama=True,
                disable_exllamav2=True
            )
        else:
            with torch.no_grad():
                self.model = AutoModel.from_pretrained(
                    model_path,
                    trust_remote_code=True,
                    torch_dtype=torch.bfloat16,
                    attn_implementation='sdpa',
                )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True,
        )
        self.model.init_tts()
        self.model.to(self.device).eval()
        ref_audio_path = os.path.join(self.module_path, "assets", "ref_audios", 'default.wav')
        self.ref_audio, _ = librosa.load(ref_audio_path, sr=16000, mono=True)

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[BaseModel] = None) -> HandlerContext:
        if not isinstance(handler_config, MiniCPMConfig):
            handler_config = MiniCPMConfig()
        context = MiniCPMContext(session_context.session_info.session_id)
        context.local_session_id = self.created_session_num + 235
        self.created_session_num += 1
        self.model.reset_session()
        context.sys_msg = {"role": "user", "content": [
            handler_config.voice_prompt + "\n",
            self.ref_audio,
            "\n" + handler_config.assistant_prompt
        ]}

        with torch.inference_mode():
            self.model.config.stream_input = True
        self._do_prefill(context, [context.sys_msg])
        zero_audio = np.zeros(shape=(context.audio_prefill_length,), dtype=np.float32)
        zero_audio_msg = self._create_message(zero_audio)
        self._do_prefill(context, [zero_audio_msg])
        return context

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_audio_entry("avatar_audio", 1, 24000))
        inputs = {
            ChatDataType.HUMAN_AUDIO: HandlerDataInfo(
                type=ChatDataType.HUMAN_AUDIO,
            )
        }
        outputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                definition=definition,
            )
        }
        return HandlerDetail(
            inputs=inputs, outputs=outputs,
        )

    @staticmethod
    def _create_message(audio: Optional[np.ndarray]):
        if audio is None:
            return None
        msg = {"role": "user", "content":[audio]}
        return msg

    def _do_prefill(self, context: HandlerContext, msgs, max_slice_nums=None):
        context = cast(MiniCPMContext, context)
        extra_params = {}
        if max_slice_nums is not None:
            extra_params["max_slice_nums"] = max_slice_nums
        for msg in msgs:
            logger.info(f"Prefilling session={str(context.local_session_id)}, params={extra_params}, msg={msg}")
            self.model.streaming_prefill(
                session_id=str(context.local_session_id),
                msgs=[msg],
                tokenizer=self.tokenizer,
                **extra_params
            )
            if context.dump_audio:
                for content_data in msg["content"]:
                    if isinstance(content_data, np.ndarray):
                        audio = content_data
                        context.audio_dump_file.write(audio.tobytes())

    def handle(self, context: HandlerContext, inputs: ChatData,
                     output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        output_definition = output_definitions.get(ChatDataType.AVATAR_AUDIO).definition
        context = cast(MiniCPMContext, context)
        audio = None
        _video = None
        if inputs.type == ChatDataType.CAMERA_VIDEO:
            _video = inputs.data.get_main_data()
        elif inputs.type == ChatDataType.HUMAN_AUDIO:
            audio = inputs.data.get_main_data()
        else:
            return
        speech_id = inputs.data.get_meta("speech_id")
        if speech_id is None:
            speech_id = context.session_id

        if audio is not None:
            # prefill audio
            if audio is not None:
                audio = audio.squeeze()
            for audio_segment in slice_data(context.audio_prefill_slice_context, audio):
                if audio_segment is None or audio_segment.shape[0] == 0:
                    continue
                msg = self._create_message(audio_segment)
                self._do_prefill(context, [msg], max_slice_nums=1)

        speech_end = inputs.data.get_meta("human_speech_end", False)
        if not speech_end:
            return

        # prefill remainder audio in slice context
        remainder_audio = context.audio_prefill_slice_context.flush()
        if remainder_audio is not None:
            if remainder_audio.shape[0] < context.audio_prefill_slice_context.slice_size:
                remainder_audio = np.concatenate(
                    [remainder_audio,
                     np.zeros(shape=(context.audio_prefill_slice_context.slice_size - remainder_audio.shape[0]))])
            self._do_prefill(context, [self._create_message(remainder_audio)], max_slice_nums=1)

        logger.info(f"Start s2s inference for speech {speech_id}")
        t_start = time.monotonic()
        is_first_result = True
        result_audio = []
        result_text = ""
        with torch.no_grad():
            self.model.config.stream_input = True
            logger.info(f"Generating start with session={str(context.local_session_id)}")
            for result in self.model.streaming_generate(
                session_id = str(context.local_session_id),
                tokenizer = self.tokenizer,
                generate_audio = True,
            ):
                if is_first_result:
                    is_first_result = False
                    dur_first_segment = time.monotonic() - t_start
                    logger.info(f"First segment took {dur_first_segment*1000:.2f} milli")
                out_audio, sr, text = result["audio_wav"], result["sampling_rate"], result["text"]
                out_audio = cast(torch.Tensor, out_audio)
                out_audio = out_audio.numpy()
                result_audio.append(out_audio)
                result_text += text
                if context.dump_audio:
                    dump_audio = librosa.resample(out_audio, orig_sr=24000, target_sr=16000)
                    context.audio_dump_file.write(dump_audio.tobytes())
                out_audio = out_audio[np.newaxis, ...]
                output = DataBundle(output_definition)
                output.set_main_data(out_audio)
                output.add_meta("avatar_speech_text", text)
                output.add_meta("speech_id", speech_id)
                logger.info(f"Generated audio of size {out_audio.shape[-1]}, sample_rate={sr}")
                yield output
        end_output = DataBundle(output_definition)
        end_output.set_main_data(np.zeros(shape=(1, 50), dtype=np.float32))
        end_output.add_meta("avatar_speech_end", True)
        end_output.add_meta("speech_id", speech_id)
        yield end_output

    def destroy_context(self, context: HandlerContext):
        pass
