import logging

from django.contrib.auth import BACKEND_SESSION_KEY
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from social_django.middleware import SocialAuthExceptionMiddleware

from distronode_base.authentication.authenticator_plugins.utils import get_authenticator_plugins

logger = logging.getLogger('distronode_base.authentication.middleware')


def get_authenticator_module_paths() -> list:
    plugins = get_authenticator_plugins()
    plugins = [f'{name}.AuthenticatorPlugin' for name in plugins]
    return plugins


class AuthenticatorBackendMiddleware(MiddlewareMixin):
    _plugins = None

    @property
    def plugins(self):
        if not self._plugins:
            self._plugins = get_authenticator_module_paths()
        return self._plugins

    def process_request(self, request):
        if not hasattr(request, "session"):
            raise ImproperlyConfigured(
                "The Django AuthenticatorBackendMiddleware requires session "
                "middleware to be installed. Edit your MIDDLEWARE setting to "
                "insert "
                "'django.contrib.sessions.middleware.SessionMiddleware' before "
                "'AuthenticatorBackendMiddleware'."
            )

        # If the session backend is one from one of the Authenticator plugins, change it to
        # distronode_base.authentication.backend.DistronodeBaseAuth so that the user can be logged
        # in since the Authenticator backends aren't in AUTHENTICATION_BACKENDS
        if backend := request.session.get(BACKEND_SESSION_KEY, None):
            if backend in self.plugins:
                request.session[BACKEND_SESSION_KEY] = "distronode_base.authentication.backend.DistronodeBaseAuth"


class SocialExceptionHandlerMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        strategy = getattr(request, "social_strategy", None)
        error_url = strategy.setting("LOGIN_ERROR_URL")
        backend = getattr(request, "backend", None)
        backend_name = getattr(backend, "name", "unknown-backend")
        logger.error(f"Auth failure for backend {backend_name} - {repr(exception)}, redirecting to {error_url}")
        return error_url
