import datetime
import uuid
from .task import Task
from .state import *



class Storage:
    def __init__(self):
        self.agents = {}
        self.tasks = {}

    def reg_hb(self,**kwargs):
        id = kwargs['id']
        agent = self.agents.get(id)
        if not agent:
            agent ={}
        agent['timestamp'] = datetime.datetime.now().timestamp()
        agent['busy'] = False
        agent['info'] = kwargs
        self.agents[id] = agent

    def add_task(self, task:dict):
        task['task_id'] = uuid.uuid4().hex
        task = Task(**task)
        self.tasks[task.id] = task
        return task.id

    def get_agent(self):
        return list(self.agents.keys())

    def iter_task(self, states={WATTING,RUNNING}):
        yield from (task for task in self.tasks.values() if task.state in states)

    def get_task(self,agent_id):
        for task in self.iter_task():
            if agent_id in task.targets:
                if task.state == WATTING:
                    task.state = RUNNING

                task.targets[agent_id]['state'] = RUNNING
                return [task.id, task.script, task.timeout]

    def result(self,msg:dict):
        task = self.tasks[msg['id']]
        agent = task.targets[msg['agent_id']]
        agent['state'] = SUCCEED if msg['code'] ==0 else FAILED








