from .handshake_handler import HandshakeHandler
from .pingpong_handler import PingPongHandler

handler_types = {"Handshake": HandshakeHandler.handle,
                 "Ping": PingPongHandler.handle}
