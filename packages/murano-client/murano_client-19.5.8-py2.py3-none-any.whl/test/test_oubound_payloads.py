import os
import unittest
import uuid
import time
import json
import logging
from six.moves import queue
from murano_client.client import OutboundPayload, MuranoClient

test_dir = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class TestOutboundPayloads(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
    @classmethod
    def tearDownClass(cls):
        pass
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_maxretries_default(self):
        self.assertEqual(OutboundPayload.MaxRetries, 10)
    def test_override_maxretries(self):
        OutboundPayload.override_maxretries(1)
        self.assertEqual(OutboundPayload.MaxRetries, 1)
    def test_inc_retries(self):
        tell = OutboundPayload(
            payload='dummy',
            timestamp=time.time(),
            outbound_protocol='https')
        tell.inc_retries()
        self.assertEqual(tell.retries(), 1)


class TestTellFunctionOverride(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
    @classmethod
    def tearDownClass(cls):
        pass
    def setUp(self):
        self.test_q = queue.Queue()

        def tell_function_override(o_payload):
            self.test_q.put(o_payload)

        self.client = MuranoClient(
            murano_host='https://dne.m2.exosite.io/',
            watchlist=['config_io'],
            tell_function_override=tell_function_override
        )

    def tearDown(self):
        pass

    def test_001_tell_function_override(self):
        self.client.tell_thread.start()
        obp = OutboundPayload(
            resource="it_doesn't_matter",
            timestamp=1234567890.0,
            payload="what the rock is cooking",
            outbound_protocol=self.client.outbound_protocol)
        self.client.outbound_queue.put(obp)
        time.sleep(0.1) # give some time for the tell thread to do its job
        self.client.tell_thread.stop()
        self.assertEqual(obp.resource, list(self.test_q.get())[0])


def main():
    unittest.main()

if __name__ == "__main__":
    main()
