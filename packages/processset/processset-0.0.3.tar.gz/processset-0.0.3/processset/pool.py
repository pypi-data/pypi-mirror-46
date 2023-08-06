"""
    processset - pool
"""

from typing import List

from processset.job import Job
from processset.processtype import Process


class Pool:
    size: int = 0
    job: Job
    nodes: List[Process] = []

    def __init__(self, size: int, job: Job):
        self.job = job
        self.increase(size)

    def increase(self, size: int):
        self.size += size
        for _ in range(size):
            new_process = Process(job=self.job)
            self.nodes.append(new_process)
            new_process.start()

    def decrease(self, size: int):
        self.size -= size
        self.size = max(self.size, 0)
        for _ in range(size):
            if not self.nodes:
                break
            removed_process = self.nodes.pop(0)
            removed_process.kill()

    def destroy(self):
        self.decrease(self.size)

    def debug(self):
        nodes = filter(lambda p: p.is_alive(), self.nodes)
        nodes = list(map(lambda p: str(p.pid), nodes))
        print("%s alive nodes, pids: %s" % (len(nodes), " ".join(nodes)))
