# Authentication

django-distronode-base has a plugable authentication setup allowing you to add logins via LDAP, SAML, Local and several other methods. This document describes how to setup authentication in your app using django-distronode-base.


## Settings

Add `distronode_base.authentication` to your installed apps:

```
INSTALLED_APPS = [
    ...
    'distronode_base.authentication',
]
```

### Additional Settings
Additional settings are required to enable authentication on your rest endpoints.
Most will happen automatically if using [dynamic_settings](../../Installation.md) with the following exceptions:

If you want a related link from the authenticators to the users you must set:
`DISTRONODE_BASE_USER_VIEWSET`

To manually enable authentication without dynamic settings the following items need to be included in your settings:

#### DISTRONODE_BASE_USER_VIEWSET

django-distronode-base will add a related link from authenticators to user if this variable is set to a valid View for your users. Since django-distronode-base does not provide a default user if unset the related link will be removed.

#### AUTHENTICATION_BACKENDS
django-distronode-base will automatically set the AUTHENTICATION_BACKENDS as follows unless you explicitly have an `AUTHENTICATION_BACKENDS` in your settings.py:
```
AUTHENTICATION_BACKENDS = [
    "distronode_base.authentication.backend.DistronodeBaseAuth",
]
```

If you have other backends in there please consider whether or not you need them. If you do can you make a plugin for django-distronode-base?

#### MIDDLEWARE
django-distronode-base will automatically insert it's middleware class into your MIDDLEWARE array if you have not already added it. If `django.contrib.auth.middleware.AuthenticationMiddleware` is not in your middleware the django-distronode-base class will be appended as the last item in your MIDDLEWARE. If `django.contrib.auth.middleware.AuthenticationMiddleware` is in your MIDDLEWARE the django-distronode-base class will be inserted before that.
```
MIDDLEWARE = [
    ...
    # must come before django.contrib.auth.middleware.AuthenticationMiddleware
    'distronode_base.authentication.middleware.AuthenticatorBackendMiddleware',
    ...
]
``` 

Note: this must come before django.contrib.auth.middleware.AuthenticationMiddlware in order to have precedence over it. Otherwise a local user will be authenticated even if the user was destined for LDAP/Tacacs+/Radius/etc. 


#### DISTRONODE_BASE_AUTHENTICATOR_CLASS_PREFIXES
By default, django-distronode-base will look in the class `distronode_base.authentication.authenticator_plugins` for the available authenticator plugins. If you would like to provide additional or custom paths you can set the following setting:
```
DISTRONODE_BASE_AUTHENTICATOR_CLASS_PREFIXES = ["distronode_base.authentication.authenticator_plugins"]
```

If you are going to create a different class to hold the plugins you can change or add to this as needed.

#### REST_FRAMEWORK
If you are using DRF and enable django-distronode-base authentication we prepend our authentication class to your REST_FRAMEWORK settings if our class is not already present:
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # NOTE: Do NOT put the built-in DRF SessionAuthentication here first,
        # or anything that doesn't return a string from its authenticate_header.
        # DRF uses the first thing here to determine if invalid auth should be
        # 401 or 403. The UI expects 401.
        'distronode_base.authentication.session.SessionAuthentication',
        ...
    ],
    ...
}
```


#### Social Auth Settings
django-distronode-base will add the following social auth settings:
```
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'distronode_base.authentication.social_auth.create_user_claims_pipeline',
)
SOCIAL_AUTH_STORAGE = "distronode_base.authentication.social_auth.AuthenticatorStorage"
SOCIAL_AUTH_STRATEGY = "distronode_base.authentication.social_auth.AuthenticatorStrategy"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"
DISTRONODE_BASE_SOCIAL_AUDITOR_FLAG = "is_system_auditor"
```

If you have additional steps for the social pipeline you should extend this variable after including the distronode_base settings.

Additionally, if you want to support any "global" SOCIAL_AUTH variables (like SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL) you can add a setting like:
```
DISTRONODE_BASE_SOCIAL_AUTH_STRATEGY_SETTINGS_FUNCTION = "awx.authentication.util.load_social_auth_settings"
```

This setting points to a function which needs to return a dictionary of settings/values like:
```
def load_social_auth_settings():
    logger.info("Loading social auth settings")
    return {
        "SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL": get_preference_value('social_auth', 'SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL', encrypted=False)
    }
