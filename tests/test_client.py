import string

import pytest

from actions import Client
from actions.utils import IS_WINDOWS


@pytest.mark.parametrize('letter', string.ascii_letters)
def test_client(letter):
    c = Client('run-server')
    assert c.request(letter) == letter
    c.shutdown_server()


@pytest.mark.parametrize('letter', string.ascii_letters)
def test_multiple_clients(letter):
    clients = [Client('run-server') for _ in range(10)]
    for client in clients:
        assert client.request(letter) == letter
    for client in clients:
        client.shutdown_server()


@pytest.mark.skipif(not IS_WINDOWS, reason='only valid on Windows')
@pytest.mark.parametrize('letter', string.ascii_letters)
def test_client_exe(letter):
    c = Client('frozen-server')
    assert c.request(letter) == letter
    c.shutdown_server()


@pytest.mark.parametrize('port', [10000, 20000, 30000, 40000, 50000, 60000, 61000, 62000])
def test_port(port):
    c = Client('run-server', port=port)
    assert c._conn.port == port
    c.shutdown_server()


@pytest.mark.skipif(not IS_WINDOWS, reason='only valid on Windows')
@pytest.mark.parametrize('port', [10000, 20000, 30000, 40000, 50000, 60000, 61000, 62000])
def test_port_exe(port):
    c = Client('frozen-server', port=port)
    assert c._conn.port == port
    c.shutdown_server()
