from configparser import ConfigParser, NoOptionError
from pathlib import Path
from typing import Any, Dict

import pytest

import smartmeter_datacollector_configurator.configurator as configurator
from smartmeter_datacollector_configurator.dto import ConfigDto, MeterDto, MeterType, MqttSinkDto


@pytest.fixture
def cfg_basic() -> Dict[str, Any]:
    return {
        "reader0": {
            "type": "lge450",
            "port": "/test/port",
        },
        "sink0": {
            "type": "mqtt",
            "host": "localhost",
        },
        "logging": {
            "default": "INFO",
        }
    }


@pytest.fixture
def cfg_tls(cfg_basic) -> Dict[str, Any]:
    cfg_basic["sink0"]["port"] = "8883"
    cfg_basic["sink0"]["tls"] = "True"
    cfg_basic["sink0"]["check_hostname"] = "True"
    return cfg_basic


@pytest.fixture
def cfg_with_ca(cfg_tls, tmp_path: Path) -> Dict[str, Any]:
    cfg_tls["sink0"]["check_hostname"] = False
    cfg_tls["sink0"]["ca_file_path"] = str(tmp_path / configurator.CA_FILE_NAME)
    return cfg_tls


def test_read_valid_config_from_file(cfg_basic: Dict[str, Any], tmp_path: Path):
    file_path = tmp_path / configurator.CONFIG_FILE_NAME
    parser = ConfigParser()
    parser.read_dict(cfg_basic)
    with open(file_path, 'w', encoding="utf-8") as file:
        parser.write(file, True)

    dto = configurator.retrieve_config(str(tmp_path))

    assert isinstance(dto, ConfigDto)
    assert len(dto.meters) == 1
    assert isinstance(dto.meters[0], MeterDto)
    assert dto.meters[0].type == MeterType.LGE450
    assert dto.meters[0].port == cfg_basic["reader0"]["port"]

    assert isinstance(dto.mqtt_sink, MqttSinkDto)
    assert dto.mqtt_sink.host == cfg_basic["sink0"]["host"]

    assert dto.log_level == cfg_basic["logging"]["default"]


def test_read_valid_tls_config_from_file(cfg_tls: Dict[str, Any], tmp_path: Path):
    file_path = tmp_path / configurator.CONFIG_FILE_NAME
    parser = ConfigParser()
    parser.read_dict(cfg_tls)
    with open(file_path, 'w', encoding="utf-8") as file:
        parser.write(file, True)

    dto = configurator.retrieve_config(str(tmp_path))

    assert isinstance(dto, ConfigDto)

    assert isinstance(dto.mqtt_sink, MqttSinkDto)
    assert dto.mqtt_sink.port == int(cfg_tls["sink0"]["port"])
    assert dto.mqtt_sink.tls == bool(cfg_tls["sink0"]["tls"])
    assert dto.mqtt_sink.check_hostname == bool(cfg_tls["sink0"]["check_hostname"])


def test_read_valid_config_with_ca_cert_from_file(cfg_with_ca: Dict[str, Any], tmp_path: Path):
    file_path = tmp_path / configurator.CONFIG_FILE_NAME
    ca_file_path = tmp_path / configurator.CA_FILE_NAME
    parser = ConfigParser()
    parser.read_dict(cfg_with_ca)
    with open(file_path, 'w', encoding="utf-8") as file:
        parser.write(file, True)
    TEST_CA = "123456789123456789ABCDEF"
    ca_file_path.write_text(TEST_CA, encoding='utf-8')

    dto = configurator.retrieve_config(str(tmp_path))

    assert isinstance(dto.mqtt_sink, MqttSinkDto)
    assert dto.mqtt_sink.check_hostname == bool(cfg_with_ca["sink0"]["check_hostname"])
    assert dto.mqtt_sink.ca_cert == TEST_CA


def test_retrieve_empty_config_if_file_not_found():
    dto = configurator.retrieve_config("/inextistent/path/")

    assert not dto.meters
    assert not dto.mqtt_sink
    assert not dto.logger_sink
    assert dto.log_level == "WARNING"


def test_retrieve_config_ignore_inexistent_ca_cert(cfg_with_ca: Dict[str, Any], tmp_path: Path):
    file_path = tmp_path / configurator.CONFIG_FILE_NAME
    parser = ConfigParser()
    parser.read_dict(cfg_with_ca)
    with open(file_path, 'w', encoding="utf-8") as file:
        parser.write(file, True)

    dto = configurator.retrieve_config(str(tmp_path))

    assert isinstance(dto.mqtt_sink, MqttSinkDto)
    assert dto.mqtt_sink.ca_cert == None


def test_write_config_to_file(cfg_tls: Dict[str, Any], tmp_path: Path):
    file_path = tmp_path / configurator.CONFIG_FILE_NAME

    dto = ConfigDto.parse_obj({
        "meters": [
            MeterDto.parse_obj(cfg_tls["reader0"])
        ],
        "mqtt_sink": MqttSinkDto.parse_obj(cfg_tls["sink0"]),
        "log_level": cfg_tls["logging"]["default"]
    })

    configurator.write_config_from_dto(str(tmp_path), dto)

    parser = ConfigParser()
    assert parser.read(file_path)[0] == str(file_path)

    assert parser.has_section("reader0")
    meter = parser["reader0"]
    assert meter["type"] == cfg_tls["reader0"]["type"]
    assert meter["port"] == cfg_tls["reader0"]["port"]
    assert meter.get("key") == None

    assert parser.has_section("sink0")
    sink = parser["sink0"]
    assert sink["type"] == cfg_tls["sink0"]["type"]
    assert sink["tls"] == cfg_tls["sink0"]["tls"]
    assert sink.get("ca_file_path") == None


def test_write_config_with_ca_cert_to_file(cfg_with_ca: Dict[str, Any], tmp_path: Path):
    file_path = tmp_path / configurator.CONFIG_FILE_NAME
    ca_file_path = tmp_path / configurator.CA_FILE_NAME
    TEST_CA = "123456789123456789ABCDEF"

    dto = ConfigDto.parse_obj({
        "mqtt_sink": MqttSinkDto.parse_obj({
            "host": cfg_with_ca['sink0']["host"],
            "tls": True,
            "ca_cert": TEST_CA,
        }),
    })

    configurator.write_config_from_dto(str(tmp_path), dto)

    parser = ConfigParser()
    parser.read(file_path)

    with pytest.raises(NoOptionError):
        parser.get("sink0", "ca_cert")

    assert parser.get("sink0", "ca_file_path") == str(tmp_path / configurator.CA_FILE_NAME)

    assert ca_file_path.read_text(encoding='utf-8') == TEST_CA
