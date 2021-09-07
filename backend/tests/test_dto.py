import pytest

from smartmeter_datacollector_configurator.dto import (ConfigDto, CredentialsDto, LoggerSinkDto, MeterDto, MeterType,
                                                       MqttSinkDto, SinkType)


def test_meter_dto_valid():
    MeterDto.parse_obj({
        "type": MeterType.LGE450,
        "port": "/dev/port",
        "key": "KEY"
    })

    MeterDto.parse_obj({
        "type": "lge450",
        "port": "/dev/port",
        "key": "KEY",
    })

    MeterDto.parse_obj({
        "type": MeterType.LGE450,
        "port": "/dev/port",
    })


def test_meter_dto_invalid_type():
    with pytest.raises(ValueError):
        MeterDto.parse_obj({
            "type": "invalid_meter",
            "port": "/dev/port",
        })

    with pytest.raises(ValueError):
        MeterDto.parse_obj({
            "type": "",
            "port": "/dev/port",
        })

    with pytest.raises(ValueError):
        MeterDto.parse_obj({
            "port": "/dev/port",
        })


def test_meter_dto_invalid_port():
    with pytest.raises(ValueError):
        MeterDto.parse_obj({
            "type": MeterType.LGE450,
            "port": "",
        })

    with pytest.raises(ValueError):
        MeterDto.parse_obj({
            "type": MeterType.LGE450,
        })


def test_mqtt_sink_dto_valid():
    MqttSinkDto.parse_obj({
        "host": "localhost",
    })

    MqttSinkDto.parse_obj({
        "type": SinkType.MQTT,
        "host": "localhost",
    })

    MqttSinkDto.parse_obj({
        "host": "localhost",
        "port": 2000,
        "tls": True,
        "ca_cert": "CA_CERT",
        "check_hostname": False,
        "password": "PWD",
        "username": "USER",
    })


def test_mqtt_sink_dto_invalid_type():
    with pytest.raises(ValueError):
        MqttSinkDto.parse_obj({
            "type": SinkType.LOGGER,
            "host": "localhost",
        })


def test_mqtt_sink_dto_invalid_host():
    with pytest.raises(ValueError):
        MqttSinkDto.parse_obj({
            "host": " ",
        })

    with pytest.raises(ValueError):
        MqttSinkDto.parse_obj({
            "host": "",
        })

    with pytest.raises(ValueError):
        MqttSinkDto.parse_obj({})


def test_mqtt_sink_dto_invalid_port():
    with pytest.raises(ValueError):
        MqttSinkDto.parse_obj({
            "host": "localhost",
            "port": 0,
        })

    with pytest.raises(ValueError):
        MqttSinkDto.parse_obj({
            "host": "localhost",
            "port": -3,
        })

    with pytest.raises(ValueError):
        MqttSinkDto.parse_obj({
            "host": "localhost",
            "port": 65555,
        })


def test_mqtt_sink_dto_invalid_missing_password():
    with pytest.raises(ValueError):
        MqttSinkDto.parse_obj({
            "host": "localhost",
            "username": "user",
        })


def test_logger_sink_dto_valid():
    LoggerSinkDto.parse_obj({
        "name": "TestLogger",
    })

    LoggerSinkDto.parse_obj({
        "type": SinkType.LOGGER,
        "name": "TestLogger",
    })

    LoggerSinkDto.parse_obj({})


def test_logger_sink_dto_invalid_name():
    with pytest.raises(ValueError):
        LoggerSinkDto.parse_obj({
            "name": "",
        })


def test_logger_sink_dto_invalid_type():
    with pytest.raises(ValueError):
        LoggerSinkDto.parse_obj({
            "type": SinkType.MQTT,
        })


def test_config_dto_valid():
    ConfigDto.parse_obj({})

    meter_dto = MeterDto.parse_obj({
        "type": MeterType.LGE450,
        "port": "/dev/port",
    })

    ConfigDto.parse_obj({
        "log_level": "info ",
    })

    ConfigDto.parse_obj({
        "log_level": "INFO",
        "meters": [
            meter_dto
        ],
        "mqtt_sink": MqttSinkDto(host="localhost"),
        "logger_sink": LoggerSinkDto()
    })


def test_config_dto_invalid_logger_level():
    with pytest.raises(ValueError):
        ConfigDto.parse_obj({
            "log_level": "INEXISTENT_LEVEL",
        })


def test_credentials_dto_valid():
    CredentialsDto(password="1234567890")
    cred = CredentialsDto(password=" 1234abcd")

    assert cred.password == "1234abcd"


def test_credentials_dto_invalid_pwd():
    with pytest.raises(ValueError):
        CredentialsDto()

    with pytest.raises(ValueError):
        CredentialsDto(password="")

    with pytest.raises(ValueError):
        CredentialsDto(password=" ")

    with pytest.raises(ValueError):
        CredentialsDto(password="1234567")

    with pytest.raises(ValueError):
        CredentialsDto(password="1234554321123455432112345543211")
