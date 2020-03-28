from typing import Tuple, List
from state import State
from alphabeta import alphabeta, TimeError
from math import inf
from systeme_expert.moteur_deduction import chainage
from systeme_expert.regles_expert import Faits, Regles



class GlobalStrategy:
    def __init__(self, alphabeta_depth, heuristic):
        self.alphabeta_depth = alphabeta_depth
        self.heuristic = heuristic

    def respond(self, state: State, time_message_received) -> Tuple[int, List]:
        if len(state.human_species.tile_coordinates()) == 0:
            # no more humans, switch to expert system
            return self.respond_with_expert_system(state, time_message_received)
        else:
            return self.respond_with_alphabeta(state, time_message_received)

    def respond_with_alphabeta(self, state: State, time_message_received) -> Tuple[int, List]:
        state_copy = state.copy_state()
        times = [0, 0, 0]
        always_split = False
        _, moves, reduce_depth, times = alphabeta(state_copy, self.alphabeta_depth, -inf, inf, True, self.heuristic,
                                    time_message_received, times, always_split)
        if reduce_depth:
            self.alphabeta_depth -= 1
        # print("\n")
        # print(f"time to get moves: {times[0]}, time to remove illegal: {times[1]}")
        # print(f"time to score: {times[2]}")
        return len(moves), moves

    def respond_with_expert_system(self, state: State, time_message_received) -> Tuple[int, List]:
        state_copy = state.copy_state()
        strategy = chainage(Faits, Regles, state_copy)
        moves = strategy.play(state, time_message_received)

        return len(moves), moves
