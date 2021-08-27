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


async def restart_demo() -> List[str]:
    demo_services = [
        GRAFANA_SERVICE,
        TELEGRAF_SERVICE,
        INFLUX_SERVICE,
        BROKER_SERVICE
    ]
    not_installed = []

    # Stop all demo services
    for service in demo_services:
        proc = await asyncio.create_subprocess_exec(
            SYSCTL_BIN,
            "stop",
            service)

        return_code = await proc.wait()
        try:
            _check_for_error(return_code, service)
        except NotInstalledError:
            # continue if one of the services is not installed
            not_installed.append(service)
            continue

    demo_services.reverse()
    # Start all demo services in other directions
    for service in demo_services:
        proc = await asyncio.create_subprocess_exec(
            SYSCTL_BIN,
            "start",
            service)

        return_code = await proc.wait()
        try:
            _check_for_error(return_code, service)
        except NotInstalledError:
            # continue if one of the services is not installed
            continue

    if len(not_installed) > 0:
        LOGGER.warning("Services %s not found.", not_installed)
    else:
        LOGGER.info("Demo services successfully restarted.")

    return not_installed


def retrieve_tty_devices() -> List[str]:
    cmd = f"{LS_BIN} /dev/ttyUSB*"
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
