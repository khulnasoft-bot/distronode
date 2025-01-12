# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Toshio Kuratomi <tkuratomi@distronode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from distronode import context


class FakeOptions:
    pass


def test_set_global_context():
    options = FakeOptions()
    options.tags = [u'production', u'webservers']
    options.check_mode = True
    options.start_at_task = u'Start with くらとみ'

    expected = frozenset((('tags', (u'production', u'webservers')),
                          ('check_mode', True),
                          ('start_at_task', u'Start with くらとみ')))

    context._init_global_context(options)
    assert frozenset(context.CLIARGS.items()) == expected
