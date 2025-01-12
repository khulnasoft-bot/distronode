# Copyright: Contributors to the Distronode project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations


import time
import pytest

from distronode.modules.unarchive import ZipArchive, TgzArchive


@pytest.fixture
def fake_distronode_module():
    return FakeDistronodeModule()


def max_zip_timestamp():
    """Return the max clamp value that will be selected."""
    try:
        return time.mktime(time.struct_time((2107, 12, 31, 23, 59, 59, 0, 0, 0)))
    except OverflowError:
        return time.mktime(time.struct_time((2038, 1, 1, 0, 0, 0, 0, 0, 0)))


class FakeDistronodeModule:
    def __init__(self):
        self.params = {}
        self.tmpdir = None


class TestCaseZipArchive:
    @pytest.mark.parametrize(
        'side_effect, expected_reason', (
            ([ValueError, '/bin/zipinfo'], "Unable to find required 'unzip'"),
            (ValueError, "Unable to find required 'unzip' or 'zipinfo'"),
        )
    )
    def test_no_zip_zipinfo_binary(self, mocker, fake_distronode_module, side_effect, expected_reason):
        mocker.patch("distronode.modules.unarchive.get_bin_path", side_effect=side_effect)
        fake_distronode_module.params = {
            "extra_opts": "",
            "exclude": "",
            "include": "",
            "io_buffer_size": 65536,
        }

        z = ZipArchive(
            src="",
            b_dest="",
            file_args="",
            module=fake_distronode_module,
        )
        can_handle, reason = z.can_handle_archive()

        assert can_handle is False
        assert expected_reason in reason
        assert z.cmd_path is None

    @pytest.mark.parametrize(
        ("test_input", "expected"),
        [
            pytest.param(
                "19800000.000000",
                time.mktime(time.struct_time((1980, 0, 0, 0, 0, 0, 0, 0, 0))),
                id="invalid-month-1980",
            ),
            pytest.param(
                "19791231.000000",
                time.mktime(time.struct_time((1980, 1, 1, 0, 0, 0, 0, 0, 0))),
                id="invalid-year-1979",
            ),
            pytest.param(
                "19810101.000000",
                time.mktime(time.struct_time((1981, 1, 1, 0, 0, 0, 0, 0, 0))),
                id="valid-datetime",
            ),
            pytest.param(
                "21081231.000000",
                max_zip_timestamp(),
                id="invalid-year-2108",
            ),
            pytest.param(
                "INVALID_TIME_DATE",
                time.mktime(time.struct_time((1980, 1, 1, 0, 0, 0, 0, 0, 0))),
                id="invalid-datetime",
            ),
        ],
    )
    def test_valid_time_stamp(self, mocker, fake_distronode_module, test_input, expected):
        mocker.patch(
            "distronode.modules.unarchive.get_bin_path",
            side_effect=["/bin/unzip", "/bin/zipinfo"],
        )
        fake_distronode_module.params = {
            "extra_opts": "",
            "exclude": "",
            "include": "",
            "io_buffer_size": 65536,
        }

        z = ZipArchive(
            src="",
            b_dest="",
            file_args="",
            module=fake_distronode_module,
        )
        assert z._valid_time_stamp(test_input) == expected


class TestCaseTgzArchive:
    def test_no_tar_binary(self, mocker, fake_distronode_module):
        mocker.patch("distronode.modules.unarchive.get_bin_path", side_effect=ValueError)
        fake_distronode_module.params = {
            "extra_opts": "",
            "exclude": "",
            "include": "",
            "io_buffer_size": 65536,
        }
        fake_distronode_module.check_mode = False

        t = TgzArchive(
            src="",
            b_dest="",
            file_args="",
            module=fake_distronode_module,
        )
        can_handle, reason = t.can_handle_archive()

        assert can_handle is False
        assert 'Unable to find required' in reason
        assert t.cmd_path is None
        assert t.tar_type is None
