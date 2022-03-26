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
    c = Client('start_server')
    assert c.request(letter) == letter
    c.shutdown_server()
