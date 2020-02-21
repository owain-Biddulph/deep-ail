from client import ClientSocket
import config
from state import State
from response import respond




def play_game(strategy):
    client_socket = ClientSocket()
    client_socket.send_NME("DeepAIl")
    # set message
    client_socket.get_message()
    state = State(client_socket.message)
    print(f"received rows: {state.nb_rows}, cols : {state.nb_columns}")
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

    #start of the game
    while(True):
        client_socket.get_message()
        state.update(client_socket.message)
        if client_socket.message[0] == "upd":
            nb_moves, moves = strategy(state)
            client_socket.send_MOV(nb_moves, moves)

if __name__ == '__main__':
    play_game(respond)

