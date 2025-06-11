from typing import Type

from pydantic import BaseModel

from service.rtc_service.base_turn_provider import (
    BaseRtcTurnProvider,
    BaseRtcTurnEntity,
)


class TurnServerConfigData(BaseModel):
    urls: list[str]
    username: str
    credential: str


class TurnServerProvider(BaseRtcTurnProvider):

    def get_config_model(self) -> Type[BaseModel]:
        return TurnServerConfigData

    def prepare_rtc_configuration(self, config: BaseModel):
        result = BaseRtcTurnEntity()
        result.rtc_configuration = {
            "iceServers": [
                {
                    "urls": config.urls,
                    "username": config.username,
                    "credential": config.credential,
                }
            ]
        }
        return result
