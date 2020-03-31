import time

from client import ClientSocket
from heuristics.basic import Heuristic
from state import State
from response import GlobalStrategy
from argparse import ArgumentParser


def play_game(strategy, args):
    client_socket = ClientSocket(args.ip, args.port)
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
        time_message_received = time.time()
        state.update(client_socket.message)
        if client_socket.message[0] == "upd":
            t2 = time.time()
            nb_moves, moves = strategy.respond(state, time_message_received)
            t3 = time.time()
            print(f"time to think about strategy : {t3 - t2}")
            client_socket.send_mov(nb_moves, moves)


if __name__ == '__main__':
    parser = ArgumentParser(description='This script launches the connection and the game.')

    parser.add_argument(dest='ip', default='localhost', type=str, help='IP adress the connection should be made to.')
    parser.add_argument(dest='port', default='5555', type=int, help='Chosen port for the connection.')

    args = parser.parse_args()
    heuristic = Heuristic()
    strategy = GlobalStrategy(3, heuristic)
    play_game(strategy, args)
