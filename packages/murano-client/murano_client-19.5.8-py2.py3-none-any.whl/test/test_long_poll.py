import os
import unittest
import uuid
import time
import logging
from murano_client.client import MuranoClient, MuranoClientException, MuranoHTTP

class TestLongPoll(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not 'MURANO_HOST' in os.environ:
            cls.fail(cls, 'need MURANO_HOST')

        cls.client = MuranoClient(
            murano_host=os.environ['MURANO_HOST'],
            murano_id="unittest.test.test_long_poll-{}".format(uuid.uuid1()),
            watchlist=['config_io'],
            debug='DEBUG'
        )
        cls.client.http_activate()
        print(cls.client.murano_token())
    @classmethod
    def tearDownClass(cls):
        pass
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_timeout_ms_int(self):
        resp = self.client.http_long_poll(
            'config_io', timeout_ms=1000)
        self.assertEqual(304, resp.code)
    def test_timeout_ms_str(self):
        resp = self.client.http_long_poll(
            'config_io', timeout_ms='1000')
        self.assertEqual(304, resp.code)
    def test_timeout_ms_float(self):
        resp = self.client.http_long_poll(
            'config_io', timeout_ms=1000.0)
        self.assertEqual(304, resp.code)

    def test_timeout_ms_int_modify_ts_int(self):
        resp = self.client.http_long_poll(
            'config_io', timeout_ms=1000, modify_ts=int(time.time()-10))
        self.assertEqual(304, resp.code)
    def test_timeout_ms_str_modify_ts_str(self):
        resp = self.client.http_long_poll(
            'config_io', timeout_ms='1000', modify_ts=str(int(time.time()-10)))
        self.assertEqual(304, resp.code)
    def test_timeout_ms_float_modify_ts_float(self):
        resp = self.client.http_long_poll(
            'config_io', timeout_ms=1000.0, modify_ts=float(time.time()-10))
        self.assertEqual(304, resp.code)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
