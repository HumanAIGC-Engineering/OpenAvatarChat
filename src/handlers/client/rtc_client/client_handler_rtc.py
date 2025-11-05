import asyncio
from pathlib import Path
from typing import Dict, Optional, cast, Union, Tuple
from uuid import uuid4

from loguru import logger

from engine_utils.directory_info import DirectoryInfo
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import gradio
import numpy as np
from fastapi import FastAPI

# ============================================================================
# H.264 Hardware Encoder Configuration (must execute before importing fastrtc)
# ============================================================================
from aiortc.codecs import CODECS, h264
from aiortc import codecs as aiortc_codecs
import av
import fractions

# Global variables for H.264 encoder selection
_selected_h264_encoder = 'libx264'
_actual_h264_encoder = None

def _prioritize_h264():
    """Prioritize H.264 codec over VP8 in aiortc codec list"""
    video_codecs = CODECS["video"]
    h264_codecs = [c for c in video_codecs if "H264" in c.mimeType]
    other_codecs = [c for c in video_codecs if "H264" not in c.mimeType]
    CODECS["video"] = h264_codecs + other_codecs
    logger.info(f"Video codec priority: {[c.mimeType for c in CODECS['video'][:3]]}")

def _configure_h264_hardware_encoding():
    """Configure H.264 to use hardware encoder (must execute before importing fastrtc)"""
    global _selected_h264_encoder, _actual_h264_encoder
    
    # Configure H.264 bitrate
    h264.DEFAULT_BITRATE = 1500000  # 1.5 Mbps default
    h264.MIN_BITRATE = 500000       # 0.5 Mbps minimum
    h264.MAX_BITRATE = 2500000      # 2.5 Mbps maximum
    
    # Detect available hardware encoders (priority: NVENC > QSV > VideoToolbox)
    hardware_encoders = ['h264_nvenc', 'h264_qsv', 'h264_videotoolbox']
    for encoder in hardware_encoders:
        try:
            test_codec = av.CodecContext.create(encoder, "w")
            test_codec.width = 640
            test_codec.height = 480
            test_codec.pix_fmt = "yuv420p"
            test_codec.framerate = fractions.Fraction(30, 1)
            test_codec.time_base = fractions.Fraction(1, 30)
            _selected_h264_encoder = encoder
            logger.info(f"Detected H.264 hardware encoder: {encoder}")
            break
        except Exception as e:
            logger.debug(f"Hardware encoder {encoder} not available: {e}")
    
    if _selected_h264_encoder == 'libx264':
        logger.warning("No hardware encoder available, will use libx264 (CPU encoding)")
    
    # Monkey patch H264Encoder._encode_frame to use hardware encoder with fallback
    def patched_encode_frame(self, frame, force_keyframe):
        if self.codec and (
            frame.width != self.codec.width or frame.height != self.codec.height
            or abs(self.target_bitrate - self.codec.bit_rate) / self.codec.bit_rate > 0.1
        ):
            self.buffer_data = b""
            self.buffer_pts = None
            self.codec = None

        if force_keyframe:
            frame.pict_type = av.video.frame.PictureType.I
        else:
            frame.pict_type = av.video.frame.PictureType.NONE

        if self.codec is None:
            # Try to create encoder, fallback to software encoder if hardware fails
            encoder_to_use = _selected_h264_encoder
            codec_created = False
            
            try:
                self.codec = av.CodecContext.create(encoder_to_use, "w")
                self.codec.width = frame.width
                self.codec.height = frame.height
                self.codec.bit_rate = self.target_bitrate
                self.codec.pix_fmt = "yuv420p"
                self.codec.framerate = fractions.Fraction(h264.MAX_FRAME_RATE, 1)
                self.codec.time_base = fractions.Fraction(1, h264.MAX_FRAME_RATE)
                
                # Configure encoder-specific options
                if encoder_to_use == 'libx264':
                    self.codec.options = {"level": "31", "tune": "zerolatency"}
                    self.codec.profile = "Baseline"
                elif encoder_to_use == 'h264_nvenc':
                    self.codec.options = {"preset": "llhq", "zerolatency": "1", "profile": "baseline"}
                elif encoder_to_use == 'h264_qsv':
                    self.codec.options = {"preset": "veryfast", "profile": "baseline"}
                elif encoder_to_use == 'h264_videotoolbox':
                    self.codec.options = {"realtime": "1", "profile": "baseline"}
                
                codec_created = True
                logger.info(f"H.264 encoder created: {encoder_to_use}")
                
            except Exception as e:
                logger.warning(f"Failed to create {encoder_to_use} encoder: {e}")
                
                # Fallback to libx264 if hardware encoder fails
                if encoder_to_use != 'libx264':
                    logger.info("Falling back to libx264 software encoder")
                    try:
                        self.codec = av.CodecContext.create("libx264", "w")
                        self.codec.width = frame.width
                        self.codec.height = frame.height
                        self.codec.bit_rate = self.target_bitrate
                        self.codec.pix_fmt = "yuv420p"
                        self.codec.framerate = fractions.Fraction(h264.MAX_FRAME_RATE, 1)
                        self.codec.time_base = fractions.Fraction(1, h264.MAX_FRAME_RATE)
                        self.codec.options = {"level": "31", "tune": "zerolatency"}
                        self.codec.profile = "Baseline"
                        
                        encoder_to_use = "libx264"
                        codec_created = True
                        logger.info("H.264 encoder created: libx264 (fallback)")
                        
                    except Exception as fallback_error:
                        logger.error(f"Failed to create fallback encoder: {fallback_error}")
                        raise
                else:
                    logger.error(f"Failed to create libx264 encoder: {e}")
                    raise
            
            if codec_created:
                actual_encoder = self.codec.name
                global _actual_h264_encoder
                _actual_h264_encoder = actual_encoder

        data_to_send = b""
        for package in self.codec.encode(frame):
            data_to_send += bytes(package)
        if data_to_send:
            yield from self._split_bitstream(data_to_send)
    
    # Patch get_encoder
    original_get_encoder = aiortc_codecs.get_encoder
    def patched_get_encoder(codec):
        encoder = original_get_encoder(codec)
        logger.debug(f"get_encoder({codec.mimeType}) -> {type(encoder).__name__}")
        return encoder
    
    # Patch RTCPeerConnection.setRemoteDescription to enforce H.264 codec priority
    # This ensures H.264 is selected during WebRTC negotiation instead of VP8
    from aiortc import RTCPeerConnection
    original_set_remote = RTCPeerConnection.setRemoteDescription
    
    async def patched_set_remote_description(self, sessionDescription):
        """Re-order transceiver codecs after SDP negotiation to prioritize H.264"""
        logger.debug(f"setRemoteDescription called with {sessionDescription.type}")
        
        # Call original method (creates/configures transceivers and negotiates codecs)
        await original_set_remote(self, sessionDescription)
        
        # Re-order video transceiver codecs to prioritize H.264
        from aiortc.codecs import get_capabilities
        from aiortc.rtcpeerconnection import filter_preferred_codecs
        
        for transceiver in self._RTCPeerConnection__transceivers:
            if transceiver.kind == "video":
                logger.debug(f"Transceiver codecs before: {[c.mimeType for c in transceiver._codecs[:3]]}")
                
                # Get our re-ordered codec capabilities (H.264 first)
                capabilities = get_capabilities("video")
                current_codecs = transceiver._codecs
                
                # Manually call filter_preferred_codecs to re-order
                refiltered = filter_preferred_codecs(current_codecs, capabilities.codecs)
                transceiver._codecs = refiltered
                
                logger.info(f"Video codecs negotiated: {[c.mimeType for c in transceiver._codecs[:2]]}")
    
    # Apply all patches
    h264.H264Encoder._encode_frame = patched_encode_frame
    aiortc_codecs.get_encoder = patched_get_encoder
    RTCPeerConnection.setRemoteDescription = patched_set_remote_description
    logger.info("H.264 encoder configuration completed")

