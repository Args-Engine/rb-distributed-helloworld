import time
import handlers
import socket


class ServerMiddleware:

    def __init__(self,coordinator):
        self.coordinator = coordinator

    class Session:
        def __init__(self):
            self.timestamp = time.time()


    def check(self, session: Session) -> bool:
        return session.timestamp - time.time() > 2

    def create_session(self) -> Session:
        print("Creating Session for new Client")
        return self.Session()

    def handle(self, session: Session, s: socket, key: str, msg, success: bool) -> None:
        print(msg)
        print(key)
        handler = handlers.handler_types.get(key)
        if handler is not None:
            handler(s, msg, success)
            session.timestamp = time.time()
        else:
            if key == "Available":
                self.coordinator.inform(session, msg.available)
                self.coordinator.answer(session, s)
