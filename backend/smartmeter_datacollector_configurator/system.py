import asyncio
import logging
from typing import List

LOGGER = logging.getLogger("uvicorn.error")

SYSCTL_BIN = "/bin/systemctl"

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


class SystemError(Exception):
    pass


async def restart_datacollector() -> None:
    proc = await asyncio.create_subprocess_exec(
        SYSCTL_BIN,
        "restart",
        DATACOL_SERVICE)

    return_code = await proc.wait()
    _analyze_return_code(return_code, DATACOL_SERVICE)


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
            _analyze_return_code(return_code, service)
        except NotInstalledError:
            # continue if one of the services is not installed
            not_installed += service
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
            _analyze_return_code(return_code, service)
        except NotInstalledError:
            # continue if one of the services is not installed
            continue

    return not_installed


def _analyze_return_code(return_code: int, service: str) -> None:
    if return_code == 4:
        LOGGER.error("%s is not installed.", service)
        raise NotInstalledError(f"{service} is not installed.")
    elif return_code == 5:
        LOGGER.error("Insufficient system privileges.")
        raise NoPermissionError()
    elif return_code > 0:
        LOGGER.error("General error while restarting %s", service)
        raise SystemError("Return code: %i", return_code)

    LOGGER.info("%s successfully restarted.", service)
