# pylint: disable=C0103,C0301,C0325,W1202

import ssl
import logging
import time
from threading import Timer
import six
from paho.mqtt.client import Client as PahoSNIMqttClient
from murano_client import logger
from murano_client import BaseMuranoClient, __version__
if six.PY2:
    from urlparse import urlparse
elif six.PY3:
    from urllib.parse import urlparse

PahoReturnCodes = {
    0: "success, connection accepted",
    1: "connection refused, bad protocol",
    2: "refused, client-id error",
    3: "refused, service unavailable",
    4: "refused, bad username or password",
    5: "refused, not authorized"
}

LOG = logger.getLogger(__name__)


class MqttMsg(object):
    """
        This class is a wrapper class for MQTT
        messages. It is likely that he paho client
        will be used basicaly forever, but in the
        event that the protocol library changes,
        wrapping the message object will help
        us change the underlying library without
        breaking changes propagating upstream.
    """
    def __init__(self, msg):
        self.dup = msg.dup
        self.info = msg.info
        self.mid = msg.mid
        self.payload = msg.payload
        self.qos = msg.qos
        self.retain = msg.retain
        self.state = msg.state
        self.timestamp = msg.timestamp
        self.topic = msg.topic

class MqttPublishHandler(object):
    """
        ['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__getitem__',
        '__hash__', '__init__', '__iter__', '__module__', '__new__', '__next__', '__reduce__',
        '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__',
        '__subclasshook__', '_condition', '_iterpos', '_published', '_set_as_published',
        'is_published', 'mid', 'next', 'rc', 'wait_for_publish']
    """
    def __init__(self, msg_info):
        self.rc = msg_info.rc
        self.mid = msg_info.mid
        self.is_published = msg_info.is_published
        self.wait_for_publish = msg_info.wait_for_publish
        self.next = msg_info.next

