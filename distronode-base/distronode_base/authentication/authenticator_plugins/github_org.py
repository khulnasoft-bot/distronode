import logging

from social_core.backends.github import GithubOrganizationOAuth2

from distronode_base.authentication.authenticator_configurators.github import GithubOrganizationConfiguration
from distronode_base.authentication.authenticator_plugins.base import AbstractAuthenticatorPlugin
from distronode_base.authentication.social_auth import SocialAuthMixin, SocialAuthValidateCallbackMixin

logger = logging.getLogger('distronode_base.authentication.authenticator_plugins.github_organization')


class AuthenticatorPlugin(SocialAuthMixin, SocialAuthValidateCallbackMixin, GithubOrganizationOAuth2, AbstractAuthenticatorPlugin):
    configuration_class = GithubOrganizationConfiguration
    logger = logger
    type = "github-org"
    category = "sso"
    configuration_encrypted_fields = ['SECRET']
