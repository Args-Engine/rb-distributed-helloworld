import socket
import messages.handshake as hs


class HandshakeHandler:

    @staticmethod
    def handle(client: socket, _, success: bool):
        if success:
            client.send(hs.Handshake().to_sendable())
