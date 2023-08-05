# pylint: disable=C0325,C0103,C0111
import logging
import time
from murano_client.commands.mqtt import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args
from murano_client import logger

LOG = logger.getLogger('gdc.mqtt.sub')

class ExoCommand(ExositeConnection):
    """Subscribe to Murano device using the MQTT protocol.

  usage:
    subscribe [options]

  options:
    -h --help                       Show this screen.
    --disconnect-after <seconds>    Only subscribe for <seconds> seconds.

    """
    Name = 'subscribe'
    def execute(self):
        from murano_client.ini import Device
        from murano_client.mqtt import MuranoMQTT

        if self.global_args.get('--file'):
            mqtt_client = Device(self.global_args.get('--file'))
        else:
            mqtt_client = MuranoMQTT(**build_api_opts_from_docopt_args(self.global_args))

        def on_message(client, userdata, msg):
            _, resource, timestamp = msg.topic.split('/')[0:3]
            print("{}.{}={}".format(resource, timestamp, msg.payload.decode()))
        mqtt_client.on_message = on_message

        mqtt_client.start()

        try:
            start = time.time()
            mqtt_client.loop_start()
            while True:
                if mqtt_client.disconnect_after_seconds:
                    if time.time() - start >= mqtt_client.disconnect_after_seconds:
                        break
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
