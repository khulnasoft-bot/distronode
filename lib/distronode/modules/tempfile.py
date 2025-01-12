# -*- coding: utf-8 -*-

# Copyright: (c) 2016, Krzysztof Magosa <krzysztof@magosa.pl>
# Copyright: (c) 2017, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


DOCUMENTATION = """
---
module: tempfile
version_added: "2.3"
short_description: Creates temporary files and directories
description:
  - The M(distronode.builtin.tempfile) module creates temporary files and directories. C(mktemp) command
    takes different parameters on various systems, this module helps to avoid troubles related to that.
    Files/directories created by module are accessible only by creator. In case you need to make them
    world-accessible you need to use M(distronode.builtin.file) module.
  - For Windows targets, use the M(distronode.windows.win_tempfile) module instead.
options:
  state:
    description:
      - Whether to create file or directory.
    type: str
    choices: [ directory, file ]
    default: file
  path:
    description:
      - Location where temporary file or directory should be created.
      - If path is not specified, the default system temporary directory will be used.
    type: path
  prefix:
    description:
      - Prefix of file/directory name created by module.
    type: str
    default: distronode.
  suffix:
    description:
      - Suffix of file/directory name created by module.
    type: str
    default: ""
extends_documentation_fragment: action_common_attributes
attributes:
    check_mode:
        support: none
    diff_mode:
        support: none
    platform:
        platforms: posix
seealso:
- module: distronode.builtin.file
- module: distronode.windows.win_tempfile
author:
  - Krzysztof Magosa (@krzysztof-magosa)
"""

EXAMPLES = """
- name: Create temporary build directory
  distronode.builtin.tempfile:
    state: directory
    suffix: build

- name: Create temporary file
  distronode.builtin.tempfile:
    state: file
    suffix: temp
  register: tempfile_1

- name: Create a temporary file with a specific prefix
  distronode.builtin.tempfile:
     state: file
     suffix: txt
     prefix: myfile_

- name: Use the registered var and the file module to remove the temporary file
  distronode.builtin.file:
    path: "{{ tempfile_1.path }}"
    state: absent
  when: tempfile_1.path is defined
"""

RETURN = """
path:
  description: Path to created file or directory.
  returned: success
  type: str
  sample: "/tmp/distronode.bMlvdk"
"""

from os import close
from tempfile import mkstemp, mkdtemp
from traceback import format_exc

from distronode.module_utils.basic import DistronodeModule
from distronode.module_utils.common.text.converters import to_native


def main():
    module = DistronodeModule(
        argument_spec=dict(
            state=dict(type='str', default='file', choices=['file', 'directory']),
            path=dict(type='path'),
            prefix=dict(type='str', default='distronode.'),
            suffix=dict(type='str', default=''),
        ),
    )

    try:
        if module.params['state'] == 'file':
            handle, path = mkstemp(
                prefix=module.params['prefix'],
                suffix=module.params['suffix'],
                dir=module.params['path'],
            )
            close(handle)
        else:
            path = mkdtemp(
                prefix=module.params['prefix'],
                suffix=module.params['suffix'],
                dir=module.params['path'],
            )

        module.exit_json(changed=True, path=path)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
