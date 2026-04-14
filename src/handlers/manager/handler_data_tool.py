from typing import Dict, Optional, Any

import time

import numpy as np
from loguru import logger
import gradio
from fastapi import FastAPI
from chat_engine.common.handler_base import HandlerBase
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.chat_signal_type import ChatSignalSourceType, ChatSignalType
from chat_engine.data_models.internal.handler_definition_data import HandlerBaseInfo, HandlerDetail, HandlerDataInfo
from service.manager_service.manager_service_register import ensure_data_tool_service, get_data_tool_service
from handlers.manager.manager_handler_base import ManagerHandlerBase
from service.manager_service import register_manager_apis
from chat_engine.data_models.chat_stream_status import ChatStreamStatus
from .data_tool_models import DataToolConfig, DataToolContext
from .data_tool_utils import (
    build_chat_data_event,
    build_signal_event,
    concat_audio,
    dump_audio_to_file,
    dump_image_to_file,
    extract_frame,
    stream_key,
)


class HandlerDataTool(ManagerHandlerBase):
    """
    A passive handler that taps into engine data/signals and streams them to
    a manager websocket for structured inspection.
    """

    def __init__(self):
        super().__init__()
        self.config: Optional[DataToolConfig] = None
        self.data_service = None
        self.engine_config: Optional[ChatEngineConfigModel] = None
        
    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=DataToolConfig,
            load_priority=-50,  # load early to avoid missing signals
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        if not isinstance(handler_config, DataToolConfig):
            handler_config = DataToolConfig()
        self.config = handler_config
        self.engine_config = engine_config
        # Ensure the websocket service is ready to be registered later by manager_service
        self.data_service = ensure_data_tool_service(buffer_limit=self.config.buffer_limit)
        if self.data_service is not None:
            self.data_service.set_current_config(self._serialize_engine_config(engine_config))
        logger.info("Data tool handler loaded and data hub prepared.")

    def create_context(
        self, session_context: SessionContext, handler_config: Optional[HandlerBaseConfigModel] = None
    ) -> HandlerContext:
        if not isinstance(handler_config, DataToolConfig):
            handler_config = self.config or DataToolConfig()
        context = DataToolContext(session_context.session_info.session_id)
        context.config = handler_config
        # Ensure buffer exists for this session
        service = get_data_tool_service()
        if service is not None:
            service.ensure_context(context.session_id)
            self._register_interrupt_handler(service, context)
        return context

    def get_handler_detail(self, session_context: SessionContext, context: HandlerContext) -> HandlerDetail:
        priority = -100  # make sure we receive data even when other handlers consume once
        inputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(type=ChatDataType.AVATAR_AUDIO, input_priority=priority),
            ChatDataType.AVATAR_TEXT: HandlerDataInfo(type=ChatDataType.AVATAR_TEXT, input_priority=priority),
            ChatDataType.HUMAN_TEXT: HandlerDataInfo(type=ChatDataType.HUMAN_TEXT, input_priority=priority),
            ChatDataType.HUMAN_AUDIO: HandlerDataInfo(type=ChatDataType.HUMAN_AUDIO, input_priority=priority),
            # Duplex mode data types - for full-duplex conversation with interruption support
            ChatDataType.HUMAN_DUPLEX_TEXT: HandlerDataInfo(type=ChatDataType.HUMAN_DUPLEX_TEXT, input_priority=priority),
            ChatDataType.HUMAN_DUPLEX_AUDIO: HandlerDataInfo(type=ChatDataType.HUMAN_DUPLEX_AUDIO, input_priority=priority),
            ChatDataType.CAMERA_VIDEO: HandlerDataInfo(type=ChatDataType.CAMERA_VIDEO, input_priority=priority),
            ChatDataType.MIC_AUDIO: HandlerDataInfo(type=ChatDataType.MIC_AUDIO, input_priority=priority),
        }
        return HandlerDetail(inputs=inputs, outputs={})

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    def handle(
        self,
        context: HandlerContext,
        inputs: ChatData,
        output_definitions: Dict[ChatDataType, HandlerDataInfo],
    ):
        data_context = context  # type: ignore
        if not isinstance(data_context, DataToolContext):
            return
        if self.data_service is None:
            self.data_service = get_data_tool_service()
        if self.data_service is None:
            logger.warning("Data tool service not available, skip publishing data.")
            return

        file_path = None
        audio_types = (ChatDataType.AVATAR_AUDIO, ChatDataType.HUMAN_AUDIO, ChatDataType.HUMAN_DUPLEX_AUDIO)
        if inputs.type in audio_types:
            file_path = self._handle_audio_stream(data_context, inputs)
        elif inputs.type == ChatDataType.CAMERA_VIDEO:
            file_path = self._handle_video_stream(data_context, inputs)

        # Throttle MIC_AUDIO: publish at most once every 3 seconds
        # MIC_AUDIO 暂不实际监听，仅用于心跳检测
        if inputs.type == ChatDataType.MIC_AUDIO:
            now = time.time()
            if now - data_context.last_mic_audio_push_ts < 3.0:
                return None
            data_context.last_mic_audio_push_ts = now

        # 对音频，在未完成（未落盘）前不发送事件，避免推送中间分片
        if inputs.type in audio_types and file_path is None:
            return None

        event = build_chat_data_event(
            data_context,
            inputs,
            data_context.config or self.config or DataToolConfig(),
            file_path=file_path,
        )
        self.data_service.push_event(data_context.session_id, event)
        return None

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        data_context = context  # type: ignore
        if not isinstance(data_context, DataToolContext):
            return
        if self.data_service is None:
            self.data_service = get_data_tool_service()
        if self.data_service is None:
            return
        event = build_signal_event(data_context, signal)
        self.data_service.push_event(data_context.session_id, event)

    def destroy_context(self, context: HandlerContext):
        if not isinstance(context, DataToolContext):
            return
        if self.data_service is None:
            self.data_service = get_data_tool_service()
        if self.data_service is not None:
            self._unregister_interrupt_handler(self.data_service, context)
            self.data_service.destroy_context(context.session_id)
        context.audio_buffers.clear()
        context.video_buffers.clear()

    def destroy(self):
        pass

    def _handle_audio_stream(self, context: DataToolContext, chat_data: ChatData) -> Optional[str]:
        main_data = chat_data.data.get_main_data() if chat_data.data is not None else None
        if not isinstance(main_data, np.ndarray):
            return None
        key = chat_data.stream_id.key
        if key is None:
            # No stream id: dump immediately when last flag is set
            if chat_data.is_last_data:
                return dump_audio_to_file(
                    context.session_id,
                    main_data,
                    chat_data.data.definition.get_main_entry().sample_rate if chat_data.data else None,
                    None,
                )
            return None

        buffer = context.audio_buffers.setdefault(key, [])
        buffer.append(main_data)

        stream_mgr = context.stream_manager
        stream_obj = None
        if stream_mgr is not None and chat_data.stream_id is not None:
            try:
                stream_obj = stream_mgr.find_stream(chat_data.stream_id)
            except Exception:
                stream_obj = None

        if not chat_data.is_last_data and (stream_obj is None or stream_obj.status != ChatStreamStatus.CANCELLED):
            return None

        concat = concat_audio(buffer)
        context.audio_buffers.pop(key, None)
        definition = chat_data.data.definition if chat_data.data is not None else None
        main_entry = definition.get_main_entry() if definition is not None else None
        sample_rate = main_entry.sample_rate if main_entry is not None else None
        channels = None
        if main_entry is not None and main_entry.shape and isinstance(main_entry.shape[0], int):
            channels = main_entry.shape[0]

        return dump_audio_to_file(context.session_id, concat, sample_rate, channels)

    def _handle_video_stream(self, context: DataToolContext, chat_data: ChatData) -> Optional[str]:
        main_data = chat_data.data.get_main_data() if chat_data.data is not None else None
        if not isinstance(main_data, np.ndarray):
            return None
        key = stream_key(chat_data)
        if key is None:
            if chat_data.is_last_data:
                frame = extract_frame(main_data)
                return dump_image_to_file(context.session_id, frame)
            return None

        buffer = context.video_buffers.setdefault(key, [])
        buffer.append(main_data)

        stream_mgr = context.stream_manager
        stream_obj = None
        if stream_mgr is not None and chat_data.stream_id is not None:
            try:
                stream_obj = stream_mgr.find_stream(chat_data.stream_id)
            except Exception:
                stream_obj = None

        if not chat_data.is_last_data and (stream_obj is None or stream_obj.status != ChatStreamStatus.CANCELLED):
            return None

        # finalize
        frames = [extract_frame(arr) for arr in buffer]
        frames = [f for f in frames if f is not None]
        context.video_buffers.pop(key, None)
        if not frames:
            return None
        # use last frame for dump
        return dump_image_to_file(context.session_id, frames[-1])

    # --------------------------- Manager commands --------------------------- #
    def _register_interrupt_handler(self, service, context: DataToolContext):
        if context.interrupt_handler is not None:
            return

        def _on_interrupt(payload=None):
            self._emit_interrupt_signal(context, payload)

        context.interrupt_handler = _on_interrupt
        try:
            service.register_interrupt_handler(context.session_id, _on_interrupt)
        except Exception as e:  # pragma: no cover - defensive
            logger.warning(f"Failed to register interrupt handler: {e}")

    def _unregister_interrupt_handler(self, service, context: DataToolContext):
        handler = getattr(context, "interrupt_handler", None)
        if handler is None:
            return
        try:
            service.unregister_interrupt_handler(context.session_id, handler)
        except Exception as e:  # pragma: no cover - defensive
            logger.warning(f"Failed to unregister interrupt handler: {e}")
        context.interrupt_handler = None

    def _emit_interrupt_signal(self, context: DataToolContext, payload: Optional[Dict[str, Any]]):
        if context.signal_emitter is None:
            logger.warning("Interrupt received but signal emitter not ready.")
            return
        signal_data = None
        if isinstance(payload, dict):
            signal_data = dict(payload)
            signal_data.pop("event", None)
            signal_data.pop("session_id", None)
        signal = ChatSignal(
            type=ChatSignalType.INTERRUPT,
            source_type=ChatSignalSourceType.CLIENT,
            source_name="manager_data_tool",
            signal_data=signal_data,
        )
        context.emit_signal(signal)

    def _serialize_engine_config(self, engine_config: Any) -> Optional[Dict[str, Any]]:
        if engine_config is None:
            return None
        if isinstance(engine_config, dict):
            return dict(engine_config)
        try:
            if hasattr(engine_config, "model_dump"):
                return engine_config.model_dump(mode="json")
            if hasattr(engine_config, "dict"):
                return engine_config.dict()
        except Exception as e:  # pragma: no cover - defensive
            logger.warning(f"Failed to serialize engine config for manager monitor: {e}")
        return {"raw": str(engine_config)}


    def on_setup_app(self, app: FastAPI, ui: gradio.blocks.Block, parent_block: Optional[gradio.blocks.Block] = None):
        try:
            register_manager_apis(app, self.engine_config)
            logger.info("ManagerServiceHandler registered manager APIs.")
        except Exception as e:
            logger.error(f"Failed to register manager APIs: {e}")
