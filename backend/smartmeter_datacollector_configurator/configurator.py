import configparser
import logging

from .dto import ConfigDto, LoggerSinkDto, MqttSinkDto, ReaderDto, SinkType

LOGGER = logging.getLogger("uvicorn.error")


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
                LOGGER.warning("Type of sink not defined. Ignored.")
                continue
            if sink_dict["type"] == SinkType.MQTT:
                dto.mqttSink = MqttSinkDto.parse_obj(sink_dict)
                if "ca_file_path" in sink_dict:
                    try:
                        dto.mqttSink.caCert = _read_txt_file("./ca.crt")
                    except OSError as ex:
                        LOGGER.warning("Unable to read CA certificate file. '%s'", str(ex))
            elif sink_dict["type"] == SinkType.LOGGER:
                dto.loggerSink = LoggerSinkDto.parse_obj(sink_dict)
        elif sec == "logging":
            dto.logLevel = parser.get(sec, "default", fallback="WARNING")
    return dto


def write_config_from_dto(file_path: str, config: ConfigDto) -> None:
    parser = configparser.ConfigParser()
    for i, reader in enumerate(config.readers):
        sec_name = f"reader{i}"
        parser.add_section(sec_name)
        parser[sec_name] = reader.dict(exclude_none=True)
    sinks = (config.mqttSink, config.loggerSink)
    for i, sink in enumerate(sinks):
        if not sink:
            continue
        sec_name = f"sink{i}"
        parser.add_section(sec_name)
        sec_dict = sink.dict(exclude={"caCert"}, exclude_none=True)
        print(sec_dict)
        parser[sec_name] = sec_dict

        # Handle CA certificate file
        if isinstance(sink, MqttSinkDto) and sink.caCert:
            try:
                _write_txt_file("./ca.crt", sink.caCert)
            except OSError as ex:
                LOGGER.error("Unable to write ca certificate file. '%s'", ex)
                raise ConfigWriteError(ex) from ex
            parser[sec_name]["ca_file_path"] = "./ca.crt"

    parser.add_section("logging")
    parser["logging"] = {
        "default": config.logLevel
    }

    try:
        _write_config_file(file_path, parser)
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
    with open(file_path, 'w') as file:
        config.write(file, True)


def _read_txt_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def _write_txt_file(file_path: str, content: str) -> None:
    with open(file_path, 'w') as file:
        file.write(content)
