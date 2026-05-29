from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, ValidationInfo, field_validator

LOGGER_LEVEL = ["DEBUG", "INFO", "WARNING", "ERROR", "FATAL", "CRITICAL"]


class MeterType(str, Enum):
    LGE450 = "lge450"
    LGE360 = "lge360"
    LGE570 = "lge570"
    ISKRAAM550 = "iskraam550"
    KAMSTRUP_HAN = "kamstrup_han"


class SinkType(str, Enum):
    MQTT = "mqtt"
    LOGGER = "logger"


class BaseModel(PydanticBaseModel):
    # pylint: disable=too-few-public-methods
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True)


class MeterDto(BaseModel):
    type: MeterType
    port: str
    key: Optional[str] = None

    @field_validator("port")
    @classmethod
    def port_not_empty(cls, val: str):
        if not val.strip():
            raise ValueError("Smart meter port must not be empty.")
        return val.strip()


class MqttSinkDto(BaseModel):
    type: Literal[SinkType.MQTT] = SinkType.MQTT
    host: str
    port: int = 1883
    tls: bool = False
    ca_cert: Optional[str] = None
    check_hostname: bool = True
    password: Optional[str] = None
    username: Optional[str] = None

    @field_validator("host")
    @classmethod
    def host_not_empty(cls, val: str):
        if not val:
            raise ValueError("MQTT host must not be empty.")
        return val

    @field_validator("port")
    @classmethod
    def port_valid_range(cls, val: int):
        if val <= 0 or val > 65535:
            raise ValueError(f"Invalid MQTT sink port {val}.")
        return val

    @field_validator("username")
    @classmethod
    def username_password_exists(cls, val: Optional[str], info: ValidationInfo):
        if val and not info.data.get("password"):
            raise ValueError("No password set for username.")
        return val


class LoggerSinkDto(BaseModel):
    type: Literal[SinkType.LOGGER] = SinkType.LOGGER
    name: str = "DataLogger"

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, val: str):
        if not val.strip():
            raise ValueError("Name must not be empty.")
        return val.strip()


class ConfigDto(BaseModel):
    log_level: str = "WARNING"
    meters: List[MeterDto] = Field(default_factory=list)
    mqtt_sink: Optional[MqttSinkDto] = None
    logger_sink: Optional[LoggerSinkDto] = None

    @field_validator("log_level")
    @classmethod
    def log_level_valid(cls, val: str):
        lvl = val.strip().upper()
        if lvl not in LOGGER_LEVEL:
            raise ValueError(f"Invalid logging level '{lvl}'. Must be one of {LOGGER_LEVEL}")
        return lvl


class CredentialsDto(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def password_valid(cls, val: str):
        pwd = val.strip()
        if len(pwd) < 8 or len(pwd) > 30:
            raise ValueError("Invalid password length.")
        return pwd
