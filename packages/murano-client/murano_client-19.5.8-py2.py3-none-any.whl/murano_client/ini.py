""" His module"""

# pylint: disable=I0011,W0312,R0903,C1001,R0201,W0232,C0301,W1202

import os
import logging
from murano_client.client import MuranoClient
from murano_client import logger
# from murano_client.http import MuranoHTTP
# from murano_client.mqtt import MuranoMQTT
from murano_client.atomicconfigparser import atomicconfigparser as IniParser

LOG = logger.getLogger(__name__)

class ExoDeviceException(Exception):
    """ Custom exception class for validating
        user input and improper usage of ExoTLS class.
    """
    def __init__(self, message):
        super(ExoDeviceException, self).__init__(message)

class Device(MuranoClient, object):
    """
        TODO
    """
    def __init__(self, ini_file):
        self._ini_parser = IniParser(allow_no_value=True)
        self._ini_parser.optionxform = str
        self._ini_file = ini_file
        if not os.path.exists(self._ini_file):
            raise ExoDeviceException("Provided config file {!r} does not exist.".format(self._ini_file))
        parent_config = self.get_config_from_ini_file()
        LOG.debug("using config: {}".format(parent_config))
        _ = LOG.setLevel(getattr(logging, parent_config.get('debug'))) if parent_config.get('debug') else None
        MuranoClient.__init__(self, **parent_config)

    def set_murano_host(self, host):
        """ TODO """
        super(Device, self).set_murano_host(host)
        self.dump_to_ini_file('device', 'murano_host', host)

    def set_murano_port(self, port):
        """ TODO """
        super(Device, self).set_murano_port(port)
        self.dump_to_ini_file('device', 'murano_port', port)

    def set_murano_token(self, token):
        """ TODO """
        LOG.debug("TOKEN SET: {}".format(token))
        super(Device, self).set_murano_token(token)
        if token:
            self.dump_to_ini_file('device', 'murano_token', token)

    def set_murano_id(self, uuid):
        """ TODO """
        super(Device, self).set_murano_id(uuid)
        self.dump_to_ini_file('device', 'murano_id', uuid)

    def ini_file(self):
        """ Protected member getter. """
        return self._ini_file

    def get_config_from_ini_file(self):
        """
            Reads INI config files and converts them to a dictionary.
        """
        config = {}
        self._ini_parser.read(self.ini_file())
        sections = self._ini_parser.sections()
        if 'device' not in sections:
            raise ExoDeviceException("No 'device' section found in {}".format(self.ini_file()))
        for section in sections:
            for option in self._ini_parser.options(section):
                # anything in the 'device' section should be added to the
                # config dictionary as top-level keys that will be inputs
                # to the ExositeAPI class as kwargs. any other config sections
                # will be passed with the section as the top-level key to
                # the config settings.
                if 'device' == section:
                    # To accomodate allow_no_value=True, options with no value return
                    # None, which evaluates to False. Since options with no value are
                    # used as booleans that (when present) mean True, so if a get() on
                    # a given option returns None, set to True instead
                    value = self._ini_parser.get(section, option)
                    # if option == 'debug':
                    #     LOG.critical(str((option, value)))
                    #     value = getattr(logging, value, 'INFO')
                    if option == 'murano_port':
                        value = int(value)
                    if option == 'watchlist':
                        value = value.split(',')
                    config[option] = True if value is None else value
                else:
                    # see comment above for the boolean magic explanation
                    config[section] = {} if not config.get(section) else config.get(section)
                    value = self._ini_parser.get(section, option)
                    config[section][option] = True if value is None else value
        return config

    def update_device_from_cfg(self):
        """ Updates Device instance with values from cfg. """
        LOG.debug("Updating member variables from config file: {!r}"
                  .format(self.ini_file()))
        self._ini_parser.read(self.ini_file())

        self.set_murano_token(
            self._ini_parser.get(
                'device', 'murano_token'
            )
        )
        self.set_murano_id(
            self._ini_parser.get(
                'device', 'uuid'
            )
        )

        if self._ini_parser.has_option('device', 'murano_host'):
            self.set_murano_host(
                self._ini_parser.get(
                    'device', 'murano_host'
                )
            )
        if self._ini_parser.has_option('device', 'http_timeout'):
            self.set_http_timeout(
                self._ini_parser.getfloat('device', 'http_timeout')
            )


    def dump_to_ini_file(self, section, option, value):
        """ Utility to dump configuration data to the instance cfg file. """
        if os.path.exists(self.ini_file()):
            with open(self.ini_file(), 'r') as cfg:
                self._ini_parser.readfp(cfg)
                if self._ini_parser.has_section(section):
                    self._ini_parser.set(section, option, value)
                else:
                    LOG.debug("Unable to dump: '{!r}' '{!r}' '{!r}'"
                              .format(section, option, value))
                    return # don't bother writing it, we didn't update anything.
            self._ini_parser.write(self.ini_file())
        else:
            LOG.debug("Can't find configuration file: {!r}".format(self.ini_file()))

    def activate_device(self):
        """ If using TOKEN auth, use the appropriate protocol to retrieve a token and
        save it to the INI file. If using TLS Provisioning, don't do really anything."""
        self.client_activate()
        if self.is_activated():
            if self.using_tls():
                LOG.info("Using TLS Provisioning. No INI file updates needed.")
            else:
                LOG.info("Updating Murano Token in INI file: {}".format(self.ini_file()))
                self.dump_to_ini_file('device', 'murano_token', self.murano_token())

