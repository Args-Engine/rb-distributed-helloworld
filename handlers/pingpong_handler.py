import socket
import messages.pingpong as ping


class PingPongHandler:

    @staticmethod
    def handle(client: socket, _, success: bool):
        if success:
            client.send(ping.Ping().to_sendable())
