# pylint: disable=I0011,W0312,C0301,C0103,W0123,W1202
r"""Gateway Device Client (GDC) Command-Line interface.

GDC is a light-weight cli for common tasks using the device-client library.

Usage:
  gdc [options] [<command>] [<args>...]

Commands:
    cfg             Interface for viewing and modifying gdc configuration settings.
    http            Use the HTTP(S) Device API from the command line.
    mqtt            Start and mqtt client. Only available on Python3.x environments.

Options:
    -h --help                   Show this screen.
    -v --version                Print the current version of device-client.
    -f --file <file>            All operations will use <file> as the Device state file. This file
                                is compatible with Device class objects. Will store <cik> and
                                provision as the Murano client described in its options. This
                                option has special support for configuring the GWE config file
                                by using 'gwe' as the <file> argument.
    -t --timeout <secs>         If provided, <secs> is used as HTTP Timeout (in seconds).
                                Not implemented in Mqtt.
    -H --host <host>            If provided, <host> is used as the server hostname for
                                HTTP requests.
    -P --port <port>            If provided, <port> is used as the TCP port used for
                                communicating with Murano (default=443).
    -d --debug <lvl>            Tune the debug output (DEBUG|INFO|WARNING|ERROR|CRITICAL).
                                Logs curl commands at DEBUG.
    -u --uuid <uuid>            The id or username of a Murano device..
    -C --cert <cert>            Use <cert> for Murano Provisioning of client described in
                                the certificate subject.
    -K --pkey <pkey>            Use <pkey> in TLS communication with Murano.
    -E --cacert <cacert>        Set the CA cert for the connection to the Murano Product
                                (default:/etc/exosite/gdc/Murano_Root_CA.cer). This can be
                                changed if using a PKI system.
    -k --token <token>          The authorization token or password of a Murano device.
    <command>                   The gdc subcommand name.
    <args>                      Supported arguments for <command>.

"""
from __future__ import print_function
import imp
import os
import sys
import pkgutil
import logging
import importlib
import pkg_resources
from docopt import docopt
from docopt import DocoptExit
import murano_client.commands
from murano_client import logger
from murano_client import __version__ as VERSION

LOG = logger.getLogger('gdc')
# streamh = logging.StreamHandler(sys.stdout)
# streamh.setFormatter(FORMATTER)
# LOG.addHandler(streamh)
# LOG.propagate = False


def main():
    global_args = docopt(__doc__, version=VERSION, options_first=True)
    # print(global_args)
    if global_args.get('--version'):
        print(VERSION)
        return

    if global_args.get('--debug'):
        LOG.setLevel(getattr(logging, global_args.get('--debug')))

    if global_args.get('<command>'):
        # Retrieve the command to execute.
        command_name = global_args.pop('<command>')
        # Retrieve the command arguments.
        argv = global_args.pop('<args>')
        if argv is None:
            argv = {}

        # Retrieve the module from the 'commands' package.
        try:
            if pkg_resources.resource_exists('murano_client.commands', command_name+'.py'):
                LOG.debug('loading from module: {}'.format(pkg_resources.resource_filename('murano_client.commands', command_name)))
                the_module = importlib.import_module('murano_client.commands.' + command_name)
            elif pkg_resources.resource_exists('murano_client.commands.' + command_name, '__init__.py'):
                LOG.debug('loading from package: {}'.format(pkg_resources.resource_filename('murano_client.commands', command_name)))
                the_module = importlib.import_module('murano_client.commands.' + command_name)

            command_class = getattr(the_module, 'Command')
        except ImportError as exc:
            raise DocoptExit("Cannot find command {!r}: {}"
                             .format(command_name, exc))

        global_args['--port'] = int(global_args.get('--port')) if global_args.get('--port') else None
        # Create an instance of the command.
        command = command_class(argv, global_args)

        # Execute the command.
        command.execute()
        return

    raise DocoptExit("provide an option or subcommand\n")

if __name__ == '__main__':
    main()

