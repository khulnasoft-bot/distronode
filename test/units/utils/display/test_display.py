# -*- coding: utf-8 -*-
# Copyright (c) 2020 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


from distronode.utils.display import Display


def test_display_basic_message(capsys, mocker, display_resource):
    # Disable logging
    mocker.patch('distronode.utils.display.logger', return_value=None)

    d = Display()
    d.display(u'Some displayed message')
    out, err = capsys.readouterr()
    assert out == 'Some displayed message\n'
    assert err == ''
