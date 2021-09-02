#!/usr/bin/env python

from os import path

from setuptools import find_packages, setup

from smartmeter_datacollector_configurator.__version__ import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "../README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smartmeter-datacollector-configurator",
    version=__version__,
    description="Smart Meter Data Collector",
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
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
    ],
    license="BSD",
    python_requires=">=3.7",
    packages=find_packages(
        exclude=["contrib", "doc", "scripts", "static", "tests", "tests."]
    ),
    include_package_data=True,
    install_requires=[
        "anyio==3.3.0; python_full_version >= '3.6.2'",
        "asgiref==3.4.1; python_version >= '3.6'",
        "click==8.0.1; python_version >= '3.6'",
        "h11==0.12.0; python_version >= '3.6'",
        "idna==3.2; python_version >= '3.5'",
        "pydantic==1.8.2",
        "sniffio==1.2.0; python_version >= '3.5'",
        "starlette==0.16.0",
        "typing-extensions==3.10.0.0",
        "uvicorn==0.15.0",
    ],
    scripts=["bin/smartmeter-datacollector-configurator"],
    zip_safe=True,
    dependency_links=[],
)
