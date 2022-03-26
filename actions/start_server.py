import sys

from actions import Server


def run():
    host, port = sys.argv[1:]
    s = Server(host, port)
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        s.server_close()


if __name__ == '__main__':
    sys.exit(run())
