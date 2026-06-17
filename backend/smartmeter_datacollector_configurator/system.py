import asyncio
import logging
import subprocess
from typing import List

LOGGER = logging.getLogger("uvicorn.error")

SYSCTL_BIN = "/bin/systemctl"
LS_BIN = "/bin/ls"

DATACOL_SERVICE = "smartmeter-datacollector"

# Demo services
BROKER_SERVICE = "mosquitto"
TELEGRAF_SERVICE = "telegraf"
INFLUX_SERVICE = "influxdb"
GRAFANA_SERVICE = "grafana-server"


class NoPermissionError(Exception):
    pass


class NotInstalledError(Exception):
    pass


class GeneralSystemError(Exception):
    pass


async def restart_datacollector() -> None:
    proc = await asyncio.create_subprocess_exec(
        SYSCTL_BIN,
        "restart",
        DATACOL_SERVICE)

    return_code = await proc.wait()
    _check_for_error(return_code, DATACOL_SERVICE)
    LOGGER.info("%s successfully restarted.", DATACOL_SERVICE)


async def get_installed_demo_services() -> List[str]:
    demo_services = [
        GRAFANA_SERVICE,
        TELEGRAF_SERVICE,
        INFLUX_SERVICE,
        BROKER_SERVICE
    ]
    installed = []
    for service in demo_services:
        proc = await asyncio.create_subprocess_exec(
            SYSCTL_BIN,
            "list-unit-files",
            f"{service}.service",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL)
        await proc.wait()
        stdout, _ = await proc.communicate() if proc.stdout else (b"", None)
        if proc.returncode == 0 and service in (stdout.decode() if isinstance(stdout, bytes) else ""):
            installed.append(service)
    return installed


_DEMO_RESTART_TASK_NAME = "restart_demo"


async def trigger_demo_restart(services_to_restart: List[str]) -> bool:
    all_running_task_names = {t.get_name() for t in asyncio.all_tasks() if not t.done()}
    if _DEMO_RESTART_TASK_NAME in all_running_task_names:
        LOGGER.warning("Demo restart already in progress.")
        return False

    asyncio.create_task(restart_demo(services_to_restart), name=_DEMO_RESTART_TASK_NAME)
    return True


async def restart_demo(services_to_restart: List[str]):
    # Stop all demo services
    for service in services_to_restart:
        LOGGER.info("Restarting demo services. Stopping %s...", service)
        proc = await asyncio.create_subprocess_exec(
            SYSCTL_BIN,
            "stop",
            service)

        return_code = await proc.wait()
        _check_for_error(return_code, service)
        LOGGER.info("%s successfully stopped.", service)

    services_to_restart.reverse()
    # Start all demo services in other direction
    for service in services_to_restart:
        LOGGER.info("Restarting demo services. Starting %s...", service)
        proc = await asyncio.create_subprocess_exec(
            SYSCTL_BIN,
            "start",
            service)

        return_code = await proc.wait()
        try:
            _check_for_error(return_code, service)
        except (GeneralSystemError, NoPermissionError, NotInstalledError) as _:
            # try to start other services even if one fails, but log the error
            continue
        LOGGER.info("%s successfully started.", service)


def retrieve_tty_devices() -> List[str]:
    cmd = f"{LS_BIN} /dev/serial/by-id/*"
    try:
        output = subprocess.run(cmd, shell=True, text=True, capture_output=True, check=True)
    except subprocess.CalledProcessError as ex:
        LOGGER.error("Unable to get tty devices. (%s)", ex)
        return []
    return output.stdout.rsplit()


def _check_for_error(return_code: int, service: str) -> None:
    if return_code == 4:
        LOGGER.error("Insufficient system privileges.")
        raise NoPermissionError("Insufficient system privileges to restart service.")
    if return_code == 5:
        LOGGER.error("%s is not installed.", service)
        raise NotInstalledError(f"{service} is not installed.")
    if return_code > 0:
        LOGGER.error("General error %s", service)
        raise GeneralSystemError(f"Return code: {return_code}")
