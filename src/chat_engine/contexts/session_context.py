import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

from loguru import logger

from chat_engine.data_models.chat_engine_config_data import EngineChannelType
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundleEntry
from chat_engine.data_models.session_info_data import SessionInfoData, IOQueueType


@dataclass
class SharedStates:
    active: bool = False
    enable_vad: bool = True


class SessionContext(object):
    def __init__(self, session_info: SessionInfoData,
                 input_queues: Dict[EngineChannelType, IOQueueType],
                 output_queues: Dict[EngineChannelType, IOQueueType]):
        self.session_info = session_info
        self.input_queues = input_queues
        self.output_queues = output_queues
        self.shared_states = SharedStates()
        self.input_definitions: Dict[EngineChannelType, DataBundleDefinition] = {}
        self.input_start_time: float = -1.0

    def get_input_audio_definition(self, sample_rate: int, channel_num: int = 1, entry_name: str = "mic_audio"):
        definition = self.input_definitions.get(EngineChannelType.AUDIO, None)
        if definition is None:
            definition = DataBundleDefinition()
            definition.add_entry(DataBundleEntry.create_audio_entry(entry_name, channel_num, sample_rate))
            definition.lockdown()
            self.input_definitions[EngineChannelType.AUDIO] = definition
        return definition

    def get_input_video_definition(self, frame_shape: List[int], frame_rate: int, entry_name: str = "camera_video",
                                   allow_shape_change: bool = False):
        data_shape = [1] + frame_shape
        definition = self.input_definitions.get(EngineChannelType.VIDEO, None)
        if allow_shape_change and definition is not None:
            defined_shape = list(definition.get_main_entry().shape)
            if defined_shape != data_shape:
                logger.warning(f"Video definition updated, orign shape={defined_shape}, new shape={data_shape}")
                definition = None
        if definition is None:
            definition = DataBundleDefinition()
            definition.add_entry(DataBundleEntry.create_framed_entry(entry_name, data_shape, 0, frame_rate))
            definition.lockdown()
            self.input_definitions[EngineChannelType.VIDEO] = definition
        return definition
    
    def get_input_text_definition(self, entry_name: str = "human_text"):
        definition = self.input_definitions.get(EngineChannelType.TEXT, None)
        if definition is None:
            definition = DataBundleDefinition()
            definition.add_entry(DataBundleEntry.create_text_entry(entry_name))
            definition.lockdown()
            self.input_definitions[EngineChannelType.TEXT] = definition
        return definition

    def cleanup(self):
        for data_queue in self.input_queues.values():
            while not data_queue.empty():
                data_queue.get_nowait()
        for data_queue in self.output_queues.values():
            while not data_queue.empty():
                data_queue.get_nowait()

    def set_input_start(self):
        if self.input_start_time < 0:
            now = time.monotonic()
            self.input_start_time = now

    def get_timestamp(self) -> Tuple[int, int]:
        now = time.monotonic()
        if self.input_start_time < 0:
            return -1, 0
        else:
            return (
                round((now - self.input_start_time) * self.session_info.timestamp_base),
                self.session_info.timestamp_base
            )
