#!/usr/bin/env python
from __future__ import absolute_import, print_function

import click
import os
import sys
import subprocess
import tempfile
import optparse

if os.uname()[0] == 'Darwin':
    DEFAULT_DEBUGGER = 'lldb'
else:
    DEFAULT_DEBUGGER = 'gdb'


def inject(pid, command, debugger=DEFAULT_DEBUGGER):
    """
    Executes a command in a running Python process.
    """
    command = command.replace('\n','').replace('"', '\\"')

    with tempfile.NamedTemporaryFile() as f:
        if debugger == 'gdb':
            print('call PyGILState_Ensure()', file=f)
            print('call PyRun_SimpleString("%s")' % command, file=f)
            print('call PyGILState_Release($1)', file=f)

            args = ['gdb', '-p', str(pid), '--batch', '--command', f.name]
        elif debugger == 'lldb':
            print('call (PyGILState_STATE)PyGILState_Ensure()', file=f)
            print('call (int)PyRun_SimpleString("%s")' % command, file=f)
            print('call (void)PyGILState_Release($0)', file=f)
            print('exit', file=f)

            args = ['lldb', '-p', str(pid), '-s', f.name]
        else:
            raise ValueError('unknown debugger')

        f.flush()

        with open(os.devnull) as stdin:
            subprocess.check_call(args, close_fds=True, stdin=stdin)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('pid', type=click.INT)
@click.option('--debugger', default=DEFAULT_DEBUGGER, metavar='DEBUGGER',
              help='The debugger to send the command with.')
@click.option('--output', default='meliae-dump-{pid}.json', metavar='FILENAME',
              help='Where to output the dump file.')
def memdump(pid, debugger, output):
    """
    Generates a Maliae dump file.

    This requires the 'meliae' Python module:

        pip install --allow-external meliae --allow-unverified meliae meliae

    """
    try:
        __import__('meliae')
    except ImportError:
        print("You need to install the 'meliae' package:", file=sys.stderr)
        print("", file=sys.stderr)
        print("  pip install --allow-external meliae --allow-unverified meliae meliae", file=sys.stderr)
        return

    path = os.path.join(os.getcwd(), output.format(pid=pid))

    command = (
        "from meliae import scanner;"
        "scanner.dump_all_objects('{path}');"
    ).format(path=path)

    inject(pid, command, debugger)

    print('Dumping Meliae output to {}'.format(path), file=sys.stdout)


if __name__ == '__main__':
    cli()
