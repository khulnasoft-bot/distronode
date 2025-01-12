import logging

from social_core.backends.github_enterprise import GithubEnterpriseOAuth2

from distronode_base.authentication.authenticator_configurators.github import GithubEnterpriseConfiguration
from distronode_base.authentication.authenticator_plugins.base import AbstractAuthenticatorPlugin
from distronode_base.authentication.social_auth import SocialAuthMixin, SocialAuthValidateCallbackMixin

logger = logging.getLogger('distronode_base.authentication.authenticator_plugins.github_enterprise')


class AuthenticatorPlugin(SocialAuthMixin, SocialAuthValidateCallbackMixin, GithubEnterpriseOAuth2, AbstractAuthenticatorPlugin):
    configuration_class = GithubEnterpriseConfiguration
    logger = logger
    type = "github-enterprise"
    category = "sso"
    configuration_encrypted_fields = ['ENTERPRISE_SECRET']
