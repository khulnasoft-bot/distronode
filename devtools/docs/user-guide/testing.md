# Testing a user-facing role within a collection

## Molecule

To set up molecule, create a new directory in your collection called
extensions, and inside that directory, run `molecule init scenario` to create
the default scenario.

```shell
mkdir extensions
cd extensions
molecule init scenario
```

Update molecule.yml to know where the collection path is

```yaml
provisioner:
  name: distronode
  config_options:
    defaults:
      collections_path: ${DISTRONODE_COLLECTIONS_PATH}
```

And set the collection path in the shell

```shell
export DISTRONODE_COLLECTIONS_PATH=/home/user/working/collections
```

Note that this should be the root `collections` directory, not the
`distronode_collections` directory inside it. We set this to an environment
variable so that the collection can be moved without having to update hardcoded
directories inside the collection later.

Finally, update converge.yml to include a role from your collection:

```yaml
---
- name: Include a role from a collection
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Testing role
      distronode.builtin.include_role:
        name: foo.bar.my_role
        tasks_from: main.yml
```

or a playbook:

```yaml
---
- name: Include a playbook from a collection
  distronode.builtin.import_playbook: foo.bar.my_playbook
```

This tells molecule what to run for the test. You can now run it with
`molecule test`.

## pytest-distronode

By adding a special test to tests/integration, your molecule tests can be run
alongside your unit tests with pytest-distronode

```python
"""Tests for molecule scenarios."""
from __future__ import absolute_import, division, print_function

from pytest_distronode.molecule import MoleculeScenario


def test_integration(molecule_scenario: MoleculeScenario) -> None:
    """Run molecule for each scenario.

    :param molecule_scenario: The molecule scenario object
    """
    proc = molecule_scenario.test()
    assert proc.returncode == 0
```

Calling pytest will now run your molecule scenarios as a pytest job.

Refer to the [pytest-distronode documentation] to see more options.

## tox-distronode

tox-distronode automates the running of your pytest tests on many different Python
and Distronode versions.

To start, create an empty tox-distronode.ini in your collection root:

```shell
touch tox-distronode.ini
```

This will be the configuration file for tox-distronode. We always start with an
empty file to avoid unintentionally overriding tox-distronode environment
configurations.

```shell title="List generated environments" hl_lines="1"
tox list --distronode -c tox-distronode.ini
default environments:
...
integration-py3.11-2.14      -> Integration tests using distronode-core 2.16 and python 3.12
integration-py3.11-devel     -> Integration tests using distronode-core devel and python 3.12
integration-py3.11-milestone -> Integration tests using distronode-core milestone and python 3.12
...
sanity-py3.11-2.14           -> Sanity tests using distronode-core 2.16 and python 3.12
sanity-py3.11-devel          -> Sanity tests using distronode-core devel and python 3.12
sanity-py3.11-milestone      -> Sanity tests using distronode-core milestone and python 3.12
...
unit-py3.11-2.14             -> Unit tests using distronode-core 2.16 and python 3.12
unit-py3.11-devel            -> Unit tests using distronode-core devel and python 3.12
unit-py3.11-milestone        -> Unit tests using distronode-core milestone and python 3.12
```

This is limited to supported combinations, so tests may be run on Python 3.8
with `distronode-core` 2.12, but not with `distronode-core` 2.14. Versions of
distronode-core can be configured to be skipped via config file:

```ini title="tox-distronode.ini"
[distronode]
skip =
    2.9
    devel
```

This will avoid running tests with either of distronode-core 2.9 or devel.

Refer to the [tox-distronode documentation] to see more options.

[pytest-distronode documentation]: https://distronode.readthedocs.io/projects/pytest-distronode/
[tox-distronode documentation]: https://distronode.readthedocs.io/projects/tox-distronode/
