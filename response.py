from typing import Tuple, List
from state import State
from alphabeta import alphabeta, TimeError
from math import inf
from systeme_expert.moteur_deduction import chainage
from systeme_expert.regles_expert import Facts, Rules


class GlobalStrategy:
    """Class to manage the strategy to adopt for the turn, also allows to manage the alphabeta depth"""
    def __init__(self, alphabeta_depth, heuristic):
        self.alphabeta_depth = alphabeta_depth
        self.heuristic = heuristic

    def respond(self, state: State, time_message_received) -> Tuple[int, List]:
        if len(state.human_species.tile_coordinates()) == 0:
            # No more humans, switch to expert system
            return self.respond_with_expert_system(state, time_message_received)
        else:
            return self.respond_with_alphabeta(state, time_message_received)

    def respond_with_alphabeta(self, state: State, time_message_received) -> Tuple[int, List]:
        state_copy = state.copy_state()
        always_split = False
        _, moves, reduce_depth = alphabeta(state_copy, self.alphabeta_depth, -inf, inf, True, self.heuristic,
                                           time_message_received, always_split)
        if reduce_depth:
            self.alphabeta_depth -= 1
        return len(moves), moves

    @staticmethod
    def respond_with_expert_system(state: State, time_message_received) -> Tuple[int, List]:
        state_copy = state.copy_state()
        strategy = chainage(Facts, Rules, state_copy)
        moves = strategy.play(state, time_message_received)

        return len(moves), moves
