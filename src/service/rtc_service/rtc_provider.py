from typing import Dict, Union

import pydantic
from loguru import logger
from pydantic import BaseModel

from engine_utils.singleton import SingletonMeta
from service.rtc_service.turn_providers.twilio_service import TwilioTurnProvider
from service.rtc_service.turn_providers.turn_service import TurnServerProvider
from service.service_data_models.service_config_data import ServiceConfigData


class RTCProvider(metaclass=SingletonMeta):
    def __init__(self):
        self.rtc_turn_providers = {
            "twilio": TwilioTurnProvider(),
            "turn_server": TurnServerProvider(),
        }

    def prepare_rtc_configuration(self, config: Union[ServiceConfigData, BaseModel, Dict]):
        turn_entity = None
        if isinstance(config, ServiceConfigData):
            rtc_config = config.rtc_config
        elif isinstance(config, BaseModel):
            rtc_config = config.model_dump()
        elif isinstance(config, Dict):
            rtc_config = config
        else:
            rtc_config = None
        if rtc_config is not None:
            logger.info(f"Parsing RTC config: {rtc_config}")
            turn_provider_name = rtc_config.get("turn_provider")
            turn_provider = None
            turn_provider_config = None
            if turn_provider_name is not None:
                turn_provider = self.rtc_turn_providers.get(turn_provider_name)
                if turn_provider is None:
                    logger.warning(f"Turn provider {turn_provider_name} is not supported.")
                    turn_provider_name = None
                else:
                    config_model = turn_provider.get_config_model()
                    turn_provider_config = config_model.model_validate(rtc_config)

            if turn_provider is None:
                for provider_name, provider in self.rtc_turn_providers.items():
                    config_model = provider.get_config_model()
                    try:
                        turn_provider_config = config_model.model_validate(rtc_config)
                    except pydantic.ValidationError:
                        continue
                    else:
                        turn_provider_name = provider_name
                        turn_provider = provider
                        break
            if turn_provider is not None:
                logger.info(f"Use {turn_provider_name} as rtc turn provider.")
                turn_entity = turn_provider.prepare_rtc_configuration(turn_provider_config)
        if turn_entity is None:
            logger.info("No valid rtc provider configuration found, STUN/TURN will not be valid. "
                        "Communication across networks may not be established.")
        return turn_entity
