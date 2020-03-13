from typing import Tuple, List
import time
from state import State
from alphabeta import alphabeta
from math import inf


def respond(state: State) -> Tuple[int, List]:
    # Basic test, always moves left
    moves = []

    state_copy = state.copy_state()
    print("YOO")
    print(state_copy)
    print(state_copy.enemy_species)

    moves.append(alphabeta(state_copy, 2, -inf, inf, True)[1])
    print(moves)
    return len(moves), moves


