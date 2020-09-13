from client_net import Client
from client.middleware import ClientMiddleware

if __name__ == "__main__":
    C = Client("localhost", ClientMiddleware())
    while True:
        C.communicate()
