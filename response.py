from typing import Tuple, List
import time
from state import State
from alphabeta import alphabeta
from math import inf


def respond(state: State) -> Tuple[int, List]:
    # Basic test, always moves left
    moves = []

    state_copy = state.copy_state()

    moves.append(alphabeta(state_copy, 4, -inf, inf, True)[1])
    return len(moves), moves


