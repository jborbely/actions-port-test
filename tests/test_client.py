import string

import pytest

from actions import Client

@pytest.mark.parametrize('letter', string.ascii_letters)
def test_client(letter):
    c = Client()
    assert c.request(letter) == letter
    c.shutdown_server()
