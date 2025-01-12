# Copyright (c) 2015 Distronode, Inc.
# All Rights Reserved.
import os
import logging
import django
from api import __version__ as tower_version

# Prepare the API environment.
from api import prepare_env, MODE
from channels.routing import get_default_application  # noqa

prepare_env()  # NOQA


"""
ASGI config for API project.

It exposes the ASGI callable as a module-level variable named ``channel_layer``.

For more information on this file, see
https://channels.readthedocs.io/en/latest/deploying.html
"""

if MODE == 'production':
    logger = logging.getLogger('api.main.models.jobs')
    try:
        fd = open("/var/lib/api/.tower_version", "r")
        if fd.read().strip() != tower_version:
            raise ValueError()
    except FileNotFoundError:
        pass
    except ValueError as e:
        logger.error("Missing or incorrect metadata for controller version.  Ensure controller was installed using the setup playbook.")
        raise Exception("Missing or incorrect metadata for controller version.  Ensure controller was installed using the setup playbook.") from e


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()
channel_layer = get_default_application()
