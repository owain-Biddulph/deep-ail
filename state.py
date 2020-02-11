from typing import List, Tuple
import numpy as np


class State:
    """Class to represent the board state
    The board is a nb_rows x nb_columns x 2 numpy array, the first 2D layer represents the species, the 2nd the number
    """
    def __init__(self, set_message: Tuple[str, Tuple[int, int]]) -> None:
        self._nb_rows: int = set_message[1][0]
        self._nb_columns: int = set_message[1][0]
        self._board: np.ndarray = np.zeros((self.nb_rows, self.nb_columns, 2), dtype=int)
        self._house_list: List[Tuple[int, int]] = []
        self._starting_square = None

    @property
    def nb_rows(self) -> int:
        return self._nb_rows

    @property
    def nb_columns(self) -> int:
        return self._nb_columns

    @property
    def board(self) -> np.ndarray:
        return self._board

    def update(self, message) -> None:
        if message[0] == "hum":
            self._house_list = message[1]
        elif message[0] == "hme":
            self._starting_square = message[1]
        elif message[0] == "map" or "upd":
            for change in message[1]:
                try:
                    species: int = np.nonzero(change[2:])[0][0] + 1
                    self._board[change[0], change[1], 1] = change[1 + species]
                except IndexError:
                    species: int = 0
                    self._board[change[0], change[1], 1] = 0
                self._board[change[0], change[1], 0] = species
