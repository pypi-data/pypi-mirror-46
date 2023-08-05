Murano Client Library (Python)
==================================

.. image:: https://travis-ci.com/exosite/lib_murano_client_python.svg?token=tgjcyH1MG5sXqcVsD1kG&branch=master
    :target: https://travis-ci.com/exosite/lib_murano_client_python

A library for quickly testing, evaluating and writing client software for Murano devices.

Supported features:

* HTTPS Device API
* MQTT Device API
* TOKEN Auth
* TLS Client Cert Auth
* Command Line Interface (``gdc --help``)

Requirements
-------------------

* Python 2.7.9+, 3.4, 3.5, 3.6
* paho-mqtt (>=1.3.1)
* requests (>=2.13.0)
* docopt (>=0.6.2)
* six

Installation
-------------------

Run the following command.

    .. code-block::

        > pip install murano-client

HTTP CLI Examples
-------------------

Timestamp
~~~~~~~~~~~~~~~~~~~~~~

    .. code-block::

        > gdc -H https://t41hp23nod8s00000.m2.exosite.io/ http timestamp
        1527272454

Activate
~~~~~~~~~~~~~~~~~~~~~~

    .. code-block::

        > gdc -H https://t41hp23nod8s00000.m2.exosite.io/ -u myDeviceName-1 http activate
        97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW

Write
~~~~~~~~~~~~~~~~~~~~~~

    .. code-block::

        > gdc -H https://t41hp23nod8s00000.m2.exosite.io/ -k 97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW http write data_in '{"some": "json data"}'
        [204] No content

Record
~~~~~~~~~~~~~~~~~~~~~~

    .. code-block::

        > gdc -H https://t41hp23nod8s00000.m2.exosite.io/ -k 97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW http record $(date +%s) data_in '{"historical": "data"}'
        [204] No content

Read
~~~~~~~~~~~~~~~~~~~~~~

    .. code-block::

        > gdc -H https://t41hp23nod8s00000.m2.exosite.io/ -k 97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW http read data_in
        data_in={"historical": "data"}

Poll
~~~~~~~~~~~~~~~~~~~~~~

    .. code-block::

        > gdc  -H 'https://t41hp23nod8s00000.m2.exosite.io/' -k 97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW http poll config_io 3000
        [304] Not modified


    .. code-block::

        > gdc  -H 'https://t41hp23nod8s00000.m2.exosite.io/' -k 97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW http poll config_io 30000
        [200] config_io={"some": "config data"}

Content
~~~~~~~~~~~~~~~~~~~~~~
List Content
''''''''''''''''''''''


    .. code-block::

        > gdc -H 'https://t41hp23nod8s00000.m2.exosite.io/' -k 97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW http content list
        requests_check.v1.tar.gz
        ota_bundle_test.v2.tar.gz
        ota_bundle_test.v1.tar.gz
        gwe.v1.5.RC68.tar.gz
        gwe.v1.5.RC59.tar.gz
        gwe.v1.5.RC58.tar.gz
        gwe.v1.5.RC57.tar.gz

Get Content Info
''''''''''''''''''''''

    .. code-block::

        > gdc -H 'https://t41hp23nod8s00000.m2.exosite.io/' -k 97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW http content info gwe.v1.5.RC68.tar.gz
        application/gzip,691529,1513931066,


