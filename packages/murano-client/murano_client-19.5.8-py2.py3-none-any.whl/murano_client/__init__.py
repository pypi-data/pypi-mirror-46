# pylint: disable=W1202,R0902,W0312
"""
    This module contains the MuranoClient and MuranoTLS
    classes which are used to build protocol clients.

    E.g.
        class MqttClient(MuranoClient):
            ...

        qtclient = MqttClient(host='kjli97yjuhmk00000.m2.exosite.io')
        qtclient.start()
"""
from __future__ import print_function
import os
import sys
import json
import logging
import pkg_resources
from murano_client import logger
from .__version__ import __version__
if sys.version_info[0] == 2: # six.PY2:
    from urlparse import urlparse
elif sys.version_info[0] >=3:
    from urllib.parse import urlparse


LOG = logger.getLogger(__name__)

class ExoTLSException(Exception):
    """ Custom exception class for validating
        user input and improper usage of ExoTLS class.
    """
    pass

class MuranoTLS(object):
    """ Container class for filesystem paths to
    TLS Client Cert Auth and CA files. """


    def __init__(self, **kwargs):
        self._murano_cacert = kwargs.get('murano_cacert') or \
            pkg_resources.resource_filename('murano_client', 'Murano_Root_CA.cer')
        self._certfile = kwargs.get('certfile')
        self._pkeyfile = kwargs.get('pkeyfile')
        self.murano_cacert = lambda: self._murano_cacert
        self.certfile = lambda: self._certfile
        self.pkeyfile = lambda: self._pkeyfile
        if self.certfile() and not os.path.exists(self.certfile()):
            raise ExoTLSException("Certfile {!r} not found!"
                                  .format(self.certfile()))
        if self.pkeyfile() and not os.path.exists(self.pkeyfile()):
            raise ExoTLSException("Keyfile {!r} not found!"
                                  .format(self.pkeyfile()))

    def using_tls(self):
        """ Returns a boolean to determine whether or not
        the client is using TLS Client Cert Auth. """
        using_tls = None not in (self.certfile(), self.pkeyfile())
        LOG.debug("Using TLS Provisioning? {}".format(using_tls))
        return using_tls

class MuranoClientException(Exception):
    """ Custom exception class for validating
        user input and improper usage of
        BaseMuranoClient class.
    """
    pass

class BaseMuranoClient(MuranoTLS, object):
    """
        A base class for building protocol clients.

        A Murano Client can include but aren't necessarily
        limited to the following attributes and methods.

         - A client supports the following provisioning attributes:
            1. Token
            2. Username/Password
            3. TLS Client Certificate

         - A client supports the following provisioning methods:
            1. onep:v1 activate - provide data to provisioning
               endpoints/topics to get CIK/Token in a response
            2. username/password - use
            3. TLS Client Cert

    """
    def __init__(self, **kwargs):
        # initialize tls vars
        MuranoTLS.__init__(self, **kwargs)
        # state variables
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))) if kwargs.get('debug') else None
        self.__version__ = __version__
        self._activated = False
        self._online = False

        # provisioning and connection parameters
        self._murano_id = kwargs.get('murano_id')
        self._murano_host = kwargs.get('murano_host')
        self._murano_port = kwargs.get('murano_port') or 443
        self.set_murano_token(kwargs.get('murano_token') or None)
        if self.using_tls():
            self.set_activated(True)
            LOG.info("Using TLS, setting activated...")
            self._auth_header = lambda: {}
        else:
            self._auth_header = lambda: {'X-Exosite-CIK' : self.murano_token()}

        self.murano_host = lambda: self._murano_host
        self.murano_port = lambda: self._murano_port
        self.murano_id = lambda: self._murano_id
        self.murano_token = lambda: self._murano_token

        if urlparse(self.murano_host()).scheme == 'mqtt':
            self.set_murano_port(8883)

    def set_murano_host(self, host):
        """ TODO """
        self._murano_host = host

    def set_murano_port(self, port):
        """ TODO. """
        self._murano_port = port

    def set_murano_token(self, token):
        """ Return current murano auth token. """
        self._murano_token = token
        if token:
            self.set_activated(True)

    def set_murano_id(self, uuid):
        """ Return current murano auth token. """
        self._murano_id = uuid

    def set_activated(self, boolean):
        """ Set whether or not the client is
        activated. """
        self._activated = boolean

    def is_activated(self):
        """ Return a boolean to determine
        whether or not the client is activated. """
        if self.using_tls():
            return True
        return self._activated


