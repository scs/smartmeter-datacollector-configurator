import argparse
import logging
import os

import uvicorn
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
from starlette.types import ASGIApp

from . import configurator, system
from .authentication import AuthManager, BasicAuthBackend, SetPasswordError
from .dto import ConfigDto, CredentialsDto

LOGGER = logging.getLogger("uvicorn.error")


# Endpoints
class Configuration(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request):
        dto = configurator.retrieve_config(request.app.state.config_path)
        return JSONResponse(dto.json())

    @requires("authenticated")
    async def post(self, request: Request):
        try:
            config = ConfigDto.parse_obj(await request.json())
        except ValidationError as e:
            LOGGER.warning("Validation failure: '%s'", e)
            raise HTTPException(status_code=400, detail="Validation of configuration failed.")
        try:
            configurator.write_config_from_dto(request.app.state.config_path, config)
        except configurator.ConfigWriteError as e:
            LOGGER.warning("Config write failed: '%s'", e)
            raise HTTPException(status_code=500, detail="Failed to write configuration.")

        LOGGER.info("Configuration updated.")
        LOGGER.debug("Config: %s", config)
        return PlainTextResponse()


@requires("authenticated")
async def restart_datacollector(request):
    try:
        await system.restart_datacollector()
    except (system.NoPermissionError, system.NotInstalledError, system.SystemError) as e:
        raise HTTPException(status_code=503, detail=str(e))
    return PlainTextResponse()


@requires("authenticated")
async def restart_demo(request):
    try:
        not_installed_services = await system.restart_demo()
    except (system.NoPermissionError, system.SystemError) as e:
        raise HTTPException(status_code=503, detail=str(e))
    if len(not_installed_services) > 0:
        raise HTTPException(status_code=503, detail=f"{str(not_installed_services)} are not installed.")
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
        request.app.state.auth_manager.set_new_credentials(credential_dto)
    except SetPasswordError as e:
        LOGGER.warning("Credential write error: '%s'", e)
        raise HTTPException(status_code=500, detail="Failed to write new credentials.")
    LOGGER.debug("New credentials are successfully set.")
    return PlainTextResponse()


async def get_tty_devices(request):
    devices = system.retrieve_tty_devices()
    return JSONResponse(devices)


def build_routes(static_file_path: str):
    return [
        Route('/api/config', Configuration, methods=['GET', 'POST']),
        Route('/api/restart', restart_datacollector, methods=['POST']),
        Route('/api/restart-demo', restart_demo, methods=['POST']),
        Route('/api/credentials', set_credentials, methods=['POST']),
        Route('/api/ttydevices', get_tty_devices, methods=['GET']),
        Mount('/', app=StaticFiles(directory=static_file_path, html=True))
    ]


def build_middleware():
    return [
        Middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_headers=["Authorization"],
                   allow_methods=["GET", "POST"]),
        Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
    ]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Smartmeter Datacollector Configurator Backend", add_help=True)
    parser.add_argument(
        '-c', '--config', help="Directory path where config files should be deployed.", default=".")
    parser.add_argument(
        '-s', '--static', help="Director path with the static files.", default="./static")
    parser.add_argument(
        '--host', help="Host IP, default: 127.0.0.1", default="127.0.0.1")
    parser.add_argument(
        '--port', help="Port, default: 8000", type=int, default=8000)
    parser.add_argument(
        '-d', '--dev', help="Development mode: debug log, reloading", action='store_true')
    return parser.parse_args()


def web_app() -> ASGIApp:
    args = parse_arguments()
    static_path = os.path.normpath(args.static)
    config_path = os.path.normpath(args.config)

    web_app = Starlette(
        debug=True if args.dev else False,
        routes=build_routes(static_path),
        middleware=build_middleware())

    web_app.state.config_path = config_path
    web_app.state.auth_manager = AuthManager(config_path)
    return web_app


def main():
    args = parse_arguments()
    debug_mode = True if args.dev else False
    logger_level = "debug" if args.dev else "info"

    uvicorn.run("smartmeter_datacollector_configurator.app:web_app",
                host=args.host,
                port=args.port,
                log_level=logger_level,
                reload=debug_mode,
                factory=True)
