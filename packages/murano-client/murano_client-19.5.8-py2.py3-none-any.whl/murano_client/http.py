"""This module contains all HTTP Device API and HTTP Provision Management
methods for IoT gatewayss.
"""

# pylint: disable=I0011,W0312,R0903,C1001,R0201,W0232,C0301,W1202

import sys
from murano_client import __version__, BaseMuranoClient
from murano_client import logger, constants
if sys.version_info[0] < 3:
    import httplib
    from urllib import urlencode, quote_plus, unquote_plus, unquote
    from urlparse import urljoin
else:
    import http.client as httplib
    from urllib.parse import urlencode, urljoin, quote_plus, unquote_plus, unquote

import logging
import sys
import json
import requests
import time
import os
import six

LOG = logger.getLogger(__name__)


class Http_ActivationCodes:
    """ Enum class for http response codes from Activation attempts.

        `Referenced <http://docs.exosite.com/http/#activate>`_ on 04/16/2015

        ::

            HTTP/1.1 200 OK
            Date: <date>
            Server: <server>
            Connection: Keep-Alive
            Content-Length: <length>
            Content-Type: text/plain; charset=utf-8

        On success, the response is the TOKEN.

        Response may also be:

        * HTTP/1.1 404 Not Found if the client described by <vendor>, <model>, <sn> is not found on the system.
        * HTTP/1.1 409 Conflict if the serial number is not enabled for activation.

        See HTTP Responses for a full list of responses

    """
    Timeout = 0
    OK = 200
    DeviceNotin1P = 403
    NotFound = 404
    NotEnabled = 409

class Http_ReadWriteCodes:
    """ Enum class for http response codes from dataport Read, Write and ReadWrite attempts.

        Copied from docs.exosite.com/data/#http 04/16/2015

        Typical HTTP response codes include:
        Code    Response        Description
        200     OK              Successful request, returning requested values
        204     No Content      Successful request, nothing will be returned
        4xx     Client Error    There was an error* with the request by the client
        401     Unauthorized    No or invalid TOKEN
        5xx     Server Error    There was an error with the request on the server

        * Note: aliases that are not found are not considered errors in the request.

        See the documentation for read, and write and Hybrid write/read for details.
    """
    Timeout = 0
    OK = 200
    NoContent = 204
    Unauthorized = 401
    NotModified = 304
    Conflict = 409
    ClientErrors = [400]+[c for c in range(402, 409)]+[c for c in range(410, 500)]
    ServerErrors = [c for c in range(500, 600)]

class ActivationHandler(object):
    """ Class to handle Device() activations.

        Input: Requests_Response() object generated from Exosite Activation Request.

        Object contains 'code', 'body', and 'activated' member variables.

        * If successfully Activated, member variables will contain:
            * code = 200
            * body = '<token>'
            * activated = True
        * If successfully Activated, but got a BAD TOKEN, member variables will contain:
            * code = 200
            * body = '<BAD TOKEN>'
            * activated = False
        * Otherwise:
            * code = <http response code>
            * body = 'an informative message'
            * activated = False

        Example usage:

        .. code-block:: python

            act_resp = exo.handlers.ActivationHandler(
                exo.Exo().exosite_activate(
                    uuid,
                    vendor,
                    msg.model
                )
            )

            # determine whether or not provisioning/activation worked
            if(act_resp.activated):
                my_token = act_resp.body
            else:
                print("Activation attempt FAILED: {!r}".format(act_resp.body))

    """
    def __init__(self, response):
        """
            :param response: The response object that the handler intends to parse/process.

            :type  response: Requests_Response
        """
        self.response = response
        self.code = response.status_code
        self.body = response.text
        self.activated = False

        if self.code == Http_ActivationCodes.OK:
            if len(self.body) == 40:
                self.activated = True
        elif self.code == Http_ActivationCodes.NotFound:
            self.body = "Client <id> is not found on the system."
        elif self.code == Http_ActivationCodes.DeviceNotin1P:
            self.body = "Received 403 from activation attempt. Device Not in Murano"
        elif self.code == Http_ActivationCodes.NotEnabled:
            self.body = "Received 409 from activation attempt. Device Not Enabled"
        elif self.code == Http_ActivationCodes.Timeout:
            self.body = "Request timed out"
        else:
            self.body = "code: {" + str(self.code) + "} :: Something went wrong."
    def __repr__(self):
        return 'code: {!r}, body: {!r}, success: {!r}'.format(
            self.code, self.body, self.activated)

