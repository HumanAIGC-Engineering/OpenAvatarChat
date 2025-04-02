import importlib
import os
import queue
import sys
import time
from abc import ABC
from typing import Optional, cast, Dict, List

import PIL.Image
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
    enable_video_input: bool = Field(default=False)
    skip_video_frame: int = Field(default=-1)


class MiniCPMContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[MiniCPMConfig] = None
        self.local_session_id = 0

        self.dump_audio = True
        self.audio_dump_file = None

        self.prefilling = False
        self.generating = False

        if self.dump_audio:
            dump_file_path = os.path.join(DirectoryInfo.get_project_dir(),
                                          "dump_talk_audio.pcm")
            self.audio_dump_file = open(dump_file_path, "wb")

        self.sys_msg = None

        self.audio_prefill_length = 16000
        self.audio_prefill_cache = []
        self.audio_prefill_cached_length = 0

        self.audio_prefill_slice_context = SliceContext.create_numpy_slice_context(
            slice_size=16000,
            slice_axis=0,
        )

        self.video_frame_cache = queue.Queue(maxsize=50)
        self.video_frame_head_cache: Optional[ChatData] = None

    def put_video_frame(self, frame):
        if self.config is None or not self.config.enable_video_input:
            return
        if self.video_frame_cache.full():
            self.video_frame_head_cache = self.video_frame_cache.get_nowait()
        self.video_frame_cache.put_nowait(frame)

    def fetch_video_frames(self, start_time: int, end_time: int):
        result = []
        if self.config is None or not self.config.enable_video_input:
            return result
        while True:
            if self.video_frame_head_cache is not None and self.video_frame_head_cache.timestamp[0] >= start_time:
                result.append(self.video_frame_head_cache)
            self.video_frame_head_cache = None
            try:
                self.video_frame_head_cache = self.video_frame_cache.get_nowait()
            except queue.Empty:
                break
            if self.video_frame_head_cache.timestamp[0] >= end_time:
                break
        if len(result) == 0:
            return result
        frame_skip: Optional[int] = None
        if self.config is not None:
            frame_skip = self.config.skip_video_frame

        if frame_skip is not None and frame_skip > 0:
            return result[::frame_skip+1]
        elif frame_skip == -1:
            return result[-1:]
        else:
            return result


