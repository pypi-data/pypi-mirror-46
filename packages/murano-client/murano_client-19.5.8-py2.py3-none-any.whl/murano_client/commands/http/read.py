# pylint: disable=C0325,C0103
from murano_client.commands.http import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args

class ExoCommand(ExositeConnection):
    """Read the most recent data from a resource <alias>.

  usage:
    read <alias> [<alias>]... [options]

  options:
    -h --help                   Show this screen.
    <alias>                     A Murano Product resource.

    """
    Name = 'read'
    def execute(self):
        from murano_client.http import MuranoHTTP
        from murano_client.ini import Device

        if self.global_args.get('--file'):
            api = Device(self.global_args.get('--file'))
        else:
            api = MuranoHTTP(**build_api_opts_from_docopt_args(self.global_args))

        aliases = self.args.get('<alias>')
        resp_handler = api.http_read(
            aliases if isinstance(aliases, list) else [aliases])

        print("[{}] {}".format(resp_handler.code, resp_handler.body if 204 != resp_handler.code else "No Content"))
