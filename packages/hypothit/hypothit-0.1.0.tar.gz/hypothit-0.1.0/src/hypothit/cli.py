# coding=utf-8

'''
Run Hypothesis property-based tests
'''

from __future__ import absolute_import, division, print_function

import argparse
import traceback
import ast

import hypothit


COMMAND_TEMPLATE = '''\
from hypothesis import given, assume
from hypothesis.strategies import integers

{setup}\

@given({given})
def inner({arguments}):
{assume}\
    {assertion}

inner()
'''


def function_argument_names(argument_spec):
    """Return the argument names from a Python function argument spec.

    >>> function_argument_names('foo=None, bar=baz(a, b=42)')
    ['foo', 'bar']
    """
    func_src = "def f({spec}): pass".format(spec=argument_spec)
    ast_module = ast.parse(func_src)
    ast_function = ast_module.body[0]
    assert ast_function.name == 'f'
    ast_arguments = ast_function.args  # Single _ast.arguments object
    ast_args = ast_arguments.args
    try:
        # Python 3.x
        arg_names = [arg.arg for arg in ast_args]
    except AttributeError:
        # Python 2.x
        arg_names = [arg.id for arg in ast_args]
    return arg_names


def show_version():
    print(hypothit.__version__)
    return 0


def convert_assume(expression):
    expression = expression.strip()
    if expression:
        return '    assume({})\n'.format(expression)
    return expression


def convert_setup(statement):
    statement = statement.strip()
    if statement:
        return '{}\n'.format(statement)
    return statement


def trial(args):
    '''
    Run a single test
    '''
    function_arguments = function_argument_names(args.given)

    src = COMMAND_TEMPLATE.format(
        given=args.given,
        arguments=', '.join(function_arguments),
        assume=args.assume,
        setup=args.setup,
        assertion=args.assertion,
    )

    if args.show:
        print(src, end='---\n')

    try:
        g = {}
        exec(src, g)
    except:
        # Print the traceback of any exeception thrown by exec() with line
        # numbers relative to the templated code, not this file.
        traceback.print_exc()
        return 2

    print('No falsifying example found')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.strip())
    parser.add_argument('--version', action='store_true')

    subparsers = parser.add_subparsers(title='commands')

    trial_parser = subparsers.add_parser('trial', help=trial.__doc__)
    trial_parser.add_argument('--given', metavar='STRATEGIES', required=True)
    trial_parser.add_argument('--assume', default='', metavar='CONDITION', type=convert_assume)
    trial_parser.add_argument('--setup', default='', type=convert_setup)
    trial_parser.add_argument('--show', default=True, type=bool)
    trial_parser.add_argument('assertion')
    trial_parser.set_defaults(command=trial)

    args = parser.parse_args(argv)

    if args.version:
        return show_version()

    try:
        command = args.command
    except AttributeError:
        parser.print_help()
        return 1

    return command(args)


if __name__ == '__main__':
    import sys
    sys.exit(main())
