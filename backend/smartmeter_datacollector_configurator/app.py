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
from .authentication import BasicAuthBackend
from .dto import ConfigDto

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
            LOGGER.debug("Config updated: %s", config)
        except ValidationError as e:
            LOGGER.warning("Validation failure: '%s'", e)
            raise HTTPException(status_code=400, detail=str(e))
        try:
            configurator.write_config_from_dto(DEFAULT_CONFIG_PATH, config)
        except configurator.ConfigWriteError as e:
            LOGGER.warning("Config write failed: '%s'", e)
            raise HTTPException(status_code=400, detail=str(e))

        return PlainTextResponse()


@requires("authenticated")
async def restart(request):
    return PlainTextResponse()


@requires("authenticated")
async def set_credentials(request):
    return PlainTextResponse()


routes = [
    Route('/api/config', Configuration, methods=['GET', 'POST']),
    Route('/api/restart', restart, methods=['POST']),
    Route('/api/set-credentials', set_credentials, methods=['POST']),
    Mount('/', app=StaticFiles(directory=DEFAULT_STATIC_DIR_PATH, html=True))
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_headers=["Authorization"]),
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = Starlette(debug=True, routes=routes, middleware=middleware)