# Execute configuration before importing fastrtc
_prioritize_h264()
_configure_h264_hardware_encoding()

# Import fastrtc after H.264 configuration
# noinspection PyPackageRequirements
from fastrtc import Stream  # noqa: E402

from pydantic import BaseModel, Field  # noqa: E402
from chat_engine.common.client_handler_base import ClientHandlerBase, ClientSessionDelegate  # noqa: E402
from chat_engine.common.engine_channel_type import EngineChannelType  # noqa: E402
from chat_engine.common.handler_base import HandlerDataInfo, HandlerDetail, HandlerBaseInfo  # noqa: E402
from chat_engine.contexts.handler_context import HandlerContext  # noqa: E402
from chat_engine.contexts.session_context import SessionContext  # noqa: E402
from chat_engine.data_models.chat_data.chat_data_model import ChatData  # noqa: E402
from chat_engine.data_models.chat_data_type import ChatDataType  # noqa: E402
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel, ChatEngineConfigModel  # noqa: E402
from chat_engine.data_models.chat_signal import ChatSignal  # noqa: E402
from chat_engine.data_models.runtime_data.data_bundle import (  # noqa: E402
    DataBundleDefinition, DataBundleEntry, VariableSize, DataBundle  # noqa: E402
)  # noqa: E402
from service.rtc_service.rtc_provider import RTCProvider  # noqa: E402
from service.rtc_service.rtc_stream import RtcStream  # noqa: E402


