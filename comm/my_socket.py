import socketserver


class QueueHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.server = server
        server.client_address = client_address
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        data = self.request.recv(8192)
        self.server.recv_q.put(data)
