Table of Contents
=================

   * [Installing API](#installing-api)
      * [The API Operator](#the-api-operator)
   * [Installing the API CLI](#installing-the-api-cli)
      * [Building the CLI Documentation](#building-the-cli-documentation)


# Installing API

:warning: NOTE |
--- |
If you're installing an older release of API (prior to 18.0), these instructions have changed.  Take a look at your version specific instructions, e.g., for API 17.0.1, see: [https://github.com/distronode/distronode/tree/devel/api/blob/17.0.1/INSTALL.md](https://github.com/distronode/distronode/tree/devel/api/blob/17.0.1/INSTALL.md)
If you're attempting to migrate an older Docker-based API installation, see: [Migrating Data from Local Docker](https://github.com/distronode/distronode/tree/devel/api/blob/devel/tools/docker-compose/docs/data_migration.md) |

## The API Operator

Starting in version 18.0, the [API Operator](https://github.com/distronode/distronode/tree/devel/api-operator) is the preferred way to install API. Please refer to the [API Operator](https://github.com/distronode/distronode/tree/devel/api-operator) documentation.

API can also alternatively be installed and [run in Docker](./tools/docker-compose/README.md), but this install path is only recommended for development/test-oriented deployments, and has no official published release.

# Installing the API CLI

`api` is the official command-line client for API.  It:

* Uses naming and structure consistent with the API HTTP API
* Provides consistent output formats with optional machine-parsable formats
* To the extent possible, auto-detects API versions, available endpoints, and
  feature support across multiple versions of API.

Potential uses include:

* Configuring and launching jobs/playbooks
* Checking on the status and output of job runs
* Managing objects like organizations, users, teams, etc...

The preferred way to install the API CLI is through pip directly from PyPI:

    pip3 install apikit
    api --help

## Building the CLI Documentation

To build the docs, spin up a real API server, `pip3 install sphinx sphinxcontrib-autoprogram`, and run:

    ~ cd apikit/apikit/cli/docs
    ~ TOWER_HOST=https://api.example.org TOWER_USERNAME=example TOWER_PASSWORD=secret make clean html
    ~ cd build/html/ && python -m http.server
    Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ..
