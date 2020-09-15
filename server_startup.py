from server_net import Server
from server.middleware import ServerMiddleware
from server.coordinator import Coordinator

if __name__ == "__main__":

    file = open("hivemind.txt", "r")
    S = Server(ServerMiddleware(Coordinator(file)))
    while True:
        S.communicate()
