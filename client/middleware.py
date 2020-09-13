import messages
import client_connect as cc


class ClientMiddleware:

    def __init__(self):
        self.tasks = []
        self.client_connect = cc.ClientConnect()

    def emit(self):
        if not self.client_connect.ready:
            return self.client_connect.emit()
        else:
            if len(self.tasks) == 0:
                return messages.Ping()

            else:
                raise Exception("not implemented yet")

    def consume(self, key: str, msg, success: bool):
        if not self.client_connect.ready and self.client_connect.consume(key, success):
            pass
        else:
            pass
