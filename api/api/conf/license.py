# Copyright (c) 2016 Distronode, Inc.
# All Rights Reserved.

__all__ = ['get_license']


def _get_validated_license_data():
    from api.main.utils import get_licenser

    return get_licenser().validate()


def get_license():
    """Return a dictionary representing the active license on this instance."""
    return _get_validated_license_data()
