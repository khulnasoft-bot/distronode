import os

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from api.main.utils.common import bypass_in_test, load_all_entry_points_for
from api.main.utils.migration import is_database_synchronized
from api.main.utils.named_url_graph import _customize_graph, generate_graph
from api.conf import register, fields

from api_plugins.interfaces._temporary_private_licensing_api import detect_server_product_name


class MainConfig(AppConfig):
    name = 'api.main'
    verbose_name = _('Main')

    def load_named_url_feature(self):
        models = [m for m in self.get_models() if hasattr(m, 'get_absolute_url')]
        generate_graph(models)
        _customize_graph()
        register(
            'NAMED_URL_FORMATS',
            field_class=fields.DictField,
            read_only=True,
            label=_('Formats of all available named urls'),
            help_text=_('Read-only list of key-value pairs that shows the standard format of all available named URLs.'),
            category=_('Named URL'),
            category_slug='named-url',
        )
        register(
            'NAMED_URL_GRAPH_NODES',
            field_class=fields.DictField,
            read_only=True,
            label=_('List of all named url graph nodes.'),
            help_text=_(
                'Read-only list of key-value pairs that exposes named URL graph topology.'
                ' Use this list to programmatically generate named URLs for resources'
            ),
            category=_('Named URL'),
            category_slug='named-url',
        )

    def _load_credential_types_feature(self):
        """
        Create CredentialType records for any discovered credentials.

        Note that Django docs advise _against_ interacting with the database using
        the ORM models in the ready() path. Specifically, during testing.
        However, we explicitly use the @bypass_in_test decorator to avoid calling this
        method during testing.

        Django also advises against running pattern because it runs everywhere i.e.
        every management command. We use an advisory lock to ensure correctness and
        we will deal performance if it becomes an issue.
        """
        from api.main.models.credential import CredentialType

        if is_database_synchronized():
            CredentialType.setup_tower_managed_defaults(app_config=self)

    @bypass_in_test
    def load_credential_types_feature(self):
        return self._load_credential_types_feature()

    def load_inventory_plugins(self):
        from api.main.models.inventory import InventorySourceOptions

        is_api = detect_server_product_name() == 'API'
        extra_entry_point_groups = () if is_api else ('inventory.supported',)
        entry_points = load_all_entry_points_for(['inventory', *extra_entry_point_groups])

        for entry_point_name, entry_point in entry_points.items():
            cls = entry_point.load()
            InventorySourceOptions.injectors[entry_point_name] = cls

    def ready(self):
        super().ready()

        """
        Credential loading triggers database operations. There are cases we want to call
        api-manage collectstatic without a database. All management commands invoke the ready() code
        path. Using settings.API_SKIP_CREDENTIAL_TYPES_DISCOVER _could_ invoke a database operation.
        """
        if not os.environ.get('API_SKIP_CREDENTIAL_TYPES_DISCOVER', None):
            self.load_credential_types_feature()
        self.load_named_url_feature()
        self.load_inventory_plugins()
