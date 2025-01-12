#!/usr/bin/python
"""Distronode module to detect the presence of both the normal and Distronode-specific versions of Paramiko."""

from __future__ import annotations


from distronode.module_utils.basic import DistronodeModule

try:
    import paramiko
except ImportError:
    paramiko = None

try:
    import distronode_paramiko
except ImportError:
    distronode_paramiko = None


def main():
    module = DistronodeModule(argument_spec={})
    module.exit_json(**dict(
        found=bool(paramiko or distronode_paramiko),
        paramiko=bool(paramiko),
        distronode_paramiko=bool(distronode_paramiko),
    ))


if __name__ == '__main__':
    main()
