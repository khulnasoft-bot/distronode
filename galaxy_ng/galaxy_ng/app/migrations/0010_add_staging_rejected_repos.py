from django.db import migrations

STAGING = 'staging'
REJECTED = 'rejected'

def add_repos_staging_rejected(apps, schema_editor):
    DistronodeRepository = apps.get_model('distronode', 'DistronodeRepository')
    DistronodeDistribution = apps.get_model('distronode', 'DistronodeDistribution')
    RepositoryVersion = apps.get_model('core', 'RepositoryVersion')
    db_alias = schema_editor.connection.alias

    def create_repo_and_distro(name):
        repo = DistronodeRepository.objects.using(db_alias).create(
            name=name,
            pulp_type='distronode.distronode',
            next_version=1,
        )
        RepositoryVersion.objects.using(db_alias).create(
            repository=repo,
            number=0,
            complete=True,
        )
        DistronodeDistribution.objects.using(db_alias).create(
            name=name,
            base_path=name,
            repository=repo,
            pulp_type='distronode.distronode',
        )

    if not DistronodeRepository.objects.using(db_alias).filter(name=STAGING):
        create_repo_and_distro(STAGING)

    if not DistronodeRepository.objects.using(db_alias).filter(name=REJECTED):
        create_repo_and_distro(REJECTED)


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0009_add_repoversion_to_inbound_repos'),
    ]

    operations = [
        migrations.RunPython(add_repos_staging_rejected),
    ]