class RtcClientSessionDelegate(ClientSessionDelegate):
    def __init__(self):
        self.timestamp_generator = None
        self.data_submitter = None
        self.shared_states = None
        self.output_queues = {
            EngineChannelType.AUDIO: asyncio.Queue(),
            EngineChannelType.VIDEO: asyncio.Queue(),
            EngineChannelType.TEXT: asyncio.Queue(),
        }
        self.input_data_definitions: Dict[EngineChannelType, DataBundleDefinition] = {}
        self.modality_mapping = {
            EngineChannelType.AUDIO: ChatDataType.MIC_AUDIO,
            EngineChannelType.VIDEO: ChatDataType.CAMERA_VIDEO,
            EngineChannelType.TEXT: ChatDataType.HUMAN_TEXT,
        }

    async def get_data(self, modality: EngineChannelType, timeout: Optional[float] = 0.1) -> Optional[ChatData]:
        data_queue = self.output_queues.get(modality)
        if data_queue is None:
            return None
        if timeout is not None and timeout > 0:
            try:
                data = await asyncio.wait_for(data_queue.get(), timeout)
            except asyncio.TimeoutError:
                return None
        else:
            data = await data_queue.get()
        return data

    def put_data(self, modality: EngineChannelType, data: Union[np.ndarray, str],
                 timestamp: Optional[Tuple[int, int]] = None, samplerate: Optional[int] = None, loopback: bool = False):
        if timestamp is None:
            timestamp = self.get_timestamp()
        if self.data_submitter is None:
            return
        definition = self.input_data_definitions.get(modality)
        chat_data_type = self.modality_mapping.get(modality)
        if chat_data_type is None or definition is None:
            return
        data_bundle = DataBundle(definition)
        if modality == EngineChannelType.AUDIO:
            data_bundle.set_main_data(data.squeeze()[np.newaxis, ...])
        elif modality == EngineChannelType.VIDEO:
            data_bundle.set_main_data(data[np.newaxis, ...])
        elif modality == EngineChannelType.TEXT:
            data_bundle.add_meta('human_text_end', True)
            data_bundle.add_meta('speech_id', str(uuid4()))
            data_bundle.set_main_data(data)
        else:
            return
        chat_data = ChatData(
            source="client",
            type=chat_data_type,
            data=data_bundle,
            timestamp=timestamp,
        )
        self.data_submitter.submit(chat_data)
        if loopback:
            self.output_queues[modality].put_nowait(chat_data)

    def get_timestamp(self):
        return self.timestamp_generator()

    def emit_signal(self, signal: ChatSignal):
        pass

    def clear_data(self):
        for data_queue in self.output_queues.values():
            while not data_queue.empty():
                data_queue.get_nowait()


class ClientRtcConfigModel(HandlerBaseConfigModel, BaseModel):
    connection_ttl: int = Field(default=900)
    turn_config: Optional[Dict] = Field(default=None)


class ClientRtcContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[ClientRtcConfigModel] = None
        self.client_session_delegate: Optional[RtcClientSessionDelegate] = None


