from typing import Tuple, List
import time
from state import State
from alphabeta import alphabeta



def respond(state: State) -> Tuple[int, List]:
    # Basic test, always moves left
    moves = []

    state_copy = state.copy_state()
    print("YOO")
    print(state_copy)
    print(state_copy.enemy_species)
    time.sleep(1)
    moves.append(alphabeta(state_copy, 5, -100000, 100000, True)[1])
    print(moves)
    return len(moves), moves


