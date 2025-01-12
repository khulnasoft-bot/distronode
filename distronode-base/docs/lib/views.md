# DistronodeBaseView

django-distronode-base provides a view called `distronode_base.lib.utils.views.distronode_base.DistronodeBaseView` which is indirectly parent class for all views in django-distronode-base.

This view itself is subclassed from `rest_framework.views.APIView` and is intended to be subclassed from individual services like:

```
from rest_framework.viewsets import ModelViewSet
from distronode_base.lib.utils.views.distronode_base import DistronodeBaseView

class MyServiceBaseApiView(DistronodeBaseView):
    pass

class MyServiceModelViewSet(ModelViewSet, MyServiceBaseApiView):
    pass
```

## Changing the parent view

All views in django-distronode-base actually inherit from a class called `distronode_base.lib.utils.views.django_app_api.DistronodeBaseDjangoAppApiView` which inherits, by default from `DistronodeBaseView`.

However, if you already have an existing parent view with additional features you can override the view that `DistronodeBaseDjangoAppApiView` inherits from by setting the django setting `ANSIBLE_BASE_CUSTOM_VIEW_PARENT`.

For example, lets say you had a class like `my_app.views.DefaultAPIView` like:
```
from rest_framework.views import APIView

class DefaultAPIView(APIView):
    ...
    all my good stuff
    ...
```

And lets say all of your django views already inherit from this view. To make the django views in django-distronode-base inherit from this view simply add this to your settings:
```
ANSIBLE_BASE_CUSTOM_VIEW_PARENT = 'my_app.views.DefaultAPIView'
```

This will force `DistronodeBaseDjangoAppApiView` to inherit from `my_app.views.DefaultAPIView` instead of `distronode_base.lib.utils.views.distronode_base.DistronodeBaseView`.

If you want the goodness from `DistronodeBaseView` alongside your custom you, you can also make your custom view inherit from `distronode_base.lib.utils.views.distronode_base.DistronodeBaseView` like:
```
from distronode_base.lib.utils.views.distronode_base import DistronodeBaseView
from rest_framework.views import APIView

class DefaultAPIView(DistronodeBaseView):
    ...
    all my good stuff
    ...
```


## Adding extra related fields

There may be cases where the associative router does not provide a way to add specific related views to your view. As a way to help combat this the `DistronodeBaseView` class has a method defined called `extra_related_fields` which returns an empty dict (`{}`) by default. The entries expected in this dictionary are in the format:
```
{
    "string": "url",
}
```
Where string is the name of the field under the related section in the API and URL is the URL to that object.

For example, if `extra_related_fields` returned:
```
{
    'authenticators': reverse('user-authenticators-list', kwargs={'pk': obj.pk}),
}
```

We would expect to see the related fields for an object to be something along the lines of:
```
    "related": {
        "authenticators": "/api/gateway/v1/users/1/authenticators/"
    }
```

The URL for that entry, in our example, will be generated from the reverse lookup user-authenticators-list url and should end up as something like `/api/users/:id/authenticators/` where :id comes from the `obj.pk`. 

This can be particularly useful if a feature in DAB wants to extend a view that is created by a service. In this case you can create a MixIn like `distronode_base.oauth2_provider.views.user_mixin.DABOAuth2UserViewsetMixin` which can set `extra_related_fields` and then have the view in the service extend the Mixin. 
