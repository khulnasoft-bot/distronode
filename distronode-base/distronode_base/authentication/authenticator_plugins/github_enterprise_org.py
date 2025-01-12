import logging

from social_core.backends.github_enterprise import GithubEnterpriseOrganizationOAuth2

from distronode_base.authentication.authenticator_configurators.github import GithubEnterpriseOrgConfiguration
from distronode_base.authentication.authenticator_plugins.base import AbstractAuthenticatorPlugin
from distronode_base.authentication.social_auth import SocialAuthMixin, SocialAuthValidateCallbackMixin

logger = logging.getLogger('distronode_base.authentication.authenticator_plugins.github_enterprise_organization')


class AuthenticatorPlugin(SocialAuthMixin, SocialAuthValidateCallbackMixin, GithubEnterpriseOrganizationOAuth2, AbstractAuthenticatorPlugin):
    configuration_class = GithubEnterpriseOrgConfiguration
    logger = logger
    type = "github-enterprise-org"
    category = "sso"
    configuration_encrypted_fields = ['ENTERPRISE_ORG_SECRET']
