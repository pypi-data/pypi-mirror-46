"""
    This module contains the MuranoClient class that can be used to
    quickly create an object that can use either HTTP or MQTT.
"""
# pylint: disable=W1202

import time
import json
import threading
import math
import logging
import sys
import six
import murano_client.constants
from murano_client import logger
from murano_client.http import MuranoHTTP, requests
from murano_client.mqtt import MuranoMQTT
if six.PY2:
    import Queue as queue
    from urlparse import urlparse
elif six.PY3:
    import queue
    from urllib.parse import urlparse

# NOTE: Hold a reference to Queue.Empty so at shutdown time it continues
# being defined. Otherwise it's garbage collected and the daemon threads
# raise exceptions when Empty is equal to None at process termination.
# See https://github.com/bslatkin/dpxdt/issues/88
unused_Empty = queue.Empty

LOG = logger.getLogger(__name__)


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, **kwargs):
        LOG.info("starting new thread with kwargs: {}".format(kwargs))
        super(StoppableThread, self).__init__(**kwargs)
        self.__stop_event = threading.Event()
        self.__started = False
        self.__time_started = time.time()

    def start(self):
        if not self.__started:
            super(StoppableThread, self).start()
            self.__started = True
        else:
            LOG.debug("Start method called, but already started. Everything OK.")

    def is_started(self):
        """ Method for checking whether thread has been started."""
        return self.__started

    def stop(self):
        """ Raise the stop event."""
        self.__stop_event.set()

    def is_stopped(self):
        """ Check if the stop event is set."""
        return self.__stop_event.is_set()

    def __repr__(self):
        time_running = time.time()-self.__time_started
        units = 'sec'

        if time_running >= 3600.0:
            time_running = time_running/3600.0
            units = 'hr'

        elif time_running >= 60.0:
            time_running = time_running/60.0
            units = 'min'

        return "<{}({}) running for {} ({})>".format(
            self.__class__.__name__,
            self.name,
            time_running,
            units)


class MuranoClientException(Exception):
    pass


class WatchQueue(queue.Queue):
    """
        In an effort to stop writing try-except-Empty all over the place
        for handling queue.get() calls, implimenting a queue that returns
        None if the queue is empty.
    """

    def __init__(self, **kwargs):
        LOG.debug("WatchQueue kwargs: {}".format(kwargs))
        queue.Queue.__init__(self)

    def safe_get(self, timeout=None):
        """
            This function will block forever unless timeout is overridden.
            Returns data from the queue or None if timeout is reached with
            no data.
        """
        try:
            return self.get(timeout=timeout)
        except queue.Empty:
            return None


class InboundPayload(object):
    def __init__(self, **kwargs):
        self.payload = None
        self.timestamp = None
        self.resource = None
        protocol = kwargs.get('outbound_protocol')
        if protocol == 'mqtt':
            self.payload = kwargs.get('message').payload
            self.timestamp = kwargs.get('message').topic.split('/')[2]
            self.resource = kwargs.get('message').topic.split('/')[1]
        elif protocol == 'https':
            self.payload = kwargs.get('message').split('=')[1]
            self.timestamp = time.time()
            self.resource = kwargs.get('message').split('=')[0]

    def __str__(self):
        return "{}:{}={}".format(self.resource, self.timestamp, self.payload)


class OutboundPayload(object):
    MaxRetries = 10

    def __init__(self, **kwargs):
        self.payload = kwargs.get('payload')
        self.timestamp = kwargs.get('timestamp')
        self.__retries = 0
        self.resource = kwargs.get('resource')

    @classmethod
    def override_maxretries(cls, value):
        cls.MaxRetries = value
        LOG.warning("MaxRetries overridden to: {}".format(value))

    def inc_retries(self):
        self.__retries += 1
        LOG.warning("Retries incremented: {}".format(self))

    def retries(self):
        return self.__retries

    def __str__(self):
        return "{}:{}{}={}".format(
            self.resource,
            self.timestamp,
            '.retries({}).'.format(self.__retries) if self.__retries else '',
            self.payload)


