import logging

from social_core.backends.github_enterprise import GithubEnterpriseTeamOAuth2

from distronode_base.authentication.authenticator_configurators.github import GithubEnterpriseTeamConfiguration
from distronode_base.authentication.authenticator_plugins.base import AbstractAuthenticatorPlugin
from distronode_base.authentication.social_auth import SocialAuthMixin, SocialAuthValidateCallbackMixin

logger = logging.getLogger('distronode_base.authentication.authenticator_plugins.github_enterprise_team')


class AuthenticatorPlugin(SocialAuthMixin, SocialAuthValidateCallbackMixin, GithubEnterpriseTeamOAuth2, AbstractAuthenticatorPlugin):
    configuration_class = GithubEnterpriseTeamConfiguration
    logger = logger
    type = "github-enterprise-team"
    category = "sso"
    configuration_encrypted_fields = ['SECRET']
