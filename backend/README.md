# Smart Meter Data Collector Configurator Backend

## Introduction

The backend is written with Python3 and bases on the following frameworks and libraries:
* [Uvicorn](https://www.uvicorn.org/): ASGI server implementation, using uvloop and httptools.
* [Starlette](https://www.starlette.io/): ASGI framework/toolkit
* [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management using Python type hinting.

For managing dependency packages and virtualenv [pipenv](https://pipenv.pypa.io/en/latest/) is used.

## Development

### Requirements

* Python >= 3.7
* [`pipenv`](https://pipenv.pypa.io/en/latest/)
* Optional software packages (Debian / Ubuntu)
  * python3-all
  * debhelper
  * dh-python
  * dh-systemd

### Project Setup

With
```
pipenv install --dev
```
a new `virtualenv` is set up and the listed (inclusive dev) dependencies in the Pipfile are installed.

```
pipenv shell
```
activates the created `virtualenv` and opens a shell inside.

You can also run a command directly with:
```
pipenv run <command>
```

### Running during development

Inside the `virtualenv` run:

```
python -m smartmeter-datacollector-configurator [-c <config_path>] [-s <static_path>] [-d]
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

`smartmeter-datacollector-configurator` offers a few custom `pipenv run` commands to simplify certain development workflows:
* `format_check` checks if the code follows the [`autopep8`](https://pypi.org/project/autopep8/) code formatting rules.
* `format` automatically adjusts the code to follow the `autopep8` code formatting rules.
* `isort_check` checks if the order of the import statements is correct using [`isort`](https://pycqa.github.io/isort/).
* `isort` automatically re-orders the import statements using `isort`.
* `lint_check` checks if the code follows the [`pylint`](https://pypi.org/project/pylint/) rules defined in `pyproject.toml`.
* `lint` automatically adjust the code to follow the `pylint` rules defined in `pyproject.toml`.
* `build` builds a Python package which can be uploaded to [`PyPI`](https://pypi.org/project/smartmeter-datacollector/) using `twine`.
* `build_check` uses `twine` to check if the built Python package will be accepted by `PiPI`.
* `setup_check` checks whether the dependencies defined in `Pipfile` / `Pipfile.lock` are in sync with `setup.py`.
* `setup` synchronizes the dependencies defined in `Pipfile` / `Pipfile.lock` with `setup.py`.
* `debianize` creates a `debian/` directory used to build Debian source / binary packages.
* `build_srcdeb` builds a Debian source package which can be used to build a Debian (binary) package for any platform (e.g. using [`pbuilder`](https://pbuilder-docs.readthedocs.io/en/latest/usage.html))
* `build_deb` builds a Debian package for the current development plattform.

Make sure to run `format_check` / `format`, `isort_check` / `isort`, `lint_check` / `lint`, `license`, `setup_check` / `setup` before committing changes to the repository to avoid unnecessary development cycles. `smartmeter-datacollector-configurator` uses [GitHub Actions](https://github.com/scs/smartmeter-datacollector-configurator/actions) to check if these rules apply. 

Visit [Wiki - Creating a Release](https://github.com/scs/smartmeter-datacollector/wiki/Creating-a-Release) for further documentation about contributing.
