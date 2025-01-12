#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(),
    )
    result = {
        'selinux_special_fs': module._selinux_special_fs,
        'tmpdir': module._tmpdir,
        'keep_remote_files': module._keep_remote_files,
        'version': module.distronode_version,
    }
    module.exit_json(**result)


if __name__ == '__main__':
    main()
