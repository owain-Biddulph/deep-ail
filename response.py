from typing import Tuple, List
from state import State
from alphabeta import alphabeta, TimeError
from math import inf


class GlobalStrategy:
    def __init__(self, alphabeta_depth, heuristic):
        self.alphabeta_depth = alphabeta_depth
        self.heuristic = heuristic

    def respond(self, state: State, time_message_received) -> Tuple[int, List]:
        state_copy = state.copy_state()
        times = [0, 0, 0]
        _, moves, reduce_depth, times = alphabeta(state_copy, self.alphabeta_depth, -inf, inf, True, self.heuristic,
                                    time_message_received, times)
        if reduce_depth:
            self.alphabeta_depth -= 1
        # print("\n")
        # print(f"time to get moves: {times[0]}, time to remove illegal: {times[1]}")
        # print(f"time to score: {times[2]}")
        return len(moves), moves
