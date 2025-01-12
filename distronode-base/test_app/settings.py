import os
import sys

from split_settings.tools import include

DEBUG = True

if "pytest" in sys.modules:
    # https://github.com/agronholm/typeguard/issues/260
    # Enable runtime type checking only for running tests
    # must be done here because python hooks will not reliably call the
    # typguard plugin setup before other plugins which setup Django, which loads settings.
    # Lower in this settings file, the dynamic config imports distronode_base
    from typeguard import install_import_hook

    install_import_hook(packages=["distronode_base"])

ALLOWED_HOSTS = ["*"]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id_filter': {
            '()': 'distronode_base.lib.logging.filters.RequestIdFilter',
        },
    },
    'formatters': {
        'simple': {'format': '%(asctime)s %(levelname)-8s [%(request_id)s]  %(name)s %(message)s'},
    },
    'handlers': {
        'console': {
            '()': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filters': ['request_id_filter'],
        },
    },
    'loggers': {
        'distronode_base': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
for logger in LOGGING["loggers"]:  # noqa: F405
    # We want to ensure that all loggers are at DEBUG because we have tests which validate log messages
    LOGGING["loggers"][logger]["level"] = "DEBUG"  # noqa: F405

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'social_django',
    'distronode_base.api_documentation',
    'distronode_base.authentication',
    'distronode_base.rest_filters',
    'distronode_base.jwt_consumer',
    'distronode_base.resource_registry',
    'distronode_base.rest_pagination',
    'distronode_base.rbac',
    'distronode_base.oauth2_provider',
    'test_app',
    'django_extensions',
    'debug_toolbar',
    'distronode_base.activitystream',
    'distronode_base.help_text_check',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
    'distronode_base.lib.middleware.logging.LogRequestMiddleware',
    'distronode_base.lib.middleware.logging.LogTracebackMiddleware',
]

# set some vanilla social auth plugins so that we can test the social_auth based
# users in the resource registry
AUTHENTICATION_BACKENDS = [
    'distronode_base.lib.backends.prefixed_user_auth.PrefixedUserAuthBackend',
    'social_core.backends.github.GithubOAuth2',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'test_app.authentication.logged_basic_auth.LoggedBasicAuthentication',
        'test_app.authentication.service_token_auth.ServiceTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'distronode_base.oauth2_provider.permissions.OAuth2ScopePermission',
        'distronode_base.rbac.api.permissions.DistronodeBaseObjectPermissions',
    ],
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", 55432),
        "USER": os.getenv("DB_USER", "dab"),
        "PASSWORD": os.getenv("DB_PASSWORD", "dabing"),
        "NAME": os.getenv("DB_NAME", "dab_db"),
    }
}

AUTH_USER_MODEL = 'test_app.User'

ROOT_URLCONF = 'test_app.urls'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'test_app', 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ]
        },
    },
]

INTERNAL_IPS = [
    "127.0.0.1",
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEMO_DATA_COUNTS = {'organization': 150, 'user': 379, 'team': 43}

DISTRONODE_BASE_TEAM_MODEL = 'test_app.Team'
DISTRONODE_BASE_ORGANIZATION_MODEL = 'test_app.Organization'

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECRET_KEY = "asdf1234"

DISTRONODE_BASE_AUTHENTICATOR_CLASS_PREFIXES = ['distronode_base.authentication.authenticator_plugins']

from distronode_base.lib import dynamic_config  # noqa: E402

settings_file = os.path.join(os.path.dirname(dynamic_config.__file__), 'dynamic_settings.py')
include(settings_file)

DISTRONODE_BASE_RESOURCE_CONFIG_MODULE = "test_app.resource_api"

SYSTEM_USERNAME = '_system'

DISTRONODE_BASE_MANAGED_ROLE_REGISTRY = {
    'sys_auditor': {'name': "Platform Auditor"},
    'team_member': {},
    'team_admin': {},
    'org_admin': {},
    'org_member': {},
    'cow_admin': {'shortname': 'admin_base', 'model_name': 'test_app.cow', 'name': 'Cow Admin'},
    'cow_moo': {'shortname': 'action_base', 'model_name': 'test_app.cow', 'name': 'Cow Mooer', 'action': 'say_cow'},
}
DISTRONODE_BASE_JWT_MANAGED_ROLES.append("System Auditor")  # noqa: F821 this is set by dynamic settings for jwt_consumer
DISTRONODE_BASE_ALLOW_SINGLETON_USER_ROLES = True
DISTRONODE_BASE_ALLOW_SINGLETON_TEAM_ROLES = True
DISTRONODE_BASE_RBAC_MODEL_REGISTRY = {
    "test_app.inventory": {"parent_field_name": "organization"},
    "test_app.credential": {},
    "test_app.immutabletask": {"parent_field_name": None},
}
DISTRONODE_BASE_OAUTH2_PROVIDER_PERMISSIONS_CHECK_IGNORED_VIEWS = ["drf_spectacular.views.SpectacularSwaggerView"]
ALLOW_SHARED_RESOURCE_CUSTOM_ROLES = True  # Allow making custom roles with org change permission, for example
ALLOW_LOCAL_ASSIGNING_JWT_ROLES = False

DISTRONODE_BASE_USER_VIEWSET = 'test_app.views.UserViewSet'

LOGIN_URL = "/login/login"

RESOURCE_SERVER = {
    "URL": "http://localhost",
    "SECRET_KEY": "my secret key",
    "VALIDATE_HTTPS": False,
}
RESOURCE_SERVICE_PATH = "/api/v1/service-index/"
# Backwards sync turned off, because for most of the duration of the tests
# the resource server will not actually be running
# so it will be flipped true only for specific tests that test this
RESOURCE_SERVER_SYNC_ENABLED = False

RENAMED_USERNAME_PREFIX = "dab:"
