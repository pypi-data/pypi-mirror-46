# pylint: disable=W1202
"""
    Namespace for http subcommand of gdc.commands.
"""

import sys
import logging
import six
import docopt
import pkg_resources
import importlib
from murano_client import logger

LOG = logger.getLogger('gdc.http')

class Command(object): # ExositeConnection
    """Use methods of the HTTP(S) Device API.

  usage:
    http <command> [<args>...] [options]

  commands:
    timestamp         Get the Murano timestamp.
    activate          Get a CIK/Token from a Murano Product for an id.
    read              Read resource described by <alias>.
    poll              Long poll <alias> for <request-timeout> since <if-modified-since>.
    write             Write <value> to <alias> resource.
    record            Record <value> to <alias> at time <timestamp>.
    content           Download content, get content info and list content.

  options:
    -h --help                   Show this help screen.
    -t --timeout <secs>         If provided, <secs> is used as HTTP Timeout (in seconds).
                                Not implemented in Mqtt.
    -H --host <host>            If provided, <host> is used as the server hostname for
                                HTTP requests.
    -d --debug <lvl>            Turn on verbose debug output. Also logs curl commands.
    -u --uuid <uuid>            Specify the id of the connecting client (mqtt only).
    -f --file <file>            All operations will use <file> as the Device state file. This file
                                is compatible with Device class objects. Will store <cik> and
                                provision as the Murano client described in its options. This
                                option has special support for configuring the GWE config file
                                by using 'gwe' as the <file> argument.
    -C --cert <cert>            Use <cert> for Murano Provisioning of client described in
                                  the certificate subject.
    -K --pkey <pkey>            Use <pkey> in TLS communication with Murano.
    <cik>                       A CIK (Client Interface Key) or Token.
    <command>                   The HTTP(S) Device API method name.
    <args>                      Args for subcommands.

    """
    Name = 'http'
    def __init__(self, command_args, global_args):
        """
        Initialize the commands.
        :param command_args: arguments of the command
        :param global_args: arguments of the program
        """
        self.args = docopt.docopt(self.__doc__, argv=command_args, options_first=True)
        global_args.update({k:v for k, v in self.args.items() if v})
        self.global_args = global_args

        if self.global_args.get('--debug'):
            LOG.setLevel(getattr(logging, self.global_args.get('--debug')))
            LOG.debug('global_args: {}'.format(self.global_args))

    def execute(self, **exc_args):
        """Execute the commands"""
        # Retrieve the command to execute.
        command_name = self.args.pop('<command>')
        # Retrieve the command arguments.
        command_args = self.args.pop('<args>')

        try:
            if pkg_resources.resource_exists('murano_client.commands.http', command_name+'.py'):
                LOG.debug('loading from module: {}'
                          .format(pkg_resources.resource_filename(
                              'murano_client.commands.http', command_name+'.py')))
                the_module = importlib.import_module('murano_client.commands.http.' + command_name)
            command_class = getattr(the_module, 'ExoCommand')

        except ImportError as exc:
            LOG.debug("{}: cannot find command {!r}: {}".format(self.Name, command_name, exc))
            raise docopt.DocoptExit()
        except AttributeError:
            LOG.debug('{}: unknown command: {}'.format(self.Name, command_name))
            raise docopt.DocoptExit()

        # Create an instance of the command and execute it
        command_class(command_args, self.global_args).execute()
