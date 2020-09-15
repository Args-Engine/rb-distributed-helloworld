from messages.task import Task
from threading import Thread


class Coordinator:

    def __init__(self, file):
        self.sessions = {}
        self.tasks = []
        self.lines = file.readlines()
        self.max_threads = 0
        self.parser_thread = Thread(target=self.parse)
        self.parser_thread.run()


    def inform(self, session, available):
        if not session in self.sessions:
            self.max_threads += available
        self.sessions[session] = available

    def answer(self, session, sock):
        available = self.sessions.get(session, 0)
        tasks = self.tasks[:min(available, len(self.tasks))]
        sock.send(Task(tasks).to_sendable())
        self.tasks = self.tasks[min(available, len(self.tasks)):]

    def parse(self):
        for line in self.lines:
            if line.strip().startswith("RUN"):
                self.tasks += [line.strip()[4:]]
            if line.strip().startswith("WAIT"):
                while sum(self.sessions.values()) != self.max_threads:
                    pass