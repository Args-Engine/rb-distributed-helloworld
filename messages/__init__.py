from .handshake import Handshake
from .available import Available
from .pingpong import Ping
msg_types = {"Handshake": Handshake,
             "Available": Available,
             "Ping": Ping}
