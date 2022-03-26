import sys
import time
import socket
import subprocess

IS_WINDOWS = sys.platform == 'win32'
IS_LINUX = sys.platform.startswith('linux')


def is_port_in_use(port):
    flags = 0
    if IS_WINDOWS:
        flags = 0x08000000
        cmd = ['netstat', '-a', '-n', '-p', 'TCP']
    elif IS_LINUX:
        cmd = ['ss', '-ant']
    else:
        cmd = ['lsof', '-nPw', '-iTCP']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=flags)
    out, err = p.communicate()
    if err:
        raise RuntimeError(err.decode(errors='ignore'))
    return out.find(b':%d ' % port) > 0


def get_available_port():
    sock = socket.socket()
    sock.bind(('', 0))  # any available port
    port = sock.getsockname()[1]
    sock.close()
    return port


def wait_for_server(host, port, timeout):
    stop = time.time() + max(0.0, timeout)
    while True:
        if is_port_in_use(port):
            return

        if time.time() > stop:
            raise OSError(
                'Timeout after {:.1f} seconds. '
                'Could not connect to {}:{}'.format(timeout, host, port)
            )
