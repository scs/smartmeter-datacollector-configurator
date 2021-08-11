import configparser
import logging
from typing import Dict, Any


class ConfigWriteError(Exception):
    pass


class InvalidConfigError(Exception):
    pass


def retrieve_config(file_path: str) -> Dict[str, Any]:
    parser = read_config_file(file_path)
    config = {sec: dict(parser.items(sec)) for sec in parser.sections()}
    return config


def set_config(file_path: str, config: Dict[str, Any]) -> None:
    parser = configparser.ConfigParser()
    parser.read_dict(config)
    try:
        write_config_file(file_path, parser)
    except OSError as ex:
        logging.error("Unable to write config to file. '%s'", ex)
        raise ConfigWriteError(ex) from ex


def read_config_file(file_path: str) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    read_files = parser.read(file_path)
    if read_files:
        logging.debug("Read config from file '%s'", read_files[0])
    else:
        logging.warning("Unable to read config file. Returning empty config.")
    return parser


def write_config_file(file_path: str, config: configparser.ConfigParser) -> None:
    with open(file_path, 'w') as file:
        config.write(file, True)