class HTTPWatchThread(StoppableThread):
    def __init__(self, **kwargs):
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))
                         ) if kwargs.get('debug') else None
        LOG.debug("kwargs: {}".format(kwargs))
        super(HTTPWatchThread, self).__init__()
        self.setDaemon(True)
        self.watch = kwargs.get('watch_function')
        self.name = self.__class__.__name__
        self.watchlist = kwargs.get('watchlist')
        self.watch_timeout = kwargs.get('http_timeout')
        self.inbound_queue = kwargs.get('inbound_queue')
        self.since = 0.0

    def process_response(self, response):
        now = time.time()
        tdiff = now - self.since
        # TODO: the readhandler needs to parse a human-readable last-modified header.
        # self.since = response.last_modified or math.ceil(now)
        self.since = math.ceil(now)
        LOG.info('{} watched for {}s, got: {}'.format(
            self.__class__.__name__, tdiff, response))
        if response.code in [304, 204]:
            LOG.info("No new watch data.")
            return
        elif response.code == 401:
            LOG.critical("Unauthorized. Will try again in 1 second...")
            time.sleep(1.0)
            return
        elif response.code == 404:
            LOG.critical(
                "Please verify your Murano Product resources are defined correctly.\n\n"
                "\tResources required: {}.\n\n"
                .format(self.watchlist))
            self.stop()

        if response.success:
            LOG.info(
                "Successfully received: {}"
                .format(response)
            )
            self.inbound_queue.put(
                InboundPayload(
                    message=response.body,
                    outbound_protocol='https'
                )
            )
        else:
            LOG.warning("http watcher was not successful: {}".format(response))

    def run(self):
        can_connect = False
        while not can_connect and not self.is_stopped():
            try:
                # pick a resource, test out whether we can read/connect
                self.watch(self.watchlist[0])
                can_connect = True
            except requests.exceptions.ConnectionError as __e:
                LOG.critical(
                    "ConnectionError caught, can't connect. Attempting to retry...")
                time.sleep(1.0)

        for resource in self.watchlist:
            try:
                LOG.warning(
                    "Initialization read of resource: {}"
                    .format(resource)
                )
                response = self.watch(resource)
            except requests.exceptions.ConnectionError as __e:
                LOG.critical("ConnectionError caught. Attempting to retry...")
                time.sleep(0.25)

            self.process_response(response)

        while not self.is_stopped():
            LOG.info("(re)starting watch of: {}".format(self.watchlist))

            try:
                response = self.watch(
                    self.watchlist,
                    self.watch_timeout,
                    modify_ts=self.since)
            except requests.exceptions.ConnectionError as __e:
                LOG.critical("ConnectionError caught. Attempting to retry...")
                time.sleep(0.25)
                continue

            self.process_response(response)


class HTTPTellThread(StoppableThread):
    """
        needs an outbound_queue
        objects going into the outbound queue need
        to be instances of OutboundPayload
    """

    def __init__(self, **kwargs):
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))
                         ) if kwargs.get('debug') else None
        LOG.debug("kwargs: {}".format(kwargs))
        super(HTTPTellThread, self).__init__()
        self.setDaemon(True)
        self.name = self.__class__.__name__
        self.tell = kwargs.get('tell_function')
        self.outbound_queue = kwargs.get('outbound_queue')

    def run(self):
        LOG.info("Starting tell thread.")
        while not self.is_stopped():
            tell = self.outbound_queue.safe_get(timeout=1.0)
            if tell:
                LOG.debug("Sending tell data: {}".format(tell))
                try:
                    response = self.tell(
                        {
                            tell.resource: {
                                int(tell.timestamp): tell.payload
                            }
                        }
                    )
                    LOG.info("Tell response: {}".format(response))
                except requests.exceptions.ConnectionError as __e:
                    if tell.retries() >= OutboundPayload.MaxRetries:
                        raise MuranoClientException(
                            "Maximum retries ({}) exceeded on {}: {}"
                            .format(OutboundPayload.MaxRetries,
                                    tell.__class__.__name__,
                                    tell))
                    tell.inc_retries()
                    self.outbound_queue.put(tell)
                    time.sleep(0.25)

        LOG.critical("{} has stopped!".format(self))


class MQTTTellThread(StoppableThread):
    """
        needs an outbound_queue
        objects going into the outbound queue need
        to be instances of OutboundPayload
    """

    def __init__(self, **kwargs):
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))
                         ) if kwargs.get('debug') else None
        LOG.debug("init kwargs: {}".format(kwargs))
        super(MQTTTellThread, self).__init__()
        self.setDaemon(True)
        self.name = self.__class__.__name__
        self.tell = kwargs.get('tell_function')
        self.outbound_queue = kwargs.get('outbound_queue')

    def run(self):
        LOG.info("starting tell thread run")
        while not self.is_stopped():
            LOG.debug("back to top of tell-thread main loop")
            tell = self.outbound_queue.safe_get(timeout=1.0)
            if tell and tell.resource:
                # batch record schema
                payload = json.dumps([
                    {
                        'timestamp': self.microsecond(tell.timestamp),
                        'values': {
                            tell.resource: tell.payload
                        }
                    }
                ])
                LOG.info(
                    "telling to resource {}: {}"
                    .format("$resource.batch", payload)
                )
                response = self.tell(
                    "$resource.batch",
                    payload,
                    qos=1
                )
                LOG.info(response)
            else:
                LOG.debug(
                    "No resource in outbound payload object. Cannot tell Murano anything: {}"
                    .format(tell))
        LOG.critical("{} has stopped!".format(self))

    def microsecond(self, timestamp):
        """
        Args:
            timestamp: time.time()
        Returns:
            microsecond
        """

        return int(timestamp * 1000000)


