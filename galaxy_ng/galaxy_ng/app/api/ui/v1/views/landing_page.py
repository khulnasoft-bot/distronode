from galaxy_ng.app.access_control import access_policy
from random import sample
from rest_framework.response import Response
from pulp_distronode.app.models import CollectionVersion, DistronodeDistribution
from galaxy_ng.app.models import Namespace
from galaxy_ng.app import settings
from galaxy_ng.app.api import base as api_base


class LandingPageView(api_base.APIView):
    permission_classes = [access_policy.LandingPageAccessPolicy]
    action = "retrieve"

    def get(self, request, *args, **kwargs):
        golden_name = settings.GALAXY_API_DEFAULT_DISTRIBUTION_BASE_PATH

        distro = DistronodeDistribution.objects.get(base_path=golden_name)
        repository_version = distro.repository.latest_version()
        collection_count = CollectionVersion.objects.filter(
            pk__in=repository_version.content, is_highest=True
        ).count()

        partner_count = Namespace.objects.count()

        # If there are no partners dont show the recommendation for it
        recommendations = {}
        if partner_count > 0:
            namespace = sample(list(Namespace.objects.all()), 1)[0]
            recommendations = {
                "recs": [
                    {
                        "id": "distronode-partner",
                        "icon": "bulb",
                        "action": {
                            "title": f"Check out our partner {namespace.company}",
                            "href": f"./distronode/automation-hub/partners/{namespace.name}",
                        },
                        "description": "Discover automation from our partners.",
                    }
                ]
            }

        data = {
            "estate": {
                "items": [
                    {
                        "id": "distronode-collections",
                        "count": collection_count,
                        "shape": {
                            "title": "Collections",
                            "href": "./distronode/automation-hub/",
                        },
                    },
                    {
                        "id": "distronode-partners",
                        "count": partner_count,
                        "shape": {
                            "title": "Partners",
                            "href": "./distronode/automation-hub/partners/",
                        },
                    },
                ],
            },
            "recommendations": recommendations,
            "configTryLearn": {
                "configure": [
                    {
                        "shape": {
                            "title": "Sync Red Hat certified collections",
                            "description": (
                                "Configure access to sync collections ",
                                "to Private Automation Hub.",
                            ),
                            "link": {
                                "title": "Get started",
                                "href": "./distronode/automation-hub/token",
                            },
                        },
                    }
                ],
                "try": [
                    {
                        "shape": {
                            "title": "Install Private Automation Hub",
                            "link": {
                                "title": "Get started",
                                "external": True,
                                "href": (
                                    "https://access.redhat.com/documentation/en-us/"
                                    "red_hat_distronode_automation_platform/2.1/html/"
                                    "red_hat_distronode_automation_platform_installation_guide/index"
                                ),
                            },
                        },
                    },
                    {
                        "shape": {
                            "title": "Manage repositories in Private Automation Hub",
                            "description": (
                                "Add community and privately developed collections "
                                "to your Private Automation Hub."
                            ),
                            "link": {
                                "title": "Get started",
                                "external": True,
                                "href": (
                                    "https://access.redhat.com/documentation/en-us/"
                                    "red_hat_distronode_automation_platform/2.1/html/"
                                    "publishing_proprietary_content_collections_in_"
                                    "automation_hub/index"
                                ),
                            },
                        },
                    },
                ],
                "learn": [
                    {
                        "shape": {
                            "title": "Connect Automation Hub to your automation infrastructure",
                            "link": {
                                "title": "Get started",
                                "external": True,
                                "href": (
                                    "https://docs.distronode.com/distronode-tower/latest/html/userguide/"
                                    "projects.html?extIdCarryOver=true&"
                                    "sc_cid=701f2000001Css5AAC#using-collections-in-tower"
                                ),
                            },
                        },
                    },
                    {
                        "shape": {
                            "title": "Learn about namespaces",
                            "description": (
                                "Organize collections content into namespaces users can access."
                            ),
                            "link": {
                                "title": "Learn more",
                                "external": True,
                                "href": (
                                    "https://access.redhat.com/documentation"
                                    "/en-us/red_hat_distronode_automation_platform/2.1/html"
                                    "/curating_collections_using_namespaces_in_automation_hub/index"
                                ),
                            },
                        },
                    },
                    {
                        "shape": {
                            "title": "Explore Red Hat certified collections",
                            "link": {
                                "title": "Learn more",
                                "external": True,
                                "href": "https://www.distronode.com/partners",
                            },
                        },
                    },
                ],
            },
        }

        return Response(data)
