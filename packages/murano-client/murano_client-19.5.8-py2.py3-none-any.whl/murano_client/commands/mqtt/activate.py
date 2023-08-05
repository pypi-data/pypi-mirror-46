# pylint: disable=C0325,C0103,C0111
from murano_client.commands.mqtt import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args

class ExoCommand(ExositeConnection):
    """Activate a Murano client (retreive the cik/token) via the MQTT protocol.

  usage:
    activate [options]

  options:
    -h --help                   Show this screen.
    -i --pid <pid>              The Product ID.
    -u --uuid <uuid>            Specify the username (mqtt only) or serial 
                                number (id) of the connecting client. During
                                provisioning or when using TLS Client Cert
                                auth, this is left blank/not used.
    -f --file <file>            All operations will use <file> as the Device state file. This file
                                is compatible with Device class objects. Will store <cik> and
                                provision as the Murano client described in its options. This
                                option has special support for configuring the GWE config file
                                by using 'gwe' as the <file> argument.

    """

    def execute(self):
        from murano_client.mqtt import MuranoMQTT
        from murano_client.ini import Device

        if self.global_args.get('--file'):
            mqtt_client = Device(self.global_args.get('--file'))
        else:
            mqtt_client = MuranoMQTT(**build_api_opts_from_docopt_args(self.global_args))

        mqtt_client.start(activate_only=True)
        print(mqtt_client.murano_token())






