import os
import time
import socket
import warnings
import subprocess
try:
    from http.client import HTTPConnection, CannotSendRequest
except ImportError:  # then Python 2
    from httplib import HTTPConnection, CannotSendRequest

from . import utils


class Client(object):

    def __init__(self, host='127.0.0.1', port=None, timeout=10.0):
        self._conn = None
        self._proc = None
        self._pid = None

        if port is None:
            port = utils.get_available_port()

        # start the server
        flags = 0x08000000 if utils.IS_WINDOWS else 0  # fixes issue 31, CREATE_NO_WINDOW = 0x08000000
        self._proc = subprocess.Popen(['run-server', host, str(port)], stderr=subprocess.PIPE, stdout=subprocess.PIPE, creationflags=flags)
        try:
            utils.wait_for_server(host, port, timeout)
        except OSError as err:
            self._wait(timeout=0, stacklevel=4)
            # if the subprocess was killed then self._wait sets returncode to -2
            if self._proc.returncode != -2:
                stderr = self._proc.stderr.read()
                err.reason = stderr.decode(encoding='utf-8', errors='replace')
            raise

        # connect to the server
        self._conn = HTTPConnection(host, port=port)
        reply = self.request('PID')
        self._pid = int(reply)

    def request(self, message):
        self._conn.request('GET', message)
        response = self._conn.getresponse()
        if response.status == 200:
            return response.read().decode()
        raise ValueError('got status {} -- {}'.format(response.status, response.read()))

    def shutdown_server(self, kill_timeout=10):
        try:
            self._conn.request('POST', 'SHUTDOWN')
        except CannotSendRequest:
            # can occur if the previous request raised ResponseTimeoutError
            # send the shutdown request again
            self._conn.close()
            self._conn = HTTPConnection(self._conn.host, port=self._conn.port)
            self._conn.request('POST', 'SHUTDOWN')

        self._wait(timeout=kill_timeout, stacklevel=3)

        # the frozen 32-bit server can still block the process from terminating
        # the <signal.SIGKILL 9> constant is not available on Windows
        if self._pid:
            try:
                os.kill(self._pid, 9)
            except OSError:
                pass  # the server has already stopped

        self._conn.sock.shutdown(socket.SHUT_RDWR)
        self._conn.close()
        self._conn = None
        return self._proc.stdout, self._proc.stderr

    def _wait(self, timeout=10., stacklevel=3):
        # give the server a chance to shut down gracefully
        t0 = time.time()
        while self._proc.poll() is None:
            time.sleep(0.1)
            if time.time() - t0 > timeout:
                self._proc.terminate()
                self._proc.returncode = -2
                warnings.warn('killed the 32-bit server using brute force', stacklevel=stacklevel)
                break
