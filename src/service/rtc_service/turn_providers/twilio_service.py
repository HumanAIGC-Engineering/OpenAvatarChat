from typing import Type

from pydantic import BaseModel

from service.rtc_service.base_turn_provider import BaseRtcTurnProvider, BaseRtcTurnEntity


class TwilioConfigData(BaseModel):
    twilio_account_sid: str
    twilio_auth_token: str


class TwilioTurnEntity(BaseRtcTurnEntity):
    def __init__(self):
        super().__init__()
        self.client = None
        self.token = None


class TwilioTurnProvider(BaseRtcTurnProvider):

    def get_config_model(self) -> Type[BaseModel]:
        return TwilioConfigData

    def prepare_rtc_configuration(self, config: BaseModel):
        # noinspection PyPackageRequirements
        # noinspection PyUnresolvedReferences
        from twilio.rest import Client
        result = TwilioTurnEntity()
        result.client = Client(
            config.twilio_account_sid,
            config.twilio_auth_token
        )
        result.token = result.client.tokens.create()
        result.rtc_configuration = {
            "iceServers": result.token.ice_servers,
            "iceTransportPolicy": "relay",
        }
        return result
