import copy
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Sequence, Any, Union

import numpy as np

from chat_engine.data_models.runtime_data.data_store import DataStore, DataStoreType
from chat_engine.data_models.runtime_data.time_unit_type import TimeUnitType


@dataclass
class DataBundleEntry:
    name: str
    index: int = -1
    shape: List[int] = field(default_factory=list)
    time_axis: int = -1
    sample_rate: int = 0
    time_unit: TimeUnitType = TimeUnitType.NONE

    @staticmethod
    def create_audio_entry(name: str, channel_num: int, sample_rate: int) -> "DataBundleEntry":
        return DataBundleEntry(
            name=name,
            shape=[channel_num, 1],
            time_axis=1,
            sample_rate=sample_rate,
            time_unit=TimeUnitType.AUDIO_SAMPLE,
        )

    @staticmethod
    def create_framed_entry(name: str, shape: List[int], time_axis: int, sample_rate: int=30):
        return DataBundleEntry(
            name=name,
            shape=shape,
            time_axis=time_axis,
            sample_rate=sample_rate,
            time_unit=TimeUnitType.FRAME,
        )

    @staticmethod
    def create_text_entry(name: str):
        return DataBundleEntry(
            name=name,
            shape=[1],
            time_axis=-1,
            sample_rate=-1,
            time_unit=TimeUnitType.NONE,
        )

    def get_time_axis_size(self, shape: Sequence[int]) -> Optional[int]:
        shape_size = len(shape)
        if self.time_unit != TimeUnitType.NONE:
            if self.time_axis < 0 or self.time_axis >= shape_size:
                raise RuntimeError(f"Invalid time axis {self.time_axis} for shape {self.shape}")
        else:
            return 0
        return shape[self.time_axis]

    def calculate_shape(self, timed_axis_size: int):
        if self.time_unit != TimeUnitType.NONE:
            if timed_axis_size < 0:
                raise RuntimeError(f"Invalid time axis size {timed_axis_size}")
            if self.time_axis < 0 or self.time_axis >= len(self.shape):
                raise RuntimeError(f"Invalid time axis {self.time_axis} for shape {self.shape}")
        else:
            return self.shape.copy()
        result = self.shape.copy()
        result[self.time_axis] = timed_axis_size
        return result


@dataclass
class DataBundleDefinition:
    entries: Dict[str, DataBundleEntry] = field(default_factory=dict)
    main_entry_name: Optional[str] = None
    _conformed: bool = True
    _locked: bool = False
    _lockdown_copy: Optional["DataBundleDefinition"] = None

    def _mark_dirty(self):
        self._conformed = False
        self._lockdown_copy = None

    def add_entry(self, entry: DataBundleEntry):
        if self._locked:
            raise RuntimeError("Cannot add entry to a locked definition")
        if entry.name in self.entries:
            raise RuntimeError(f"Duplicated data name {entry.name}")
        self.entries[entry.name] = entry
        if self.main_entry_name is None:
            self.main_entry_name = entry.name
        self._mark_dirty()

    def set_main_entry(self, name: str):
        if self._locked:
            raise RuntimeError("Cannot set main entry to a locked definition")
        if name not in self.entries:
            raise RuntimeError(f"Invalid main entry {name}")
        self.main_entry_name = name
        self._mark_dirty()

    def get_main_entry(self) -> Optional[DataBundleEntry]:
        if self.main_entry_name is None:
            return None
        return self.entries.get(self.main_entry_name)

    def update(self, other: "DataBundleDefinition",
               allow_partial_merge: bool=False, force_override:bool=False):
        if other is None:
            return
        if self._locked:
            raise RuntimeError("Cannot update a locked definition")
        for name, entry in other.entries.items():
            if name in self.entries and not force_override:
                if allow_partial_merge:
                    continue
                else:
                    raise RuntimeError(f"Duplicated data name {name}")
            else:
                self.entries[name] = entry
                self._mark_dirty()

    def conform(self):
        if self._conformed:
            return
        for entry_id, entry in enumerate(self.entries.values()):
            entry.index = entry_id
        self._conformed = True

    def lockdown(self) -> "DataBundleDefinition":
        if self._locked:
            return self
        if self._lockdown_copy is not None:
            return self._lockdown_copy
        self.conform()
        result = DataBundleDefinition()
        for name, entry in self.entries.items():
            result.entries[name] = copy.copy(entry)
        result.main_entry_name = self.main_entry_name
        result._conformed = True
        result._locked = True
        self._lockdown_copy = result
        return result

    @property
    def locked(self) -> bool:
        return self._locked

    @property
    def conformed(self) -> bool:
        return self._conformed


