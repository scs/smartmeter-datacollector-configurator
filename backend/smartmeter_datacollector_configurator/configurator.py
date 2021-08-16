import configparser
import logging

from . import validation
from .dto import ConfigDto, LoggerSinkDto, MqttSinkDto, ReaderDto, SinkType


class ConfigWriteError(Exception):
    pass


def retrieve_config(file_path: str) -> ConfigDto:
    parser = _read_config_file(file_path)
    dto = ConfigDto()
    for sec in parser.sections():
        if sec.startswith("reader"):
            dto.readers.append(ReaderDto.parse_obj(
                dict(parser.items(sec))
            ))
        elif sec.startswith("sink"):
            sink_dict = dict(parser.items(sec))
            if "type" not in sink_dict:
                logging.warning("Type of sink not defined. Ignored.")
                continue
            if sink_dict["type"] == SinkType.MQTT:
                dto.sinks.append(MqttSinkDto.parse_obj(sink_dict))
            elif sink_dict["type"] == SinkType.LOGGER:
                dto.sinks.append(LoggerSinkDto.parse_obj(sink_dict))
        elif sec == "logging":
            dto.logLevel = parser.get(sec, "default", fallback="WARNING")
    return dto


def write_config_from_dto(file_path: str, config: ConfigDto) -> None:
    parser = configparser.ConfigParser()
    for i, reader in enumerate(config.readers):
        sec_name = f"reader{i}"
        parser.add_section(sec_name)
        parser[sec_name] = validation.validate_reader(reader.dict())
    for i, sink in enumerate(config.sinks):
        sec_name = f"sink{i}"
        parser.add_section(sec_name)
        parser[sec_name] = validation.validate_sink(sink.dict())

    parser.add_section("logging")
    parser["logging"] = {
        "default": validation.validate_logging(config.logLevel)
    }

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
