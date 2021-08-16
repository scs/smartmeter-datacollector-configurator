import configparser
import dataclasses
import logging
from typing import Any, Dict

from . import validation
from .dto import ConfigDto, LoggerSinkDto, MqttSinkDto, ReaderDto


class ConfigWriteError(Exception):
    pass


def retrieve_config(file_path: str) -> ConfigDto:
    parser = _read_config_file(file_path)
    dto = ConfigDto()
    for sec in parser.sections():
        if sec.startswith("reader"):
            reader_dict = dict(parser.items(sec))
            dto.readers.append(ReaderDto.from_dict(reader_dict))
        elif sec.startswith("sink"):
            sink_dict = dict(parser.items(sec))
            if "type" not in sink_dict:
                logging.warning("Type not in sink config. Ignored.")
                continue
            if sink_dict["type"] == "mqtt":
                dto.sinks.append(MqttSinkDto.from_dict(sink_dict))
            elif sink_dict["type"] == "logger":
                dto.sinks.append(LoggerSinkDto.from_dict(sink_dict))
        elif sec == "logging":
            dto.logLevel = parser.get(sec, "default", fallback="WARNING")
    return dto


def write_config_from_cfg_dict(file_path: str, cfg_dict: Dict[str, Any]) -> None:
    parser = configparser.ConfigParser()
    for i, reader in enumerate(cfg_dict.get("readers", [])):
        sec_name = f"reader{i}"
        parser.add_section(sec_name)
        parser[sec_name] = validation.validate_reader(reader)
    for i, sink in enumerate(cfg_dict.get("sinks", [])):
        sec_name = f"sink{i}"
        parser.add_section(sec_name)
        parser[sec_name] = validation.validate_sink(sink)

    parser.add_section("logging")
    if "logLevel" in cfg_dict:
        parser["logging"] = {
            "default": validation.validate_logging(cfg_dict["logLevel"])}

    try:
        _write_config_file(file_path, parser)
    except OSError as ex:
        logging.error("Unable to write config to file. '%s'", ex)
        raise ConfigWriteError(ex) from ex


def _read_config_file(file_path: str) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    read_files = parser.read(file_path)
    if read_files:
        logging.debug("Read config from file '%s'", read_files[0])
    else:
        logging.warning("Unable to read config file. Returning empty config.")
    return parser


def _write_config_file(file_path: str, config: configparser.ConfigParser) -> None:
    with open(file_path, 'w') as file:
        config.write(file, True)
