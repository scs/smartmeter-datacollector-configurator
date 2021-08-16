from dataclasses import dataclass, field
from typing import Any, Dict, List, Union


@dataclass
class ReaderDto:
    type: str
    port: str
    key: str

    @classmethod
    def from_dict(cls, reader_dict: Dict[str, Any]) -> "ReaderDto":
        return ReaderDto(
            type=reader_dict.get("type", ""),
            port=reader_dict.get("port", ""),
            key=reader_dict.get("key", "")
        )


@dataclass
class MqttSinkDto:
    host: str
    port: int
    tls: bool
    type: str = "mqtt"

    @classmethod
    def from_dict(cls, sink_dict: Dict[str, Any]) -> "MqttSinkDto":
        return MqttSinkDto(
            host=sink_dict.get("host", ""),
            port=int(sink_dict.get("port", 0)),
            tls=bool(sink_dict.get("tls", False))
        )


@dataclass
class LoggerSinkDto:
    name: str
    type: str = "logger"

    @classmethod
    def from_dict(cls, sink_dict: Dict[str, Any]) -> "LoggerSinkDto":
        return LoggerSinkDto(
            name=sink_dict.get("name", "")
        )


@dataclass
class ConfigDto:
    logLevel: str = ""
    readers: List[ReaderDto] = field(default_factory=list)
    sinks: List[Union[MqttSinkDto, LoggerSinkDto]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, cfg_dict: Dict) -> "ConfigDto":
        return ConfigDto(
            logLevel=cfg_dict.get("logLevel", ""),
            readers=cfg_dict.get("readers", []),
            sinks=cfg_dict.get("sinks", [])
        )
