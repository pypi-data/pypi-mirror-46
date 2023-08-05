import json
import time

import pytest

from murano_client.client import MuranoClient, NoMemoryQueueMuranoClient


def test_MuranoClient_can_import_right_class(mocker):
    NoMemoryQueueMuranoClient = mocker.patch(
        'murano_client.client.NoMemoryQueueMuranoClient')
    MemoryQueueMuranoClient = mocker.patch(
        'murano_client.client.MemoryQueueMuranoClient')
    MuranoClient(memory_queue=False)
    NoMemoryQueueMuranoClient.assert_called_once()

    MuranoClient(memory_queue=True)
    MemoryQueueMuranoClient.assert_called_once()


def test_NoMemoryQueueMuranoClient_can_init(mocker):
    client = NoMemoryQueueMuranoClient(murano_host='mqtt://jrxncdkk2ls00000.m2.exosite.io/',
                                       watchlist=['config_io'])
    assert client.outbound_protocol == 'mqtt'
    client = NoMemoryQueueMuranoClient(murano_host='https://jrxncdkk2ls00000.m2.exosite.io/',
                                       watchlist=['config_io'])

    assert client.outbound_protocol == 'https'

    # For stopping client properly when using https
    client.start_client()
    client.stop_all()


class Response(object):
    def __init__(self, boolean):
        self.success = boolean
    def wait_for_publish(self):
        pass
    def is_published(self):
        return self.success


class TestNoMemoryQueueMuranoClientTell():

    def test_use_https_and_tell_success(self, mocker):
        client = NoMemoryQueueMuranoClient(murano_host='https://jrxncdkk2ls00000.m2.exosite.io/',
                                        watchlist=['config_io'])

        mocker.patch.object(client, 'http_record', return_value=Response(True))
        status, result = client.tell(
            resource='aa', timestamp=time.time(), payload=json.dumps({}))
        assert status

        client.start_client()
        client.stop_all()

    def test_use_matt_and_tell_fail(self, mocker):
        client = NoMemoryQueueMuranoClient(murano_host='mqtt://jrxncdkk2ls00000.m2.exosite.io/',
                                        watchlist=['config_io'])

        mocker.patch.object(client, 'publish', return_value=Response(False))
        status, result = client.tell(
            resource='aa', timestamp=time.time(), payload={})
        assert not status

    def test_use_mqtt_and_payloads(self, mocker):
        client = NoMemoryQueueMuranoClient(murano_host='mqtt://jrxncdkk2ls00000.m2.exosite.io/',
                                        watchlist=['config_io'])

        mocker.patch.object(client, 'publish', return_value=Response(True))
        data = json.dumps([{
            'timestamp': time.time(),
            'values': {
                'resource': 'payload'
            }
        }])
        status, result = client.tell(payloads=data)
        assert status
