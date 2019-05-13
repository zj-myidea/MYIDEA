from .storage import Storage


class ConnectionManager:
    def __init__(self):
        self.store = Storage()
    def handle(self,msg):
        if msg['type'] in {'register', 'heartbeat'}:
            self.store.reg_hb(**msg['payload'])
        elif msg['type'] == 'result':
            self.store.result(msg['payload'])
        return 'send back {}'.format(msg)

    def add_task(self,msg:dict):
        return self.store.add_task(msg)

    def get_task(self, agent_id):
        return self.store.get_task(agent_id)
    sendmsg = handle

    def get_agents(self):
        return self.store.get_agent()

    def set_task(self,task_id, state):
        self.store.tasks[task_id].state = state