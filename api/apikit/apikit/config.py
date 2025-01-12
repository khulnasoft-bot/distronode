import types
import os

from .utils import (
    PseudoNamespace,
    load_credentials,
    load_projects,
    to_bool,
)

config = PseudoNamespace()


def getvalue(self, name):
    return self.__getitem__(name)


if os.getenv('APIKIT_BASE_URL'):
    config.base_url = os.getenv('APIKIT_BASE_URL')

if os.getenv('APIKIT_CREDENTIAL_FILE'):
    config.credentials = load_credentials(os.getenv('APIKIT_CREDENTIAL_FILE'))

if os.getenv('APIKIT_PROJECT_FILE'):
    config.project_urls = load_projects(config.get('APIKIT_PROJECT_FILE'))

# kludge to mimic pytest.config
config.getvalue = types.MethodType(getvalue, config)

config.assume_untrusted = config.get('assume_untrusted', True)

config.client_connection_attempts = int(os.getenv('APIKIT_CLIENT_CONNECTION_ATTEMPTS', 5))
config.prevent_teardown = to_bool(os.getenv('APIKIT_PREVENT_TEARDOWN', False))
config.use_sessions = to_bool(os.getenv('APIKIT_SESSIONS', False))
config.api_base_path = os.getenv('APIKIT_API_BASE_PATH', '/api/')
config.gateway_base_path = os.getenv('APIKIT_GATEWAY_BASE_PATH', '/api/gateway/')
