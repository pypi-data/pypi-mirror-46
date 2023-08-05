# pylint: disable=C0325,C0103,C0111,W1202,C0301
from __future__ import print_function
import logging
import sys
import time
from murano_client.commands.mqtt import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args
from murano_client import logger

LOG = logger.getLogger('gdc.mqtt.pub')

class ExoCommand(ExositeConnection):
    r"""Publish data to Murano resources using the MQTT protocol.

  usage:
    publish <topic> <value> [options]

  options:
    -h --help                   Show this screen.
    <topic>                     Mqtt topic to publish to Murano resource.
    <value>                     The value to publish. If <value> is -, publish
                                data line-by-line by piping data via stdin.
    -Q --qos <qos>              Determine the Quality of Service for published
                                messages (default=1). Possible values:

                                    0 - Message sent At Most Once (supported)
                                    1 - Message sent At Least Once (supported)
                                    2 - Message sent Exactly Once (not supported)

  examples:
    # Batch Record Example
    $ gdc --debug DEBUG \
         --host t41hp23nod8s00000.m2.exosite.io \
         --cacert Murano_Root_CA.cer \
         -C device-0001.pem \
         -K device-0001-key.pem \
         mqtt \
         publish \
         \$resource.batch \
         '[{"timestamp":1526046488, "values": {"test": "some test data"}}, {"timestamp":1526046488, "values": {"temperature": 98.7}}]'

    # Simple Publish Example
    $ gdc --pid f5330e5s8cho0000 \
         --cacert Murano_Root_CA.cer \
         -C device-0001.pem \
         -K device-0001-key.pem \
         mqtt \
         publish \
         \$resource/temperature \
         98.7
    """
    Name = 'publish'
    def execute(self):
        from murano_client.ini import Device
        from murano_client.mqtt import MuranoMQTT, MqttPublishHandler
        import time

        Qos = 1
        if self.global_args.get('--qos'):
            Qos = int(self.global_args.get('--qos'))

        if self.global_args.get('--file'):
            mqtt_client = Device(self.global_args.get('--file'))

        else:
            api_opts = build_api_opts_from_docopt_args(self.global_args)
            mqtt_client = MuranoMQTT(**api_opts)

        def on_message(client, userdata, msg):
            """ Override default on_message function. """
            LOG.debug("recieved message: {}".format(msg))

        mqtt_client.on_message = on_message
        mqtt_client.start()
        mqtt_client.loop_start()

        topic = self.args.get('<topic>')
        if self.args.get('<value>') == '-':
            LOG.debug("Reading from STDIN.")
            def read_stdin():
                readline = sys.stdin.readline()
                while readline:
                    yield readline
                    readline = sys.stdin.readline()
            for line in read_stdin():
                payload = line.strip()
                LOG.debug("topic={}, qos={}, payload={}".format(topic, Qos, payload))
                before = time.time()
                handler = MqttPublishHandler(mqtt_client.publish(
                    topic,
                    payload,
                    qos=Qos
                ))
                while not handler.is_published():
                    time.sleep(0.01)
        else:
            payload = self.args.get('<value>')
            LOG.debug("topic={}, qos={}, payload={}".format(topic, Qos, payload))
            start = time.time()
            handler = MqttPublishHandler(mqtt_client.publish(
                topic,
                payload,
                qos=Qos
            ))
            if mqtt_client.disconnect_after_seconds:
                while not handler.is_published() and not time.time()-start >= mqtt_client.disconnect_after_seconds:
                    time.sleep(0.1)
            else:
                while not handler.is_published():
                    time.sleep(0.1)
            sys.exit(0 if handler.is_published() else 1)
