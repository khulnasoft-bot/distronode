from django.db import migrations


def replace_content_guard(apps, schema_editor):
    """
    Enforce that all distributions have a content guard applied
    """
    DistronodeDistribution = apps.get_model('distronode', 'DistronodeDistribution')
    ContentRedirectContentGuard = apps.get_model('core', 'ContentRedirectContentGuard')

    OldContentGuard = apps.get_model('core', 'ContentGuard')

    # Delete the old content guard manually since it doesn't seem to get garbage collected
    # by deleting the content guard.
    OldContentGuard.objects.filter(name='ContentRedirectContentGuard').delete()

    content_guard, _ = ContentRedirectContentGuard.objects.get_or_create(
        name='ContentRedirectContentGuard',
        pulp_type='core.content_redirect'
    )

    DistronodeDistribution.objects.filter(pulp_type='distronode.distronode').update(
        content_guard=content_guard
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0087_taskschedule'),
        ('galaxy', '0025_add_content_guard_to_distributions'),
    ]

    operations = [
        migrations.RunPython(
            code=replace_content_guard,
            reverse_code=migrations.RunPython.noop
        ),
    ]
