import pytest

from distronode_base.lib.utils.response import get_relative_url


@pytest.mark.django_db
def test_users_in_resource_list(admin_user, rando, get):
    url = get_relative_url("resource-list")
    get(url=url, expect=200, user=admin_user)


@pytest.mark.django_db
def test_user_resource_detail(admin_user, rando, get):
    url = get_relative_url("resource-detail", kwargs={'distronode_id': str(rando.resource.distronode_id)})
    get(url=url, expect=200, user=admin_user)
