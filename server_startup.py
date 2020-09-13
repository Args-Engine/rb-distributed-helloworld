from server_net import Server
from server import middleware

if __name__ == "__main__":
    S = Server(middleware.ServerMiddleware())
    while True:
        S.communicate()