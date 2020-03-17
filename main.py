from client import ClientSocket
from state import State
from response import respond
import time


def play_game(strategy):
    client_socket = ClientSocket()
    client_socket.send_nme("DeepAIl")
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

    # start of the game
    while True:
        client_socket.get_message()
        state.update(client_socket.message)
        t2 = time.time()
        if client_socket.message[0] == "upd":
            nb_moves, moves = strategy(state)
            t3 = time.time()
            print(f"time to think about strategy : {t3 - t2}")
            client_socket.send_mov(nb_moves, moves)


if __name__ == '__main__':
    play_game(respond)
