import pytest
from pydantic import ValidationError

from smartmeter_datacollector_configurator.dto import (ConfigDto, CredentialsDto, LoggerSinkDto, MeterDto, MeterType,
                                                       MqttSinkDto, SinkType)


def test_meter_dto_valid():
    MeterDto.model_validate({
        "type": MeterType.LGE450,
        "port": "/dev/port",
        "key": "KEY"
    })

    MeterDto.model_validate({
        "type": "lge450",
        "port": "/dev/port",
        "key": "KEY",
    })

    MeterDto.model_validate({
        "type": MeterType.LGE450,
        "port": "/dev/port",
    })


def test_meter_dto_invalid_type():
    with pytest.raises(ValidationError):
        MeterDto.model_validate({
            "type": "invalid_meter",
            "port": "/dev/port",
        })

    with pytest.raises(ValidationError):
        MeterDto.model_validate({
            "type": "",
            "port": "/dev/port",
        })

    with pytest.raises(ValidationError):
        MeterDto.model_validate({
            "port": "/dev/port",
        })


def test_meter_dto_invalid_port():
    with pytest.raises(ValidationError):
        MeterDto.model_validate({
            "type": MeterType.LGE450,
            "port": "",
        })

    with pytest.raises(ValidationError):
        MeterDto.model_validate({
            "type": MeterType.LGE450,
        })


def test_mqtt_sink_dto_valid():
    MqttSinkDto.model_validate({
        "host": "localhost",
    })

    MqttSinkDto.model_validate({
        "type": SinkType.MQTT,
        "host": "localhost",
    })

    MqttSinkDto.model_validate({
        "host": "localhost",
        "port": 2000,
        "tls": True,
        "ca_cert": "CA_CERT",
        "check_hostname": False,
        "password": "PWD",
        "username": "USER",
    })


def test_mqtt_sink_dto_invalid_type():
    with pytest.raises(ValidationError):
        MqttSinkDto.model_validate({
            "type": SinkType.LOGGER,
            "host": "localhost",
        })


def test_mqtt_sink_dto_invalid_host():
    with pytest.raises(ValidationError):
        MqttSinkDto.model_validate({
            "host": " ",
        })

    with pytest.raises(ValidationError):
        MqttSinkDto.model_validate({
            "host": "",
        })

    with pytest.raises(ValidationError):
        MqttSinkDto.model_validate({})


def test_mqtt_sink_dto_invalid_port():
    with pytest.raises(ValidationError):
        MqttSinkDto.model_validate({
            "host": "localhost",
            "port": 0,
        })

    with pytest.raises(ValidationError):
        MqttSinkDto.model_validate({
            "host": "localhost",
            "port": -3,
        })

    with pytest.raises(ValidationError):
        MqttSinkDto.model_validate({
            "host": "localhost",
            "port": 65555,
        })


def test_mqtt_sink_dto_invalid_missing_password():
    with pytest.raises(ValidationError):
        MqttSinkDto.model_validate({
            "host": "localhost",
            "username": "user",
        })


def test_logger_sink_dto_valid():
    LoggerSinkDto.model_validate({
        "name": "TestLogger",
    })

    LoggerSinkDto.model_validate({
        "type": SinkType.LOGGER,
        "name": "TestLogger",
    })

    LoggerSinkDto.model_validate({})


def test_logger_sink_dto_invalid_name():
    with pytest.raises(ValidationError):
        LoggerSinkDto.model_validate({
            "name": "",
        })


def test_logger_sink_dto_invalid_type():
    with pytest.raises(ValidationError):
        LoggerSinkDto.model_validate({
            "type": SinkType.MQTT,
        })


def test_config_dto_valid():
    ConfigDto.model_validate({})

    meter_dto = MeterDto.model_validate({
        "type": MeterType.LGE450,
        "port": "/dev/port",
    })

    ConfigDto.model_validate({
        "log_level": "info ",
    })

    ConfigDto.model_validate({
        "log_level": "INFO",
        "meters": [
            meter_dto
        ],
        "mqtt_sink": MqttSinkDto(host="localhost"),
        "logger_sink": LoggerSinkDto()
    })


def test_config_dto_invalid_logger_level():
    with pytest.raises(ValidationError):
        ConfigDto.model_validate({
            "log_level": "INEXISTENT_LEVEL",
        })


def test_credentials_dto_valid():
    CredentialsDto(password="1234567890")
    cred = CredentialsDto(password=" 1234abcd")

    assert cred.password == "1234abcd"


def test_credentials_dto_invalid_pwd():
    with pytest.raises(ValidationError):
        CredentialsDto()  # type: ignore

    with pytest.raises(ValidationError):
        CredentialsDto(password="")

    with pytest.raises(ValidationError):
        CredentialsDto(password=" ")

    with pytest.raises(ValidationError):
        CredentialsDto(password="1234567")

    with pytest.raises(ValidationError):
        CredentialsDto(password="1234554321123455432112345543211")
