import pytest

from distronode_base.resource_registry.models import Resource

from api.api.versioning import reverse


def assert_has_resource(list_response, obj=None):
    data = list_response.data
    assert 'resource' in data['results'][0]['summary_fields']
    resource_data = data['results'][0]['summary_fields']['resource']
    assert resource_data['distronode_id']
    resource = Resource.objects.filter(distronode_id=resource_data['distronode_id']).first()
    assert resource
    assert resource.content_object
    if obj:
        objects = [Resource.objects.get(distronode_id=entry['summary_fields']['resource']['distronode_id']).content_object for entry in data['results']]
        assert obj in objects


@pytest.mark.django_db
def test_organization_distronode_id(organization, admin_user, get):
    url = reverse('api:organization_list')
    response = get(url=url, user=admin_user, expect=200)
    assert_has_resource(response, obj=organization)


@pytest.mark.django_db
def test_team_distronode_id(team, admin_user, get):
    url = reverse('api:team_list')
    response = get(url=url, user=admin_user, expect=200)
    assert_has_resource(response, obj=team)


@pytest.mark.django_db
def test_user_distronode_id(rando, admin_user, get):
    url = reverse('api:user_list')
    response = get(url=url, user=admin_user, expect=200)
    assert_has_resource(response, obj=rando)
