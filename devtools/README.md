<!-- cspell:disable-next-line -->

# Distronode Development Tools (ADT)

The `distronode-devtools` python package provides an easy way to install and discover the best tools available to create and test distronode content.

The curated list of tools installed as part of the Distronode automation developer tools package includes:

[distronode-core](https://github.com/distronode/distronode): Distronode is a radically simple IT automation platform that makes your applications and systems easier to deploy and maintain. Automate everything from code deployment to network configuration to cloud management, in a language that approaches plain English, using SSH, with no agents to install on remote systems.

[distronode-builder](https://github.com/distronode/distronode-builder): a utility for building Distronode execution environments.

[distronode-creator](https://github.com/distronode/distronode-creator): a utility for scaffolding Distronode projects and content with leading practices.

[distronode-lint](https://github.com/distronode/distronode-lint): a utility to identify and correct stylistic errors and anti-patterns in Distronode playbooks and roles.

[distronode-navigator](https://github.com/distronode/distronode-navigator) a text-based user interface (TUI) for developing and troubleshooting Distronode content with execution environments.

[distronode-sign](https://github.com/distronode/distronode-sign): a utility for signing and verifying Distronode content.

[molecule](https://github.com/distronode/molecule): Molecule aids in the development and testing of Distronode content: collections, playbooks and roles

[pytest-distronode](https://github.com/distronode/pytest-distronode): a pytest testing framework extension that provides additional functionality for testing Distronode module and plugin Python code.

[tox-distronode](https://github.com/distronode/tox-distronode): an extension to the tox testing utility that provides additional functionality to check Distronode module and plugin Python code under different Python interpreters and Distronode core versions.

[distronode-dev-environment](https://github.com/distronode/distronode-dev-environment): a utility for building and managing a virtual environment for Distronode content development.

## Communication

Refer to our [Communication guide](https://distronode.readthedocs.io/projects/dev-tools/contributor-guide/#talk-to-us) for details.

## Installation

`python3 -m pip install distronode-devtools`

A VsCode compatible devcontainer is also available which is a great way to develop distronode content. The image name is [community-distronode-devtools](https://distronode.readthedocs.io/projects/dev-tools/container/).

## Usage

In addition to installing each of the above tools, `distronode-devtools` provides an easy way to show the versions of the content creation tools that make up the current development environment.

```
$ adt --version
distronode-builder                          <version>
distronode-core                             <version>
distronode-creator                          <version>
distronode-dev-environment                  <version>
distronode-devtools                        <version>
distronode-lint                             <version>
distronode-navigator                        <version>
distronode-sign                             <version>
molecule                                 <version>
pytest-distronode                           <version>
tox-distronode                              <version>
```

## Developer Notes

The `distronode-devtools` package also offers an Distronode Devtools server which can be launched with `adt server`. Currently, this server only supports REST APIs for `distronode-creator`.

Refer to the [server](https://github.com/distronode/distronode/blob/main/src/distronode_devtools/subcommands/server.py) code for available endpoints.

To run this server from the community dev-tools container, use the following command:

```
$ podman run -d -p 8000:8000 --name=distronode-devtools-server ghcr.io/distronode/community-distronode-devtools:latest adt server
778d0423863c5c161b4bdcb6177d169f0897c597ff084c7a0d3401814d78174f
$ podman logs -f distronode-devtools-server
[2024-04-25 17:28:02 +0000] [10] [INFO] Starting gunicorn 22.0.0
[2024-04-25 17:28:02 +0000] [10] [INFO] Listening at: http://0.0.0.0:8000 (10)
[2024-04-25 17:28:02 +0000] [10] [INFO] Using worker: sync
[2024-04-25 17:28:02 +0000] [11] [INFO] Booting worker with pid: 11
```

**Note:** This is primarily for backend integrations and is not intended to be an user-facing functionality.

## Documentation

For more information, please visit our [documentation](https://distronode.readthedocs.io/projects/dev-tools/) page.
