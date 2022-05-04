import socket
import socketserver
from queue import Queue

from .my_socket import QueueHandler


class TCPServer(socketserver.TCPServer):
    def __init__(self, ip, port, handler_class=QueueHandler):
        socketserver.TCPServer.__init__(
            self, (ip, port), handler_class, bind_and_activate=False
        )
        self.recv_q = Queue()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_bind()
        self.server_activate()

    def shutdown(self):
        socketserver.TCPServer.shutdown(self)

    def __del__(self):
        self.server_close()
