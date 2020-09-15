import socket
import application_params as ap
import messages


class Client:
    def __init__(self, addr: str, middleware):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.sock.connect_ex((addr, ap.PORT)) != 0:
            print("Connection failed, host not up!")

        self.established = False
        self.middleware = middleware

    def communicate(self) -> None:

        message = self.middleware.emit()

        self.sock.send(message.to_sendable())
        data = self.sock.recv(ap.MAX_MSG_LEN_CLIENT)

        for message_key, message_type in messages.msg_types.items():
            if message_type.is_this(data=data):
                self.middleware.consume(message_key, *message_type.from_sendable(data=data))
