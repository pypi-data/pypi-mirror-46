# OpenRegister

[![Package](https://img.shields.io/pypi/v/openregister.svg)](https://pypi.python.org/pypi/openregister/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openregister.svg)](https://pypi.python.org/pypi/openregister/)
[![Build](https://travis-ci.org/psd/openregister.svg?branch=master)](https://travis-ci.org/psd/openregister)
[![Coverage](https://coveralls.io/repos/github/psd/openregister/badge.svg?branch=master)](https://coveralls.io/github/psd/openregister?branch=master)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/psd/openregister/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)


*Publishing tools for GOV.UK style registers.*

A self-contained and easily installed [GOV.UK register product](https://www.gov.uk/government/publications/registers/registers) intended for use by devolved authorities and administrations.

## Installation

    pip3 install openregister

## Basic usage

    openregister serve /path/to/register.json

Runs a web server serving an index of registers on http://localhost:8088/

## Command options

    $ openregister --help

    Usage: openregister [OPTIONS] COMMAND [ARGS]...

      OpenRegister:  publishing tools for GOV.UK style registers.

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      serve*

## Server options

    $ openregister serve --help

    Usage: openregister serve [OPTIONS]

    Options:
      -h, --host TEXT      host for server, defaults to 127.0.0.1
      -r, --register TEXT  Serve a single register, otherwise serve all know
                           registers as a catalog
      -p, --port INTEGER   port for server, defaults to 8088
      -d, --debug          More verbose logging and automatically reload on
                           changes
      --help               Show this message and exit.

## Development

Development requires Python 3.5 or later, we recommend using a [virtual environment](https://docs.python.org/3/library/venv.html):

    make init
    make
    python -m openregister --help
