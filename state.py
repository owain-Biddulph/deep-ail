from typing import List, Tuple
import numpy as np


class State:
    """Class to represent the board state
    The board is a nb_rows x nb_columns x 2 numpy array, the first 2D layer represents the species, the 2nd the number
    """
    def __init__(self, set_message: Tuple[str, Tuple[int, int]]) -> None:
        self._nb_rows: int = set_message[1][0]
        self._nb_columns: int = set_message[1][1]
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

    ##renvoie la liste des cases où sont situés les vampires et leur nombre
    @property
    def vampire(self) -> List:
        vampire_list = []
        for i in range(self._nb_rows):
            for j in range(self._nb_columns):
                if self._board[i, j, 0] == 0: ##verifier que c'est bien cette valeur pour les vampires
                    vampire_list.append([i, j, self._board[i, j, 1]])
        return vampire_list

    ##renvoie la liste des cases où sont situés les werewolves et leur nombre
    @property
    def werewolf(self) -> List:
        werewolf_list = []
        for i in range(self.nb_rows):
            for j in range(self.nb_columns):
                if self._board[i, j, 0] == 1: ##verifier que c'est bien cette valeur pour les werewolves
                    werewolf_list.append([i, j, self._board[i, j, 1]])
        return werewolf_list

    ##renvoie la liste des cases où sont situés les humains et leur nombre
    @property
    def human(self) -> List:
        human_list = []
        for i in range(self.nb_rows):
            for j in range(self.nb_columns):
                if self._board[i, j, 0] == 2: ##verifier que c'est bien cette valeur pour les humans
                    human_list.append([i, j, self._board[i, j, 1]])
        return human_list

    ##renvoie la liste des mouvements possibles depuis notre state, et en format message (pour qu'on puisse le mettre en entrée de la méthode update dans accessible_state)
    def accessible_moves(self):     ##je fais pour les vampires au débuts
        moves = []
        vampires = self.vampire()
        for vampire in vampires:
            possible_moves = vampire

        return moves

    ##renvoie la liste des boards accessibles depuis le state actuel
    def accessible_states(self):
        states = []
        moves = self.accessible_moves()
        for move in moves:
            state = State(( "???", (self._nb_rows, self._nb_columns))) ##qu'est ce que prend state en entrée
            state._board = self._board
            states.append(state.update(move))
        return states






