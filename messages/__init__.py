from .handshake import Handshake
from .available import Available
from .pingpong import Ping
from .task import Task

msg_types = {"Handshake": Handshake,
             "Available": Available,
             "Ping": Ping,
             "Task": Task}