class DataBundle:
    def __init__(self, definition: DataBundleDefinition):
        self._definition: DataBundleDefinition = definition.lockdown()
        self.events: dict[str, Any] = {}
        self._data_entries: List[DataBundleEntry] = []
        self.data: List[DataStore] = []
        for entry_name, entry in self._definition.entries.items():
            self._data_entries.append(entry)
            self.data.append(DataStore(None, DataStoreType.INVALID))

    def __str__(self):
        data_infos = ""
        not_set_entries = ""
        event_str = ""
        for entry, data_store in zip(self._data_entries, self.data):
            if data_store.valid:
                if len(data_infos) > 0:
                    data_infos += ", "
                if isinstance(data_store.data, np.ndarray):
                    data_infos += (f"{entry.name}: length={entry.get_time_axis_size(data_store.data.shape)} "
                                   f"{entry.time_unit.name}")
                else:
                    data_infos += f"{entry.name}: <No Detail>"
            else:
                if len(not_set_entries) > 0:
                    not_set_entries += ", "
                not_set_entries += f"{entry.name}"
                continue
        for event_name, event_value in self.events.items():
            if len(event_str) > 0:
                event_str += ", "
            event_str += f"{event_name}: {event_value}"

        result = "DataBundle: "
        if len(data_infos) > 0:
            result += f" ValidData=[{data_infos}];"
        if len(event_str) > 0:
            result += f" Events=[{event_str}];"
        if len(not_set_entries) > 0:
            result += f" MissingData=[{not_set_entries}];"
        return result

    @property
    def definition(self):
        return self._definition

    def get_definition_entry(self, name: str) -> DataBundleEntry:
        return self._definition.entries.get(name, None)

    def get_main_definition_entry(self) -> DataBundleEntry:
        return self._definition.get_main_entry()

    # noinspection PyUnusedLocal
    def get_data_store(self, name: str, read_only: bool=True) -> DataStore:
        entry = self.get_definition_entry(name)
        if entry is None:
            return DataStore(None, DataStoreType.INVALID)
        return self.data[entry.index]

    def set_data_store(self, name: str, data_store: DataStore):
        if data_store is None or not data_store.valid:
            return
        entry = self.get_definition_entry(name)
        if entry is None:
            return
        self.data[entry.index] = data_store

    # noinspection PyMethodMayBeStatic
    def is_base_layer(self) -> bool:
        return True

    def set_array_data(self, name: str, entry: DataBundleEntry, data: np.ndarray):
        timed_axis_size = entry.get_time_axis_size(data.shape)
        if timed_axis_size is None or timed_axis_size <= 0:
            raise RuntimeError(f"Dimension mismatch: {name}: {data.shape} is not valid")
        allowed_shape = entry.calculate_shape(timed_axis_size=timed_axis_size)
        if not np.array_equal(data.shape, allowed_shape):
            raise RuntimeError(f"Shape mismatch: Shape of {name} is {data.shape}, not fit defined {allowed_shape}")
        data_store = self.get_data_store(name, read_only=False)
        return data_store.set_data(data, DataStoreType.LOCAL_MEMORY)

    def set_text_data(self, name: str, _entry: DataBundleEntry, data: str):
        data_store = self.get_data_store(name, read_only=False)
        return data_store.set_data(data, DataStoreType.LOCAL_MEMORY)

    def set_data(self, name: str, data: Union[np.ndarray, str]):
        entry = self._definition.entries.get(name, None)
        if entry is None:
            raise RuntimeError(f"Unknown data name {name}")
        if isinstance(data, np.ndarray):
            return self.set_array_data(name, entry, data)
        elif isinstance(data, str):
            return self.set_text_data(name, entry, data)
        else:
            raise RuntimeError(f"Input data type {type(data)} is not supported.")

    def set_main_data(self, data: Union[np.ndarray, str]):
        main_data_name = self._definition.main_entry_name
        if main_data_name is None:
            raise RuntimeError("No main data entry")
        return self.set_data(main_data_name, data)

    def get_data(self, name: str) -> Union[np.ndarray, str]:
        data_store = self.get_data_store(name, read_only=True)
        return data_store.get_data()

    def get_main_data(self) -> Optional[Union[np.ndarray, str]]:
        main_entry = self._definition.main_entry_name
        if main_entry is None:
            return None
        return self.get_data(main_entry)

    def add_meta(self, name, value):
        self.events[name] = value

    def get_meta(self, name, default=None):
        return self.events.get(name, default)
