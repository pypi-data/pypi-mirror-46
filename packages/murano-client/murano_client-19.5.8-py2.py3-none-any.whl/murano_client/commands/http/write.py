# pylint: disable=C0325,C0103
from murano_client.commands.http import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args
import sys


class ExoCommand(ExositeConnection):
    """Write <value> to <alias> resource.

  usage:
    write <alias> <data> [options]

  options:
    -h --help                   Show this help screen.
    <alias>                     A Murano Product resource.
    <data>                      The data to write or record. If <data> is the '-'
                                character, then data is read from stdin and a payload
                                is generated from each line (i.e. '\\n' delineated).

    """
    Name = 'write'
    def execute(self):
        from murano_client.http import MuranoHTTP
        from murano_client.ini import Device

        if self.global_args.get('--file'):
            api = Device(self.global_args.get('--file'))
        else:
            api_opts = build_api_opts_from_docopt_args(self.global_args)
            api = MuranoHTTP(**api_opts)

        alias = self.args.get('<alias>')
        data = self.args.get('<data>')
        if data == '-':
            sys.stderr.write("Reading from STDIN.\n")
            def read_stdin():
                """ generator for reading stdin. """
                readline = sys.stdin.readline()
                while readline:
                    yield readline
                    readline = sys.stdin.readline()
            for line in read_stdin():
                payload = line.strip()
                resp_handler = api.http_write(alias, payload)
                print("[{}] {}".format(resp_handler.code, resp_handler.body))

        else:
            resp_handler = api.http_write(alias, data)
            print("[{}] {}".format(resp_handler.code, resp_handler.body))
