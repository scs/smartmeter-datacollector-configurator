import logging

import uvicorn
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

import configurator


DEFAULT_STATIC_DIR_PATH = "../frontend/dist"
DEFAULT_CONFIG_PATH = "./config.ini"

logging.basicConfig(level=logging.DEBUG)


# Endpoints

class Configuration(HTTPEndpoint):
    async def get(self, request):
        return JSONResponse(configurator.retrieve_config(DEFAULT_CONFIG_PATH))

    async def post(self, request: Request):
        config = await request.json()
        # TODO validate
        configurator.set_config(DEFAULT_CONFIG_PATH, config)
        return Response()


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

app = Starlette(debug=True, routes=routes)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="debug")
