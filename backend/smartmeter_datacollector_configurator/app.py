import logging

from pydantic.error_wrappers import ValidationError
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from . import configurator
from .dto import ConfigDto

DEFAULT_STATIC_DIR_PATH = "./static"
DEFAULT_CONFIG_PATH = "./config.ini"

logging.basicConfig(level=logging.DEBUG)


# Endpoints

class Configuration(HTTPEndpoint):
    async def get(self, request):
        dto = configurator.retrieve_config(DEFAULT_CONFIG_PATH)
        return JSONResponse(dto.json())

    async def post(self, request: Request):
        try:
            config = ConfigDto.parse_obj(await request.json())
        except ValidationError as e:
            logging.error(e)
            raise HTTPException(status_code=400, detail=str(e))
        print(config)
        try:
            configurator.write_config_from_dto(DEFAULT_CONFIG_PATH, config)
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=400, detail=str(e))

        return Response("ok", media_type="text/plain")


async def restart(request):
    return PlainTextResponse()


async def set_credentials(request):
    return PlainTextResponse()


routes = [
    Route('/api/config', Configuration, methods=['GET', 'POST']),
    Route('/api/restart', restart, methods=['POST']),
    Route('/api/set-credentials', set_credentials, methods=['POST']),
    Mount('/', app=StaticFiles(directory=DEFAULT_STATIC_DIR_PATH, html=True))
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app = Starlette(debug=True, routes=routes, middleware=middleware)
