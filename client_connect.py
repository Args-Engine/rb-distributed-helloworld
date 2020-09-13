import messages


# Client Middleware extension to establish communication with the server
class ClientConnect:

    def __init__(self):
        self.ready = False

    @staticmethod
    def emit():
        print("Establishing handshake with server!")
        return messages.Handshake()

    def consume(self, key: str, success: bool):
        print("Received response from server")
        self.ready = (key == "Handshake") and success
        if self.ready:
            print("Handshake complete")

        return self.ready
