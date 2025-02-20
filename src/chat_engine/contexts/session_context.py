from dataclasses import dataclass
from typing import Dict, List

from chat_engine.data_models.chat_engine_config_data import EngineChannelType
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundleEntry
from chat_engine.data_models.session_info_data import SessionInfoData, IOQueueType


@dataclass
class SharedStates:
    active: bool = False
    enable_vad: bool = True
    is_listening: bool = False
    speech_round: int = 0
    human_speech_segment_num: int = 0


class SessionContext(object):
    def __init__(self, session_info: SessionInfoData,
                 input_queues: Dict[EngineChannelType, IOQueueType],
                 output_queues: Dict[EngineChannelType, IOQueueType]):
        self.session_info = session_info
        self.input_queues = input_queues
        self.output_queues = output_queues
        self.shared_states = SharedStates()
        self.input_definitions: Dict[EngineChannelType, DataBundleDefinition] = {}

    def get_input_audio_definition(self, sample_rate: int, channel_num: int = 1, entry_name: str = "mic_audio"):
        definition = self.input_definitions.get(EngineChannelType.AUDIO, None)
        if definition is None:
            definition = DataBundleDefinition()
            definition.add_entry(DataBundleEntry.create_audio_entry(entry_name, channel_num, sample_rate))
            definition.lockdown()
            self.input_definitions[EngineChannelType.AUDIO] = definition
        return definition

    def get_input_video_definition(self, frame_shape: List[int], frame_rate: int, entry_name: str = "camera_video"):
        definition = self.input_definitions.get(EngineChannelType.VIDEO, None)
        if definition is None:
            data_shape = [1] + frame_shape
            definition = DataBundleDefinition()
            definition.add_entry(DataBundleEntry.create_framed_entry(entry_name, data_shape, 0, frame_rate))
            definition.lockdown()
            self.input_definitions[EngineChannelType.VIDEO] = definition
        return definition

    def cleanup(self):
        for data_queue in self.input_queues.values():
            while not data_queue.empty():
                data_queue.get_nowait()
        for data_queue in self.output_queues.values():
            while not data_queue.empty():
                data_queue.get_nowait()
