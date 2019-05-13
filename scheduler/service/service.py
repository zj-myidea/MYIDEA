import zerorpc
from .cm import ConnectionManager
from .config import CONNECTIONADDRESS

class Master:
    def __init__(self):
        self.server = zerorpc.Server(ConnectionManager())

    def start(self):
        self.server.bind(CONNECTIONADDRESS)
        self.server.run()

    def shutdown(self):
        self.server.close()