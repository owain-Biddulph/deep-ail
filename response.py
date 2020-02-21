from typing import Tuple, List

from state import State


def respond(state: State) -> Tuple[int, List]:
    # Basic test, always moves left
    nb_moves = 0
    moves = []
    for x in range(state.nb_rows):
        for y in range(state.nb_columns):
            species = state.board[x, y, 0]
            if species == state.our_species:
                nb_moves +=1
                moves += [[x, y, state.board[x, y, 1], x-1, y]]
    return nb_moves, moves
