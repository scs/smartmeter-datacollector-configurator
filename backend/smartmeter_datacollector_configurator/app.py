import argparse
import logging
import os

import pkg_resources
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

STATIC_DIR = 'static'

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
        except ValidationError as ex:
            LOGGER.warning("Validation failure: '%s'", ex)
            raise HTTPException(status_code=400, detail="Validation of configuration failed.") from ex
        try:
            configurator.write_config_from_dto(request.app.state.config_path, config)
        except configurator.ConfigWriteError as ex:
            LOGGER.warning("Config write failed: '%s'", ex)
            raise HTTPException(status_code=500, detail="Failed to write configuration.") from ex

        LOGGER.info("Configuration updated.")
        LOGGER.debug("Config: %s", config)
        return PlainTextResponse()


@requires("authenticated")
async def restart_datacollector(request):
    # pylint: disable=unused-argument
    try:
        await system.restart_datacollector()
    except (system.NoPermissionError, system.NotInstalledError, system.GeneralSystemError) as ex:
        raise HTTPException(status_code=503, detail=str(ex)) from ex
    return PlainTextResponse()


@requires("authenticated")
async def restart_demo(request):
    # pylint: disable=unused-argument
    try:
        not_installed_services = await system.restart_demo()
    except (system.NoPermissionError, system.GeneralSystemError) as ex:
        raise HTTPException(status_code=503, detail=str(ex)) from ex
    if len(not_installed_services) > 0:
        raise HTTPException(status_code=503, detail=f"{str(not_installed_services)} are not installed.")
    return PlainTextResponse()


@requires("authenticated")
async def set_credentials(request: Request):
    try:
        new_password = (await request.body()).decode("utf-8")
        credential_dto = CredentialsDto(password=new_password)
    except (UnicodeDecodeError, ValidationError) as ex:
        LOGGER.warning("Credential validation error: %s", ex)
        raise HTTPException(status_code=400, detail="New credentials are invalid.") from ex
    try:
        request.app.state.auth_manager.set_new_credentials(credential_dto)
    except SetPasswordError as ex:
        LOGGER.warning("Credential write error: '%s'", ex)
        raise HTTPException(status_code=500, detail="Failed to write new credentials.") from ex
    LOGGER.debug("New credentials are successfully set.")
    return PlainTextResponse()


async def get_tty_devices(request):
    # pylint: disable=unused-argument
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
        '-s', '--static', help="Director path with the static files.", default="")
    parser.add_argument(
        '--host', help="Host IP, default: 127.0.0.1", default="127.0.0.1")
    parser.add_argument(
        '--port', help="Port, default: 8000", type=int, default=8000)
    parser.add_argument(
        '-d', '--dev', help="Development mode: debug log, reloading", action='store_true')
    return parser.parse_args()


def resolve_static(static_file_path: str) -> str:
    static_path = None
    if static_file_path:
        static_path = static_file_path
    else:
        # try to find a packaged resource
        if pkg_resources.resource_exists(__name__, STATIC_DIR):
            manager = pkg_resources.ResourceManager()
            provider = pkg_resources.get_provider(__name__)
            static_path = provider.get_resource_filename(manager, STATIC_DIR)

        if not static_path:
            # fallback to a local static directory
            static_path = STATIC_DIR

    static_path = os.path.normpath(static_path)
    LOGGER.info("Serving static files from %s.", static_path)

    return static_path


def web_app() -> ASGIApp:
    args = parse_arguments()
    static_path = resolve_static(args.static)
    config_path = os.path.normpath(args.config)

    app = Starlette(
        debug=bool(args.dev),
        routes=build_routes(static_path),
        middleware=build_middleware())

    app.state.config_path = config_path
    app.state.auth_manager = AuthManager(config_path)
    return app


def main():
    args = parse_arguments()
    debug_mode = bool(args.dev)
    logger_level = "debug" if args.dev else "info"

    uvicorn.run("smartmeter_datacollector_configurator.app:web_app",
                host=args.host,
                port=args.port,
                log_level=logger_level,
                reload=debug_mode,
                factory=True)
