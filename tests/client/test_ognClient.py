import unittest
import unittest.mock as mock

from ogn.client.client import create_aprs_login, AprsClient
from ogn.client.settings import APRS_APP_NAME, APRS_APP_VER


class OgnClientTest(unittest.TestCase):
    def test_create_aprs_login(self):
        basic_login = create_aprs_login('klaus', -1, 'myApp', '0.1')
        self.assertEqual('user klaus pass -1 vers myApp 0.1\n', basic_login)

        login_with_filter = create_aprs_login('klaus', -1, 'myApp', '0.1', 'r/48.0/11.0/100')
        self.assertEqual('user klaus pass -1 vers myApp 0.1 filter r/48.0/11.0/100\n', login_with_filter)

    def test_initialisation(self):
        client = AprsClient(aprs_user='testuser', aprs_filter='')
        self.assertEqual(client.aprs_user, 'testuser')
        self.assertEqual(client.aprs_filter, '')

    @mock.patch('ogn.client.client.socket')
    def test_connect_full_feed(self, mock_socket):
        client = AprsClient(aprs_user='testuser', aprs_filter='')
        client.connect()
        client.sock.send.assert_called_once_with('user testuser pass -1 vers {} {}\n'.format(APRS_APP_NAME, APRS_APP_VER).encode('ascii'))
        client.sock.makefile.asser_called_once_with('rw')

    @mock.patch('ogn.client.client.socket')
    def test_disconnect(self, mock_socket):
        client = AprsClient(aprs_user='testuser', aprs_filter='')
        client.connect()
        client.disconnect()
        client.sock.shutdown.assert_called_once_with(0)
        client.sock.close.assert_called_once_with()