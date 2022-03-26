import sys

from .server import Server
from .client import Client


def run():
    host, port = sys.argv[1:]
    s = Server(host, port)
    try:
        s.serve_forever()
    finally:
        s.server_close()
        return 0
