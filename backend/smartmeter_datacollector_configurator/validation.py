from typing import Dict


READER_TYPES = ["lge450"]
LOGGER_LEVEL = ["DEBUG", "INFO", "WARNING", "ERROR", "FATAL", "CRITICAL"]


class InvalidConfigError(Exception):
    pass


def validate_reader(config: Dict[str, str]) -> Dict[str, str]:
    valid_config = {}
    if "type" not in config:
        raise InvalidConfigError("Missing reader type.")
    if config["type"] not in READER_TYPES:
        raise InvalidConfigError(f"Invalid reader type {config['type']}.")
    valid_config["type"] = config["type"]

    if "port" not in config:
        raise InvalidConfigError("Missing reader port.")
    if not isinstance(config["port"], str):
        raise InvalidConfigError("Reader port must be string.")
    if not config["port"].strip():
        raise InvalidConfigError("Reader port is empty.")
    valid_config["port"] = config["port"].strip()

    # optional
    if "key" in config:
        if not isinstance(config["key"], str):
            raise InvalidConfigError("Reader key must be string.")
        valid_config["key"] = config["key"].strip()

    return valid_config


def validate_sink(config: Dict[str, str]) -> Dict[str, str]:
    if "type" not in config:
        raise InvalidConfigError("Missing sink type.")
    if config["type"] == "logger":
        return _validate_logger_sink(config)
    if config["type"] == "mqtt":
        return _validate_mqtt_sink(config)

    raise InvalidConfigError(f"Invalid sink type {config['type']}.")


def validate_logging(level: str) -> str:
    name = level.strip().upper()
    if name not in LOGGER_LEVEL:
        raise InvalidConfigError(f"Invalid logging level '{level}'.")
    return name


def _validate_logger_sink(config: Dict[str, str]) -> Dict[str, str]:
    valid_config = {}
    valid_config["type"] = config["type"]

    # optional
    if "name" in config:
        if not isinstance(config["name"], str):
            raise InvalidConfigError("Sink logger name must be string.")
        if not config["name"].strip():
            raise InvalidConfigError("Sink logger name is empty.")
        valid_config["name"] = config["name"].strip()

    return valid_config


def _validate_mqtt_sink(config: Dict[str, str]) -> Dict[str, str]:
    valid_config = {}
    valid_config["type"] = config["type"]

    if "host" not in config:
        raise InvalidConfigError("Missing MQTT sink host.")
    if not isinstance(config["host"], str):
        raise InvalidConfigError("MQTT sink host must be string.")
    if not config["host"].strip():
        raise InvalidConfigError("MQTT sink host is empty.")
    valid_config["host"] = config["host"].strip()

    if "port" not in config:
        raise InvalidConfigError("Missing MQTT sink port.")
    if not isinstance(config["port"], int):
        raise InvalidConfigError("MQTT sink port must be integer.")
    if config["port"] <= 0 or config["port"] > 65535:
        raise InvalidConfigError(f"Invalid MQTT sink port {config['port']}.")
    valid_config["port"] = config["port"]

    # optional
    if "tls" in config:
        if not isinstance(config["tls"], bool):
            raise InvalidConfigError("MQTT TLS must be boolean.")
        valid_config["tls"] = config["tls"]

    return valid_config
