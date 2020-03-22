import time

from client import ClientSocket
from heuristics.basic import Heuristic
from state import State
from response import respond, respond_test


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
    heuristic = Heuristic()
    while True:
        client_socket.get_message()
        state.update(client_socket.message)
        if client_socket.message[0] == "upd":
            t2 = time.time()
            nb_moves, moves = strategy(state, heuristic)
            t3 = time.time()
            print(f"time to think about strategy : {t3 - t2}")
            client_socket.send_mov(nb_moves, moves)


if __name__ == '__main__':
    play_game(respond_test)
