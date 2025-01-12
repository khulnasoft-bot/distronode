from django.db import migrations


def add_content_guard(apps, schema_editor):
    """
    Enforce that all distributions have a content guard applied
    """
    DistronodeDistribution = apps.get_model('distronode', 'DistronodeDistribution')
    ContentRedirectContentGuard = apps.get_model('galaxy', 'ContentRedirectContentGuard')

    content_guard, _ = ContentRedirectContentGuard.objects.get_or_create(
        name='ContentRedirectContentGuard',
        pulp_type='distronode.distronode'
    )

    DistronodeDistribution.objects.filter(
        content_guard=None,
        pulp_type='distronode.distronode'
    ).update(
        content_guard=content_guard
    )


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0024_contentredirectcontentguard'),
    ]

    operations = [
        migrations.RunPython(
            code=add_content_guard,
            reverse_code=migrations.RunPython.noop
        )
    ]
