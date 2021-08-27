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
    # pylint: disable=too-few-public-methods
    class Config:
        anystr_strip_whitespace = True
        use_enum_values = True


class ReaderDto(BaseModel):
    type: ReaderType
    port: str
    key: Optional[str]

    @validator("port")
    @classmethod
    def port_not_empty(cls, val: str):
        if not val.strip():
            raise ValueError("Smartmeter port must not be empty.")
        return val.strip()


class MqttSinkDto(BaseModel):
    type = SinkType.MQTT
    host: str
    port: int = 1883
    tls: bool = False
    ca_cert: Optional[str]
    check_hostname: bool = True
    password: Optional[str]
    username: Optional[str]

    @validator("host")
    @classmethod
    def host_not_empty(cls, val: str):
        if not val:
            raise ValueError("MQTT host must not be empty.")
        return val

    @validator("port")
    @classmethod
    def port_valid_range(cls, val: int):
        if val <= 0 or val > 65535:
            raise ValueError(f"Invalid MQTT sink port {val}.")
        return val

    @validator("username")
    @classmethod
    def username_password_exists(cls, val: str, values):
        if val and not values["password"]:
            raise ValueError("No password set for username.")
        return val


class LoggerSinkDto(BaseModel):
    type = SinkType.LOGGER
    name: str = "DataLogger"

    @validator("name")
    @classmethod
    def name_not_empty(cls, val: str):
        if not val.strip():
            raise ValueError("Name must not be empty.")
        return val.strip()


class ConfigDto(BaseModel):
    log_level: str = "WARNING"
    readers: List[ReaderDto] = []
    mqtt_sink: Optional[MqttSinkDto]
    logger_sink: Optional[LoggerSinkDto]

    @validator("log_level")
    @classmethod
    def log_level_valid(cls, val: str):
        lvl = val.strip().upper()
        if lvl not in LOGGER_LEVEL:
            raise ValueError(f"Invalid logging level '{lvl}'. Must be one of {LOGGER_LEVEL}")
        return lvl


class CredentialsDto(BaseModel):
    password: str

    @validator("password")
    @classmethod
    def password_valid(cls, val: str):
        pwd = val.strip()
        if len(pwd) < 8 or len(pwd) > 30:
            raise ValueError("Invalid password length.")
        return pwd
