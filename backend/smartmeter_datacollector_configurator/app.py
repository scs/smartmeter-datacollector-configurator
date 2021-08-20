import logging

from pydantic.error_wrappers import ValidationError
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from . import configurator
from .authentication import BasicAuthBackend, SetPasswordError, auth_manager
from .dto import ConfigDto, CredentialsDto

DEFAULT_STATIC_DIR_PATH = "./static"
DEFAULT_CONFIG_PATH = "./config.ini"
LOGGER = logging.getLogger("uvicorn.error")


# Endpoints
class Configuration(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request):
        dto = configurator.retrieve_config(DEFAULT_CONFIG_PATH)
        return JSONResponse(dto.json())

    @requires("authenticated")
    async def post(self, request: Request):
        try:
            config = ConfigDto.parse_obj(await request.json())
        except ValidationError as e:
            LOGGER.warning("Validation failure: '%s'", e)
            raise HTTPException(status_code=400, detail="Validation of configuration failed.")
        try:
            configurator.write_config_from_dto(DEFAULT_CONFIG_PATH, config)
        except configurator.ConfigWriteError as e:
            LOGGER.warning("Config write failed: '%s'", e)
            raise HTTPException(status_code=500, detail="Failed to write configuration.")

        LOGGER.info("Configuration updated.")
        LOGGER.debug("Config: %s", config)
        return PlainTextResponse()


@requires("authenticated")
async def restart(request):
    return PlainTextResponse()


@requires("authenticated")
async def set_credentials(request: Request):
    try:
        new_password = (await request.body()).decode("utf-8")
        credential_dto = CredentialsDto(password=new_password)
    except (UnicodeDecodeError, ValidationError) as e:
        LOGGER.warning("Credential validation error: %s", e)
        raise HTTPException(status_code=400, detail="New credentials are invalid.")
    try:
        auth_manager.set_new_credentials(credential_dto)
    except SetPasswordError as e:
        LOGGER.warning("Credential write error: '%s'", e)
        raise HTTPException(status_code=500, detail="Failed to write new credentials.")
    LOGGER.debug("New credentials are successfully set.")
    return PlainTextResponse()


routes = [
    Route('/api/config', Configuration, methods=['GET', 'POST']),
    Route('/api/restart', restart, methods=['POST']),
    Route('/api/credentials', set_credentials, methods=['POST']),
    Mount('/', app=StaticFiles(directory=DEFAULT_STATIC_DIR_PATH, html=True))
]

middleware = [
    Middleware(CORSMiddleware,
               allow_origins=['*'],
               allow_headers=["Authorization"],
               allow_methods=["GET", "POST"]),
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = Starlette(debug=True, routes=routes, middleware=middleware)
