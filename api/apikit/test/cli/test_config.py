import os
import json
import pytest
from requests.exceptions import ConnectionError

from apikit.cli import CLI
from apikit import config


def test_host_from_environment():
    cli = CLI()
    cli.parse_args(['api'], env={'CONTROLLER_HOST': 'https://xyz.local'})
    with pytest.raises(ConnectionError):
        cli.connect()
    assert config.base_url == 'https://xyz.local'


def test_host_from_argv():
    cli = CLI()
    cli.parse_args(['api', '--conf.host', 'https://xyz.local'])
    with pytest.raises(ConnectionError):
        cli.connect()
    assert config.base_url == 'https://xyz.local'


def test_username_and_password_from_environment():
    cli = CLI()
    cli.parse_args(['api'], env={'CONTROLLER_USERNAME': 'mary', 'CONTROLLER_PASSWORD': 'secret'})
    with pytest.raises(ConnectionError):
        cli.connect()

    assert config.credentials.default.username == 'mary'
    assert config.credentials.default.password == 'secret'


def test_username_and_password_argv():
    cli = CLI()
    cli.parse_args(['api', '--conf.username', 'mary', '--conf.password', 'secret'])
    with pytest.raises(ConnectionError):
        cli.connect()

    assert config.credentials.default.username == 'mary'
    assert config.credentials.default.password == 'secret'


def test_config_precedence():
    cli = CLI()
    cli.parse_args(['api', '--conf.username', 'mary', '--conf.password', 'secret'], env={'CONTROLLER_USERNAME': 'IGNORE', 'CONTROLLER_PASSWORD': 'IGNORE'})
    with pytest.raises(ConnectionError):
        cli.connect()

    assert config.credentials.default.username == 'mary'
    assert config.credentials.default.password == 'secret'


def test_config_file_precedence():
    """Ignores APIKIT_CREDENTIAL_FILE if cli args are set"""
    os.makedirs('/tmp/api-test/', exist_ok=True)
    with open('/tmp/api-test/config.json', 'w') as f:
        json.dump({'default': {'username': 'IGNORE', 'password': 'IGNORE'}}, f)

    cli = CLI()
    cli.parse_args(
        ['api', '--conf.username', 'mary', '--conf.password', 'secret'],
        env={
            'APIKIT_CREDENTIAL_FILE': '/tmp/api-test/config.json',
        },
    )
    with pytest.raises(ConnectionError):
        cli.connect()

    assert config.credentials.default.username == 'mary'
    assert config.credentials.default.password == 'secret'


def test_config_file_precedence_2():
    """Ignores APIKIT_CREDENTIAL_FILE if TOWER_* vars are set."""
    os.makedirs('/tmp/api-test/', exist_ok=True)
    with open('/tmp/api-test/config.json', 'w') as f:
        json.dump({'default': {'username': 'IGNORE', 'password': 'IGNORE'}}, f)

    cli = CLI()
    cli.parse_args(['api'], env={'APIKIT_CREDENTIAL_FILE': '/tmp/api-test/config.json', 'TOWER_USERNAME': 'mary', 'TOWER_PASSWORD': 'secret'})
    with pytest.raises(ConnectionError):
        cli.connect()

    assert config.credentials.default.username == 'mary'
    assert config.credentials.default.password == 'secret'


def test_config_file():
    """Reads username and password from APIKIT_CREDENTIAL_FILE."""
    os.makedirs('/tmp/api-test/', exist_ok=True)
    with open('/tmp/api-test/config.json', 'w') as f:
        json.dump({'default': {'username': 'mary', 'password': 'secret'}}, f)

    cli = CLI()
    cli.parse_args(
        ['api'],
        env={
            'APIKIT_CREDENTIAL_FILE': '/tmp/api-test/config.json',
        },
    )
    with pytest.raises(ConnectionError):
        cli.connect()

    assert config.credentials.default.username == 'mary'
    assert config.credentials.default.password == 'secret'
