import unittest.mock
from pathlib import Path

import pytest

from smartmeter_datacollector_configurator.authentication import AuthManager, SetPasswordError
from smartmeter_datacollector_configurator.dto import CredentialsDto


def test_auth_check_credentials(tmp_path: Path):
    manager = AuthManager(str(tmp_path))

    # password file must have been created
    pwd_file = tmp_path / AuthManager.PWD_FILE_NAME
    assert pwd_file.is_file()

    assert manager.check_credentials(AuthManager.USERNAME, AuthManager.DEFAULT_PASSWORD)
    assert not manager.check_credentials(AuthManager.USERNAME, "incorrect_pw")
    assert not manager.check_credentials("invalid_username", AuthManager.DEFAULT_PASSWORD)
    assert not manager.check_credentials("invalid_username", "invalid_password")


def test_auth_set_credentials(tmp_path: Path):
    manager = AuthManager(str(tmp_path))
    pwd_file = tmp_path / AuthManager.PWD_FILE_NAME

    assert pwd_file.read_text(encoding='utf-8') == AuthManager.DEFAULT_PASSWORD

    NEW_PWD = "new_password"
    cred_dto = CredentialsDto(password=NEW_PWD)
    manager.set_new_credentials(cred_dto)

    assert pwd_file.read_text(encoding='utf-8') == NEW_PWD

    assert not manager.check_credentials(AuthManager.USERNAME, AuthManager.DEFAULT_PASSWORD)
    assert manager.check_credentials(AuthManager.USERNAME, NEW_PWD)


def test_auth_raise_error_if_unable_to_write():
    with unittest.mock.patch('smartmeter_datacollector_configurator.authentication.open') as open_mock:
        open_mock.side_effect = OSError()
        with pytest.raises(SetPasswordError):
            manager = AuthManager("/some/path")
