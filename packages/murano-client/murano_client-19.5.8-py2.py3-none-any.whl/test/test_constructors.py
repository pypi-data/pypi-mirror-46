import unittest
from murano_client.client import MuranoClient, MuranoClientException, MuranoHTTP

class TestMuranoClient(unittest.TestCase):
    def test_no_kwargs(self):
        with self.assertRaises(MuranoClientException):
            MuranoClient()
    def test_no_watchlist(self):
        with self.assertRaises(MuranoClientException):
            MuranoClient(
                murano_host='mqtt://f5330e5s8cho0000.m2.exosite.io/')
    def test_good_mqtt_url(self):
        client = MuranoClient(
            watchlist=['config_io'],
            murano_host='mqtt://f5330e5s8cho0000.m2.exosite.io/'
        )
        self.assertEqual('mqtt', client.outbound_protocol)
    def test_good_http_url(self):
        client = MuranoClient(
            watchlist=['config_io'],
            murano_host='https://f5330e5s8cho0000.m2.exosite.io/'
        )
        self.assertEqual('https', client.outbound_protocol)


class TestMuranoHttp(unittest.TestCase):
    def test_urljoin(self):
        # With "/" at the end of murano_host
        http = MuranoHTTP(murano_host='https://f5330e5s8cho0000.m2.exosite.io/')
        self.assertEqual('https://f5330e5s8cho0000.m2.exosite.io/provision/activate', http._activate_url())
        # Without "/" at the end of murano_host
        http = MuranoHTTP(murano_host='https://f5330e5s8cho0000.m2.exosite.io')
        self.assertEqual('https://f5330e5s8cho0000.m2.exosite.io/provision/activate', http._activate_url())


def main():
    unittest.main()

if __name__ == "__main__":
    main()
