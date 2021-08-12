import configparser
import logging
from typing import Dict, Any

from . import validation


class ConfigWriteError(Exception):
    pass


def retrieve_config(file_path: str) -> Dict[str, Any]:
    parser = _read_config_file(file_path)
    config = {}
    for sec in parser.sections():
        if sec.startswith("reader") or sec.startswith("sink"):
            config[sec] = dict(parser.items(sec))
        elif sec == "logging":
            config[sec] = parser.get(sec, "default", fallback="WARNING")
    return config


def set_config(file_path: str, config: Dict[str, Any]) -> None:
    parser = configparser.ConfigParser()
    for key, val in config.items():
        if key.startswith("reader"):
            parser.add_section(key)
            parser[key] = validation.validate_reader(val)
        elif key.startswith("sink"):
            parser.add_section(key)
            parser[key] = validation.validate_sink(val)
        elif key == "logging":
            parser.add_section(key)
            parser[key] = {"default": validation.validate_logging(val)}
        else:
            raise validation.InvalidConfigError(f"Unknown section name {key}.")
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
