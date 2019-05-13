import zerorpc
import threading
from .config import CONNECTIONADDRESS,AGENT_INFO_PATH,UUIDPATH
from utils import getlogger
from .mes import Message
from .state import *
from .executor import Executor


logger = getlogger(__name__,AGENT_INFO_PATH)

class ConnectionManager:
    def __init__(self):
        self.client = zerorpc.Client()
        self.event = threading.Event()
        self.message = Message(UUIDPATH)
        self.state = WATTING
        self.executor = Executor()

    def start(self,timeout=5):
        try:
            self.event.clear()
            self.client.connect(CONNECTIONADDRESS)
            print(self.client.sendmsg(self.message.reg()))
            while not self.event.wait(timeout):
                print(self.client.sendmsg(self.message.heartbeat()))

                if self.state == WATTING:
                    task = self.client.get_task(self.message.id)
                    if task:
                        self.state = RUNNING

                        code, output = self.executor.run(task[1], task[2])
                        # if code ==0:
                        #     self.state = SUCCEED
                        #     pass
                        # else:
                        #     self.state = FAILED
                        print(self.client.sendmsg(self.message.result(task[0],code,output)))
                        state = SUCCEED if code == 0 else FAILED

                        self.client.set_task(task[0],state)

                        self.state = WATTING

        except Exception as e:
            logger.error('{}'.format(e))
            raise e

    def shutdown(self):
        self.event.set()
        self.client.close()













