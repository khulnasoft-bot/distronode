from unittest import mock

from distronode_base.authentication.models.authenticator import Authenticator
from distronode_base.lib.checks import check_charfield_has_max_length


def test_check_charfield_has_max_length_fails():
    with mock.patch.object(Authenticator._meta.get_field('type'), 'max_length', new=None):
        errors = check_charfield_has_max_length(None)
        assert len(errors) == 1
        assert errors[0].id == 'distronode_base.E001'
