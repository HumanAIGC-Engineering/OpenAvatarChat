from dataclasses import dataclass
from enum import IntEnum
from typing import Any


class DataStoreType(IntEnum):
    INVALID = 0
    LOCAL_MEMORY = 1


@dataclass
class DataStore:
    data: Any
    storage: DataStoreType = DataStoreType.INVALID

    @property
    def valid(self):
        return self.storage != DataStoreType.INVALID

    def set_data(self, data: Any, storage: DataStoreType):
        self.data = data
        self.storage = storage

    def get_data(self):
        return self.data
