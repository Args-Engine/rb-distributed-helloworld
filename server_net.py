import select
import socket
import time

import application_params as ap
import messages
import handlers


class Server:
    def __init__(self, middleware):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)

        server_addr = ("localhost", ap.PORT)

        print("Starting to listen on %s:%s" % server_addr)

        self.socket.bind(server_addr)
        self.socket.listen(5)

        self.read_list = [self.socket]

        self.middleware = middleware
        self.sessions = {}

    def communicate(self) -> None:

        for session in self.sessions.values():
            self.middleware.check(session)

        readable, writeable, exceptional = select.select(self.read_list, [], [])
        for s in readable:
            if s is self.socket:
                client_sock, addr = self.socket.accept()
                self.read_list.append(client_sock)
                self.sessions[client_sock] = self.middleware.create_session()
            else:

                # receive Data
                data = s.recv(ap.MAX_MSG_LEN_SRV)

                # get all message types
                for message_key, message_type in messages.msg_types.items():

                    # check if the current message matches the type
                    if message_type.is_this(data=data):

                        session = self.sessions.get(s)
                        if session is None:
                            raise Exception("got data from a client in a different Timeline "
                                            "https://youtu.be/Vpqffgak7To")

                        self.middleware.handle(session, s, message_key, *message_type.from_sendable(data=data))