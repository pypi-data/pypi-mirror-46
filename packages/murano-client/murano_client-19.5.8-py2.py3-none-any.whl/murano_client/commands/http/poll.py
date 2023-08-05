# pylint: disable=C0325,C0103
from murano_client.commands.http import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args

class ExoCommand(ExositeConnection):
    """Long poll <alias> for <request-timeout> since <if-modified-since>.

  usage:
    poll <alias> <request-timeout> [<if-modified-since>] [options]

  options:
    -h --help                   Show this screen.
    <alias>                     A Murano Product resource.
    <request-timeout>           The amount of time, in milliseconds, to long-poll on <alias>.
    <if-modified-since>         The timestamp (unix epoch) from which to check for new data on <alias>.


    """
    Name = 'poll'
    def execute(self):
        from murano_client.http import MuranoHTTP
        from murano_client.ini import Device

        if self.global_args.get('--file'):
            api = Device(self.global_args.get('--file'))
        else:
            api_opts = build_api_opts_from_docopt_args(self.global_args)
            api = MuranoHTTP(**api_opts)

        alias = self.args.get('<alias>')
        resp_handler = api.http_long_poll(
            alias,
            self.args.get('<request-timeout>'),
            self.args.get('<if-modified-since>') if self.args.get('<if-modified-since>') else None
        )

        print("[{}] {}".format(resp_handler.code, resp_handler.body))
