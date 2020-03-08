from itertools import permutations
import numpy as np
from typing import List

from state import State
from heuristics.basic import evaluate


def alphabeta(state, depth: int, alpha: int, beta: int, maximizing_player: bool):

    if depth == 0:
        return [evaluate(state), None]

    if maximizing_player:
        current_value = -100000
        possible_moves = all_possible_moves(state, state.our_species)
        if possible_moves is None:
            return [-100000, None]  # No more friendly units, we have lost
        best_move = None
        for move in possible_moves:
            child_state = state.copy_state()
            child_state.next_state([move], state.our_species)
            alphabeta_result = alphabeta(child_state, depth - 1, alpha, beta, False)[0]
            if current_value < alphabeta_result:
                current_value = alphabeta_result
                best_move = move
            alpha = max(alpha, current_value)
            if alpha >= beta:
                break  # beta cut-off

        return [current_value, best_move]
    else:
        current_value = 100000
        possible_moves = all_possible_moves(state, state.enemy_species)
        if possible_moves is None:
            return [100000, None]  # No more enemy units, we have won
        best_move = None
        for move in possible_moves:
            child_state = state.copy_state()
            child_state.next_state([move], state.enemy_species)
            alphabeta_result = alphabeta(state, depth - 1, alpha, beta, False)[0]
            if current_value > alphabeta_result:
                current_value = alphabeta_result
                best_move = move

            beta = min(beta, current_value)
            if alpha >= beta:
                break  # alpha cut-off
        return [current_value, best_move]


def all_possible_moves(state: State, species: int) -> List:
    active_squares = list(zip(*np.where(state.board[:, :, 0] == species)))
    possible_moves = None
    for square in active_squares:
        x, y = square
        nb_units = state.board[x, y, 1]
        # Ugly but I think it is probably the fastest way
        # TODO: check
        if x == 0:
            if y == 0:
                possible_moves = [
                    (x, y, nb_units, x + 1, y + 1),
                    (x, y, nb_units, x + 1, y),
                    (x, y, nb_units, x, y + 1),
                ]
            elif y == state.nb_rows - 1:
                possible_moves = [
                    (x, y, nb_units, x + 1, y - 1),
                    (x, y, nb_units, x + 1, y),
                    (x, y, nb_units, x, y - 1),
                ]
            else:
                possible_moves = [
                    (x, y, nb_units, x + 1, y),
                    (x, y, nb_units, x + 1, y + 1),
                    (x, y, nb_units, x + 1, y - 1),
                    (x, y, nb_units, x, y + 1),
                    (x, y, nb_units, x, y - 1),
                ]
        elif x == state.nb_columns - 1:
            if y == 0:
                possible_moves = [
                    (x, y, nb_units, x - 1, y + 1),
                    (x, y, nb_units, x - 1, y),
                    (x, y, nb_units, x, y + 1),
                ]
            elif y == state.nb_rows - 1:
                possible_moves = [
                    (x, y, nb_units, x - 1, y - 1),
                    (x, y, nb_units, x - 1, y),
                    (x, y, nb_units, x, y - 1),
                ]
            else:
                possible_moves = [
                    (x, y, nb_units, x - 1, y),
                    (x, y, nb_units, x - 1, y + 1),
                    (x, y, nb_units, x - 1, y - 1),
                    (x, y, nb_units, x, y + 1),
                    (x, y, nb_units, x, y - 1),
                ]
        elif y == 0:
            possible_moves = [
                (x, y, nb_units, x, y + 1),
                (x, y, nb_units, x + 1, y + 1),
                (x, y, nb_units, x - 1, y + 1),
                (x, y, nb_units, x + 1, y),
                (x, y, nb_units, x - 1, y),
            ]
        elif y == state.nb_rows - 1:
            possible_moves = [
                (x, y, nb_units, x, y - 1),
                (x, y, nb_units, x + 1, y - 1),
                (x, y, nb_units, x - 1, y - 1),
                (x, y, nb_units, x + 1, y),
                (x, y, nb_units, x - 1, y),
            ]
        else:
            possible_moves = [
                (x, y, nb_units, x, y + 1),
                (x, y, nb_units, x, y - 1),
                (x, y, nb_units, x + 1, y),
                (x, y, nb_units, x - 1, y),
                (x, y, nb_units, x + 1, y + 1),
                (x, y, nb_units, x - 1, y - 1),
                (x, y, nb_units, x + 1, y - 1),
                (x, y, nb_units, x - 1, y + 1),
            ]
    return possible_moves


