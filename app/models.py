
from enum import Enum

class ResponseStatus(Enum):
    OK = 0
    FAIL = 1

class Task:
    task = None
    status = None
    data = None

    def __init__(self, task, status, taskData):
        self.task = task
        self.status = status
        self.data = taskData

    def serialize(self):
        return {
            'task': self.task,
            'status': self.status,
            'data': self.data.serialize()
        }

class TaskData:
    device = None

    def __init__(self, device):
        self.device = device

class CmdData(TaskData):
    cmd = None

    def __init__(self, device, cmd):
        super().__init__(device)
        self.cmd = cmd

    def serialize(self):
        return {
            'device': self.device,
            'cmd': self.cmd
        }

class PingData(TaskData):

    def __init__(self, device):
        super().__init__(device)

    def serialize(self):
        return {
            'device': self.device
        }
