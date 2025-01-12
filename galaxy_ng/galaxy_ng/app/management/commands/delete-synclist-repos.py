import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from pulp_distronode.app.models import DistronodeDistribution, DistronodeRepository

from galaxy_ng.app.models import SyncList

log = logging.getLogger(__name__)


def set_synclist_distro_by_name(name):
    distro = DistronodeDistribution.objects.get(name=name)
    synclist = SyncList.objects.get(name=name)
    synclist.distribution = distro
    synclist.save()


class Command(BaseCommand):
    """This command deletes DistronodeRepository in the format of #####-synclists.

    Example:
    django-admin delete-synclist-repos --number 100 --hard
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, help="Max number to delete, for batching", required=True
        )
        parser.add_argument(
            "--hard",
            action="store_true",
            help="Flag --hard does not skip any synclist repos",
            default=False,
            required=False,
        )

    def handle(self, *args, **options):
        log.info("Deleting DistronodeRepository in the format of #####-synclists")
        number_to_delete = options["number"]

        synclist_repos = DistronodeRepository.objects.filter(name__endswith="-synclist")

        if options["hard"]:
            log.info("Peforming delete of all repos")
            for repo in synclist_repos[:number_to_delete]:
                log.info(f"Deleting repo: {repo}")
                with transaction.atomic():
                    set_synclist_distro_by_name(repo.name)
                    repo.delete()

        else:
            log.info("Peforming delete, will skip repo if does not find expected distro")
            for repo in synclist_repos[:number_to_delete]:
                log.info(f"Deleting repo: {repo}")
                with transaction.atomic():
                    if not DistronodeDistribution.objects.filter(name=repo.name):
                        log.error(
                            f"No distribution found matching the repo name '{repo.name}', skipping"
                        )
                        continue
                    distro = DistronodeDistribution.objects.filter(name=repo.name).first()
                    if distro.repository.name != "published":
                        log.error(
                            f"Distribution '{repo.name}' does not point at 'pubished' repo "
                            f"but points at {distro.repository.name}, skipping"
                        )
                        continue
                    set_synclist_distro_by_name(repo.name)
                    repo.delete()
