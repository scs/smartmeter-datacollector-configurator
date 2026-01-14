# Smart Meter Data Collector Configurator Backend

## Introduction

The backend is written with Python3 and bases on the following frameworks and libraries:
* [Uvicorn](https://www.uvicorn.org/): ASGI server implementation, using uvloop and httptools.
* [Starlette](https://www.starlette.io/): ASGI framework/toolkit
* [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management using Python type hinting.

For managing dependency packages and virtualenv [poetry](https://python-poetry.org/) is used.

## Development

### Requirements

* Python >= 3.10, <= 3.14
* [`poetry`](https://python-poetry.org/)
* Optional software packages
  * debhelper
  * dh-make

### Project Setup

With
```
poetry install
```
This will install all runtime and development dependencies for `smartmeter-datacollector-configurator` in a new virtual environment. Now you are ready to start working on the project.

### Running during development

Inside the `virtualenv` run:

```
python -m smartmeter_datacollector_configurator [-c <config_path>] [-s <static_path>] [-d]
```

Now, the backend is running on port `8000` listening to `127.0.0.1`. With the option `-d` hot-reloading and debug logs are enabled.

For development purposes it is possible to create an empty `static` folder inside the `backend` directory and start the application without the `-s` option. At the same time you start the frontend (`npm run serve`) in a separate shell. The API calls of the frontend, during development, are directed to a local backend to port 8000.

### Command line arguments

The following command line arguments are supported:
* `-h, --help`: Shows the help output of `smartmeter-datacollector-configurator`.
* `-c, --config PATH`: Directory path where the configuration files are read and deployed (default: Current directory `./`).
* `-s,--static PATH`: Directory path where the static frontend files are located. If left empty the app check if a static directory exists in the package location and falls back to the current directory `./static`.
* `--host`: Listening host IP (default: `127.0.0.1`).
* `--port`: Listening port number (default: `8000`).
* `-d, --dev`: Enable development mode which provides debug logging and hot reloading.

### Custom commands & workflows

`smartmeter-datacollector-configurator` offers a few custom `poetry run poe` commands to simplify certain development workflows:
* `build_py` builds a Python package which can be uploaded to [`PyPI`](https://pypi.org/project/smartmeter-datacollector/)
* `build_shiv` builds a self-contained zipapp (`.pyz`) including dependencies (but without interpreter) using [`shiv`](https://shiv.readthedocs.io)
* `build_deb` builds a Debian package for the current development platform
* `build_srcdeb` builds a Debian source package which can be used to build a Debian (binary) package for any platform
* `clean` removes build output from the working directory
* `debianize` creates a `debian/` directory used to build Debian source / binary packages
* `format` automatically adjusts the code to follow the [`autopep8`](https://pypi.org/project/autopep8/) code formatting rules
* `format_check` checks if the code follows the `autopep8` code formatting rules
* `isort` automatically re-orders the import statements using `isort`
* `isort_check` checks if the order of the import statements is correct using [`isort`](https://pycqa.github.io/isort/)
* `lint` automatically adjust the code to follow the [`pylint`](https://pypi.org/project/pylint/) rules defined in `pyproject.toml`
* `lint_check` checks if the code follows the `pylint` rules defined in `pyproject.toml`
* `test` runs all unit tests using `pytest`

Make sure to run `format_check` / `format`, `isort_check` / `isort`, `lint_check` / `lint`before committing changes to the repository to avoid unnecessary development cycles. `smartmeter-datacollector-configurator` uses [GitHub Actions](https://github.com/scs/smartmeter-datacollector-configurator/actions) to check if these rules apply. 

Visit [Wiki - Creating a Release](https://github.com/scs/smartmeter-datacollector/wiki/Creating-a-Release) for further documentation about contributing.
