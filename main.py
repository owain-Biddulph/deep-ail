from client import ClientSocket
import config
from state import State
from response import response


def main():
    client_socket = ClientSocket()
    client_socket.send_message(("nme", "DeepAil"))
    # set message
    client_socket.get_message()
    state = State(client_socket.message)
    # hum message
    client_socket.get_message()
    state.update(client_socket.message)
    # hme message
    client_socket.get_message()
    state.update(client_socket.message)
    # map message
    client_socket.get_message()
    state.update(client_socket.message)

if "__name__" == "__main__":
    main()