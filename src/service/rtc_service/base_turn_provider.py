from abc import ABC, abstractmethod
from typing import Type, Dict

from pydantic import BaseModel


class BaseRtcTurnEntity:
    def __init__(self):
        self.rtc_configuration: Dict = {}


class BaseRtcTurnProvider(ABC):
    @abstractmethod
    def get_config_model(self) -> Type[BaseModel]:
        pass

    @abstractmethod
    def prepare_rtc_configuration(self, config: BaseModel) -> BaseRtcTurnEntity:
        pass