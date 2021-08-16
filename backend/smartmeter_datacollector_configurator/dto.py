from abc import ABC
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class ReaderType(str, Enum):
    LGE450 = "lge450"


class SinkType(str, Enum):
    MQTT = "mqtt"
    LOGGER = "logger"


class ReaderDto(BaseModel):
    type: ReaderType
    port: str
    key: Optional[str]


class MqttSinkDto(BaseModel):
    type = SinkType.MQTT
    host: str
    port: int = 1883
    tls: bool = False


class LoggerSinkDto(BaseModel):
    type = SinkType.LOGGER
    name: str = "DataLogger"


class ConfigDto(BaseModel):
    logLevel: str = "WARNING"
    readers: List[ReaderDto] = []
    sinks: List[Union[MqttSinkDto, LoggerSinkDto]] = []
