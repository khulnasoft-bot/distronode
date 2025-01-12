#!/usr/bin/python
from __future__ import annotations

import os

from distronode.module_utils.basic import DistronodeModule


def main():
    # This module verifies that DistronodeModule works when cwd does not exist.
    # This situation can occur as a race condition when the following conditions are met:
    #
    # 1) Execute a module which has high startup overhead prior to instantiating DistronodeModule (0.5s is enough in many cases).
    # 2) Run the module async as the last task in a playbook using connection=local (a fire-and-forget task).
    # 3) Remove the directory containing the playbook immediately after playbook execution ends (playbook in a temp dir).
    #
    # To ease testing of this race condition the deletion of cwd is handled in this module.
    # This avoids race conditions in the test, including timing cwd deletion between AnsiballZ wrapper execution and DistronodeModule instantiation.
    # The timing issue with AnsiballZ is due to cwd checking in the wrapper when code coverage is enabled.

    temp = os.path.abspath('temp')

    os.mkdir(temp)
    os.chdir(temp)
    os.rmdir(temp)

    module = DistronodeModule(argument_spec=dict())
    module.exit_json(before=temp, after=os.getcwd())


if __name__ == '__main__':
    main()
