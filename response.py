from typing import Tuple, List
from state import State
from alphabeta import alphabeta
from math import inf


def respond(state: State, heuristic) -> Tuple[int, List]:
    state_copy = state.copy_state()
    times = [0, 0, 0]
    _, moves, times = alphabeta(state_copy, 3, -inf, inf, True, heuristic, times)
    print("\n")
    print(f"time to get moves: {times[0]}, time to remove illegal: {times[1]}")
    print(f"time to score: {times[2]}")
    return len(moves), moves


