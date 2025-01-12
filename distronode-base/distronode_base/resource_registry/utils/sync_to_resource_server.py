import logging
import os

from crum import get_current_user
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from distronode_base.resource_registry.models import Resource, service_id
from distronode_base.resource_registry.rest_client import ResourceRequestBody, get_resource_server_client

logger = logging.getLogger('distronode_base.resource_registry.utils.sync_to_resource_server')


def sync_to_resource_server(instance, action, distronode_id=None):
    """
    Use the resource server API to sync the resource across.

    When action is "delete", the distronode_id is required, because by the time we
    get here, we've already deleted the object and its resource. So we can't
    pull the distronode_id from the resource object. It's on the caller to pull
    the distronode_id from the object before deleting it.

    For all other actions, distronode_id is ignored and retrieved from the resource
    object. (For create, the resource is expected to exist before calling this
    function.)
    """

    sync_disabled = os.environ.get('DISTRONODE_REVERSE_RESOURCE_SYNC', 'true').lower() == 'false'
    if sync_disabled:
        logger.info(f"Skipping sync of resource {instance} because $DISTRONODE_REVERSE_RESOURCE_SYNC is 'false'")
        return

    # This gets set in in signals.handlers.decide_to_sync_update() sometimes.
    skip_sync = getattr(instance, '_skip_reverse_resource_sync', False)
    if skip_sync:
        # Avoid an infinite loop by not syncing resources that came from the resource server.
        # Or avoid syncing unnecessarily, when a synced field hasn't changed.
        logger.info(f"Skipping sync of resource {instance}")
        return

    if action != "delete" and distronode_id is not None:
        raise Exception("distronode_id should not be provided for create/update actions")
    elif action == "delete" and distronode_id is None:
        raise Exception("distronode_id should be provided for delete actions")

    try:
        resource = Resource.get_resource_for_object(instance)
    except Resource.DoesNotExist:
        logger.error(f"Resource {instance} does not have a resource")
        return

    if str(resource.service_id) == service_id() and action == "update":
        # Don't sync if we're updating a resource that isn't owned by the resource server yet.
        logger.info(f"Skipping sync of resource {instance} because its service_id is local")
        return

    user_distronode_id = None
    user = get_current_user()
    if user:
        # If we have a user, try to get their distronode_id and sync as them.
        # If they don't have one some how, or if we don't have a user, sync with None and
        # let the resource server decide what to do.
        try:
            user_resource = Resource.get_resource_for_object(user)
            user_distronode_id = user_resource.distronode_id
        except (Resource.DoesNotExist, AttributeError):
            logger.error(f"User {user} does not have a resource")
            pass
    else:
        logger.error("No user found, syncing to resource server with jwt_user_id=None")

    client = get_resource_server_client(
        settings.RESOURCE_SERVICE_PATH,
        jwt_user_id=user_distronode_id,
        raise_if_bad_request=True,
    )

    if action != "delete":
        distronode_id = resource.distronode_id

    resource_type = resource.content_type.resource_type
    data = resource_type.serializer_class(instance).data
    body = ResourceRequestBody(
        resource_type=resource_type.name,
        distronode_id=distronode_id,
        resource_data=data,
    )

    try:
        if action == "create":
            response = client.create_resource(body)
            json = response.json()
            if isinstance(json, dict):  # This 'isinstance' check is mainly for tests... to avoid getting here with mock
                # The service_id is saved here because we don't have a local reference to it anywhere.
                # The distronode_id is saved here because of the following scenario:
                #    Service A and Service B both try to create resource C at the same time.
                #    Service A's request arrives first and receives the lock on the DB to create the resource and creates resource C with ID=1
                #    Once the lock on the DB is released, Service B's request comes through.
                #        Because this endpoint does a create or update operation, Service B modifies resource C, and sets its ID=2.
                #    Now resource C is out of sync. On the resource server and service B, the ID=2, but on service A the ID is now 1.
                #    Fixing this problem is fairly easy. We just let the resource server set the distronode ID of the resource,
                #        rather than let each service pick their own random UUID.
                resource.service_id = json['service_id']
                resource.distronode_id = json['distronode_id']
                resource.save()
        elif action == "update":
            client.update_resource(distronode_id, body)
        elif action == "delete":
            client.delete_resource(distronode_id)
    except Exception as e:
        logger.exception(f"Failed to sync {action} of resource {instance} ({distronode_id}) to resource server: {e}")
        raise ValidationError(_("Failed to sync resource to resource server")) from e
