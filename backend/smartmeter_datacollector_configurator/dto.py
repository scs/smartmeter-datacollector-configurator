from enum import Enum
from typing import List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic.class_validators import validator

LOGGER_LEVEL = ["DEBUG", "INFO", "WARNING", "ERROR", "FATAL", "CRITICAL"]


class ReaderType(str, Enum):
    LGE450 = "lge450"


class SinkType(str, Enum):
    MQTT = "mqtt"
    LOGGER = "logger"


class BaseModel(PydanticBaseModel):
    class Config:
        anystr_strip_whitespace = True
        use_enum_values = True


class ReaderDto(BaseModel):
    type: ReaderType
    port: str
    key: Optional[str]

    @validator("port")
    def port_not_empty(cls, v: str):
        if not v.strip():
            raise ValueError("Smartmeter port must not be empty.")
        return v.strip()


class MqttSinkDto(BaseModel):
    type = SinkType.MQTT
    host: str
    port: int = 1883
    tls: bool = False
    caCert: Optional[str]
    username: Optional[str]
    password: Optional[str]

    @validator("host")
    def host_not_empty(cls, v: str):
        if not v:
            raise ValueError("MQTT host must not be empty.")
        return v

    @validator("port")
    def port_valid_range(cls, v: int):
        if v <= 0 or v > 65535:
            raise ValueError(f"Invalid MQTT sink port {v}.")
        return v


class LoggerSinkDto(BaseModel):
    type = SinkType.LOGGER
    name: str = "DataLogger"

    @validator("name")
    def name_not_empty(cls, v: str):
        if not v.strip():
            raise ValueError("Name must not be empty.")
        return v.strip()


class ConfigDto(BaseModel):
    logLevel: str = "WARNING"
    readers: List[ReaderDto] = []
    mqttSink: Optional[MqttSinkDto]
    loggerSink: Optional[LoggerSinkDto]

    @validator("logLevel")
    def log_level_valid(cls, v: str):
        lvl = v.strip().upper()
        if lvl not in LOGGER_LEVEL:
            raise ValueError(f"Invalid logging level '{lvl}'. Must be one of {LOGGER_LEVEL}")
        return lvl


class CredentialsDto(BaseModel):
    password: str

    @validator("password")
    def password_valid(cls, v: str):
        pwd = v.strip()
        if len(pwd) < 8 or len(pwd) > 30:
            raise ValueError("Invalid password length.")
        return pwd
