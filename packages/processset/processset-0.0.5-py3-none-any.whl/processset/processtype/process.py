from multiprocessing import Process as p

from processset.job import Job


class Process:
    pid: int

    def __init__(self, job: Job):
        self.process = p(target=job)

    def start(self):
        self.process.start()
        self.pid = self.process.pid

    def kill(self):
        self.process.kill()

    def is_alive(self):
        return self.process.is_alive()
