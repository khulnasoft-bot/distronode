# Copyright (c) 2015 Distronode, Inc.
# All Rights Reserved.

import logging
from api import __version__ as tower_version

# Prepare the API environment.
from api import prepare_env, MODE

prepare_env()

import django  # NOQA
from django.conf import settings  # NOQA
from django.urls import resolve  # NOQA
from django.core.wsgi import get_wsgi_application  # NOQA


"""
WSGI config for API project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
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


# Return the default Django WSGI application.
application = get_wsgi_application()