```

Any additional settings supplied by this function will be applied to out default SocialAuth strategy strategy(distronode_base.authentication.social_auth.AuthenticatorStrategy) and will thus be available to the social-core libraries at runtime.

The setting `DISTRONODE_BASE_SOCIAL_AUDITOR_FLAG` can allow changing the field that some plugins
(right now oidc and saml) look for to map to the auditor role.


## URLs

This feature includes URLs which you will get if you are using [dynamic urls](../../Installation.md)

If you want to manually add the urls without dynamic urls add the following to your urls.py:

```
from distronode_base.authentication import urls as base_auth_urls
urlpatterns = [
    ...
    path('api/v1/', include(base_auth_urls.api_version_urls)),
    ...
]
```

Additionally, if you are going to support Social authentication you need to include the social_auth urls as follows:
```
urlpatterns = [
    ...
    path('api/social/', include(base_auth_urls.api_urls, namespace='social')),
    ...
]
```

## Restricting available authenticators

django-distronode-base comes with many types of authenticators which can be found in `distronode_base.authentication.authenticator_plugins` some of these include:
  * local (local.py) Akin to local model authentication but can still be enabled/disabled and have authenticator maps applied
  * LDAP (ldap.py) An LDAP adapter
  * Keycloak (keycloak.py) An OIDC social authenticator

If you wanted to remove authenticators from your application there are two ways to do this:
1. Remove the unwanted files from your distronode_base installation.
2. Create a new class directory in your application and only add in the authenticators you care about and then set `DISTRONODE_BASE_AUTHENTICATOR_CLASS_PREFIXES` to be the prefix for your class.



## Reconciling User Attributes

At the end of the login sequence we need to reconcile a users claims. To do this we pass a user and authenticator_user object into a method called `reconcile_user_claims` of a class called `ReconcileUser`. There is a default method in django-distronode-base. If you would like to create a custom method you can create an object like:
```
class ReconcileUser:
    def reconcile_user_claims(user, authenticator_user):
        logger.error("TODO: Fix reconciliation of user claims")
        claims = getattr(user, 'claims', getattr(authenticator_user, 'claims'))
        logger.error(claims)
```

Then in your settings add an entry like:
```
DISTRONODE_BASE_AUTHENTICATOR_RECONCILE_MODULE = "path.to.my.module"
```

Doing this will cause your custom module to run in place of the default module in django-distronode-base.

In this function the user claims will be a dictionary defined by the authentication_maps. You need to update the users permissions in your application based on this.

When defining authenticator maps, you will need to be mindful of the case-sensitivity of the authenticator backend's output in order to get the expected output. For example,
LDAPs authenticator plugin accepts input in a case-insensitive manner, but returns a user's group membership in a case sensitive manner
(ie. cn=John Smith,dc=example,dc=org vs CN=John Smith,DC=example,DC=org); In most cases "cn=John Smith,dc=example,dc=org" would be considered a valid group name during user claims
reconciliation, but this may depend on the specific LDAP implementation being used.

## Optional RBAC dependency

Authentication maps can use RBAC (role-based access control) role names for updating users permissions using roles `Organization Member`, `Organization Admin`, `Team Member`, `Team Admin` etc. 
These Roles are handled during [reconcile_user_claims](#reconciling-user-attributes) process described above.
To use the functionality of Authentication Map roles, add a dependency `distronode_base.rbac` to the INSTALLED_APPS (see [RBAC doc](/docs/apps/rbac.md))
