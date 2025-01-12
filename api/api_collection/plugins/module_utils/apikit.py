from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .controller_api import ControllerModule
from distronode.module_utils.basic import missing_required_lib

try:
    from apikit.api.client import Connection
    from apikit.api.pages.api import ApiV2
    from apikit.api import get_registered_page

    HAS_API_KIT = True
except ImportError:
    HAS_API_KIT = False


class ControllerAPIKitModule(ControllerModule):
    connection = None
    apiV2Ref = None

    def __init__(self, argument_spec, **kwargs):
        kwargs['supports_check_mode'] = False

        super().__init__(argument_spec=argument_spec, **kwargs)

        # Die if we don't have API_KIT installed
        if not HAS_API_KIT:
            self.fail_json(msg=missing_required_lib('apikit'))

        # Establish our conneciton object
        self.connection = Connection(self.host, verify=self.verify_ssl)

    def authenticate(self):
        try:
            self.connection.login(username=self.username, password=self.password)
            self.authenticated = True
        except Exception:
            self.fail_json("Failed to authenticate")

    def get_api_v2_object(self):
        if not self.apiV2Ref:
            if not self.authenticated:
                self.authenticate()
            v2_index = get_registered_page('/api/v2/')(self.connection).get()
            self.api_ref = ApiV2(connection=self.connection, **{'json': v2_index})
        return self.api_ref

    def logout(self):
        if self.authenticated:
            self.connection.logout()
