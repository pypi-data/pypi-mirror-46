# pylint: disable=C0325,C0103,C0111
from __future__ import print_function
import os
import sys
import logging
import docopt
import six
from murano_client.atomicconfigparser import atomicconfigparser as CfgParser
from murano_client.atomicconfigparser import NoOptionError, NoSectionError
from murano_client import logger
if six.PY2:
    prompt = raw_input
elif six.PY3:
    prompt = input

LOG = logger.getLogger('gdc.cfg')

class Command(object):
    """System wide INI file editor and viewer.

  usage:
    cfg <file> [get <section> <option>]
    cfg <file> set <section> [<option> <value> -U]

  options:
    -h --help                   Show this screen.
    get                         Print a section or option.
    set                         Update or create a new section or option.
    <file>                      The name of the INI file.
    <section>                   The name of the INI file section.
    <option>                    The name of the INI option.
    <value>                     The name of the INI option value.
    --unset -U                  Remove the section or option.

    """
    Name = 'cfg'
    def __init__(self, command_args, global_args):
        """
        Initialize the commands.
        :param command_args: arguments of the command
        :param global_args: arguments of the program
        """
        self.args = docopt.docopt(self.__doc__, argv=command_args)
        global_args.update({k:v for k, v in self.args.items() if v})
        self.global_args = global_args

        if self.global_args.get('--debug'):
            LOG.setLevel(eval('logging.'+self.global_args.get('--debug')))

    def execute(self):

        the_file = self.global_args.get('<file>')

        if not os.path.exists(the_file):
            print("No config file exists at: {}".format(the_file))
            sys.exit(-1)

        parser = CfgParser(allow_no_value=True)
        parser.read(the_file)

        if self.global_args.get('get'):
            to_print = ''
            try:
                if self.global_args.get('<section>') and self.global_args.get('<option>'):
                    to_print = parser.get(
                        self.global_args.get('<section>'),
                        self.global_args.get('<option>')
                    )
                elif self.global_args.get('<section>'):
                    for item in parser.items(self.global_args.get('<section>')):
                        if item[1]:
                            to_print += item[0] + ' = ' + item[1]
                        else:
                            to_print += item[0]
                        to_print += '\n'
                else:
                    to_print = open(the_file, 'r').read()
                print(to_print, end='')
            except NoOptionError as exc:
                print(exc.message)
                sys.exit(-1)
            except NoSectionError as exc:
                print(exc.message)
                sys.exit(-1)
        elif self.global_args.get('set'):
            with open(the_file, 'r') as cfg:
                parser.readfp(cfg)
                if self.global_args.get('<section>'):
                    if not self.global_args.get('--unset'):
                        if not parser.has_section(self.global_args.get('<section>')):
                            parser.add_section(self.global_args.get('<section>'))
                        if self.global_args.get('<option>'):
                            parser.set(
                                self.global_args.get('<section>'),
                                self.global_args.get('<option>'),
                                self.global_args.get('<value>')
                            )
                    else:
                        if not self.global_args.get('<option>'):
                            # unset used only with section
                            parser.remove_section(self.global_args.get('<section>'))
                        else:
                            parser.remove_option(
                                self.global_args.get('<section>'),
                                self.global_args.get('<option>')
                            )
                    parser.write(the_file)
        else:
            print(open(the_file, 'r').read())
