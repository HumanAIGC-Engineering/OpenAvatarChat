import struct
from dataclasses import dataclass
from typing import List, Optional, Dict, Union, Any

import numpy as np
from loguru import logger

from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundle
from chat_engine.data_models.runtime_data.motion_data_descriptors import MotionDataDescription, BufferDescription
from chat_engine.data_models.runtime_data.motion_entry_serializer_base import BaseMotionEntrySerializer
from chat_engine.data_models.runtime_data.motion_entry_serializers.int16_audio_serializer import \
    MotionEntryAudioInt16Serializer


@dataclass
class MotionDataEntryRegistry:
    name: str
    output_data_type: np.dtype
    serializer: Optional[BaseMotionEntrySerializer] = None
    serializer_context: Any = None


class MotionDataSerializer:
    def __init__(self):
        self.name_mapping: Dict[str, MotionDataEntryRegistry] = {}
        self.record_serializer: Dict[str, ]
        self.last_batch_name: Optional[str] = None
        self.batch_num: int = 0

    def register_data(self, data_name: str, output_name: str, data_type: str,
                      entry_serializer: Optional[BaseMotionEntrySerializer] = None):
        serializer_context = None
        if entry_serializer is not None:
            serializer_context = entry_serializer.create_context()
        self.name_mapping[data_name] = MotionDataEntryRegistry(
            name=output_name,
            output_data_type=np.dtype(data_type),
            serializer=entry_serializer,
            serializer_context=serializer_context,
        )

    def register_audio_data(self, data_name: str):
        self.register_data(
            data_name,
            "audio",
            "int16",
            MotionEntryAudioInt16Serializer(),
        )

    def _update_description(self, description: MotionDataDescription, data_list: List[np.ndarray],
                            data_bundle: DataBundle, write_channel_names: bool):
        definition = data_bundle.definition
        for data_name, registry in self.name_mapping.items():
            entry = definition.find_entry(data_name)
            if entry is None:
                continue
            data_item = data_bundle.get_data(data_name)

            data_desc = BufferDescription()
            data_desc.sample_rate = entry.sample_rate
            data_desc.data_id = len(data_list)
            data_desc.timeline_axis = entry.time_axis
            data_desc.channel_axis = entry.channel_axis
            if write_channel_names:
                data_desc.channel_names = entry.channel_names

            if isinstance(data_item, np.ndarray):
                data_desc.shape = list(data_item.shape)
                data_desc.data_type = data_item.dtype.name
                if registry.serializer is not None:
                    serialize_result = registry.serializer.serialize(
                        registry.serializer_context,
                        description,
                        data_desc,
                        data_item,
                    )
                    data_desc = serialize_result.buffer_descriptor
                    data_item = serialize_result.data
                else:
                    data_desc.data_type = registry.output_data_type.name
                    if registry.output_data_type.name != str(data_item.dtype):
                        data_item = data_item.astype(registry.output_data_type)
            elif isinstance(data_item, str):
                data_desc.data_type = np.dtype(np.uint8).name
                data_desc.shape = [len(data_item)]
            else:
                logger.warning(f"Unsupported data type {type(data_item)} for data {data_name}.")
                continue

            description.data_records[registry.name] = data_desc
            data_list.append(data_item)

    @classmethod
    def _dump_to_bytes(cls, description: MotionDataDescription, data_list: List[np.ndarray]):
        binary_offset = 0
        binary_data = bytes()
        for data_name, data_desc in description.data_records.items():
            if data_desc.data_id < 0:
                continue
            data_item = data_list[data_desc.data_id]
            if isinstance(data_item, bytes):
                data_size = len(data_item)
                binary_data += data_item
            elif isinstance(data_item, np.ndarray):
                data_size = data_item.nbytes
                binary_data += data_item.tobytes()
            elif isinstance(data_item, str):
                raw_bytes = data_item.encode("utf-8")
                data_size = len(raw_bytes)
                binary_data += raw_bytes
            else:
                continue
            data_desc.data_offset = binary_offset
            binary_offset += data_size

        fourcc = b"JBIN"
        json_str = description.model_dump_json()
        desc_bytes = bytes(json_str, "utf-8")
        json_size = len(desc_bytes)
        bin_size = len(binary_data)
        header = fourcc + struct.pack("<II", json_size, bin_size)
        return header + desc_bytes + binary_data

    def _serialize_data_bundle(self, data: DataBundle, include_channel_names: bool = False,
                               definition_only: bool = False):
        description = MotionDataDescription()
        data_items = []

        description.metadata = data.metadata.copy()
        description.events = data.events.copy()
        if not definition_only:
            # TODO this should be changed to something else instead of hardcoded name
            batch_name = data.get_meta("speech_id")

            if self.last_batch_name is not None and batch_name != self.last_batch_name:
                self.batch_num += 1

            description.batch_name = batch_name
            description.batch_id = self.batch_num
            description.start_of_batch = data.start_of_stream
            description.end_of_batch = data.end_of_stream

            self.last_batch_name = batch_name

            if description.end_of_batch:
                self.reset()
        else:
            self.reset()

        write_channel_names = include_channel_names or definition_only
        self._update_description(description, data_items, data, write_channel_names)

        return self._dump_to_bytes(description, data_items)

    def _serialize_definition(self, definition: DataBundleDefinition, include_channel_names: bool = False):
        data_bundle = DataBundle(definition)
        for data_name, registry in self.name_mapping.items():
            entry = definition.find_entry(data_name)
            if entry is not None:
                default_data = entry.create_default_data(registry.output_data_type)
                data_bundle.set_data(data_name, default_data)
        return self._serialize_data_bundle(data_bundle, include_channel_names, definition_only=True)

    def serialize(self, data: Union[DataBundle, DataBundleDefinition], include_channel_names: bool = False):
        if isinstance(data, DataBundle):
            return self._serialize_data_bundle(data, include_channel_names)
        if isinstance(data, DataBundleDefinition):
            return self._serialize_definition(data, include_channel_names)
        raise ValueError(f"Unsupported data type {type(data)}.")

    def reset(self):
        for registry in self.name_mapping.values():
            if registry.serializer is not None:
                registry.serializer.reset(registry.serializer_context)
