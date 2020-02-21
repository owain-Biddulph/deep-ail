from typing import Any, Tuple

from state import State


def respond(state:State):
    #pour l'instant, on va juste toujours à gauche
    nb_moves = 0
    moves = []
    for x in range(state.nb_rows):
        for y in range(state.nb_columns):
            species = state.board[0, x, y]
            if species == state.our_species:
                nb_moves +=1
                moves += [[x, y, state.board[1, x, y], x-1, y]]
    return (nb_moves, moves)