Download Content
''''''''''''''''''''''

    .. code-block::

        > gdc -H 'https://t41hp23nod8s00000.m2.exosite.io/' -k 97eWgtm9Et5VxwuJT8NiOK7w27Ly2GS092oSxgpW http content download gwe.v1.5.RC68.tar.gz
        WARNING:urllib3.response:Received response with both Content-Length and Transfer-Encoding set. This is expressly forbidden by RFC 7230 sec 3.3.2. Ignoring Content-Length and attempting to process response as Transfer-Encoding: chunked.
        > file gwe.v1.5.RC68.tar.gz
        gwe.v1.5.RC68.tar.gz: gzip compressed data, last modified: Fri Dec 22 08:24:23 2017, from Unix


MQTT CLI Examples
-------------------
Activate
~~~~~~~~~~~~~~~~~~~~~~
Activate a client with via MQTT.


    .. code-block::

        > gdc -H mqtt://t41hp23nod8s00000.m2.exosite.io/ -u cleanup-stuff mqtt activate
        oihLldO3f53dqyJYDmiRCijVsf4eQJeUxFSBnEsk


Publish
~~~~~~~~~~~~~~~~~~~~~~
Publish a single payload with MQTT.


    .. code-block::

        > gdc -H mqtt://t41hp23nod8s00000.m2.exosite.io/ -k oihLldO3f53dqyJYDmiRCijVsf4eQJeUxFSBnEsk mqtt publish \$resource/data_in "{\"time\": $(date +%s)}"
        rc=0, mid=1: {"time": 1528214840}


Subscribe
~~~~~~~~~~~~~~~~~~~~~~
Subscribe to a murano client.

**NOTE:** MQTT Subscribe works on all resources of a Murano client. Subscribing to a specific resource is not supported. Unsubscribe is also not supported.


    .. code-block::

        > gdc -H mqtt://t41hp23nod8s00000.m2.exosite.io/ -k oihLldO3f53dqyJYDmiRCijVsf4eQJeUxFSBnEsk mqtt subscribe
        update_interval.1528215003884000=60


Pubsub
~~~~~~~~~~~~~~~~~~~~~~
Use this command to publish newline-delineated date to a client resource while simultaneously subscribing to its resources.


    .. code-block::

        > while true
        do
            echo "{\"time\": $(date +%s)}"
            sleep 0.5
        done | gdc -H mqtt://t41hp23nod8s00000.m2.exosite.io/ \
                   -k oihLldO3f53dqyJYDmiRCijVsf4eQJeUxFSBnEsk \
                   mqtt pubsub \
                   \$resource/config_io
        update_interval.1528215003884000=60



Client Applications
-------------------
For examples of how to import this library, see the commands in the ``murano_client/commands/`` directory.

Simple HTTP Example Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    .. code-block::

        #!/usr/bin/env python

        # example.py

        import time
        import uuid
        import json
        from murano_client.http import MuranoHTTP, Http_ReadWriteCodes

        HTTP_TIMEOUT = 5*60*1000 # 5 minutes
        config_io = None

        client_params = {
            "murano_host": "https://t41hp23nod8s00000.m2.exosite.io/",
            "murano_id": str(uuid.uuid4()),
            "http_timeout": 5.0,
            "debug": "DEBUG",
        }

        print("Client parameters: {}".format(json.dumps(client_params)))

        hc = MuranoHTTP(**client_params)
        hc.set_http_timeout(HTTP_TIMEOUT)

        while not hc.is_activated():
            hc.http_activate()
            print("TOKEN: {}".format(hc.murano_token()))
            if not hc.is_activated():
                time.sleep(HTTP_TIMEOUT)

        print("Starting long poll...")

        while True:
            response_handler = hc.http_long_poll(
                    'config_io',
                    HTTP_TIMEOUT,
                    time.time()
                )

            if response_handler.code == Http_ReadWriteCodes.NotModified:
                print("no config_io yet...")
            elif response_handler.code == Http_ReadWriteCodes.OK:
                print(response_handler.body)
                config_io = json.loads(response_handler.body.strip("config_io="))
                print("got config_io: {}".format(config_io))
                hc.http_write('config_io', "ACK")
            else:
                print(response_handler)

            if config_io:
                print(hc.http_write('data_in', str(uuid.uuid4())))




Simple MQTT Example Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    .. code-block::

        #!/usr/bin/env python

        # example.py
        from __future__ import print_function
        import time
        import uuid
        import json
        from murano_client.mqtt import MuranoMQTT

        client_params = {
            "murano_host": "mqtt://t41hp23nod8s00000.m2.exosite.io/",
            "murano_id": str(uuid.uuid4()),
            # "debug": "DEBUG",
        }

        print("Client parameters: {}".format(json.dumps(client_params)))

        mc = MuranoMQTT(**client_params)
        mc.start()

        mc.Config_IO = None

        print("Starting activation...")
        if not mc.is_activated():
            mc.activate()
            print("TOKEN: {}".format(mc.murano_token()))

        def on_message(cls, userdata, msg):
            """ Override default on_message function. """
            _, resource, timestamp = msg.topic.split('/')[0:3]
            print("{}.{}={}".format(resource, timestamp, msg.payload))
            if 'config_io' == resource:
                try:
                    cls.Config_IO = json.loads(msg.payload.decode())
                    print("New Config_IO: {}".format(cls.Config_IO))
                except ValueError:
                    print("Invalid JSON: {}".format(msg.payload.decode()))
        mc.on_message = on_message

        print("Starting program...")

        mc.start()

        while True:

            if mc.Config_IO:
                rand_data = str(uuid.uuid4())
                rc, mid = mc.publish(
                                     '$resource/data_in',
                                     rand_data,
                                     qos=0
                                     )
                print("rc={}, mid={}, data={}"
                      .format(rc, mid, rand_data))
            else:
                print("waiting for config_io object...")

            mc.loop()
            time.sleep(1)



Simple ``MuranoClient`` Client Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``MuranoClient`` class takes the following constructor parameters:

* ``murano_host`` - Required. The application will use the appropriate protocol to communicate with Murano according to the Product settings.
* ``murano_id`` - This is the device identifier (e.g. serial number, etc.).
* ``watchlist`` - Provide a list of resources from which to be notified of when new data is available. **NOTE:** Currently only one resource is supported.
* ``http_timeout`` - Specify the length of time in between Long Poll connections when using HTTP.
* ``debug`` - Turn the logging up or down. Valid values are the string values ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR`` and ``CRITICAL``.

The application, below, uses the ``MuranoClient`` class's MQTT option to "echo" payloads from the ``config_io`` resource to the ``data_in`` resource.


    .. code-block::

        #!/usr/bin/env python

        import sys
        import signal
        import time
        from murano_client.client import MuranoClient

        c = MuranoClient(
            murano_host='mqtt://t41hp23nod8s00000.m2.exosite.io/',
            murano_id=sys.argv[1],
            watchlist=['config_io'],
            http_timeout=5*60,
            debug='DEBUG')

        def stop(signal, frame):
            print("stopping")
            c.stop_all()
            sys.exit(0)

        signal.signal(signal.SIGINT, stop)

        c.client_activate()
        c.start_client()

        while True:
            data_from_murano = c.watch()
            if data_from_murano:
                c.tell(
                    resource='data_in',
                    timestamp=time.time(),
                    payload=data_from_murano.payload
                )



The example below uses the HTTP option to periodically write the current time into the ``data_in`` resource.

**IMPORTANT:**


    .. code-block::

        #!/usr/bin/env python

        import sys
        import signal
        import time
        from murano_client.client import MuranoClient

        c = MuranoClient(
            murano_host='https://t41hp23nod8s00000.m2.exosite.io/',
            murano_id=sys.argv[1],
            watchlist=['config_io'],
            http_timeout=5,
            debug='DEBUG'
        )

        def stop(signal, frame):
            c.stop_all()
            sys.exit(0)

        signal.signal(signal.SIGINT, stop)

        c.client_activate()
        c.start_client()

        while True:
            c.tell(
                resource='data_in',
                timestamp=time.time(),
                payload='chirp: {}'.format(time.time())
            )
            print(c.watch(timeout=1.0))



INI State File
-------------------
Required:

* ``murano_host``
* ``murano_id``
* ``watchlist`` - comma delineated list of Murano resources

Optional:

* ``murano_port`` - (https default: 443, mqtt default: 8883)
* ``debug``
* ``murano_token``

Example INI files:

##NOTE:## If client hasn't provisioned yet, exclude ``murano_token``. The ``Device`` class will set/save it after it activates.

    .. code-block::

        # device.ini
        [device]
        murano_host = mqtt://t41hp23nod8s00000.m2.exosite.io/
        murano_id = 4321
        murano_port = 443
        watchlist = config_io
        debug = DEBUG
        murano_token = XaFfMaOvrGxJgWk2Iftgw1cplYuZeSsUoKlKn0lb

Example application code that used the INI example, above.

    .. code-block::

        #!/usr/bin/env python

        from murano_client.ini import Device

        d = Device('device.ini')
        d.client_activate()
        d.start_client()
        print(d.watch()) # now set a value in the watchlist

Example CLI commands that use the INI file, above.

    .. code-block::

        gdc -f device.ini http timestamp
        gdc -f device.ini http activate
        gdc -f device.ini http read config_io
        gdc -f device.ini http write data_in '{"a": "3.14"}'
        gdc -f device.ini http record $(date +%s) data_in '{"a": "3.14"}'
        gdc -f device.ini mqtt timestamp
        gdc -f device.ini mqtt activate
        gdc -f device.ini mqtt publish \$resource/data_in '{"a": "3.14"}'
        gdc -f device.ini mqtt subscribe


Logging
-------------------------

The ``murano_client`` library has a log file rotator built in. It is utilized via system environment variables only. It supports the following parameters:

* ``MURANO_CLIENT_DEBUG``           - case-insensitive, default:warning (debug|info|warning|error|critical).
* ``MURANO_CLIENT_LOGFILE``         - case-sensitive, default:stderr, can override to stdout or any file path.
* ``MURANO_CLIENT_LOG_MAX_BYTES``   - integer(bytes), default:1024000
* ``MURANO_CLIENT_MAX_BACKUPS``     - integer(number-of-backups), default:3

.. code-block::

    export MURANO_CLIENT_DEBUG=debug
    export MURANO_CLIENT_LOGFILE=/var/log/murano_client.log
    export MURANO_CLIENT_LOG_MAX_BYTES=$((1024*100))
    export MURANO_CLIENT_MAX_BACKUPS=2

**NOTE:** Any application (e.g. ``edged``) can override the ``MURANO_CLIENT_DEBUG`` parameter during runtime with the ``debug=<level>`` keyword argument to ``MuranoClient`` objects.

Test
-------------------------

To execute tests:

    .. code-block::

        > export MURANO_HOST https://x28f1bttwbtzw0000.m2.exosite.io/
        > pip install -U tox
        > tox