class MQTTWatchThread(StoppableThread):
    def __init__(self, **kwargs):
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))
                         ) if kwargs.get('debug') else None
        LOG.debug("kwargs: {}".format(kwargs))
        super(MQTTWatchThread, self).__init__()
        self.setDaemon(True)
        self.watch = kwargs.get('watch_function')
        self.name = '-'.join([self.__class__.__name__, kwargs.get('resource')])
        self.resource = kwargs.get('resource')
        self.watch_timeout = kwargs.get('http_timeout')
        self.inbound_queue = kwargs.get('inbound_queue')

    def run(self):
        since = 0.0
        while not self.is_stopped():
            LOG.info("(re)starting watch of: {}".format(self.resource))

            message = self.watch(timeout=self.watch_timeout)
            now = time.time()
            tdiff = now - since
            since = math.ceil(now)
            LOG.info('watch time {}: {}'.format(tdiff, message))
            if message:
                LOG.info(
                    "putting new message in inbound queue!")
                self.inbound_queue.put(InboundPayload(
                    message=message, outbound_protocol='mqtt'))

        LOG.critical("{} has stopped!".format(self))


class MuranoClient(object):
    def __new__(cls, memory_queue=True, **kwargs):
        if(memory_queue):
            return MemoryQueueMuranoClient(**kwargs)
        else:
            return NoMemoryQueueMuranoClient(**kwargs)

    def __init__(self):
        pass


