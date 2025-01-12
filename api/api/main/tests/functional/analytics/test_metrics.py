import pytest

from prometheus_client.parser import text_string_to_metric_families
from api.main import models
from api.main.analytics.metrics import metrics
from api.api.versioning import reverse

EXPECTED_VALUES = {
    'api_system_info': 1.0,
    'api_organizations_total': 1.0,
    'api_users_total': 1.0,
    'api_teams_total': 1.0,
    'api_inventories_total': 1.0,
    'api_projects_total': 1.0,
    'api_job_templates_total': 1.0,
    'api_workflow_job_templates_total': 1.0,
    'api_hosts_total': 1.0,
    'api_hosts_total': 1.0,
    'api_schedules_total': 1.0,
    'api_sessions_total': 0.0,
    'api_status_total': 0.0,
    'api_running_jobs_total': 0.0,
    'api_instance_capacity': 100.0,
    'api_instance_consumed_capacity': 0.0,
    'api_instance_remaining_capacity': 100.0,
    'api_instance_cpu': 0.0,
    'api_instance_memory': 0.0,
    'api_instance_info': 1.0,
    'api_license_instance_total': 0,
    'api_license_instance_free': 0,
    'api_pending_jobs_total': 0,
    'api_database_connections_total': 1,
}


@pytest.mark.django_db
def test_metrics_counts(organization_factory, job_template_factory, workflow_job_template_factory):
    objs = organization_factory('org', superusers=['admin'])
    jt = job_template_factory('test', organization=objs.organization, inventory='test_inv', project='test_project', credential='test_cred')
    workflow_job_template_factory('test')
    models.Team(organization=objs.organization).save()
    models.Host(inventory=jt.inventory).save()
    models.Schedule(rrule='DTSTART;TZID=America/New_York:20300504T150000', unified_job_template=jt.job_template).save()

    output = metrics()
    gauges = text_string_to_metric_families(output.decode('UTF-8'))

    for gauge in gauges:
        for sample in gauge.samples:
            # name, label, value, timestamp, exemplar
            name, _, value, _, _ = sample
            assert EXPECTED_VALUES[name] == value


def get_metrics_view_db_only():
    return reverse('api:metrics_view') + '?dbonly=1'


@pytest.mark.django_db
def test_metrics_permissions(get, admin, org_admin, alice, bob, organization):
    assert get(get_metrics_view_db_only(), user=admin).status_code == 200
    assert get(get_metrics_view_db_only(), user=org_admin).status_code == 403
    assert get(get_metrics_view_db_only(), user=alice).status_code == 403
    assert get(get_metrics_view_db_only(), user=bob).status_code == 403
    organization.auditor_role.members.add(bob)
    assert get(get_metrics_view_db_only(), user=bob).status_code == 403

    bob.is_system_auditor = True
    assert get(get_metrics_view_db_only(), user=bob).status_code == 200


@pytest.mark.django_db
def test_metrics_http_methods(get, post, patch, put, options, admin):
    assert get(get_metrics_view_db_only(), user=admin).status_code == 200
    assert put(get_metrics_view_db_only(), user=admin).status_code == 405
    assert patch(get_metrics_view_db_only(), user=admin).status_code == 405
    assert post(get_metrics_view_db_only(), user=admin).status_code == 405
    assert options(get_metrics_view_db_only(), user=admin).status_code == 200