class WriteHandler(object):
    """
TODO
    """
    def __init__(self, response):
        self.response = response
        self.code = response.status_code
        self.body = response.text
        self.online = True
        self.success = False
        self.authorized = True

        if self.code == Http_ReadWriteCodes.OK or self.code == Http_ReadWriteCodes.NoContent:
            self.body = "No content"
            self.success = True
        elif self.code == Http_ReadWriteCodes.Unauthorized:
            self.body = "No or invalid TOKEN."
            self.authorized = False
        elif self.code in Http_ReadWriteCodes.ClientErrors:
            self.body = "Response code: {" + str(self.code) + "} :: \
There was an error* with the request by the client.  Error Message: " + self.body
        elif self.code in Http_ReadWriteCodes.ServerErrors:
            self.body = "Response code: {" + str(self.code) + "} :: \
There was an error with the request on the server."
        elif self.code == Http_ReadWriteCodes.Timeout:
            self.online = False
    def __repr__(self):
        return 'code: {!r}, body: {!r}, success: {!r}, authorized: {!r}'.format(
            self.code, self.body, self.success, self.authorized)

class RecordHandler(object):
    """
TODO
    """
    def __init__(self, response):
        self.response = response
        self.code = response.status_code
        self.body = response.text
        self.online = True
        self.success = False
        self.authorized = True
        self.conflict = False

        if self.code == Http_ReadWriteCodes.OK or self.code == Http_ReadWriteCodes.NoContent:
            self.body = "No content"
            self.success = True
        elif self.code == Http_ReadWriteCodes.Unauthorized:
            self.body = "No or invalid TOKEN."
            self.authorized = False
        elif self.code == Http_ReadWriteCodes.Conflict:
            self.conflict = True
        elif self.code in Http_ReadWriteCodes.ClientErrors:
            self.body = "Response code: {" + str(self.code) + "} :: \
There was an error* with the request by the client."
        elif self.code in Http_ReadWriteCodes.ServerErrors:
            self.body = "Response code: {" + str(self.code) + "} :: \
There was an error with the request on the server."
        elif self.code == Http_ReadWriteCodes.Timeout:
            self.online = False
    def __repr__(self):
        return('code: {!r}, body: {!r}, success: {!r}, authorized: {!r}, online: {!r}, conflict: {!r}, response: {}'
               .format(self.code, self.body, self.success, self.authorized, self.online, self.conflict, self.response))

    def get_conflict_timestamps(self):
        """
            Returns a list of timestamps that were marked as
            conflicting by Exosite from the body of the response.
        """
        # get rid of % encoding, throw away the dataport/alias name
        # by using index-1 of the '=' split
        data = unquote_plus(self.body).split('=')[1]
        return [float(x) for x in data.split(',')]

