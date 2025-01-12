import logging

from social_core.backends.github import GithubTeamOAuth2

from distronode_base.authentication.authenticator_configurators.github import GithubTeamConfiguration
from distronode_base.authentication.authenticator_plugins.base import AbstractAuthenticatorPlugin
from distronode_base.authentication.social_auth import SocialAuthMixin, SocialAuthValidateCallbackMixin

logger = logging.getLogger('distronode_base.authentication.authenticator_plugins.github_team')


class AuthenticatorPlugin(SocialAuthMixin, SocialAuthValidateCallbackMixin, GithubTeamOAuth2, AbstractAuthenticatorPlugin):
    configuration_class = GithubTeamConfiguration
    logger = logger
    type = "github-team"
    category = "sso"
    configuration_encrypted_fields = ['SECRET']