class NoMemoryQueueMuranoClient(MuranoHTTP, MuranoMQTT):
    def __init__(self, **kwargs):
        """
            The inbound queue is designed so that objects of this class can call
            inbound_queue.safe_get([timeout]) and the payload objects from Murano
            will be formatted in a predictable way.

                Payload format of items in inbound_queue:

                    <resource>=
        """
        LOG.debug(
            "Initializing Murano[HTTP|MQTT] Client with kwargs: {}"
            .format(kwargs)
        )

        self.inbound_queue = WatchQueue()  # data from murano
        self.outbound_protocol = None

        murano_host = kwargs.get('murano_host', None)
        if murano_host:
            self.outbound_protocol = urlparse(murano_host).scheme

        LOG.info("Using protocol {}".format(self.outbound_protocol))

        if not self.outbound_protocol:
            if six.PY3:
                sys.tracebacklimit = None
            else:
                sys.tracebacklimit = 0
            raise MuranoClientException(
                "Cannot parse supported protocol from murano_host parameter: {}"
                .format(kwargs.get('murano_host')))

        self.watch_threads = []
        watchlist = kwargs.get('watchlist')
        if not watchlist:
            if six.PY3:
                sys.tracebacklimit = None
            else:
                sys.tracebacklimit = 0
            raise MuranoClientException(
                "Required parameter 'watchlist' empty or not provided: {}"
                .format(watchlist))

        if self.outbound_protocol == 'mqtt':  # no need for this for http
            kwargs['queue_inbound_messages'] = WatchQueue()
            MuranoMQTT.__init__(self, **kwargs)

            for resource in kwargs.get('watchlist'):
                LOG.info('watching: {}'.format(resource))
                self.watch_threads.append(
                    MQTTWatchThread(
                        watch_function=kwargs['queue_inbound_messages'].safe_get,
                        inbound_queue=self.inbound_queue,
                        resource=resource,
                        http_timeout=kwargs.get(
                            'http_timeout')*1000 if kwargs.get('http_timeout') else 10*1000
                    )
                )
            LOG.info("done init'ing thread objects.")
        elif self.outbound_protocol == 'https':
            MuranoHTTP.__init__(self, **kwargs)

            LOG.info('watching: {}'.format(watchlist))
            self.watch_threads.append(
                HTTPWatchThread(
                    watch_function=self.http_long_poll,
                    inbound_queue=self.inbound_queue,
                    watchlist=watchlist,
                    http_timeout=kwargs.get(
                        'http_timeout',
                        murano_client.constants.DEFAULT_HTTP_TIMEOUT)*1000
                )
            )

    def stop_all(self):
        LOG.critical("Stopping all threads!!!")
        for watcher in self.watch_threads:
            if not watcher.is_stopped():
                watcher.stop()
            LOG.critical("Waiting for {} to stop...".format(watcher))
            watcher.join(timeout=0.25)
        if self.outbound_protocol == 'https':
            LOG.critical("Closing HTTP connection!!!")
            self.close_session()
        if self.outbound_protocol == 'mqtt':
            LOG.critical("Closing MQTT connection!!!")

            def on_disconnect_override(client, userdata, rc):  # pylint: disable=C0103
                """ MQTT on_disconnect handler override function."""
                LOG.critical("Default reconnect behavior overridden.")
                LOG.critical("Disconnecting: client: {} userdata: {} rc: {}"
                             .format(client, userdata, rc))
            self.on_disconnect = on_disconnect_override
            self.disconnect()

            LOG.critical("All threads have stopped.")
        return

    def start_client(self):
        if self.outbound_protocol == 'mqtt':
            self.start()
            self.loop_start()
        self.start_watchers()

    def start_watchers(self):
        LOG.info("Starting watchers.")
        for thread in self.watch_threads:
            LOG.debug("starting: {}".format(thread))
            thread.setDaemon(True)
            thread.start()

    def tell(self, resource=None, timestamp=None, payload=None, payloads=None):
        """
        single payload in payloads:
            https:
                {'alias1': {'ts1': 'some data', 'ts2': 'some more data'}, 'alias2': {'ts2': 'data data data', 'ts3': 'datum dateo''}}
            mqtt:

        Returns:
            status:
                True or False
            result:
                server response or error message
        Examples:
            status, result = no_queue_tell({"config_io": {1554975272.470659: {"a": 1234}}})
            print('status: {}, result: {}'.format(status, result))
            # https
            >>>> status: True, result: code: 204, body: 'No content', success: True, authorized: True
            # mqtt
            >>>> status: True, result: (0, 1)
        """
        def parse_http_payload(resource=None, timestamp=None, payload=None):
            return {
                resource:
                {
                    timestamp: payload
                }
            }

        def parse_mqtt_payload(resource=None, timestamp=None, payload=None):
            return json.dumps([{
                'timestamp': timestamp,
                'values': {
                    resource: payload
                }
            }])

        try:
            if self.outbound_protocol == 'https':
                if not payloads:
                    payloads = parse_http_payload(
                        resource=resource,
                        timestamp=timestamp,
                        payload=payload
                    )
                response = self.http_record(payloads)
                if response.success:
                    return True, response
                else:
                    return False, response
            elif self.outbound_protocol == 'mqtt':
                if not payloads:
                    payloads = parse_mqtt_payload(
                        resource=resource,
                        timestamp=timestamp,
                        payload=payload
                    )
                response = self.publish(
                    '$resource.batch',
                    payloads,
                    qos=1
                )
                response.wait_for_publish()

                if response.is_published():
                    return True, response
                else:
                    return False, response
        except (requests.exceptions.ConnectionError, Exception) as err:
            LOG.warning(err)
            return False, err

    def ack(self, resource, payload):
        """
        Args:
            resource: dataport
            payload: data to Murano
        Returns:
            status:
                True or False
            result:
                server response or error message
        Examples:
            status, result = ack('config_io', json.dumps({"a": 1234}))
            print('status: {}, result: {}'.format(status, result))
            # https
            >>>> status: True, result: code: 204, body: 'No content', success: True, authorized: True
            # mqtt
            >>>> status: True, result: (0, 1)
        """
        try:
            if self.outbound_protocol == 'https':
                response = self.http_write(resource, payload)
                if response.success:
                    return True, response
                else:
                    return False, response
            elif self.outbound_protocol == 'mqtt':
                response = self.publish(
                    '$resource/' + resource,
                    payload,
                    qos=1
                )
                response.wait_for_publish()

                if response.is_published():
                    return True, response
                else:
                    return False, response
        except (requests.exceptions.ConnectionError, Exception) as err:
            LOG.warning("Ack failed:", err)
            return False, err

    def watch(self, **kwargs):
        if kwargs.get('timeout'):
            from_murano = self.inbound_queue.safe_get(
                timeout=kwargs.get('timeout'))
            LOG.info(
                "got from murano, putting in inbound queue: {}".format(from_murano))
            return from_murano
        else:
            while True:
                from_murano = self.inbound_queue.safe_get(timeout=1.0)
                if from_murano:
                    LOG.info(
                        "got from murano, putting in inbound queue: {}".format(from_murano))
                    return from_murano
                else:
                    LOG.debug("No data from murano: {}".format(from_murano))

    def client_activate(self):
        if self.outbound_protocol == 'mqtt':
            self.start(activate_only=True)
        elif self.outbound_protocol == 'https':
            self.http_activate()


