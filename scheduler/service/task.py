from .state import *


class Task:
    def __init__(self,task_id, script,targets,timeout=0, paraller=1,
                 fail_rate=0, fail_count=-1):
        self.id = task_id
        self.script = script
        self.targets = {agent_id:{'state':WATTING,'output':''}for agent_id in targets}
        self.timeout= timeout
        self.paraller = paraller
        self.fail_rate = fail_rate
        self.fail_count = fail_count
        self.state = WATTING
        self.target_count = len(targets)
