from itertools import permutations
import numpy as np
from typing import Tuple, List
import time
import random

from state import State


def respond(state: State) -> Tuple[int, List]:
    # Basic test, always moves left
    moves = []
    possible_moves = all_possible_moves(state)
    time.sleep(0.5)
    moves.append(random.choice(possible_moves))
    print(moves)
    return len(moves), moves


def all_possible_moves(state: State) -> List:
    our_squares = list(zip(*np.where(state.board[:, :, 0] == state.our_species)))
    print(our_squares)
    possible_moves = None
    for square in our_squares:
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
            print('here')
            possible_moves = [
                (x, y, nb_units, x + 1, y - 1),
                (x, y, nb_units, x + 1, y),
                (x, y, nb_units, x - 1, y - 1),
                (x, y, nb_units, x - 1, y),
                (x, y, nb_units, x, y - 1),
            ]
        else:
            pos = set(permutations([-1, -1, 0, 1, 1], 2))
            possible_moves = [(x, y, nb_units, x - t, y - u) for (t, u) in pos]

        return possible_moves
