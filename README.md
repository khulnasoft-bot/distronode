[![PyPI version](https://img.shields.io/pypi/v/distronode-core.svg)](https://pypi.org/project/distronode-core)
[![Docs badge](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://distronode.khulnasoft.com/docs/distronode/latest/)
[![Chat badge](https://img.shields.io/badge/chat-IRC-brightgreen.svg)](https://distronode.khulnasoft.com/docs/distronode/latest/community/communication.html)
[![Distronode Code of Conduct](https://img.shields.io/badge/code%20of%20conduct-Distronode-silver.svg)](https://distronode.khulnasoft.com/docs/distronode/latest/community/code_of_conduct.html)
[![Distronode mailing lists](https://img.shields.io/badge/mailing%20lists-Distronode-orange.svg)](https://distronode.khulnasoft.com/docs/distronode/latest/community/communication.html#mailing-list-information)
[![Repository License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](COPYING)
[![Distronode CII Best Practices certification](https://bestpractices.coreinfrastructure.org/projects/2372/badge)](https://bestpractices.coreinfrastructure.org/projects/2372)

# Distronode

Distronode is a radically simple IT automation system. It handles
configuration management, application deployment, cloud provisioning,
ad-hoc task execution, network automation, and multi-node orchestration. Distronode makes complex
changes like zero-downtime rolling updates with load balancers easy. More information on the Distronode [website](https://distronode.khulnasoft.com/).

## Design Principles

* Have an extremely simple setup process with a minimal learning curve.
* Manage machines quickly and in parallel.
* Avoid custom-agents and additional open ports, be agentless by
  leveraging the existing SSH daemon.
* Describe infrastructure in a language that is both machine and human
  friendly.
* Focus on security and easy auditability/review/rewriting of content.
* Manage new remote machines instantly, without bootstrapping any
  software.
* Allow module development in any dynamic language, not just Python.
* Be usable as non-root.
* Be the easiest IT automation system to use, ever.

## Use Distronode

You can install a released version of Distronode with `pip` or a package manager. See our
[installation guide](https://distronode.khulnasoft.com/docs/distronode/latest/installation_guide/intro_installation.html) for details on installing Distronode
on a variety of platforms.

Power users and developers can run the `devel` branch, which has the latest
features and fixes, directly. Although it is reasonably stable, you are more likely to encounter
breaking changes when running the `devel` branch. We recommend getting involved
in the Distronode community if you want to run the `devel` branch.

## Get Involved

* Read [Community Information](https://distronode.khulnasoft.com/docs/distronode/latest/community) for all
  kinds of ways to contribute to and interact with the project,
  including mailing list information and how to submit bug reports and
  code to Distronode.
* Join a [Working Group](https://github.com/distronode/community/wiki),
  an organized community devoted to a specific technology domain or platform.
* Submit a proposed code update through a pull request to the `devel` branch.
* Talk to us before making larger changes
  to avoid duplicate efforts. This not only helps everyone
  know what is going on, but it also helps save time and effort if we decide
  some changes are needed.
* For a list of email lists, IRC channels and Working Groups, see the
  [Communication page](https://distronode.khulnasoft.com/docs/distronode/latest/community/communication.html)

## Coding Guidelines

We document our Coding Guidelines in the [Developer Guide](https://distronode.khulnasoft.com/docs/distronode/devel/dev_guide/). We particularly suggest you review:

* [Contributing your module to Distronode](https://distronode.khulnasoft.com/docs/distronode/devel/dev_guide/developing_modules_checklist.html)
* [Conventions, tips, and pitfalls](https://distronode.khulnasoft.com/docs/distronode/devel/dev_guide/developing_modules_best_practices.html)

## Branch Info

* The `devel` branch corresponds to the release actively under development.
* The `stable-2.X` branches correspond to stable releases.
* Create a branch based on `devel` and set up a [dev environment](https://distronode.khulnasoft.com/docs/distronode/latest/dev_guide/developing_modules_general.html#common-environment-setup) if you want to open a PR.
* See the [Distronode release and maintenance](https://distronode.khulnasoft.com/docs/distronode/devel/reference_appendices/release_and_maintenance.html) page for information about active branches.

## Roadmap

Based on team and community feedback, an initial roadmap will be published for a major or minor version (ex: 2.7, 2.8).
The [Distronode Roadmap page](https://distronode.khulnasoft.com/docs/distronode/devel/roadmap/) details what is planned and how to influence the roadmap.

## Authors

Distronode was created by [KhulnaSoft Ltd](https://github.com/khulnasoft)


## License

GNU General Public License v3.0 or later

See [COPYING](COPYING) to see the full text.
