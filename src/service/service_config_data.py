from typing import Optional, Union

from pydantic import BaseModel, Field


class TwilioConfigData(BaseModel):
    twilio_account_sid: str
    twilio_auth_token: str


RTCServiceConfigData = Union[TwilioConfigData]


class ServiceConfigData(BaseModel):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8080)
    cert_file: Optional[str] = Field(default=None)
    cert_key: Optional[str] = Field(default=None)
    rtc_config: Optional[RTCServiceConfigData] = Field(default=None)
