import messages
import client_connect as cc


class ClientMiddleware:

    def __init__(self, dispatcher):
        self.client_connect = cc.ClientConnect()
        self.dispatcher = dispatcher

    def emit(self):
        if not self.client_connect.ready:
            return self.client_connect.emit()
        else:
            if self.dispatcher.available != 0:
                return messages.Available(self.dispatcher.get_available())

            else:
                return messages.Ping()

    def consume(self, key: str, msg, success: bool):
        if not self.client_connect.ready and self.client_connect.consume(key, success):
            pass
        else:
            if success:
                if key == "Task":
                    self.dispatcher.ingest(msg.tasks)
