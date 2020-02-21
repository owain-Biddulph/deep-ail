from client import ClientSocket
from state import State
from response import respond


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
    # upd message
    client_socket.get_message()
    state.update(client_socket.message)

    # start of the game
    while True :
        client_socket.get_message()
        state.update(client_socket.message)
        if client_socket.message[0] == "upd":
            nb_moves, moves = strategy(state)
            client_socket.send_mov(nb_moves, moves)


if __name__ == '__main__':
    play_game(respond)
