from typing import Tuple, List

from state import State


def respond(state: State) -> Tuple[int, List]:
    # Basic test, always moves left
    moves = []
    for x in range(state.nb_rows):
        for y in range(state.nb_columns):
            if state.board[x, y, 0] == state.our_species:
                moves += [[x, y, state.board[x, y, 1], max(0, x-1), y]]
    return len(moves), moves
