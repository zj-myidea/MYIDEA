from .cm import ConnectionManager
from utils import getlogger
import threading


logger = getlogger(__name__,'./agent.log')
class Agent:

    def __init__(self):
        self.connect = ConnectionManager()
        self.event = threading.Event()

    def start(self):
        while not self.event.is_set():
            try:
                self.connect.start()
            except Exception as e:
                logger.error('{}'.format(e))
                self.connect.shutdown()
            self.event.wait(3)
    def shutdown(self):
        self.connect.shutdown()
        self.event.set()