class ReadHandler(object):
    """
Hard-wired to urllib.unquote(url).decode('utf-8') all
responses.
    """
    def __init__(self, response):
        self.response = response
        self.code = response.status_code

        if six.PY2:
            self.body = unquote_plus(response.text).decode('utf-8')
        else:
            self.body = unquote_plus(response.text)
        self.online = True
        self.success = False
        self.authorized = True
        # self.last_modified = None

        if self.code == Http_ReadWriteCodes.OK or self.code == Http_ReadWriteCodes.NoContent:
            self.success = True
        elif self.code == Http_ReadWriteCodes.Unauthorized:
            self.body = "No or invalid TOKEN."
            self.authorized = False
        elif self.code == Http_ReadWriteCodes.NotModified:
            self.body = "Not modified"
        elif self.code in Http_ReadWriteCodes.ClientErrors:
            self.body = "There was an error* with the request by the client."
        elif self.code in Http_ReadWriteCodes.ServerErrors:
            self.body = "There was an error with the request on the server."
        elif self.code == Http_ReadWriteCodes.Timeout:
            self.online = False

        """
            TODO: the last-modified header is human-readable. Need to parse this.
            Exception in thread HTTPWatchThread-config_io:
            Traceback (most recent call last):
              File "/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 801, in __bootstrap_inner
                self.run()
              File "/usr/local/lib/python2.7/site-packages/murano_client-1.0.development-py2.7.egg/murano_client/client.py", line 116, in run
                modify_ts=since)
              File "/usr/local/lib/python2.7/site-packages/murano_client-1.0.development-py2.7.egg/murano_client/http.py", line 421, in http_long_poll
                return ReadHandler(self.send_get(url, headers))
              File "/usr/local/lib/python2.7/site-packages/murano_client-1.0.development-py2.7.egg/murano_client/http.py", line 256, in __init__
                self.last_modified = int(self.response.headers.get('Last-Modified'))
            ValueError: invalid literal for int() with base 10: 'Fri, 15 Jun 2018 19:04:13 GMT'
        """

        # if self.response.headers.get('Last-Modified'):
        #     self.last_modified = int(self.response.headers.get('Last-Modified'))
    def __repr__(self):
        return 'code: {}, body: {}, success: {}, authorized: {}'.format(
            self.code, self.body, self.success, self.authorized)

class ReadWriteHandler(object):
    """
Hard-wired to urllib.unquote(url).decode('utf-8') all
responses.
    """
    def __init__(self, response):
        self.response = response
        self.code = response.status_code
        self.body = unquote(response.text).decode('utf-8')
        self.online = True
        self.success = False
        self.authorized = True

        if self.code == Http_ReadWriteCodes.OK or self.code == Http_ReadWriteCodes.NoContent:
            self.success = True
        elif self.code == Http_ReadWriteCodes.Unauthorized:
            self.body = "No or invalid TOKEN."
            self.authorized = False
        elif self.code in Http_ReadWriteCodes.ClientErrors:
            self.body = "There was an error* with the request by the client."
        elif self.code in Http_ReadWriteCodes.ServerErrors:
            self.body = "There was an error with the request on the server."
        elif self.code == Http_ReadWriteCodes.Timeout:
            self.online = False
    def __repr__(self):
        return 'code: {!r}, body: {!r}, success: {!r}, authorized: {!r}'.format(
            self.code, self.body, self.success, self.authorized)


