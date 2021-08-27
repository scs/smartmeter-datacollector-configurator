import configparser
import logging

from .dto import ConfigDto, LoggerSinkDto, MqttSinkDto, ReaderDto, SinkType

CA_FILE_NAME = "ca.crt"
CONFIG_FILE_NAME = "datacollector.ini"

LOGGER = logging.getLogger("uvicorn.error")


class ConfigWriteError(Exception):
    pass


def retrieve_config(config_dir: str) -> ConfigDto:
    parser = _read_config_file(f"{config_dir}/{CONFIG_FILE_NAME}")
    dto = ConfigDto()
    for sec in parser.sections():
        if sec.startswith("reader"):
            dto.readers.append(ReaderDto.parse_obj(
                dict(parser.items(sec))
            ))
        elif sec.startswith("sink"):
            sink_dict = dict(parser.items(sec))
            if "type" not in sink_dict:
                LOGGER.warning("Type of sink not defined. Ignored.")
                continue
            if sink_dict["type"] == SinkType.MQTT:
                dto.mqtt_sink = MqttSinkDto.parse_obj(sink_dict)
                if "ca_file_path" in sink_dict:
                    try:
                        dto.mqtt_sink.ca_cert = _read_txt_file(f"{config_dir}/{CA_FILE_NAME}")
                    except OSError as ex:
                        LOGGER.warning("Unable to read CA certificate file. '%s'", str(ex))
            elif sink_dict["type"] == SinkType.LOGGER:
                dto.logger_sink = LoggerSinkDto.parse_obj(sink_dict)
        elif sec == "logging":
            dto.log_level = parser.get(sec, "default", fallback="WARNING")
    return dto


def write_config_from_dto(config_dir: str, config: ConfigDto) -> None:
    parser = configparser.ConfigParser()
    for i, reader in enumerate(config.readers):
        sec_name = f"reader{i}"
        parser.add_section(sec_name)
        parser[sec_name] = reader.dict(exclude_none=True)
    sinks = (config.mqtt_sink, config.logger_sink)
    for i, sink in enumerate(sinks):
        if not sink:
            continue
        sec_name = f"sink{i}"
        parser.add_section(sec_name)
        sec_dict = sink.dict(exclude={"ca_cert"}, exclude_none=True)
        parser[sec_name] = sec_dict

        # Handle CA certificate file
        if isinstance(sink, MqttSinkDto) and sink.ca_cert:
            try:
                _write_txt_file(f"{config_dir}/{CA_FILE_NAME}", sink.ca_cert)
            except OSError as ex:
                LOGGER.error("Unable to write ca certificate file. '%s'", ex)
                raise ConfigWriteError(ex) from ex
            parser[sec_name]["ca_file_path"] = f"{config_dir}/{CA_FILE_NAME}"

    parser.add_section("logging")
    parser["logging"] = {
        "default": config.log_level
    }

    try:
        _write_config_file(f"{config_dir}/{CONFIG_FILE_NAME}", parser)
    except OSError as ex:
        LOGGER.error("Unable to write config to file. '%s'", ex)
        raise ConfigWriteError(ex) from ex


def _read_config_file(file_path: str) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    read_files = parser.read(file_path)
    if read_files:
        LOGGER.debug("Read config from file '%s'", read_files[0])
    else:
        LOGGER.warning("Unable to read config file. Returning empty config.")
    return parser


def _write_config_file(file_path: str, config: configparser.ConfigParser) -> None:
    with open(file_path, 'w', encoding="utf-8") as file:
        config.write(file, True)


def _read_txt_file(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()


def _write_txt_file(file_path: str, content: str) -> None:
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(content)
