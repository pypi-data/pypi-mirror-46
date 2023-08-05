# -*- coding: utf-8 -*-

"""Tests for `hypothit` package."""

from __future__ import absolute_import, division, print_function

import re
import textwrap

import pytest

from hypothit import cli


def test_function_argument_names():
    assert cli.function_argument_names('') == []
    assert cli.function_argument_names('a=None') == ['a']
    assert cli.function_argument_names('foo=None, bar=baz(a, b=42)') == ['foo', 'bar']


def test_convert_assume():
    assert cli.convert_assume('') == ''
    assert cli.convert_assume('42') == '    assume(42)\n'
    assert cli.convert_assume('\t42  ') == '    assume(42)\n'


def test_convert_setup():
    assert cli.convert_setup('') == ''
    assert cli.convert_setup('import foo; foo.bar()') == 'import foo; foo.bar()\n'
    assert cli.convert_setup('\t42  ') == '42\n'


def test_main_trial_falsify(capsys):
    rc = cli.main([
        'trial',
        '--given', 'a=integers()',
        '--assume', 'a!=0',
        'assert a==42',
    ])
    assert rc == 2

    captured = capsys.readouterr()

    assert captured.out == textwrap.dedent('''\
        from hypothesis import given, assume
        from hypothesis.strategies import integers


        @given(a=integers())
        def inner(a):
            assume(a!=0)
            assert a==42

        inner()
        ---
        Falsifying example: inner(a=1)
        '''
    )

    traceback_lines = captured.err.rstrip('\n').split('\n')
    assert traceback_lines[0] == 'Traceback (most recent call last):'
    assert traceback_lines[-1] == 'AssertionError'


def test_main_trial_satisfy(capsys):
    rc = cli.main([
        'trial',
        '--given', 'a=integers()',
        '--assume', 'a!=0',
        'assert a is not None',
    ])
    assert rc == 0

    captured = capsys.readouterr()

    assert captured.out == textwrap.dedent('''\
        from hypothesis import given, assume
        from hypothesis.strategies import integers


        @given(a=integers())
        def inner(a):
            assume(a!=0)
            assert a is not None

        inner()
        ---
        No falsifying example found
        '''
    )

    assert captured.err == ''
