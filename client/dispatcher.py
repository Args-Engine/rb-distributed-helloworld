from multiprocessing import cpu_count
from queue import Queue
from threading import Thread
from .runner import Runner


class Dispatcher:

    def __init__(self):
        self.tasks = Queue()
        self.available = cpu_count()
        self.runners = []



        self.manage_thread = Thread(target=self.run)
        self.manage_thread.start()



    def get_available(self):
        return max(self.available, 1)

    def ingest(self, tasks):
        self.available -= len(tasks)
        for task in tasks:
            self.tasks.put(task)

    def run(self):
        while True:
            if not self.tasks.empty():
                task = self.tasks.get()
                self.runners += [Runner(task, task)]
                
            for runner in self.runners:
                if runner.done():
                    self.available += 1
                    self.runners.remove(runner)