class MuranoHTTP(BaseMuranoClient, object):
    """Instances of the ExositeAPI class contain all methods and members needed to
    interface with the Exosite HTTP Data API. ExositeAPI objects are very versatile and are
    used in a multitude of Gateway Engine components like ``gwe`` and ``gmq``. It is also the
    base-class for the Device class which is a INI-style configuration file based class.

    """
    def __init__(self, **kwargs):
        """
            TODO
        """
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))) if kwargs.get('debug') else None
        LOG.debug("MuranoHTTP init kwargs: {}".format(kwargs))
        BaseMuranoClient.__init__(self, **kwargs)
        self._user_agent = '{}-{}'.format(self.__class__.__name__, __version__)
        if kwargs.get('http_timeout'):
            self._timeout_secs = float(kwargs.get('http_timeout'))
        else:
            self._timeout_secs = float(constants.DEFAULT_HTTP_TIMEOUT)
        LOG.debug("MuranoHTTP timeout: {}".format(self.timeout()))
        self._form_encode = kwargs.get('form_encode')
        self._custom_auth = kwargs.get('custom_auth')
        self._session = None
        self._raise = kwargs.get('raise_exceptions')

        self._activate_url = lambda: urljoin(self.murano_host(), '/provision/activate')
        self._content_url = lambda: urljoin(self.murano_host(), '/provision/download')
        self._stack_alias_url = lambda: urljoin(self.murano_host(), '/onep:v1/stack/alias')
        self._stack_record_url = lambda: urljoin(self.murano_host(), '/onep:v1/stack/record')
        self._http_accept = 'application/x-www-form-urlencoded; charset=utf-8'
        self._http_content_type = 'application/x-www-form-urlencoded; charset=utf-8'

        if self._custom_auth and not isinstance(self._custom_auth, dict):
            assert isinstance(self._custom_auth, dict), \
                "Custom headers must be dictionaries if overridding default (None)."

        if self.using_tls():
            self.set_activated(True)
            self._auth_header = lambda: {}
        else:
            self._auth_header = lambda: {'X-Exosite-CIK' : self.murano_token()} \
                if not isinstance(self._custom_auth, dict) \
                else self._custom_auth

    def __str__(self):
        """ So we can print self representation by calling str(self). """
        return str({
            'version': __version__,
            'murano_host': self.murano_host(),
            'murano_id': self.murano_id()
        })

    def no_form_encode(self):
        """ Turns off the usage of SSL in HTTP API."""
        self._form_encode = False
    def form_encode(self):
        """ Turns on the usage of SSL in HTTP API."""
        self._form_encode = True
    def set_http_debug(self, enable):
        """Sets httplib debug level when 'enable' is set to True. """
        if enable:
            httplib.HTTPConnection.debuglevel = 1
        else:
            httplib.HTTPConnection.debuglevel = 0
    def set_http_timeout(self, timeout):
        self._timeout_secs = timeout
    def timeout(self):
        """ returns :code:`self._timeout_secs`
        """
        return self._timeout_secs
    def url_decode(self, obj):
        """ Helper function to urllib.url_decode objects read from dataports. """
        return unquote_plus(obj)

    def close_session(self):
        self._session.close()

    def _http_listContent(self):
        """ Method for retrieving a list of Content area contents. """
        headers = {'User-Agent' : self._user_agent}
        headers.update(self._auth_header())
        LOG.debug('headers: {}'.format(headers))
        return self.send_get(self._content_url(), headers)

    def _http_getContent(self, content_id, stream=None):
        """ Method to retrieve specific content from Content area. """
        headers = {'User-Agent' : self._user_agent}
        headers.update(self._auth_header())
        url = self._content_url() + '?id={}'.format(quote_plus(content_id))
        return self.send_get(url, headers, stream=stream)

    def _http_getContentInfo(self, content_id):
        """ Method to retrieve information on Content area content. """
        headers = {'User-Agent' : self._user_agent}
        headers.update(self._auth_header())
        url = self._content_url() + '?id={}&info=true'.format(quote_plus(content_id))

        return self.send_get(url, headers)

    def _http_read(self, read_list):
        '''
            read_list: List of data sources to read from
        '''
        headers = {
            'User-Agent' : self._user_agent,
            'Accept' : self._http_accept
        }
        headers.update(self._auth_header())
        url = self._stack_alias_url()
        if read_list:
            url = url + '?'
            for alias in read_list:
                url = url + quote_plus(alias) + '&'
            # trim trailing '&'
            url = url[:-1]
        else:
            raise Exception('Tried to read from Exosite, but no alias given')
        return ReadHandler(self.send_get(url, headers))

    def http_long_poll(self, dataport, timeout_ms=None, modify_ts=None):
        '''
            read_list: List of data sources to read from
        '''
        headers = {
            'User-Agent' : self._user_agent,
            'Accept' : self._http_accept,
        }
        if timeout_ms:
            if isinstance(timeout_ms, int):
                timeout_ms = str(timeout_ms)
            elif isinstance(timeout_ms, float):
                timeout_ms = str(int(timeout_ms))
            headers['Request-Timeout'] = timeout_ms
        headers.update(self._auth_header())
        if modify_ts is not None:
            headers['If-Modified-Since'] = str(int(modify_ts))

        url = self._stack_alias_url() + '?'
        if isinstance(dataport, list):
            for dp in dataport:
                url = url + quote_plus(dp) + '&'
            url = url[:-1]
        else:
            url = url + quote_plus(dataport)

        return ReadHandler(self.send_get(url, headers))

    def _http_write_dict(self, write_dict):
        """ Wrapper function for http_write.
            url_encodes a python dictionary and calls
            http_write.
            Cannot handle nested dicts. """
        body = urlencode(write_dict) if self._form_encode else write_dict
        resp = self._http_write(body)
        return resp

    def _http_write(self, body):
        """ Method to write to a device dataport. """
        headers = {
            'User-Agent' : self._user_agent,
            'Content-Type' : self._http_content_type,
            'Content-Length' : str(len(body))
        }
        headers.update(self._auth_header())
        url = self._stack_alias_url()
        return WriteHandler(self.send_post(url, headers, body))

    def _http_record(self, record_dict):
        """ Method to record to a device dataport.

            The POST data must look like the following:

            ::

                alias=<alias 1>&<timestamp 1>=<value 1>&<timestamp 2>=<value 2>&alias=<alias 2>&<timestamp 3>=<value 3>&<timestamp 4>=<value 4>

            Since this can't be easily decoded with a Python dictionary, the schema
            for the input dictionary must be as follows:

                {'alias1': {'ts1': 'some data', 'ts2': 'some more data'}, 'alias2': {'ts2': 'data data data', 'ts3': 'datum dateo''}}
        """
        data = ''
        record_dict_len = len(record_dict)
        record_keys = list(record_dict)
        for i in range(0, record_dict_len):
            if i > 0:
                data += '&'
            data += 'alias={}'.format(record_keys[i])
            ts_dict = record_dict[record_keys[i]]
            ts_dict_len = len(ts_dict)
            ts_keys = list(ts_dict)
            for j in range(0, ts_dict_len):
                value = quote_plus(ts_dict[ts_keys[j]].encode('utf-8'))
                data += '&{}={}'.format(ts_keys[j], value)


        LOG.debug("Recording data: {}".format(data))
        headers = {
            'User-Agent' : self._user_agent,
            'Content-Type' : self._http_content_type,
            'Content-Length' : str(len(data))
        }
        headers.update(self._auth_header())
        url = self._stack_record_url()
        return RecordHandler(self.send_post(url, headers, data))

    def _http_readwrite(self, read_list, write_dict):
        '''
            read_list: List of data source to read from
            write_dict: Dictionary of k,v to write to.  (Do not url encode)
        '''
        body = urlencode(write_dict) if self._form_encode else write_dict
        headers = {
            'User-Agent' : self._user_agent,
            'Accept' : self._http_accept,
            'Content-Type' : self._http_content_type,
            'Content-Length' : str(len(body))
        }
        headers.update(self._auth_header())
        url = self._stack_alias_url()
        if read_list > 0:
            url = url + '?'
            for alias in read_list:
                url = url + quote_plus(alias) + '&'
            url = url[:-1] # strip off last '&'
        return ReadWriteHandler(self.send_post(url, headers, body))

    def _http_activate(self):
        """ Method to activate device.
            Returns ActivationHandler() object. """

        if not self.using_tls():
            body = 'id={}'.format(self.murano_id())
        else:
            LOG.critical("TLS Client Cert reprovisioning not yet implemented.")
        headers = {
            'User-Agent' : self._user_agent,
            'Content-Type' : self._http_content_type
        }
        _ = headers.update({'Content-Length': str(len(body))}) if not body is None else None
        return ActivationHandler(self.send_post(self._activate_url(), headers, body))

    def _log_curl_cmd(self, method, url, headers, body=None):
        curl_headers = ' '.join(
            [' \\\n    -H "{}: {}"'.format(key, value) \
                for (key, value) in headers.items()
            ]
        )
        cmd = "\ncurl -X {}".format(method) + \
              " \\\n    '{}'".format(url) + \
              "{}".format(curl_headers)
        cmd = cmd + " \\\n    -d '{}'".format(body) if not body is None else cmd
        cmd = cmd + " \\\n    --cert {} \\\n    --key {}".format(
            self.certfile(), self.pkeyfile()) if self.using_tls() else cmd
        cmd = cmd + " \\\n    --cacert {}".format(self.murano_cacert()) if self.murano_cacert() else cmd
        LOG.debug(cmd)

    def send_get(self, url, headers, stream=None, timeout=None):
        """ Method wrapper for requests.get().
            Input req_info: a tuple describing the type of request. Used for data usage
            logging and statistics collection.

            There is one special case in this method. If stream=True,
            then it is assumed that the caller is using wants the raw 'requests'
            object so she may iterate over the streaming content for larger
            file downloads from the Murano content area. Otherwise, the return
            object is of type exo.handlers.Requests_Response.
         """
        cert = None
        try:
            if not self._session:
                self._session = requests.Session()

            if self.using_tls():
                cert = (self.certfile(), self.pkeyfile())
                LOG.debug("Using {} auth for Murano Connection..."
                          .format(cert))
            self._log_curl_cmd('GET', url, headers)
            response = self._session.get(
                url,
                headers=headers,
                timeout=timeout or self.timeout(),
                stream=stream,
                verify=self.murano_cacert() or True,
                cert=cert
            )
        except requests.exceptions.ReadTimeout as __e:
            LOG.info("Caught exception {!r}".format(__e))
            if self._raise:
                raise
            # Treat all exceptions as Timeouts.
            # funky way of giving Requests_Response the
            # object members it needs to perform its duties.
            return type('requests_override', (object,),
                        {'status_code': Http_ReadWriteCodes.Timeout,
                         'text': str(__e),
                         'iter_content': None,
                         'headers': {}})

        LOG.debug("Stream option set to {}".format(stream))
        return response

    def send_post(self, url, headers, body):
        """ Method wrapper for requests.post().
            Input req_info: a tuple describing the type of request. Used for data usage
            logging and statistics collection.
        """
        cert = None
        try:
            if not self._session:
                self._session = requests.Session()
            if self.using_tls():
                cert = (self.certfile(), self.pkeyfile())
                LOG.debug("Using {} auth for Murano Connection..."
                          .format(cert))

            self._log_curl_cmd('POST', url, headers, body=body)
            response = self._session.post(
                url,
                data=body,
                headers=headers,
                timeout=self.timeout(),
                verify=self.murano_cacert() or True,
                cert=cert
            )

        except requests.exceptions.ReadTimeout as __e:
            LOG.info("Caught exception {!r}".format(__e))
            if self._raise:
                raise
            # Treat all exceptions as Timeouts.
            # funky way of giving Requests_Response
            # the object members it needs to perform its duties.
            return type('requests_override', (object,),
                        {'status_code': Http_ReadWriteCodes.Timeout,
                         'text': str(__e),
                         'iter_content': None,
                         'headers': {}})

        return response

    def exosite_timestamp(self):
        """
            Gets the exosite server timestamp from m2.exosite.io/timestamp.

            Returns:
                Timestamp as int.
        """
        headers = {
            'User-Agent' : self._user_agent,
            'Accept' : "*/*"
        }
        return self.send_get(self.murano_host() + 'timestamp', headers)

    def http_activate(self):
        """ Instead of over-riding http_activate(), here is
            logic to deal with activating self. """

        if not self.is_activated():
            act_handler = self._http_activate()
            if act_handler.activated:
                LOG.info("Activation succeeded.")
                self.set_murano_token(act_handler.body)
            else:
                LOG.warning(
                    "Activation for {!r} failed: {!r}".format(
                        str(self), str(act_handler))
                )
        else:
            LOG.info("Already activated.")

    def http_write(self, dataport, value):
        """ Member function that returns WriteHandler(). """
        body = {dataport: value} if self._form_encode else '{}={}'.format(dataport, value)
        LOG.debug("writing ({0}): {1}".format(dataport, value))
        headers = {
            'User-Agent' : self._user_agent,
            'Content-Type' : self._http_content_type,
            'Content-Length' : str(len(body))
        }
        headers.update(self._auth_header())
        url = self._stack_alias_url()

        write_hand = WriteHandler(self.send_post(url, headers, body))
        if write_hand.success:
            pass
        elif write_hand.code == Http_ReadWriteCodes.Unauthorized:
            LOG.debug(
                "BAD TOKEN. Writing {!r} to dataport {!r} failed: {!r}".format(
                    body, dataport, str(write_hand))
            )
            self.set_activated(False)
        else:
            LOG.debug("Error when trying to write {!r} to dataport {!r}: {!r}"
                      .format(body, dataport, str(write_hand)))
        self._online = write_hand.online
        return write_hand

    def http_write_multiple(self, write_dict):
        """ Member function that returns WriteHandler(). """

        LOG.debug("Writing {0}".format(write_dict))
        write_hand = self._http_write_dict(write_dict)
        if write_hand.success:
            pass
        elif write_hand.code == Http_ReadWriteCodes.Unauthorized:
            LOG.debug(
                "BAD TOKEN. Writing {!r} failed: {!r}".format(
                    write_dict, str(write_hand))
            )
            self.set_activated(False)
        else:
            LOG.debug("Error when trying to write {!r}: {!r}".format(
                write_dict, str(write_hand))
                     )
        self._online = write_hand.online
        return write_hand

    def http_record(self, record_dict):
        """ Member function that returns WriteHandler(). """
        # body = ''
        # for dataport in record_dict.keys():
        #   body += '{0}={1}&'.format(dataport, record_dict[dataport])
        # body = body[:-1] # strip off last '&'
        LOG.debug("Recording {0}".format(record_dict))

        record_hand = self._http_record(record_dict)
        if record_hand.success:
            pass
        elif record_hand.code == Http_ReadWriteCodes.Unauthorized:
            LOG.debug(
                "BAD TOKEN. Recording {!r} failed: {!r}".format(
                    record_dict, str(record_hand))
            )
            self.set_activated(False)
        else:
            LOG.debug("Error when trying to write {!r}: {!r}"
                      .format(record_dict, str(record_hand)))
        self._online = record_hand.online
        return record_hand

    def http_read(self, read_list):
        """ Member function that utilizes ReadHandler(). """
        if not isinstance(read_list, list):
            read_list = [read_list]
        read_hand = self._http_read(read_list)
        if read_hand.success:
            pass
        elif read_hand.code == Http_ReadWriteCodes.Unauthorized:
            LOG.debug("BAD TOKEN. Reading {!r} failed: {!r}"
                      .format(read_hand, str(read_hand)))
            self.set_activated(False)
        else:
            LOG.debug("Error when trying to read from dataport(s) {}: {}"
                      .format(read_list, read_hand))
        self._online = read_hand.online
        return read_hand

    def http_read_write(self, read_list, write_dict):
        """ Member function that utilizes ReadWriteHandler(). """
        readwrite_hand = self._http_readwrite(read_list, write_dict)
        if readwrite_hand.success:
            pass
        elif readwrite_hand.code == Http_ReadWriteCodes.Unauthorized:
            LOG.debug("BAD TOKEN. Setting activated = False. Unable to read {!r} nor write {!r}: {!r}"
                      .format(read_list, write_dict, str(readwrite_hand)))
            self.set_activated(False)
        else:
            LOG.debug("Error when trying to read from dataport(s) {!r} and write {!r}: {!r}"
                      .format(read_list, write_dict, str(readwrite_hand)))
        self._online = readwrite_hand.online
        return readwrite_hand

