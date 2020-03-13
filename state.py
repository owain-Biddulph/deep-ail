from typing import List, Tuple

import numpy as np

import utils


class State:
    """Class to represent the board state
    The board is a nb_rows x nb_columns x 2 numpy array, the first 2D layer represents the species, the 2nd the number
    """

    def __init__(self, set_message: Tuple[str, Tuple[int, int]]) -> None:
        self._nb_rows: int = set_message[1][0]
        self._nb_columns: int = set_message[1][1]
        self._board: np.ndarray = np.zeros((self.nb_columns, self.nb_rows, 2), dtype=int)
        self._house_list: List[Tuple[int, int]] = []
        self._starting_square = None
        self.our_species = None
        self.enemy_species = None

        self.our_troops: List[int] = None
        self.enemy_troops: List[int] = None
        self.vampire_troops: List[int] = [0]
        self.werewolf_troops: List[int] = [0]

        self.our_tiles: List[List[int]] = None
        self.enemy_tiles: List[List[int]] = None
        self.human_tiles: List[List[int]] = list()
        self.vampire_tiles: List[List[int]] = list()
        self.werewolf_tiles: List[List[int]] = list()

    @property
    def nb_rows(self) -> int:
        return self._nb_rows

    @property
    def nb_columns(self) -> int:
        return self._nb_columns

    @property
    def board(self) -> np.ndarray:
        return self._board

    def display_board(self):
        print(np.transpose(self._board, axes=(0, 2, 1)))

    def update(self, message) -> None:
        """
        Update board state

        :param message: message from server
        """
        if message[0] == "hum":
            self._house_list = message[1]

        elif message[0] == "hme":
            self._starting_square = message[1]

        elif message[0] == "map":
            x_home, y_home = self._starting_square
            werewolf_tiles = list()
            vampire_tiles = list()
            werewolf_troops = 0
            vampire_troops = 0

            for change in message[1]:
                # il y a des humains
                if change[2] != 0:
                    self._board[change[0], change[1], 0] = 1
                    self._board[change[0], change[1], 1] = change[2]
                    self.human_tiles.append([change[0], change[1], change[2]])

                # il y a des vampires
                if change[3] != 0:
                    self._board[change[0], change[1], 0] = 2
                    self._board[change[0], change[1], 1] = change[3]
                    self.vampire_tiles.append([change[0], change[1], change[3]])
                    self.vampire_troops[0] += change[3]
                    if (change[0], change[1]) == (x_home, y_home):
                        self.our_species = 2
                        self.enemy_species = 3

                # il y a des loups garous
                if change[4] != 0:
                    self._board[change[0], change[1], 0] = 3
                    self._board[change[0], change[1], 1] = change[4]
                    self.werewolf_tiles.append([change[0], change[1], change[4]])
                    self.werewolf_troops[0] += change[4]
                    if (change[0], change[1]) == (x_home, y_home):
                        self.our_species = 3
                        self.enemy_species = 2

            if self.our_species == 2:  # nous sommes les vampires
                self.our_tiles = vampire_tiles
                self.our_troops = vampire_troops
                self.enemy_tiles = werewolf_tiles
                self.enemy_troops = werewolf_troops

            elif self.our_species == 3:  # nous sommes les loups garous
                self.our_tiles = werewolf_tiles
                self.our_troops = werewolf_troops
                self.enemy_tiles = vampire_tiles
                self.enemy_troops = vampire_troops

        elif message[0] == "upd":
            for change in message[1]:
                # il y a des humains
                if change[2] != 0:
                    self._board[change[0], change[1], 0] = 1
                    self._board[change[0], change[1], 1] = change[2]

                # il y a des vampires
                elif change[3] != 0:
                    self._board[change[0], change[1], 0] = 2
                    self._board[change[0], change[1], 1] = change[3]
                    self.vampire_tiles.append([change[0], change[1], change[3]])
                    self.vampire_troops[0] += change[
                        3]  # TODO c'est faux, si les troupes se déplacent, on n'en ajoute pas.

                # il y a des loups garous
                elif change[4] != 0:
                    self._board[change[0], change[1], 0] = 3
                    self._board[change[0], change[1], 1] = change[4]
                    self.werewolf_tiles.append([change[0], change[1], change[4]])
                    self.werewolf_troops[0] += change[4]

                # quelque chose est parti
                else:
                    self._board[change[0], change[1], 0] = 0
                    self._board[change[0], change[1], 1] = 0
                    # on cherche les cases à enlever s'il y en a

    def __add_unit(self, n, x, y, species_to_add):
        # Add n units in (x,y) position.
        if self.board[x, y, 0] == 0:
            # No unit in (x,y). Settlement of n units.
            self.board[x, y, 1] = n
            self.board[x, y, 0] = species_to_add
        else:
            # If the outcome is certain, return that, otherwise return a loss
            win_probability = utils.win_probability(n, self.board[x, y, 1], self.board[x, y, 0])
            if win_probability in [0, 1]:
                (species, survivors) = utils.battle_simulation(n, species_to_add, self.board[x, y, 1],
                                                               self.board[x, y, 0])
            else:
                species = self.board[x, y, 0]
                survivors = np.random.binomial(self.board[x, y, 1], 1-win_probability)
            self.board[x, y, 1] = survivors
            self.board[x, y, 0] = species

    def __remove_unit(self, n, x, y):
        # Remove n units in (x,y) position.
        if n < self.board[x, y, 1]:
            # Removing n units.
            self.board[x, y, 1] -= n
        elif n == self.board[x, y, 1]:
            # Removing all the units and cleaning the board.
            self.board[x, y, :] = 0
        else:
            raise Exception('nope')

    def next_state(self, moves, species):
        # Given a list of moves, outputs the next board state.
        # self.display_board()
        for move in moves:
            x_init, y_init = move[0], move[1]
            n = move[2]
            x_end, y_end = move[3], move[4]
            self.__remove_unit(n, x_init, y_init)
            self.__add_unit(n, x_end, y_end, species)
        # self.display_board()

    def copy_state(self):
        """
        return a copy of self as a new State object
        
        :return: State object
        """
        copy = State(("set", (self._nb_rows, self._nb_columns)))

        copy._nb_rows = self._nb_rows
        copy._nb_columns = self._nb_columns
        copy._board = np.copy(self._board)
        copy._house_list = np.copy(self._house_list)
        copy._starting_square = np.copy(self._starting_square)
        copy.our_species = self.our_species
        copy.enemy_species = self.enemy_species

        copy.our_troops = self.our_troops
        copy.enemy_troops = self.enemy_troops
        copy.vampire_troops = self.vampire_troops
        copy.werewolf_troops = self.werewolf_troops

        copy.our_tiles = self.our_tiles
        copy.enemy_tiles = self.enemy_tiles
        copy.human_tiles = self.human_tiles
        copy.vampire_tiles = self.vampire_tiles
        copy.werewolf_tiles = self.werewolf_tiles

        return copy
