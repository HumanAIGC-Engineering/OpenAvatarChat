from typing import Optional, Dict

from pydantic import BaseModel, Field


class ServiceConfigData(BaseModel):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8080)
    cert_file: Optional[str] = Field(default=None)
    cert_key: Optional[str] = Field(default=None)
