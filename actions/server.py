import os
import threading
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:  # then Python 2
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class Server(HTTPServer):

    def __init__(self, host, port):
        HTTPServer.__init__(self, (host, int(port)), _RequestHandler)


class _RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        message = str(os.getpid()) if self.path == 'PID' else self.path
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode())

    def do_POST(self):
        if self.path == 'SHUTDOWN':
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_error(400)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass
