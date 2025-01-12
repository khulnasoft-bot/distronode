from django.db import migrations

def create_inbound_repo_per_namespace(apps, schema_editor):
    DistronodeRepository = apps.get_model('distronode', 'DistronodeRepository')
    DistronodeDistribution = apps.get_model('distronode', 'DistronodeDistribution')
    Namespace = apps.get_model('galaxy', 'Namespace')
    db_alias = schema_editor.connection.alias

    for namespace in Namespace.objects.using(db_alias).all():
        name = f'inbound-{namespace.name}'
        repo = DistronodeRepository.objects.using(db_alias).create(
            name=name,
            pulp_type='distronode.distronode',
        )
        DistronodeDistribution.objects.using(db_alias).create(
            name=name,
            base_path=name,
            repository=repo,
            pulp_type='distronode.distronode',
        )


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0002_add_synclist_20200330_squashed'),
    ]

    operations = [
        migrations.RunPython(create_inbound_repo_per_namespace, elidable=True)
    ]