class MemoryQueueMuranoClient(NoMemoryQueueMuranoClient):
    def __init__(self, **kwargs):
        """
            The inbound queue is designed so that objects of this class can call
            inbound_queue.safe_get([timeout]) and the payload objects from Murano
            will be formatted in a predictable way.

                Payload format of items in inbound_queue:

                    <resource>=
        """
        LOG.debug(
            "Initializing Murano[HTTP|MQTT] Client with kwargs: {}"
            .format(kwargs)
        )
        super(MemoryQueueMuranoClient, self).__init__(**kwargs)
        self.outbound_queue = WatchQueue()  # data to murano

        if not self.murano_host():
            raise MuranoClientException("no murano_host specified.")

        # ###################################################### #
        # ########### HTTP HTTP HTTP HTTP HTTP ################# #
        # ###################################################### #

        if self.outbound_protocol == 'https':
            LOG.info("done init'ing thread objects.")

            if kwargs.get('tell_function_override'):
                tell_function_override = kwargs.get('tell_function_override')
                if not callable(tell_function_override):
                    raise MuranoClientException(
                        "tell function override must be a callable function.")
                tell_function = tell_function_override
            else:
                tell_function = self.http_record

            self.tell_thread = HTTPTellThread(
                outbound_queue=self.outbound_queue,
                tell_function=tell_function)

        # ###################################################### #
        # ########### MQTT MQTT MQTT MQTT MQTT ################# #
        # ###################################################### #

        elif self.outbound_protocol == 'mqtt':
            if kwargs.get('tell_function_override'):
                tell_function_override = kwargs.get('tell_function_override')
                if not callable(tell_function_override):
                    raise MuranoClientException(
                        "tell function override must be a callable function.")
                tell_function = tell_function_override
            else:
                tell_function = self.publish

            self.tell_thread = MQTTTellThread(
                outbound_queue=self.outbound_queue,
                tell_function=tell_function)

        retries = kwargs.get('payload_retries')
        if retries:
            LOG.warning("Overriding outbound payload retries to: {}"
                        .format(retries))
            OutboundPayload.override_maxretries(int(retries))

        self.monitor_thread = StoppableThread(
            name='Monitor',
            target=self._monitor_thread,
            args=())
        self.monitor_thread.setDaemon(True)

    def stop_all(self):
        LOG.critical("Stopping all threads!!!")
        self.tell_thread.stop()
        LOG.critical("Waiting for {} to stop...".format(self.tell_thread))
        self.tell_thread.join()
        self.monitor_thread.stop()
        LOG.critical("Waiting for {} to stop...".format(
            self.monitor_thread))
        self.monitor_thread.join()

        super(MemoryQueueMuranoClient, self).stop_all()

    def start_client(self):
        self.tell_thread.start()
        self.monitor_thread.start()

        super(MemoryQueueMuranoClient, self).start_client()

    def _monitor_thread(self):
        time.sleep(5)
        while not self.monitor_thread.is_stopped():
            try:
                for thread in threading.enumerate():
                    LOG.info("running thread: {}".format(thread))
                LOG.info("inbound_queue size: {}".format(
                    self.inbound_queue.qsize()))
                LOG.info("outbound_queue size: {}".format(
                    self.outbound_queue.qsize()))
                for watcher in self.watch_threads:
                    if not watcher.is_alive():
                        # TODO: send signal to parent pid?
                        LOG.critical(
                            "Watcher thread has died! {}".format(watcher))
                if not self.tell_thread.is_alive():
                    LOG.critical(
                        "Tell thread has died! {}".format(self.tell_thread))
            except Exception:
                LOG.exception("Non-critical Exception.")
            time.sleep(5)
        LOG.critical("{} has stopped!".format(self.monitor_thread))

    def tell(self, **kwargs):
        o_p = OutboundPayload(
            resource=kwargs.get('resource'),
            timestamp=kwargs.get('timestamp'),
            payload=kwargs.get('payload'),
            outbound_protocol=self.outbound_protocol)
        LOG.info("telling to outbound queue: {}".format(o_p))
        self.outbound_queue.put(o_p)
