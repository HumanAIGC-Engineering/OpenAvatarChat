import asyncio
import queue
import threading
import time
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple, Iterable

import numpy as np
from loguru import logger

from chat_engine.common.chat_data_type import ChatDataType
from chat_engine.common.engine_channel_type import EngineChannelType
from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo
from chat_engine.contexts.handler_context import HandlerContext, HandlerResultType
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel, ChatEngineConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundle
from chat_engine.data_models.session_info_data import IOQueueType


@dataclass
class HandlerEnv:
    handler_info: HandlerBaseInfo
    handler: HandlerBase
    config: HandlerBaseConfigModel
    context: Optional[HandlerContext] = None
    input_queue: Optional[queue.Queue] = None
    output_info: Optional[Dict[ChatDataType, HandlerDataInfo]] = None


@dataclass
class HandlerRecord:
    env: HandlerEnv
    pump_thread: Optional[threading.Thread] = None


@dataclass
class DataSource:
    owner: str = ""
    source_queue: IOQueueType = None
    target_types: List[ChatDataType] = None


@dataclass
class DataSink:
    owner: str = ""
    sink_queue: queue.Queue = None
    data_type: ChatDataType = ChatDataType.NONE


class ChatSession:
    input_type_mapping = {
        EngineChannelType.VIDEO: [ChatDataType.CAMERA_VIDEO],
        EngineChannelType.AUDIO: [ChatDataType.MIC_AUDIO],
    }

    def __init__(self, session_context: SessionContext, engine_config: ChatEngineConfigModel):
        self.session_context = session_context

        self.data_sinks: Dict[ChatDataType, List[DataSink]] = {}
        self.inputs: List[DataSource] = []
        self.outputs: Dict[Tuple[str, ChatDataType], DataSink] = {}

        self.handlers: Dict[str, HandlerRecord] = {}
        self.input_pump_thread: Optional[threading.Thread] = None

        for channel_type, input_queue in session_context.input_queues.items():
            target_types = self.input_type_mapping.get(channel_type, None)
            if target_types is None:
                logger.warning(f"Channel type of {channel_type} is not supported, ignored.")
                continue
            self.inputs.append(DataSource(
                owner="",
                source_queue=input_queue,
                target_types=target_types
            ))

        for output_type, output_info in engine_config.outputs.items():
            engine_channel_type = output_info.type.channel_type
            if engine_channel_type not in session_context.output_queues:
                logger.warning(f"Channel type of {engine_channel_type} not found in engine outputs, "
                               f"configured output {output_info} will be ignored.")
                continue
            output_key = (output_info.handler, output_info.type)
            if output_key in self.outputs:
                logger.warning(f"Duplicate output {output_key} to {output_type} found, ignored.")
                continue
            output_queue = session_context.output_queues[engine_channel_type]
            self.outputs[output_key] = DataSink(
                owner="",
                sink_queue=output_queue,
                data_type = output_info.type,
            )

    @classmethod
    def packet_audio_data(cls, session_context: SessionContext, audio_data: Tuple[int, np.ndarray],
                          _target_type: ChatDataType):
        sr, audio_array = audio_data
        definition = session_context.get_input_audio_definition(sr, 1)
        data_bundle = DataBundle(definition)
        audio_array = audio_array.squeeze()[np.newaxis, ...]
        data_bundle.set_main_data(audio_array)
        return data_bundle

    @classmethod
    def packet_video_data(cls, session_context: SessionContext, video_data: np.ndarray,
                           _target_type: ChatDataType):
        frame_rate, image = video_data
        image = image.squeeze()
        definition = session_context.get_input_video_definition(
            list(image.shape), frame_rate,
            allow_shape_change=True
        )
        data_bundle = DataBundle(definition)
        input_image = image[np.newaxis, ...]
        data_bundle.set_main_data(input_image)
        return data_bundle

    @classmethod
    def packet_input_data(cls, session_context: SessionContext, input_data, target_type: ChatDataType):
        chat_data = ChatData(
            type=target_type,
        )
        data_bundle = None
        timestamp = None
        if len(input_data) > 2:
            timestamp = input_data[2]
            input_data = input_data[:2]
        if target_type.channel_type == EngineChannelType.AUDIO:
            data_bundle = cls.packet_audio_data(session_context, input_data, target_type)
        elif target_type.channel_type == EngineChannelType.VIDEO:
            data_bundle = cls.packet_video_data(session_context, input_data, target_type)
        if data_bundle is None:
            logger.warning(f"Unsupported target type {target_type}")
            return None
        chat_data.data = data_bundle
        if timestamp is not None:
            chat_data.timestamp = timestamp
        return chat_data

    @classmethod
    def inputs_pumper(cls, session_context: SessionContext, inputs: List[DataSource],
                    sinks: Dict[ChatDataType, List[DataSink]],
                    outputs: Dict[Tuple[str, ChatDataType], DataSink]):
        shared_states = session_context.shared_states
        while shared_states.active:
            input_data_list = []
            timestamp = session_context.get_timestamp()

            for input_source in inputs:
                input_queue = input_source.source_queue
                try:
                    input_data = input_queue.get_nowait()
                    input_data_list.append((input_source, input_data))
                except (queue.Empty, asyncio.QueueEmpty):
                    continue
            if len(input_data_list) == 0:
                time.sleep(0.03)
                continue
            for input_source, input_data in input_data_list:
                for target_type in input_source.target_types:
                    chat_data = cls.packet_input_data(session_context, input_data, target_type)
                    if chat_data is None:
                        continue
                    if not chat_data.is_timestamp_valid():
                        chat_data.timestamp = timestamp
                    chat_data.source = input_source.owner
                    cls.distribute_data(chat_data, sinks, outputs)

    @classmethod
    def _packet_chat_data(cls, handler_name: str, output_info, session_context: SessionContext,
                          data: HandlerResultType):
        if data is None:
            return None
        timestamp = session_context.get_timestamp()
        single_output = None
        if len(output_info) == 1:
            single_output = list(output_info.keys())[0]

        if isinstance(data, ChatData):
            chat_data = data
        elif isinstance(data, DataBundle):
            if single_output is None:
                msg = f"Bare DataBundle is supported only if handler outputs single chat data type."
                raise ValueError(msg)
            chat_data = ChatData(
                data=data,
                type=single_output,
                timestamp=timestamp,
            )
        elif isinstance(data, Tuple) and len(data) == 2:
            chat_data_type, raw_data = data
            if not isinstance(chat_data_type, ChatDataType) or not isinstance(raw_data, np.ndarray):
                msg = f"Unsupported handler output type {type(data)}"
                raise ValueError(msg)
            if chat_data_type not in output_info:
                msg = f"Handler output type {chat_data_type} is not configured in outputs declaration."
                raise ValueError(msg)
            data_bundle = DataBundle(definition=output_info[chat_data_type].definition)
            data_bundle.set_main_data(raw_data)
            chat_data = ChatData(
                data=data_bundle,
                type=chat_data_type,
                timestamp=timestamp,
            )
        else:
            msg = f"Unsupported handler output type {type(data)}"
            raise ValueError(msg)
        if not chat_data.is_timestamp_valid():
            chat_data.timestamp = timestamp
        chat_data.source = handler_name
        return chat_data

    @classmethod
    def distribute_data(cls, data: ChatData, sinks: Dict[ChatDataType, List[DataSink]],
                       outputs: Dict[Tuple[str, ChatDataType], DataSink]):
        source_key = (data.source, data.type)
        data_sink = outputs.get(source_key, None)
        if data_sink is not None:
            data_sink.sink_queue.put_nowait(data)
        sink_list = sinks.get(data.type, [])
        for sink in sink_list:
            if sink.owner == data.source:
                continue
            sink.sink_queue.put_nowait(data)

    @classmethod
    def submit_data(cls, data: HandlerResultType, handler_name: str, output_info, session_context: SessionContext,
                    sinks: Dict[ChatDataType, List[DataSink]], outputs: Dict[Tuple[str, ChatDataType], DataSink]):
        chat_data = cls._packet_chat_data(handler_name, output_info, session_context, data)
        if chat_data is not None:
            cls.distribute_data(chat_data, sinks, outputs)

    @classmethod
    def handler_pumper(cls, session_context: SessionContext, handler_env: HandlerEnv,
                       sinks: Dict[ChatDataType, List[DataSink]],
                       outputs: Dict[Tuple[str, ChatDataType], DataSink]):
        shared_states = session_context.shared_states
        input_queue = handler_env.input_queue
        handler = handler_env.handler
        output_info = handler_env.output_info
        if output_info is None:
            output_info = {}
        while shared_states.active:
            try:
                input_data = input_queue.get_nowait()
            except (queue.Empty, asyncio.QueueEmpty):
                time.sleep(0.03)
                continue
            handler_result = handler.handle(handler_env.context, input_data, output_info)
            if not isinstance(handler_result, Iterable):
                handler_result = [handler_result]
            for handler_output in handler_result:
                if handler_result is None:
                    continue
                chat_data = cls._packet_chat_data(
                    handler_env.handler_info.name,
                    output_info,
                    session_context,
                    handler_output
                )
                if chat_data is None:
                    continue
                cls.distribute_data(chat_data, sinks, outputs)

    def prepare_handler(self, handler: HandlerBase, handler_info: HandlerBaseInfo,
                        handler_config: HandlerBaseConfigModel):
        handler_env = HandlerEnv(handler_info=handler_info, handler=handler, config=handler_config)
        handler_env.context = handler.create_context(self.session_context, handler_env.config)
        handler_env.context.owner = handler_info.name
        handler_env.input_queue = queue.Queue()
        io_detail = handler.get_handler_detail(self.session_context, handler_env.context)
        inputs = io_detail.inputs
        for input_type, input_info in inputs.items():
            sink_list = self.data_sinks.setdefault(input_type, [])
            data_sink = DataSink(owner=handler_info.name, sink_queue=handler_env.input_queue)
            sink_list.append(data_sink)
        handler_env.output_info = io_detail.outputs

        self.handlers[handler_info.name] = HandlerRecord(env=handler_env)

    def start(self):
        self.session_context.shared_states.active = True
        for handler_name, handler_record in self.handlers.items():
            start_args = (self.session_context, handler_record.env,
                          self.data_sinks, self.outputs)
            handler_record.env.context.data_submitter = lambda data: self.submit_data(
                data, handler_name, handler_record.env.output_info, self.session_context,
                self.data_sinks, self.outputs
            )
            handler_record.env.handler.start_context(self.session_context, handler_record.env.context)
            handler_record.pump_thread = threading.Thread(target=self.handler_pumper, args=start_args)
            handler_record.pump_thread.start()
        input_pumper_args = (self.session_context, self.inputs, self.data_sinks, self.outputs)
        self.input_pump_thread = threading.Thread(target=self.inputs_pumper, args=input_pumper_args)
        self.input_pump_thread.start()
        self.session_context.set_input_start()

    def stop(self):
        self.session_context.shared_states.active = False
        if self.input_pump_thread:
            self.input_pump_thread.join()
            self.input_pump_thread = None
        for handler_name, handler_record in self.handlers.items():
            if handler_record.pump_thread:
                handler_record.pump_thread.join()
                handler_record.pump_thread = None
            handler_record.env.handler.destroy_context(handler_record.env.context)
        self.handlers.clear()
        self.session_context.cleanup()
        logger.info("chat session stopped")

    def get_timestamp(self):
        return self.session_context.get_timestamp()
