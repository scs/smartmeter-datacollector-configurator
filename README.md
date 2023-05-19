# Smart Meter Data Collector Configurator

<p align="center">
    <a href="LICENSE"><img alt="License: BSD-3-Clause" src="https://img.shields.io/badge/license-3--clause%20BSD-green"></a> <a href="https://github.com/scs/smartmeter-datacollector-configurator/pulls"><img alt="Pull Requests Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a> <a href="https://github.com/scs/smartmeter-datacollector-configurator/pulls"><img alt="Contributions Welcome" src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg"></a>
    <br />
    <img alt="Backend Python Code Checks" src="https://github.com/scs/smartmeter-datacollector-configurator/actions/workflows/backend-code-checks.yml/badge.svg?branch=master"> <img alt="Frontend Code Checks" src="https://github.com/scs/smartmeter-datacollector-configurator/actions/workflows/frontend-code-checks.yml/badge.svg?branch=master"> <a href="https://pypi.org/project/smartmeter-datacollector-configurator/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/smartmeter-datacollector-configurator"></a>
</p>

---

The `smartmeter-datacollector-configurator` is a web application to simplify the process of generating a valid initial configuration for `smartmeter-datacollector`.

It supports
* a graphical approach to manage the configuration
* input validation to avoid invalid configurations
* loading / saving / discarding a configuration
* restarting `smartmeter-datacollector` (only if installed as a Debian package)
* restarting the [demo](https://github.com/scs/smartmeter-datacollector/wiki/Demo-(Raspberry-Pi-Image)) applications which comes with the custom [Raspberry Pi Image](https://github.com/scs/smartmeter-datacollector-pi-gen)

You find further documentation about the configuration options at [Wiki - Configuration](https://github.com/scs/smartmeter-datacollector/wiki/smartmeter-datacollector-configurator) and about running the installed package at [Wiki - How to Use](https://github.com/scs/smartmeter-datacollector/wiki/How-to-use#smart-meter-data-collector-configurator-application).

The web application consists of a backend and frontend combined in this repository. See the READMEs in the respective subdirectory.