class HandlerS2SMiniCPM(HandlerBase, ABC):
    def __init__(self):
        super().__init__()
        self.device = 'cuda:0'
        self.model = None
        self.tokenizer = None
        self.ref_audio = None
        self.created_session_num = 0

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=MiniCPMConfig,
        )

    @staticmethod
    def _build_auto_gptq_minicpmo():
        install_mark = os.path.join(DirectoryInfo.get_project_dir(), "auto-gptq-minicpmo")
        if os.path.isfile(install_mark):
            return
        install_scripts = os.path.join(DirectoryInfo.get_project_dir(), "scripts", "build_auto_gptq.sh")
        cmd = f"cd {DirectoryInfo.get_project_dir()} && chmod +x {install_scripts} && {install_scripts}"
        logger.warning(f"Cmd: {cmd}")
        result = os.system(cmd)
        logger.warning(f"Build auto-gptq MiniCPM-o result: {result}")
        auto_gptq_path = os.path.join(DirectoryInfo.get_project_dir(), "AutoGPTQ")
        if auto_gptq_path not in sys.path:
            sys.path.append(auto_gptq_path)
        importlib.invalidate_caches()

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        model_name = "MiniCPM-o-2_6"
        if isinstance(handler_config, MiniCPMConfig):
            model_name = handler_config.model_name
        project_dir = DirectoryInfo.get_project_dir()
        model_path = os.path.join(project_dir, engine_config.model_root, model_name)
        if model_name == "MiniCPM-o-2_6-int4":
            # noinspection PyUnresolvedReferences
            logger.warning(f"python path: {sys.path}")
            try:
                auto_gptq = importlib.import_module("auto_gptq")
            except ModuleNotFoundError:
                logger.warning("AutoGPTQ not installed, try to install it.")
                from utils.components_builder.autogptq_minicpmo_builder import AutoGPTQMiniCPMOBuilder
                builder = AutoGPTQMiniCPMOBuilder()
                builder.install()
                auto_gptq = importlib.import_module("auto_gptq")
            # from auto_gptq import AutoGPTQForCausalLM
            self.model = auto_gptq.AutoGPTQForCausalLM.from_quantized(
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
        ref_audio_path = os.path.join(self.handler_root, "MiniCPM-o", "assets", "ref_audios", 'default.wav')
        self.ref_audio, _ = librosa.load(ref_audio_path, sr=16000, mono=True)

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[BaseModel] = None) -> HandlerContext:
        if not isinstance(handler_config, MiniCPMConfig):
            handler_config = MiniCPMConfig()
        context = MiniCPMContext(session_context.session_info.session_id)
        context.config = handler_config
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

    def start_context(self, session_context, handler_context):
        pass

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_audio_entry("avatar_audio", 1, 24000))
        inputs = {
            ChatDataType.HUMAN_AUDIO: HandlerDataInfo(
                type=ChatDataType.HUMAN_AUDIO,
            ),
            ChatDataType.CAMERA_VIDEO: HandlerDataInfo(
                type=ChatDataType.CAMERA_VIDEO,
            ),
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
    def _create_message(audio: Optional[np.ndarray], video_frames: Optional[List[ChatData]] = None):
        if audio is None:
            return None
        contents = []
        if video_frames is not None and len(video_frames) > 0:
            contents.append("<unit>")
            for video_frame in video_frames:
                frame_array = video_frame.data.get_main_data()
                if frame_array is None:
                    continue
                image = PIL.Image.fromarray(np.squeeze(frame_array)[..., ::-1])
                contents.append(image)

        contents.append(audio)
        msg = {"role": "user", "content": contents}
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
        video = None
        if inputs.type == ChatDataType.CAMERA_VIDEO:
            video = inputs
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
            context.audio_prefill_slice_context.update_start_id(inputs.timestamp[0])
            for audio_segment in slice_data(context.audio_prefill_slice_context, audio):
                segment_size = audio_segment.shape[0]
                if audio_segment is None or segment_size == 0:
                    continue
                segment_start_id = context.audio_prefill_slice_context.get_last_slice_start_index()
                segment_end_id = segment_start_id + segment_size
                video_frames = context.fetch_video_frames(segment_start_id, segment_end_id)
                logger.info(f"Got {len(video_frames)} video frames with time {[x.timestamp[0] for x in video_frames]}")
                msg = self._create_message(audio_segment, video_frames)
                self._do_prefill(context, [msg], max_slice_nums=1)
                if not context.prefilling:
                    context.prefilling = True

        if video is not None:
            context.put_video_frame(video)

        speech_end = inputs.data.get_meta("human_speech_end", False)
        if not speech_end:
            return

        # prefill remainder audio in slice context
        end_segment_start_id = context.audio_prefill_slice_context.get_next_slice_start_index()
        remainder_audio = context.audio_prefill_slice_context.flush()
        if remainder_audio is not None:
            segment_size = remainder_audio.shape[0]
            if segment_size < context.audio_prefill_slice_context.slice_size:
                remainder_audio = np.concatenate(
                    [remainder_audio,
                     np.zeros(shape=(context.audio_prefill_slice_context.slice_size - remainder_audio.shape[0]))])
            end_segment_end_id = end_segment_start_id + segment_size
            video_frames = context.fetch_video_frames(end_segment_start_id, end_segment_end_id)
            logger.info(f"Got {len(video_frames)} video frames with time {[x.timestamp[0] for x in video_frames]}")
            self._do_prefill(context, [self._create_message(remainder_audio, video_frames)], max_slice_nums=1)

        context.prefilling = False

        logger.info(f"Start s2s inference for speech {speech_id}")
        t_start = time.monotonic()
        is_first_result = True
        result_audio = []
        result_text = ""
        if not context.generating:
            context.generating = True
        with torch.no_grad():
            self.model.config.stream_input = True
            logger.info(f"Generating start with session={str(context.local_session_id)}")
            for result in self.model.streaming_generate(
                session_id=str(context.local_session_id),
                tokenizer=self.tokenizer,
                generate_audio=True,
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
                context.submit_data(output)
                # yield output
        end_output = DataBundle(output_definition)
        end_output.set_main_data(np.zeros(shape=(1, 50), dtype=np.float32))
        end_output.add_meta("avatar_speech_end", True)
        end_output.add_meta("speech_id", speech_id)
        context.generating = False
        context.submit_data(end_output)
        # yield end_output

    def destroy_context(self, context: HandlerContext):
        pass
