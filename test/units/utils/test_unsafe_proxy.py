# -*- coding: utf-8 -*-
# (c) 2018 Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from distronode.utils.unsafe_proxy import DistronodeUnsafe, DistronodeUnsafeBytes, DistronodeUnsafeText, wrap_var
from distronode.module_utils.common.text.converters import to_text, to_bytes


def test_wrap_var_text():
    assert isinstance(wrap_var(u'foo'), DistronodeUnsafeText)


def test_wrap_var_bytes():
    assert isinstance(wrap_var(b'foo'), DistronodeUnsafeBytes)


def test_wrap_var_string():
    assert isinstance(wrap_var('foo'), DistronodeUnsafeText)


def test_wrap_var_dict():
    assert isinstance(wrap_var(dict(foo='bar')), dict)
    assert not isinstance(wrap_var(dict(foo='bar')), DistronodeUnsafe)
    assert isinstance(wrap_var(dict(foo=u'bar'))['foo'], DistronodeUnsafeText)


def test_wrap_var_dict_None():
    assert wrap_var(dict(foo=None))['foo'] is None
    assert not isinstance(wrap_var(dict(foo=None))['foo'], DistronodeUnsafe)


def test_wrap_var_list():
    assert isinstance(wrap_var(['foo']), list)
    assert not isinstance(wrap_var(['foo']), DistronodeUnsafe)
    assert isinstance(wrap_var([u'foo'])[0], DistronodeUnsafeText)


def test_wrap_var_list_None():
    assert wrap_var([None])[0] is None
    assert not isinstance(wrap_var([None])[0], DistronodeUnsafe)


def test_wrap_var_set():
    assert isinstance(wrap_var(set(['foo'])), set)
    assert not isinstance(wrap_var(set(['foo'])), DistronodeUnsafe)
    for item in wrap_var(set([u'foo'])):
        assert isinstance(item, DistronodeUnsafeText)


def test_wrap_var_set_None():
    for item in wrap_var(set([None])):
        assert item is None
        assert not isinstance(item, DistronodeUnsafe)


def test_wrap_var_tuple():
    assert isinstance(wrap_var(('foo',)), tuple)
    assert not isinstance(wrap_var(('foo',)), DistronodeUnsafe)
    assert isinstance(wrap_var(('foo',))[0], DistronodeUnsafe)


def test_wrap_var_tuple_None():
    assert wrap_var((None,))[0] is None
    assert not isinstance(wrap_var((None,))[0], DistronodeUnsafe)


def test_wrap_var_None():
    assert wrap_var(None) is None
    assert not isinstance(wrap_var(None), DistronodeUnsafe)


def test_wrap_var_unsafe_text():
    assert isinstance(wrap_var(DistronodeUnsafeText(u'foo')), DistronodeUnsafeText)


def test_wrap_var_unsafe_bytes():
    assert isinstance(wrap_var(DistronodeUnsafeBytes(b'foo')), DistronodeUnsafeBytes)


def test_wrap_var_no_ref():
    thing = {
        'foo': {
            'bar': 'baz'
        },
        'bar': ['baz', 'qux'],
        'baz': ('qux',),
        'none': None,
        'text': 'text',
    }
    wrapped_thing = wrap_var(thing)
    assert thing is not wrapped_thing
    assert thing['foo'] is not wrapped_thing['foo']
    assert thing['bar'][0] is not wrapped_thing['bar'][0]
    assert thing['baz'][0] is not wrapped_thing['baz'][0]
    assert thing['none'] is wrapped_thing['none']
    assert thing['text'] is not wrapped_thing['text']


def test_DistronodeUnsafeText():
    assert isinstance(DistronodeUnsafeText(u'foo'), DistronodeUnsafe)


def test_DistronodeUnsafeBytes():
    assert isinstance(DistronodeUnsafeBytes(b'foo'), DistronodeUnsafe)


def test_to_text_unsafe():
    assert isinstance(to_text(DistronodeUnsafeBytes(b'foo')), DistronodeUnsafeText)
    assert to_text(DistronodeUnsafeBytes(b'foo')) == DistronodeUnsafeText(u'foo')


def test_to_bytes_unsafe():
    assert isinstance(to_bytes(DistronodeUnsafeText(u'foo')), DistronodeUnsafeBytes)
    assert to_bytes(DistronodeUnsafeText(u'foo')) == DistronodeUnsafeBytes(b'foo')
