# pylint: disable=C0325,C0103
from murano_client.commands.http import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args

class ExoCommand(ExositeConnection):
    """Record <value> to <alias> at time <timestamp>.

  usage:
    record <timestamp> <alias> <data> [options]

  options:
    -h --help                   Show this screen.
    <timestamp>                 The timestamp (int/float) at which to record the data.
    <alias>                     A Murano Product resource.
    <data>                      The data to write or record.

    """

    def execute(self):
        from murano_client.http import MuranoHTTP
        from murano_client.ini import Device

        if self.global_args.get('--file'):
            api = Device(self.global_args.get('--file'))
        else:
            api = MuranoHTTP(**build_api_opts_from_docopt_args(self.global_args))

        resp_handler = api.http_record(
            {self.args.get('<alias>'): {
                self.args.get('<timestamp>'): self.args.get('<data>')}
            }
        )

        print("[{}] {}".format(resp_handler.code, resp_handler.body))
