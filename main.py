from client import ClientSocket
from state import State
from response import respond
import time


def play_game(strategy):
    t0 = time.time()
    client_socket = ClientSocket()
    t1 = time.time()
    print(f"time to connect to socket : {t1 - t0}")
    client_socket.send_nme("DeepAIl")
    t2 = time.time()
    print(f"time to send NME : {t2 - t1}")
    # set message
    client_socket.get_message()
    t3 = time.time()
    print(f"time to get SET message : {t3 - t2}")
    state = State(client_socket.message)
    t4 = time.time()
    print(f"time to initialize state : {t4 - t3}")
    # hum message
    client_socket.get_message()
    t5 = time.time()
    print(f"time to get HUM message : {t5 - t4}")
    state.update(client_socket.message)
    t6 = time.time()
    print(f"time to update state with HUM : {t6 - t5}")
    # hme message
    client_socket.get_message()
    t7 = time.time()
    print(f"time to get HME message : {t7 - t6}")
    state.update(client_socket.message)
    t8 = time.time()
    print(f"time to update state with HME : {t8 - t7}")
    # map message
    client_socket.get_message()
    t9 = time.time()
    print(f"time to get MAP message : {t9 - t8}")
    state.update(client_socket.message)
    t10 = time.time()
    print(f"time to update state with MAP : {t10 - t9}")

    # start of the game
    while True:
        t0 = time.time()
        client_socket.get_message()
        t1 = time.time()
        print(f"time to get UPD message : {t1 - t0}")
        state.update(client_socket.message)
        t2 = time.time()
        print(f"time to update state with UPD : {t2 - t1}")
        if client_socket.message[0] == "upd":
            nb_moves, moves = strategy(state)
            t3 = time.time()
            print(f"time to think about strategy : {t3 - t2}")
            client_socket.send_mov(nb_moves, moves)
            t4 = time.time()
            print(f"time to send MOV message : {t4 - t3}")


if __name__ == '__main__':
    play_game(respond)
