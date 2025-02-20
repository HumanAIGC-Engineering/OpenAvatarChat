from pydantic import BaseModel, Field


class LoggerConfigData(BaseModel):
    log_level: str = Field(default="INFO")
