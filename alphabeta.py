from itertools import permutations
import numpy as np
from typing import List

from state import State
from heuristics.basic import evaluate


def alphabeta(state, depth: int, alpha: int, beta: int, maximizing_player: bool):

    print(f'DEPTH :{depth}')
    if depth == 0:
        return [evaluate(state), None]

    if maximizing_player:
        current_value = -100000
        possible_moves = all_possible_moves(state, state.our_species)
        if possible_moves is None:
            return [-100000, None] # ca veut dire qu'on n'a plus de bonhommes donc qu'on a perdu
        best_move = None
        for move in possible_moves:
            child_state_board = state.next_state([move], state.our_species)
            board_backup = state._board
            state._board = child_state_board
            alphabeta_result = alphabeta(state, depth - 1, alpha, beta, False)[0]
            if current_value < alphabeta_result:
                current_value = alphabeta_result
                best_move = move
            state._board = board_backup
            print(f"current value = {current_value}")
            alpha = max(alpha, current_value)
            if alpha >= beta:
                break # beta cut-off

        return [current_value, best_move]
    else:
        current_value = 100000
        possible_moves = all_possible_moves(state, state.enemy_species)
        if possible_moves is None:
            return [100000, None] # ca veut dire qu'ils n'ont plus de bonhommes donc qu'on a gagné
        best_move = None
        for move in possible_moves:
            child_state_board = state.next_state([move], state.enemy_species)
            board_backup = state._board
            state._board = child_state_board
            alphabeta_result = alphabeta(state, depth - 1, alpha, beta, False)[0]
            if current_value > alphabeta_result:
                current_value = alphabeta_result
                best_move = move
            state._board = board_backup

            beta = min(beta, current_value)
            if alpha >= beta:
                break # alpha cut-off
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
                    (x, y, nb_units, x + 1, y),
                    (x, y, nb_units, x + 1, y + 1),
                    (x, y, nb_units, x, y + 1),
                ]
            elif y == state.nb_rows - 1:
                possible_moves = [
                    (x, y, nb_units, x + 1, y),
                    (x, y, nb_units, x + 1, y - 1),
                    (x, y, nb_units, x, y - 1),
                ]
            else:
                possible_moves = [
                    (x, y, nb_units, x + 1, y + 1),
                    (x, y, nb_units, x + 1, y),
                    (x, y, nb_units, x + 1, y - 1),
                    (x, y, nb_units, x, y + 1),
                    (x, y, nb_units, x, y - 1),
                ]
        elif x == state.nb_columns - 1:
            if y == 0:
                possible_moves = [
                    (x, y, nb_units, x - 1, y),
                    (x, y, nb_units, x - 1, y + 1),
                    (x, y, nb_units, x, y + 1),
                ]
            elif y == state.nb_rows - 1:
                possible_moves = [
                    (x, y, nb_units, x - 1, y),
                    (x, y, nb_units, x - 1, y - 1),
                    (x, y, nb_units, x, y - 1),
                ]
            else:
                possible_moves = [
                    (x, y, nb_units, x - 1, y + 1),
                    (x, y, nb_units, x - 1, y),
                    (x, y, nb_units, x - 1, y - 1),
                    (x, y, nb_units, x, y + 1),
                    (x, y, nb_units, x, y - 1),
                ]
        elif y == 0:
            possible_moves = [
                (x, y, nb_units, x + 1, y + 1),
                (x, y, nb_units, x + 1, y),
                (x, y, nb_units, x - 1, y + 1),
                (x, y, nb_units, x - 1, y),
                (x, y, nb_units, x, y + 1),
            ]
        elif y == state.nb_rows - 1:
            possible_moves = [
                (x, y, nb_units, x + 1, y - 1),
                (x, y, nb_units, x + 1, y),
                (x, y, nb_units, x - 1, y - 1),
                (x, y, nb_units, x - 1, y),
                (x, y, nb_units, x, y - 1),
            ]
        else:
            print('here')
            pos = set(permutations([-1, -1, 0, 1, 1], 2))
            possible_moves = [(x, y, nb_units, x - t, y - u) for (t, u) in pos]
    print(possible_moves)
    return possible_moves


