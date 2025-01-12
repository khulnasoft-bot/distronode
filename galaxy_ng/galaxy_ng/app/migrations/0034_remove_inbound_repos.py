from django.db import migrations


def remove_inbound_repos(apps, schema_editor):
    """Remove inbound repositories and point distribution to staging repository"""

    DistronodeDistribution = apps.get_model('distronode', 'DistronodeDistribution')
    DistronodeRepository = apps.get_model('distronode', 'DistronodeRepository')

    repos = DistronodeRepository.objects.filter(name__startswith="inbound-")

    staging_repo = DistronodeRepository.objects.get(name="staging")

    DistronodeDistribution.objects.filter(name__startswith="inbound-").update(
        repository_id=staging_repo.pk
    )

    repos.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0033_update_validated_repo'),
    ]

    operations = [
        migrations.RunPython(
            code=remove_inbound_repos,
            reverse_code=migrations.RunPython.noop
        )
    ]
