#!/usr/bin/env python

from os import path

from setuptools import find_packages, setup

from smartmeter_datacollector_configurator.__version__ import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smartmeter-datacollector-configurator",
    version=__version__,
    description="Smart Meter Data Collector Configurator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scs/smartmeter-datacollector-configurator",
    project_urls={
        "Source": "https://github.com/scs/smartmeter-datacollector-configurator",
        "Bug Reports": "https://github.com/scs/smartmeter-datacollector-configurator/issues",
        "Pull Requests": "https://github.com/scs/smartmeter-datacollector-configurator/pulls",
        "SCS": "https://www.scs.ch",
    },
    author="Supercomputing Systems AG",
    author_email="info@scs.ch",
    maintainer="Supercomputing Systems AG",
    maintainer_email="info@scs.ch",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
    license="BSD",
    python_requires=">=3.8",
    packages=find_packages(
        exclude=["contrib", "doc", "scripts", "static", "tests", "tests."]
    ),
    include_package_data=True,
    install_requires=[
        "anyio==4.3.0; python_version >= '3.8'",
        "click==8.1.7; python_version >= '3.7'",
        "exceptiongroup==1.2.0; python_version < '3.11'",
        "h11==0.14.0; python_version >= '3.7'",
        "idna==3.6; python_version >= '3.5'",
        'pydantic==1.10.14',
        "sniffio==1.3.1; python_version >= '3.7'",
        'starlette==0.37.2',
        "typing-extensions==4.10.0; python_version >= '3.8'",
        'uvicorn==0.29.0'
    ],
    scripts=["bin/smartmeter-datacollector-configurator"],
    zip_safe=True,
    dependency_links=[],
)
