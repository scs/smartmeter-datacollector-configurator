import base64
import binascii
import logging

from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
from starlette.requests import HTTPConnection

from .dto import CredentialsDto

LOGGER = logging.getLogger("uvicorn.error")


class SetPasswordError(Exception):
    pass


class AuthManager:
    USERNAME = "admin"
    DEFAULT_PASSWORD = "smartmeter"
    PWD_FILE_NAME = "password.txt"

    def __init__(self, config_dir_path: str) -> None:
        self._password = self._read_pwd_file(f"{config_dir_path}/{self.PWD_FILE_NAME}")
        self._config_path = config_dir_path

    def check_credentials(self, username: str, password: str) -> bool:
        if username == self.USERNAME and password == self._password:
            LOGGER.debug("User %s successfully authenticated.", username)
            return True
        LOGGER.warning("User %s failed to authenticate.", username)
        return False

    def set_new_credentials(self, new_credentials: CredentialsDto) -> None:
        self._password = new_credentials.password
        self._write_pwd_file(self._password, f"{self._config_path}/{self.PWD_FILE_NAME}")

    @staticmethod
    def _read_pwd_file(file_path: str) -> str:
        try:
            with open(file_path, "r") as file:
                pwd = file.readline()
                if not pwd.strip():
                    raise ValueError("Password file is empty.")
                return pwd
        except (OSError, ValueError) as e:
            LOGGER.warning(f"Unable to read password file. '{e}' \n\tGenerating new file with default password.")
            AuthManager._write_pwd_file(AuthManager.DEFAULT_PASSWORD, file_path)
            return AuthManager.DEFAULT_PASSWORD

    @staticmethod
    def _write_pwd_file(password: str, file_path: str) -> None:
        try:
            with open(file_path, "w") as file:
                file.write(password.strip())
        except OSError as e:
            LOGGER.error(f"Unable to write password file. '{e}'")
            raise SetPasswordError(e) from e


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: HTTPConnection):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return
            decoded_credentials = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError('Invalid credentials.')

        username, _, password = decoded_credentials.partition(":")
        auth_manager: AuthManager = request.app.state.auth_manager

        if auth_manager.check_credentials(username, password):
            return AuthCredentials(["authenticated"]), SimpleUser(username)
        return None
