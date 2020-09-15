import application_params as ap
from typing import List

"""
Message Structure:

    2 bytes of id length + the word '~Task' (=id) + 2 byte of tasks (=N)+
    N * ( 2 bytes of task len (=Z) + Z bytes of task ) 
    
    i.e: 0x000A+b'~Task'+0x00010011+b'echo Hello World'
"""


class Task:
    id = b'~Task'
    id_len = len(id)
    min_msg_len = ap.INT_LEN + id_len + ap.INT_LEN

    def __init__(self, tasks: List[str]):
        self.tasks = tasks

    def to_sendable(self):
        return int.to_bytes(self.id_len, ap.INT_LEN, byteorder=ap.BYTE_ORDER, signed=ap.SIGNED) \
               + self.id \
               + int.to_bytes(len(self.tasks), ap.INT_LEN, byteorder=ap.BYTE_ORDER, signed=ap.SIGNED) \
               + self.tasks_to_bytes()

    def tasks_to_bytes(self):

        data = b''
        for task in self.tasks:
            task_len = len(task)

            data += int.to_bytes(task_len, ap.INT_LEN, byteorder=ap.BYTE_ORDER, signed=ap.SIGNED)
            data += task.encode('ascii')

        return data

    @staticmethod
    def is_this(data: bytes):

        # Check if the bytes are the right length
        if len(data) < Task.min_msg_len:
            return False

        # Decode bytes
        msz = int.from_bytes(data[:ap.INT_LEN], byteorder=ap.BYTE_ORDER, signed=ap.SIGNED)
        msg = data[ap.INT_LEN:msz + ap.INT_LEN]

        # Check if decoded length is correct
        if msz != Task.id_len:
            return False

        # Check if decoded message is correct
        if msg != Task.id:
            return False

        # All Checks Passed
        return True

    @staticmethod
    def from_sendable(data: bytes):
        if Task.is_this(data):
            numTasks = int.from_bytes(data[ap.INT_LEN + Task.id_len:ap.INT_LEN + Task.id_len+ap.INT_LEN],
                                      byteorder=ap.BYTE_ORDER, signed=ap.SIGNED)

            tasks = []

            raw_task_data = data[ap.INT_LEN * 2 + Task.id_len:]

            for x in range(numTasks):
                task, remainder = Task.decode_task(raw_task_data)
                tasks += [task]
                raw_task_data = remainder

            return Task(tasks), True
        return None, False

    @staticmethod
    def decode_task(data: bytes):

        task_len = int.from_bytes(data[:ap.INT_LEN], byteorder=ap.BYTE_ORDER, signed=ap.SIGNED)
        task = data[ap.INT_LEN:ap.INT_LEN+task_len].decode('ascii')

        return task, data[ap.INT_LEN + task_len:]


if __name__ == "__main__":
    p = Task(["echo Hello World", "find *.obj"])

    raw = p.to_sendable()

    p1, failure = Task.from_sendable(raw)

    print(p1.tasks)
