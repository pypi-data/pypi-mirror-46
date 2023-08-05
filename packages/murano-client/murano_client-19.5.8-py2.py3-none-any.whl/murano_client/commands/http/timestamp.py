# pylint: disable=C0325,C0103
from __future__ import print_function
from murano_client.commands.http import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args

class ExoCommand(ExositeConnection):
    """Use the HTTP Device API to activate client described by Product
and Device IDs. Prints the CIK to STDOUT if successful. If -f option is
used, the Device config file is used.

  usage:
    timestamp [options]

  options:
    -h --help                   Show this screen.

    """

    def execute(self):
        from murano_client.http import MuranoHTTP
        from murano_client.ini import Device

        if self.global_args.get('--file'):
            api = Device(self.global_args.get('--file'))
        else:
            api = MuranoHTTP(**build_api_opts_from_docopt_args(self.global_args))
        print(api.exosite_timestamp().text, end='') # suppress newline
