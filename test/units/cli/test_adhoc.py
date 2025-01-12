# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import pytest
import re

from distronode import context
from distronode.cli.adhoc import AdHocCLI, display
from distronode.errors import DistronodeOptionsError


def test_parse():
    """ Test adhoc parse"""
    with pytest.raises(ValueError, match='A non-empty list for args is required'):
        adhoc_cli = AdHocCLI([])

    adhoc_cli = AdHocCLI(['distronodetest'])
    with pytest.raises(SystemExit):
        adhoc_cli.parse()


def test_with_command():
    """ Test simple adhoc command"""
    module_name = 'command'
    adhoc_cli = AdHocCLI(args=['distronode', '-m', module_name, '-vv', 'localhost'])
    adhoc_cli.parse()
    assert context.CLIARGS['module_name'] == module_name
    assert display.verbosity == 2


def test_simple_command():
    """ Test valid command and its run"""
    adhoc_cli = AdHocCLI(['/bin/distronode', '-m', 'command', 'localhost', '-a', 'echo "hi"'])
    adhoc_cli.parse()
    ret = adhoc_cli.run()
    assert ret == 0


def test_no_argument():
    """ Test no argument command"""
    adhoc_cli = AdHocCLI(['/bin/distronode', '-m', 'command', 'localhost'])
    adhoc_cli.parse()
    with pytest.raises(DistronodeOptionsError) as exec_info:
        adhoc_cli.run()
    assert 'No argument passed to command module' == str(exec_info.value)


def test_did_you_mean_playbook():
    """ Test adhoc with yml file as argument parameter"""
    adhoc_cli = AdHocCLI(['/bin/distronode', '-m', 'command', 'localhost.yml'])
    adhoc_cli.parse()
    with pytest.raises(DistronodeOptionsError) as exec_info:
        adhoc_cli.run()
    assert 'No argument passed to command module (did you mean to run distronode-playbook?)' == str(exec_info.value)


def test_play_ds_positive():
    """ Test _play_ds"""
    adhoc_cli = AdHocCLI(args=['/bin/distronode', 'localhost', '-m', 'command'])
    adhoc_cli.parse()
    ret = adhoc_cli._play_ds('command', 10, 2)
    assert ret['name'] == 'Distronode Ad-Hoc'
    assert ret['tasks'] == [{'action': {'module': 'command', 'args': {}}, 'async_val': 10, 'poll': 2, 'timeout': 0}]


def test_play_ds_with_include_role():
    """ Test include_role command with poll"""
    adhoc_cli = AdHocCLI(args=['/bin/distronode', 'localhost', '-m', 'include_role'])
    adhoc_cli.parse()
    ret = adhoc_cli._play_ds('include_role', None, 2)
    assert ret['name'] == 'Distronode Ad-Hoc'
    assert ret['gather_facts'] == 'no'


def test_run_import_playbook():
    """ Test import_playbook which is not allowed with ad-hoc command"""
    import_playbook = 'import_playbook'
    adhoc_cli = AdHocCLI(args=['/bin/distronode', '-m', import_playbook, 'localhost'])
    adhoc_cli.parse()
    with pytest.raises(DistronodeOptionsError) as exec_info:
        adhoc_cli.run()
    assert context.CLIARGS['module_name'] == import_playbook
    assert "'%s' is not a valid action for ad-hoc commands" % import_playbook == str(exec_info.value)


def test_run_no_extra_vars():
    adhoc_cli = AdHocCLI(args=['/bin/distronode', 'localhost', '-e'])
    with pytest.raises(SystemExit) as exec_info:
        adhoc_cli.parse()
    assert exec_info.value.code == 2


def test_distronode_version(capsys):
    adhoc_cli = AdHocCLI(args=['/bin/distronode', '--version'])
    with pytest.raises(SystemExit):
        adhoc_cli.run()
    version = capsys.readouterr()
    version_lines = version.out.splitlines()

    assert len(version_lines) == 9, 'Incorrect number of lines in "distronode --version" output'
    assert re.match(r'distronode \[core [0-9.a-z]+\]', version_lines[0]), 'Incorrect distronode version line in "distronode --version" output'
    assert re.match('  config file = .*$', version_lines[1]), 'Incorrect config file line in "distronode --version" output'
    assert re.match('  configured module search path = .*$', version_lines[2]), 'Incorrect module search path in "distronode --version" output'
    assert re.match('  distronode python module location = .*$', version_lines[3]), 'Incorrect python module location in "distronode --version" output'
    assert re.match('  distronode collection location = .*$', version_lines[4]), 'Incorrect collection location in "distronode --version" output'
    assert re.match('  executable location = .*$', version_lines[5]), 'Incorrect executable locaction in "distronode --version" output'
    assert re.match('  python version = .*$', version_lines[6]), 'Incorrect python version in "distronode --version" output'
    assert re.match('  jinja version = .*$', version_lines[7]), 'Incorrect jinja version in "distronode --version" output'
    assert re.match('  libyaml = .*$', version_lines[8]), 'Missing libyaml in "distronode --version" output'
