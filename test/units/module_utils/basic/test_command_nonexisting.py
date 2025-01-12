from __future__ import annotations

import json
import sys
import pytest
import subprocess
from distronode.module_utils.common.text.converters import to_bytes
from distronode.module_utils import basic


def test_run_non_existent_command(monkeypatch):
    """ Test that `command` returns std{out,err} even if the executable is not found """
    def fail_json(msg, **kwargs):
        assert kwargs["stderr"] == b''
        assert kwargs["stdout"] == b''
        sys.exit(1)

    def popen(*args, **kwargs):
        raise OSError()

    monkeypatch.setattr(basic, '_DISTRONODE_ARGS', to_bytes(json.dumps({'DISTRONODE_MODULE_ARGS': {}})))
    monkeypatch.setattr(subprocess, 'Popen', popen)

    am = basic.DistronodeModule(argument_spec={})
    monkeypatch.setattr(am, 'fail_json', fail_json)
    with pytest.raises(SystemExit):
        am.run_command("lecho", "whatever")
