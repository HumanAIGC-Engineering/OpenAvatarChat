import asyncio
import queue
import threading
import time
import typing
from typing import Dict, List, Iterable

from loguru import logger

from chat_engine.core.signal_manager import SignalManager
from chat_engine.core.stream_manager import StreamManager, ChatDataSubmitter
from chat_engine.data_models.chat_stream_status import ChatStreamStatus

from chat_engine.common.logic_base import LogicBase
from chat_engine.common.handler_base import HandlerBase

from chat_engine.data_models.internal.chat_data_endpoints import DataSink
from chat_engine.data_models.internal.handler_definition_data import HandlerBaseInfo
from chat_engine.data_models.internal.handler_session_data import HandlerRegistry, HandlerRecord, HandlerEnv
from chat_engine.data_models.internal.logic_definition_data import LogicBaseInfo
from chat_engine.data_models.internal.logic_session_data import LogicEnv

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.engine_channel_type import EngineChannelType
from chat_engine.data_models.chat_engine_config_data import (HandlerBaseConfigModel, ChatEngineConfigModel,
                                                             LogicBaseConfigModel)
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule
from chat_engine.data_models.chat_signal_type import ChatSignalSourceType, ChatSignalType

from chat_engine.contexts.session_context import SessionContext


class ChatSession:
    input_type_mapping = {
        EngineChannelType.VIDEO: [ChatDataType.CAMERA_VIDEO],
        EngineChannelType.AUDIO: [ChatDataType.MIC_AUDIO],
        EngineChannelType.TEXT: [ChatDataType.HUMAN_TEXT]
    }

    def __init__(self, session_context: SessionContext, _engine_config: ChatEngineConfigModel):
        self.session_context = session_context
        self.signal_manager = SignalManager(self.session_context.session_clock)
        self.signal_manager.init()
        self.stream_manager = StreamManager(self.signal_manager)
        self.stream_manager.enable_debug_logging(True)
        self.data_sinks: Dict[ChatDataType, List[DataSink]] = {}
        self.handlers: Dict[str, HandlerRecord] = {}
        self._playback_begin_event_ids: Dict[str, str] = {}
        self._register_playback_auto_recorder()

    @classmethod
    def handler_pumper(cls, session_context: SessionContext, handler_env: HandlerEnv):
        shared_states = session_context.shared_states
        input_queue = handler_env.input_queue
        handler = handler_env.handler
        context = handler_env.context
        output_info = handler_env.output_info
        # Use handler_output_info (with original type keys) if available,
        # so handler code can use its declared types even with output_type_override
        handler_visible_output_info = handler_env.handler_output_info or output_info
        if output_info is None:
            output_info = {}
        if handler_visible_output_info is None:
            handler_visible_output_info = {}
        handler.warmup_context(session_context, context)
        
        # Track stream begin events for auto history recording
        stream_begin_events: Dict[str, str] = {}  # stream_key -> event_id
        
        while shared_states.active:
            try:
                input_data = input_queue.get_nowait()
            except (queue.Empty, asyncio.QueueEmpty):
                time.sleep(0.03)
                continue
            
            context.data_submitter.update_input_stream(input_data)

            # Consumer-side cancel guard: drop data from cancelled streams.
            # The production-side guard in stream_data() blocks new data, but residual
            # data may already be in the queue from before cancel(). This check ensures
            # the handler never processes data after a stream has been cancelled.
            if input_data.stream_id is not None:
                _sm = getattr(context, 'stream_manager', None)
                if _sm is not None:
                    _stream = _sm.find_stream(input_data.stream_id)
                    if _stream is not None and _stream.status == ChatStreamStatus.CANCELLED:
                        continue

            # Auto-record STREAM_BEGIN to history
            if (input_data.is_first_data 
                and handler.should_auto_record_history(input_data.type)
                and input_data.stream_id is not None):
                stream_key_obj = input_data.stream_id.key
                stream_key_str = str(stream_key_obj) if stream_key_obj else None
                event_id = handler.on_history_record(
                    context,
                    signal_type=ChatSignalType.STREAM_BEGIN,
                    data_type=input_data.type,
                    source_stream_key=stream_key_str,
                )
                if event_id and stream_key_str:
                    stream_begin_events[stream_key_str] = event_id
            
            # Accumulate streaming text data for TEXT types
            # Use timestamp as chunk_id for deduplication across multiple handlers
            if (handler.should_auto_record_history(input_data.type)
                and input_data.stream_id is not None
                and input_data.data is not None
                and context.session_history is not None):
                try:
                    text_data = input_data.data.get_main_data()
                    if text_data and isinstance(text_data, str):
                        stream_key_obj = input_data.stream_id.key
                        stream_key_str = str(stream_key_obj) if stream_key_obj else None
                        if stream_key_str:
                            # Use timestamp as unique chunk identifier for deduplication
                            chunk_id = f"{input_data.timestamp[0]}:{input_data.timestamp[1]}"
                            context.session_history.accumulate_stream_data(stream_key_str, text_data, chunk_id)
                except Exception:
                    pass
            
            # Map input type back to original type if there's a reverse mapping
            # This allows handler code to check against its declared input types
            actual_type = input_data.type
            if handler_env.input_type_reverse_mapping:
                original_type = handler_env.input_type_reverse_mapping.get(actual_type)
                if original_type:
                    input_data.type = original_type
            
            # 使用 try-except 包裹 handler.handle()，防止单次处理失败导致整个 pumper 线程退出
            try:
                handler_result = handler.handle(context, input_data, handler_visible_output_info)
            except Exception as e:
                handler_name = handler_env.handler_info.name if handler_env.handler_info else "Unknown"
                logger.opt(exception=e).error(f"Handler {handler_name} raised exception during handle(), "
                                              f"input type: {input_data.type}, stream: {input_data.stream_id}")
                # 重置 input_data.type 然后继续处理下一个数据
                input_data.type = actual_type
                continue
            
            # Restore the actual type after handle() call
            input_data.type = actual_type
            
            # Auto-record STREAM_END to history with accumulated data content
            if (input_data.is_last_data 
                and handler.should_auto_record_history(input_data.type)
                and input_data.stream_id is not None):
                stream_key_obj = input_data.stream_id.key
                stream_key_str = str(stream_key_obj) if stream_key_obj else None
                begin_event_id = stream_begin_events.pop(stream_key_str, None) if stream_key_str else None
                # Use accumulated data instead of just the last chunk
                data_content = None
                if context.session_history is not None and stream_key_str:
                    data_content = context.session_history.finalize_stream_accumulator(stream_key_str)
                # Fallback to last chunk data if no accumulator
                if not data_content and input_data.data is not None:
                    try:
                        data_content = input_data.data.get_main_data()
                    except Exception:
                        pass
                handler.on_history_record(
                    context,
                    signal_type=ChatSignalType.STREAM_END,
                    data_type=input_data.type,
                    data=data_content,
                    related_event_id=begin_event_id,
                    source_stream_key=stream_key_str,
                )
            
            if not isinstance(handler_result, Iterable):
                handler_result = [handler_result]
            for handler_output in handler_result:
                if context.data_submitter is None:
                    continue
                context.data_submitter.submit(handler_output)

    def _register_playback_auto_recorder(self):
        """Register signal listeners to auto-record CLIENT_PLAYBACK stream lifecycle to SessionHistory."""
        for signal_type in (ChatSignalType.STREAM_BEGIN, ChatSignalType.STREAM_END, ChatSignalType.STREAM_CANCEL):
            self.signal_manager.register_listener(
                listener=self._on_playback_stream_signal,
                signal_filter=SignalFilterRule(signal_type, None, ChatDataType.CLIENT_PLAYBACK),
            )

    def _on_playback_stream_signal(self, signal: ChatSignal):
        """Auto-record CLIENT_PLAYBACK stream lifecycle events to SessionHistory.
        
        Parent stream ancestry (AVATAR_AUDIO etc.) is navigable through StreamManager
        at query time — no need to denormalize into history events.
        """
        session_history = self.session_context.session_history
        if session_history is None or signal.related_stream is None:
            return
        stream_key_str = signal.related_stream.stream_key_str

        if signal.type == ChatSignalType.STREAM_BEGIN:
            event_id = session_history.create_and_add_event(
                data_type=ChatDataType.CLIENT_PLAYBACK,
                signal_type=ChatSignalType.STREAM_BEGIN,
                source_stream_key=stream_key_str,
                owner=signal.source_name,
            )
            if event_id and stream_key_str:
                self._playback_begin_event_ids[stream_key_str] = event_id
        elif signal.type in (ChatSignalType.STREAM_END, ChatSignalType.STREAM_CANCEL):
            begin_event_id = self._playback_begin_event_ids.pop(stream_key_str, None) if stream_key_str else None
            session_history.create_and_add_event(
                data_type=ChatDataType.CLIENT_PLAYBACK,
                signal_type=signal.type,
                source_stream_key=stream_key_str,
                owner=signal.source_name,
                parent_event_id=begin_event_id,
            )

    def prepare_handler(self, handler: HandlerBase, handler_info: HandlerBaseInfo,
                        handler_config: HandlerBaseConfigModel):
        handler_env = HandlerEnv(handler_info=handler_info, handler=handler, config=handler_config)
        handler_env.context = handler.create_context(self.session_context, handler_env.config)
        handler_env.context.owner = handler_info.name
        handler_env.input_queue = queue.Queue()
        io_detail = handler.get_handler_detail(self.session_context, handler_env.context)
        io_detail.validate()
        
        # Type override mappings: original_type -> actual_type
        input_type_mapping: Dict[ChatDataType, ChatDataType] = {}
        output_type_mapping: Dict[ChatDataType, ChatDataType] = {}
        
        # Apply input type overrides from configuration
        if handler_config.input_type_override:
            logger.info(f"Handler {handler_info.name}: processing input_type_override {handler_config.input_type_override}, current inputs: {list(io_detail.inputs.keys())}")
            for orig_type_name, target_type_name in handler_config.input_type_override.items():
                try:
                    orig_type = ChatDataType[orig_type_name]
                    target_type = ChatDataType[target_type_name]
                    if orig_type in io_detail.inputs:
                        input_info = io_detail.inputs.pop(orig_type)
                        input_info.type = target_type
                        io_detail.inputs[target_type] = input_info
                        input_type_mapping[orig_type] = target_type
                        logger.info(f"Handler {handler_info.name}: input type override {orig_type_name} -> {target_type_name}")
                    else:
                        logger.warning(f"Handler {handler_info.name}: input type {orig_type_name} not in handler's declared inputs, skipping override")
                except KeyError as e:
                    logger.warning(f"Handler {handler_info.name}: invalid type override - {e}")
        
        # Apply output type overrides from configuration
        # Note: We only create streamer for the target type, not the original type.
        # Handler code can still use original type names because _output_type_mapping
        # handles the translation in ChatDataSubmitter.get_streamer()
        if handler_config.output_type_override:
            for orig_type_name, target_type_name in handler_config.output_type_override.items():
                try:
                    orig_type = ChatDataType[orig_type_name]
                    target_type = ChatDataType[target_type_name]
                    if orig_type in io_detail.outputs:
                        output_info = io_detail.outputs.pop(orig_type)
                        output_info.type = target_type
                        io_detail.outputs[target_type] = output_info
                        # Record mapping so handler can use original type names via get_streamer()
                        output_type_mapping[orig_type] = target_type
                        logger.debug(f"Handler {handler_info.name}: output type override {orig_type_name} -> {target_type_name}")
                except KeyError as e:
                    logger.warning(f"Handler {handler_info.name}: invalid type override - {e}")
        
        inputs = io_detail.inputs
        for input_type, input_info in inputs.items():
            sink_list = self.data_sinks.setdefault(input_type, [])
            data_sink = DataSink(owner=handler_info.name, sink_queue=handler_env.input_queue, consume_info=input_info)
            sink_list.append(data_sink)
        handler_env.output_info = io_detail.outputs
        
        # Build reverse mapping: actual_type -> original_type
        # This allows handler code to check against its originally declared types
        if input_type_mapping:
            handler_env.input_type_reverse_mapping = {v: k for k, v in input_type_mapping.items()}

        # Build handler-visible output_info with original type keys
        # so handler code can use its declared types (e.g. HUMAN_TEXT instead of HUMAN_DUPLEX_TEXT)
        if output_type_mapping:
            output_type_reverse = {v: k for k, v in output_type_mapping.items()}
            handler_output_info = {}
            for key, value in io_detail.outputs.items():
                orig_key = output_type_reverse.get(key, key)
                handler_output_info[orig_key] = value
            handler_env.handler_output_info = handler_output_info

        handler_context = handler_env.context

        filters = io_detail.signal_filters
        if filters is None or len(filters) == 0:
            filters = [SignalFilterRule(None, None, None)]
        # TODO multiple signal filter should be merged.
        for signal_filter in filters:
            self.signal_manager.register_listener(
                listener=lambda signal: handler.on_signal(handler_env.context, signal),
                signal_filter=signal_filter
            )
        handler_context.signal_emitter = self.signal_manager.get_emitter(handler_info.name)
        handler_context.data_submitter = ChatDataSubmitter()
        # Set type mapping for override support - handlers can use original type names
        if output_type_mapping:
            handler_context.data_submitter.set_output_type_mapping(output_type_mapping)
        # Inject session history for duplex conversation support
        handler_context.session_history = self.session_context.session_history
        # Inject stream_manager so handlers can query stream graph and create lifecycle streams
        handler_context.stream_manager = self.stream_manager

        for output_type, output_data_info in handler_env.output_info.items():
            streamer = self.stream_manager.create_streamer(
                data_info=output_data_info,
                data_sinks=self.data_sinks,
                producer_name=handler_info.name,
                data_name=output_data_info.data_name,
                config=output_data_info.output_stream_config,
                )
            handler_context.data_submitter.register_streamer(streamer)
        self.handlers[handler_info.name] = HandlerRecord(env=handler_env)
        return handler_env

    def create_logic_context(self, handler_registries: List[HandlerRegistry], logic: LogicBase,
                             logic_info: LogicBaseInfo, logic_config: LogicBaseConfigModel):
        logic_env = LogicEnv(logic_info=logic_info, logic=logic, config=logic_config)
        logic_env.context = logic.create_context(handler_registries, self.session_context, logic_env.config)
        logic_env.context.owner = logic_info.name
        logic_detail = logic.get_logic_detail(self.session_context, logic_env.context)
        logic_detail.validate()
        inputs = logic_detail.inspected_streamers

    def sort_sinks(self):
        for input_type, sink_list in self.data_sinks.items():
            sink_list.sort(key=lambda x: x.consume_info)

    def start(self):
        if self.session_context.shared_states.active:
            return
        self.sort_sinks()
        self.session_context.shared_states.active = True
        for handler_name, handler_record in self.handlers.items():
            start_args = (self.session_context, handler_record.env)
            handler_record.env.handler.start_context(self.session_context, handler_record.env.context)
            handler_record.pump_thread = threading.Thread(target=self.handler_pumper, args=start_args)
            handler_record.pump_thread.start()
        self.session_context.get_clock().start()

    def stop(self):
        self.session_context.shared_states.active = False
        for handler_name, handler_record in self.handlers.items():
            if handler_record.pump_thread:
                handler_record.pump_thread.join()
                handler_record.pump_thread = None
            handler_record.env.handler.destroy_context(handler_record.env.context)
        self.signal_manager.shutdown()
        self.handlers.clear()
        self.session_context.cleanup()
        logger.info("chat session stopped")

    def get_timestamp(self):
        return self.session_context.get_clock().get_timestamp()

    def emit_signal(self, signal: ChatSignal):
        self.signal_manager.get_emitter("chat_session").emit(signal)