class ClientHandlerRtc(ClientHandlerBase):
    def __init__(self):
        super().__init__()
        self.engine_config = None
        self.handler_config = None
        self.rtc_streamer_factory: Optional[RtcStream] = None

        self.output_bundle_definitions: Dict[EngineChannelType, DataBundleDefinition] = {}

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=ClientRtcConfigModel,
            client_session_delegate_class=RtcClientSessionDelegate,
        )

    def prepare_rtc_definitions(self):
        self.rtc_streamer_factory = RtcStream(
            session_id=None,
            expected_layout="mono",
            input_sample_rate=16000,
            output_sample_rate=24000,
            output_frame_size=480,
            fps=30,
            stream_start_delay=0.5,
        )
        self.rtc_streamer_factory.client_handler_delegate = self.handler_delegate

        audio_output_definition = DataBundleDefinition()
        audio_output_definition.add_entry(DataBundleEntry.create_audio_entry(
            "mic_audio",
            1,
            16000,
        ))
        audio_output_definition.lockdown()
        self.output_bundle_definitions[EngineChannelType.AUDIO] = audio_output_definition

        video_output_definition = DataBundleDefinition()
        video_output_definition.add_entry(DataBundleEntry.create_framed_entry(
            "camera_video",
            [VariableSize(), VariableSize(), VariableSize(), 3],
            0,
            30
        ))
        video_output_definition.lockdown()
        self.output_bundle_definitions[EngineChannelType.VIDEO] = video_output_definition

        text_output_definition = DataBundleDefinition()
        text_output_definition.add_entry(DataBundleEntry.create_text_entry(
            "human_text",
        ))
        text_output_definition.lockdown()
        self.output_bundle_definitions[EngineChannelType.TEXT] = text_output_definition

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        self.engine_config = engine_config
        self.handler_config = cast(ClientRtcConfigModel, handler_config)
        self.prepare_rtc_definitions()

    def setup_rtc_ui(self, ui, parent_block, fastapi: FastAPI, avatar_config):
        turn_entity = RTCProvider().prepare_rtc_configuration(self.handler_config.turn_config)
        if turn_entity is None:
            turn_entity = RTCProvider().prepare_rtc_configuration(self.engine_config.turn_config)

        webrtc = Stream(
            modality="audio-video",
            mode="send-receive",
            time_limit=self.handler_config.connection_ttl,
            rtc_configuration=turn_entity.rtc_configuration if turn_entity is not None else None,
            handler=self.rtc_streamer_factory,
            concurrency_limit=self.handler_config.concurrent_limit,
        )
        webrtc.mount(fastapi)

        @fastapi.get('/openavatarchat/initconfig')
        async def init_config():
            config = {
                "avatar_config": avatar_config,
                "rtc_configuration": turn_entity.rtc_configuration if turn_entity is not None else None,
            }
            return JSONResponse(status_code=200, content=config)

        frontend_path = Path(DirectoryInfo.get_src_dir() + '/handlers/client/rtc_client/frontend/dist')
        if frontend_path.exists():
            logger.info(f"Serving frontend from {frontend_path}")
            fastapi.mount('/ui', StaticFiles(directory=frontend_path), name="static")
            fastapi.add_route('/', RedirectResponse(url='/ui/index.html'))
        else:
            logger.warning(f"Frontend directory {frontend_path} does not exist")
            fastapi.add_route('/', RedirectResponse(url='/gradio'))

        if parent_block is None:
            parent_block = ui
        with ui:
            with parent_block:
                gradio.components.HTML(
                    """
                    <h1 id="openavatarchat">
                       The Gradio page is no longer available. Please use the openavatarchat-webui submodule instead.
                    </h1>
                    """,
                    visible=True
                )

    def on_setup_app(self, app: FastAPI, ui: gradio.blocks.Block, parent_block: Optional[gradio.blocks.Block] = None):
        avatar_config = {}
        self.setup_rtc_ui(ui, parent_block, app, avatar_config)

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        if not isinstance(handler_config, ClientRtcConfigModel):
            handler_config = ClientRtcConfigModel()
        context = ClientRtcContext(session_context.session_info.session_id)
        context.config = handler_config
        return context

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    def on_setup_session_delegate(self, session_context: SessionContext, handler_context: HandlerContext,
                                  session_delegate: ClientSessionDelegate):
        handler_context = cast(ClientRtcContext, handler_context)
        session_delegate = cast(RtcClientSessionDelegate, session_delegate)

        session_delegate.timestamp_generator = session_context.get_timestamp
        session_delegate.data_submitter = handler_context.data_submitter
        session_delegate.input_data_definitions = self.output_bundle_definitions
        session_delegate.shared_states = session_context.shared_states

        handler_context.client_session_delegate = session_delegate

    def create_handler_detail(self, _session_context, _handler_context):
        inputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO
            ),
            ChatDataType.AVATAR_VIDEO: HandlerDataInfo(
                type=ChatDataType.AVATAR_VIDEO
            ),
            ChatDataType.AVATAR_TEXT: HandlerDataInfo(
                type=ChatDataType.AVATAR_TEXT
            ),
            ChatDataType.HUMAN_TEXT: HandlerDataInfo(
                type=ChatDataType.HUMAN_TEXT
            ),
        }
        outputs = {
            ChatDataType.MIC_AUDIO: HandlerDataInfo(
                type=ChatDataType.MIC_AUDIO,
                definition=self.output_bundle_definitions[EngineChannelType.AUDIO]
            ),
            ChatDataType.CAMERA_VIDEO: HandlerDataInfo(
                type=ChatDataType.CAMERA_VIDEO,
                definition=self.output_bundle_definitions[EngineChannelType.VIDEO]
            ),
            ChatDataType.HUMAN_TEXT: HandlerDataInfo(
                type=ChatDataType.HUMAN_TEXT,
                definition=self.output_bundle_definitions[EngineChannelType.TEXT]
            ),
        }
        return HandlerDetail(
            inputs=inputs,
            outputs=outputs
        )

    def get_handler_detail(self, session_context: SessionContext, context: HandlerContext) -> HandlerDetail:
        return self.create_handler_detail(session_context, context)

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        context = cast(ClientRtcContext, context)
        if context.client_session_delegate is None:
            return
        data_queue = context.client_session_delegate.output_queues.get(inputs.type.channel_type)
        if data_queue is not None:
            data_queue.put_nowait(inputs)

    def destroy_context(self, context: HandlerContext):
        pass
