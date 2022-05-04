from .server import TCPServer

import os
import json
import socket
import threading
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
HABITAT_IP = os.environ.get("HABITAT_IP")
JANET_IP = os.environ.get("JANET_IP")


class Exchange:
    def __init__(self, janet_q):
        self.janet_q = janet_q

        self.server = TCPServer(HABITAT_IP, 9999)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        
        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.receive_thread.start()

    def receive(self):        
        while True:
            message = self.server.recv_q.get()
            if message:
                self.janet_q.put(message)

    def send(self, message):
        try:
            # TODO: Change this to use environ
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((JANET_IP, 9998))
            sock.send(message.encode())
            sock.close()
        except Exception as e:
            print(e)
    
    def destroy(self):
        self.server.shutdown()
