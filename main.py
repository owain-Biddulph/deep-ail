from client import ClientSocket
import config
from state import State
from response import respond


#def strategy(state):
    #return(nb_moves, moves)


def strategiedebile(state):
    nb_moves = 0
    moves = []
    for y in range(state.nb_rows):
        for x in range(state.nb_columns):
            # print(x, y, 'display')
            state.display_board()
            species = state.board[0, x, y]
            if species == state.our_species:
                print(f"species : {species}, our species : {state.our_species}")
                nb_moves +=1
                moves += [[x, y, state.board[1, x, y], x-1, y]]
                print(f"playing move {moves}")
    return (nb_moves, moves)

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
    play_game(strategiedebile)

