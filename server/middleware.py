import time
import handlers
import socket


class ServerMiddleware:
    class Session:
        def __init__(self):
            self.timestamp = time.time()

    def check(self, session: Session) -> bool:
        return session.timestamp - time.time() > 2

    def create_session(self) -> Session:
        return self.Session()

    def handle(self, session: Session, s: socket, key: str, msg, success: bool) -> None:
        handler = handlers.handler_types.get(key)
        if handler is not None:
            handler(s, msg, success)
            session.timestamp = time.time()
        else:
            raise Exception("this Middleware does not support non-default messages")