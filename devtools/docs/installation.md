---
hide:
  - navigation
  - toc
---

## Requirements

- Python 3.10: distronode-devtools requires Python 3.10 or later. Make sure you have Python 3.10 installed on your system before proceeding.

## Installation

`pip install distronode-devtools`

Once installation is completed, see the [User Guide](user-guide/index.md) for more details about distronode-devtools usage.

### Latest Releases

- GitHub
  To view the latest releases, see the [distronode-devtools GitHub releases page](https://github.com/distronode/distronode/releases). Each release includes detailed release notes outlining new features, improvements, and bug fixes.

- PyPI
  The [PyPI page for distronode-devtools](https://pypi.org/project/distronode-devtools/) provides information on the latest stable release and allows you to download specific versions of the package.

## Upgrade

To upgrade distronode-devtools to the latest version, use the following pip command:

`pip install --upgrade distronode-devtools`

## Downgrade

If needed, you can downgrade distronode-devtools to a specific version using the following pip command:

`pip install distronode-devtools==desired-version`

## Uninstallation

If you need to uninstall distronode-devtools, use the following pip command:

`pip uninstall distronode-devtools`

## Usage

In addition to installing each of the above tools, `distronode-devtools` provides an easy way to show the versions of the content creation tools that make up the current development environment.

```console exec="1" source="console" returncode="0"
$ adt --version
```