class MuranoMQTT(PahoSNIMqttClient, BaseMuranoClient, object):
    def __init__(self, **kwargs):
        """
        :param pid: Specify the Murano Product ID. This will set the Vendor and the Model member variables to the same.

        :type  vendor: string
        """
        BaseMuranoClient.__init__(self, **kwargs)
        PahoSNIMqttClient.__init__(self, client_id="")
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))) if kwargs.get('debug') else None

        LOG.debug("kwargs: {}".format(kwargs))
        tls_set_args = {'cert_reqs': ssl.CERT_OPTIONAL}
        if self.murano_cacert():
            tls_set_args.update(ca_certs=self.murano_cacert())

        if self.using_tls():
            tls_set_args.update({
                'certfile': self.certfile(),
                'keyfile': self.pkeyfile(),
            })
        LOG.info("tls_set_args: {}".format(tls_set_args))
        self.tls_set(**tls_set_args)
        # TODO: this is unacceptable: https://github.com/eclipse/paho.mqtt.python#tls_insecure_set
        self.tls_insecure_set(kwargs.get('tls_insecure_set') or False)
        if kwargs.get("password"):
            uuid = self.murano_id()
        else:
            uuid = ""
        pw = self.murano_token()
        LOG.info("setting username/password: id: {}, token: {}"
                 .format(uuid, pw))
        self.username_pw_set(uuid, pw)
        if not kwargs.get('murano_port'):
            LOG.debug("no murano_port specified. default to 8883")
            self.set_murano_port(8883)
        else:
            LOG.debug("murano_port overridden in kwargs: {}".format(kwargs.get('murano_port')))
            self.set_murano_port(kwargs.get('murano_port'))
        LOG.debug("mqtt host: {}, port: {}".format(
            self.murano_host(), self.murano_port()))

        self.on_log = self.default_on_log
        self.on_connect = self.default_on_connect
        self.on_disconnect = self.default_on_disconnect
        self.on_message = self.default_on_message
        self.on_publish = self.default_on_publish

        self.time_connected = 0.0
        self._connected = False
        self.is_connected = lambda: self._connected
        self.__cannot_connect = False
        self.cannot_connect = lambda: self.__cannot_connect
        self.duration_connected = lambda: time.time() - self.time_connected
        self.put_messages_in_this_queue = kwargs.get('queue_inbound_messages')
        self.disconnect_after_seconds = kwargs.get('disconnect_after_seconds')
        # ensure PINGREQ's are sent to keep connection alive/prevent half-open connections
        self.keepalive_seconds = 300
        kas = kwargs.get('mqtt_keepalive')
        if kas:
            self.keepalive_seconds = float(kas)
        if self.disconnect_after_seconds:
            self.disconnect_after_seconds = float(self.disconnect_after_seconds)
        self.always_reconnect = True

    def __str__(self):
        return 'id: {} host: {} port: {} auth: {}'.format(
            self.murano_id(), self.murano_host(), self.murano_port(), self.using_tls())

    def default_on_log(self, client, userdata, level, buf):
        """ Default mqtt logger."""
        LOG.log(level, "client: {} userdata: {} buf: {} mid: {}"
                .format(client, userdata, buf, buf[buf.find('(')+len('Mid: ')+1:buf.find(')')]))

    def default_on_message(self, client, userdata, msg):
        """ Default on_message function for tunable logging. """
        LOG.info("dup: {} info: {} mid: {} qos: {} retain: {} state: {} timestamp: {} topic: {}"
                 .format(msg.dup,
                         msg.info,
                         msg.mid,
                         msg.qos,
                         msg.retain,
                         msg.state,
                         msg.timestamp,
                         msg.topic))
        if six.PY3:
            msg.payload = msg.payload.decode('utf-8')
        LOG.debug("client: {} userdata: {} payload: {}"
                  .format(str(client), userdata, msg.payload))
        if self.put_messages_in_this_queue:
            LOG.info("Putting message in user-defined queue: {}".format(msg))
            self.put_messages_in_this_queue.put(msg)

    def default_on_publish(self, client, userdata, result):
        """ Default on_publish method for logging. """
        LOG.info("client: {} userdata: {} result (mid): {}"
                 .format(client, userdata, result))

    def default_on_connect(self, client, userdata, flags, rc):
        """ Default on_connect method for tracking connection status and logging. """
        LOG.info("client: {} userdata: {} flags: {} rc: {} reason: {}"
                 .format(client, userdata, flags, rc, PahoReturnCodes[rc]))
        self.time_connected = time.time()
        self._connected = True
        if PahoReturnCodes[rc] == PahoReturnCodes[4]:
            LOG.critical("Cannot connect to Murano: {}".format(PahoReturnCodes[4]))
            self.always_reconnect = False
            self.__cannot_connect = True
            self.disconnect()
        if self.disconnect_after_seconds:
            self.always_reconnect = False
            disconnect_timer = Timer(float(self.disconnect_after_seconds), self.disconnect)
            disconnect_timer.start()
            LOG.info("disconnecting in {} seconds".format(self.disconnect_after_seconds))

    def default_on_disconnect(self, client, userdata, rc):
        """ Default on_disconnect method for tracking connection status and logging. """
        LOG.debug("client: {} userdata: {} rc: {} reason: {}"
                  .format(client, userdata, rc, PahoReturnCodes[rc]))
        LOG.info("time connected: {}".format(time.time()-self.time_connected))
        self.time_connected = 0.0
        self._connected = False
        if rc != 0 and self.always_reconnect:
            LOG.warning("ExositeMQTT default disconnection handler: {}, {}"
                        .format(rc, PahoReturnCodes[rc]))
            self.connect(
                urlparse(self.murano_host()).netloc,
                self.murano_port(),
                keepalive=self.keepalive_seconds)

    def mqtt_activate(self):
        default_on_message = self.on_message

        def on_message(self, userdata, msg):
            LOG.debug("Activation succeeded!")
            self.set_murano_token(msg.payload.decode())
            LOG.info(self.murano_token())
            self.username_pw_set("", self.murano_token())
            LOG.debug("activate_on_message: {} :: {} :: {}"
                      .format(self, userdata, msg.payload))

        if not self.using_tls():
            LOG.debug("Using token or user/pw method of provisioning.")
            self.on_message = on_message
            LOG.debug("publishing activate message...")
            rc, mid = self.publish("$provision/" + self.murano_id(), "", qos=1)
            LOG.debug("activation publish rc: {}, mid: {}, reason: {}".format(rc, mid, PahoReturnCodes[rc]))
            LOG.info("Waiting for activation...")
        else:
            LOG.debug("Using TLS Client Cert for provisioning.")

        start_time = time.time()
        while not self.is_activated():
            time.sleep(0.1)
            if time.time() - start_time >= 1.0:
                LOG.debug(".")
            if self.disconnect_after_seconds:
                if time.time() - start_time >= self.disconnect_after_seconds:
                    LOG.critical("Aborting activation due to disconnect_after_seconds: {}"
                                .format(self.disconnect_after_seconds))
                    break
        if self.is_activated():
            LOG.debug("Activated. Took {} seconds.".format(time.time()-start_time))
        else:
            LOG.debug("Activation attempt was unsuccessful after {} seconds"
                      .format(time.time()-start_time))
        self.on_message = default_on_message

    def start(self, activate_only=False):
        LOG.info("starting...")
        try:
            self.connect(
                urlparse(self.murano_host()).netloc,
                self.murano_port(),
                keepalive=self.keepalive_seconds)
            self.loop_start()
            start_time = time.time()
            while not self.is_connected() and not self.cannot_connect():
                time.sleep(0.1)
                if time.time() - start_time >= 1.0:
                    LOG.debug(".")
            if not self.is_activated() and self.is_connected():
                self.mqtt_activate()
            LOG.info("Started. Time taken to connect: {}.".format(time.time()-start_time))
        except ssl.SSLError as exc:
            LOG.error(dir(exc))
            LOG.error(exc.errno)
            LOG.error(exc.reason)
            LOG.error(exc.strerror)
        if activate_only or self.cannot_connect():
            self.loop_stop()
            self.disconnect()

