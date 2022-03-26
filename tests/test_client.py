import string

import pytest

from actions import Client


@pytest.mark.parametrize('letter', string.ascii_letters)
def test_client(letter):
    c = Client()
    assert c.request(letter) == letter
    c.shutdown_server()


@pytest.mark.parametrize('letter', string.ascii_letters)
def test_multiple_clients(letter):
    clients = [Client() for _ in range(10)]
    for client in clients:
        assert client.request(letter) == letter
    for client in clients:
        client.shutdown_server()
