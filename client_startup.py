from client_net import Client
from client.middleware import ClientMiddleware
from client.dispatcher import Dispatcher

if __name__ == "__main__":
    C = Client("localhost", ClientMiddleware(Dispatcher()))
    while True:
        C.communicate()
