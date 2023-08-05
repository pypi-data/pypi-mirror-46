# pylint: disable=C0325,C0103,W0212
from murano_client.commands.http import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args
import docopt

class ExoCommand(ExositeConnection):
    """Record <value> to <alias> at time <timestamp>.

  usage:
    content [<subcommand> <content_name>] [options]

  subcommands:
    list
    info <content_name>
    download <content_name>

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

        if self.args.get('<subcommand>') == 'list':
            resp = api._http_listContent()
            if resp.status_code == 200:
                print(resp.text)
            else:
                print("[{}] {}".format(resp.status_code, resp.text))
            return
        if not self.args.get('<content_name>'):
            raise docopt.DocoptExit("subcommand: {!r} requires <content_name>."
                                    .format(self.args.get('<subcommand>')))
        if self.args.get('<subcommand>') == 'info':
            resp = api._http_getContentInfo(self.args.get('<content_name>'))
            print("[{}] {}".format(resp.status_code, resp.text))
            return
        elif self.args.get('<subcommand>') == 'download':
            resp = api._http_getContent(self.args.get('<content_name>'))
            if resp.status_code == 200:
                with open(self.args.get('<content_name>'), 'wb+') as __f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            __f.write(chunk)
            print("[{}] {}".format(resp.status_code, self.args.get('<content_name>')))
