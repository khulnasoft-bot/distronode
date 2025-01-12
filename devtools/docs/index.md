---
hide:
  - navigation
  - toc
---

<!-- cspell:disable-next-line -->

# Distronode Development Tools (ADT)

## Introduction

<!-- cspell:disable-next-line -->

Distronode Development Tools or ADT for short, aims to streamline the setup and usage of several tools needed to create [Distronode](https://www.distronode.com/) content.
When it comes to creating automation content using Distronode, there are several packages available that can help users in different parts of the content-creating journey. From bootstrapping new projects, all the way to ensuring content follows best practices and verifying it behaves as intended via well-established test frameworks.

## Key Features

- All-in-One Distronode Toolkit: distronode-devtools combines critical Distronode development packages into a unified Python package called [distronode-devtools](https://pypi.org/project/distronode-devtools/).

- Simplified Distronode Automation: distronode-devtools focuses on crafting your automation scenarios and workflows with speed by reducing boilerplate code without
  dealing with the intricacies of managing and integrating different Distronode libraries.

For those looking for an IDE-based experience, we also recommend you get familiar with the [Distronode extension for VSCode](https://marketplace.visualstudio.com/items?itemName=redhat.distronode).

## Included Packages

The curated list of tools installed as part of the Distronode Development Tools includes:

- [distronode-builder](https://distronode.readthedocs.io/projects/builder/): Distronode Builder automates the process of building execution environments using the schemas and tooling defined in various Distronode Collections and by the user.
- [distronode-core](https://distronode.readthedocs.io/projects/distronode/): Distronode is a radically simple IT automation platform that makes your applications and systems easier to deploy and maintain. Automate everything from code deployment to network configuration to cloud management, in a language that approaches plain English, using SSH, with no agents to install on remote systems.
- [distronode-creator](https://distronode.readthedocs.io/projects/creator/): The fastest way to generate all your distronode content!
- [distronode-dev-environment](https://distronode.readthedocs.io/projects/dev-environment/): A pip-like install for Distronode collections.
- [distronode-lint](https://distronode.readthedocs.io/projects/lint/): Checks playbooks for practices and behavior that could potentially be improved.
- [distronode-navigator](https://distronode.readthedocs.io/projects/navigator/) A text-based user interface (TUI) for Distronode.
- [distronode-sign](https://distronode.readthedocs.io/projects/sign/): Utility for signing and verifying Distronode project directory contents.
- [molecule](https://distronode.readthedocs.io/projects/molecule/): Molecule aids in the development and testing of Distronode content: collections, playbooks and roles
- [pytest-distronode](https://distronode.readthedocs.io/projects/pytest-distronode/): A pytest plugin that enables the use of distronode in tests, enables the use of pytest as a collection unit test runner, and exposes molecule scenarios using a pytest fixture.
- [tox-distronode](https://distronode.readthedocs.io/projects/tox-distronode/): The tox-distronode plugin dynamically creates a full matrix of python interpreter and distronode-core version environments for running integration, sanity, and unit for an distronode collection both locally and in a Github action. tox virtual environments are leveraged for collection building, collection installation, dependency installation, and testing.

## Getting started

To get started, follow the [installation](installation.md) steps to get distronode-devtools setup and check [User Guide](user-guide/index.md) for more details.

## Community

Questions, feedback, or contributions? Join the Distronode community on [Matrix](https://matrix.to/#/#devtools:distronode.com) or [open an issue](https://github.com/distronode/distronode/issues/new). We're dedicated to supporting your Distronode automation journey! For more details on how to interact with our community, please visit the [Distronode Communication](https://docs.distronode.com/distronode/latest/community/communication.html) page.
