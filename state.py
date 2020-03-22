from collections import defaultdict
from typing import List, Tuple, Iterable, Optional

import numpy as np

import utils


class Species:
    """Class to contain the a tile list, and unit count for a given species, with some handy methods"""
    def __init__(self, type_: Optional[int] = None, l: List[Tuple[int, int, int]] = None):
        self.tiles: defaultdict = defaultdict(lambda: 0)
        if l is not None:
            self.tiles.update({(x, y): n for x, y, n in l})
        self.units: int = sum(self.tiles.values())
        self.type: int = type_

    def remove_tile(self, coordinates: Tuple[int, int]):
        self.units -= self.tiles.pop(coordinates, 0)

    def tile_coordinates(self) -> List[Tuple[int, int]]:
        return list(self.tiles.keys())

    def tile_contents(self): #-> List[ [int, int, int]]:
        """Returns a list of the species tile coordinates and contents ordered incrementally by unit count"""
        return sorted(list(map(lambda x: (x[0][0], x[0][1], x[1]), self.tiles.items())), key=lambda x: x[-1])

    def add_units(self, coordinates: Tuple[int, int], units: int):
        self.tiles[coordinates] += units
        self.units += units

    def remove_units(self, coordinates: Tuple[int, int], units: int):
        if units >= self.tiles[coordinates]:
            self.units -= self.tiles.pop(coordinates, 0)
        else:
            self.tiles[coordinates] -= units
            self.units -= units

    def update_tile(self, update: Iterable[int]):
        self.remove_tile(update[:2])
        if update[self.type+1] != 0:
            self.add_units(update[:2], update[self.type+1])


class State:
    """Class to represent the board state
    The board is a nb_rows x nb_columns x 2 numpy array, the first 2D layer represents the species, the 2nd the number
    """

    def __init__(self, set_message: Tuple[str, Tuple[int, int]], set_species: bool = True) -> None:
        self._nb_rows: int = set_message[1][0]
        self._nb_columns: int = set_message[1][1]
        self._board: np.ndarray = np.zeros((self.nb_columns, self.nb_rows, 2), dtype=int)
        self._house_list: List[Tuple[int, int]] = []
        self._starting_square = None
        self.our_species: Optional[Species] = None
        self.enemy_species: Optional[Species] = None
        self.human_species: Optional[Species] = None
        if set_species:
            self.our_species = Species()
            self.enemy_species = Species()
            self.human_species = Species(1)

    @property
    def nb_rows(self) -> int:
        return self._nb_rows

    @property
    def nb_columns(self) -> int:
        return self._nb_columns

    @property
    def board(self) -> np.ndarray:
        return self._board

    def update_board(self, update: Iterable[int]):
        x, y = update[:2]
        if update[2] != 0:
            self._board[x, y, 0] = 1
            self._board[x, y, 1] = update[2]
        elif update[3] != 0:
            self._board[x, y, 0] = 2
            self._board[x, y, 1] = update[3]
        elif update[4] != 0:
            self._board[x, y, 0] = 3
            self._board[x, y, 1] = update[4]
        else:
            self._board[x, y, :] = 0

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
            # Determine species
            for change in message[1]:
                if change[3] != 0:
                    if (change[0], change[1]) == (x_home, y_home):
                        self.our_species.type = 2
                        self.enemy_species.type = 3
                    else:
                        self.our_species.type = 3
                        self.enemy_species.type = 2
                    break
                if change[4] != 0:
                    if (change[0], change[1]) == (x_home, y_home):
                        self.our_species.type = 3
                        self.enemy_species.type = 2
                    else:
                        self.our_species.type = 2
                        self.enemy_species.type = 3
                    break
            for change in message[1]:
                self.update_board(change)
                self.our_species.update_tile(change)
                self.enemy_species.update_tile(change)
                self.human_species.update_tile(change)

        elif message[0] == "upd":
            for change in message[1]:
                self.update_board(change)
                self.our_species.update_tile(change)
                self.enemy_species.update_tile(change)
                self.human_species.update_tile(change)

    def __add_unit(self, n, x, y, species_to_add):
        # Add n units in (x,y) position.
        if self.board[x, y, 0] == 0:  # No unit in (x,y), just add n units.
            self.board[x, y, 1] = n
            self.board[x, y, 0] = species_to_add
            if species_to_add == 1:
                self.human_species.add_units((x, y), n)
            elif species_to_add == self.our_species.type:
                self.our_species.add_units((x, y), n)
            else:
                self.enemy_species.add_units((x, y), n)

        elif self.board[x, y, 0] == species_to_add:  # The target tile contains the same species, just add them
            self.board[x, y, 1] += n
            if species_to_add == 1:
                self.human_species.add_units((x, y), n)
            elif species_to_add == self.our_species.type:
                self.our_species.add_units((x, y), n)
            else:
                self.enemy_species.add_units((x, y), n)
        else:  # There is some form of battle
            # If the outcome is certain, return that, otherwise return a loss
            win_probability = utils.win_probability(n, self.board[x, y, 1], self.board[x, y, 0])
            if win_probability in [0, 1]:
                (species, survivors) = utils.battle_simulation(n, species_to_add, self.board[x, y, 1],
                                                               self.board[x, y, 0])
                # Species update depends on who was there originally
                if self._board[x, y, 0] == species:  # If the species that was attacked wins (can’t be human)
                    if species == self.our_species.type:
                        self.our_species.remove_units((x, y), self._board[x, y, 1] - survivors)
                    elif species == self.enemy_species.type:
                        self.enemy_species.remove_units((x, y), self._board[x, y, 1] - survivors)
                else:  # If the attacking species wins (can’t be human)
                    if species == self.our_species.type:
                        self.our_species.add_units((x, y), survivors)
                        if self._board[x, y, 0] == 1:
                            self.human_species.remove_tile((x, y))
                        else:
                            self.enemy_species.remove_tile((x, y))
                    elif species == self.enemy_species.type:
                        self.enemy_species.add_units((x, y), survivors)
                        if self._board[x, y, 0] == 1:
                            self.human_species.remove_tile((x, y))
                        else:
                            self.our_species.remove_tile((x, y))
            else:  # If the outcome is not certain
                survivors = np.random.binomial(self._board[x, y, 1], 1-win_probability)
                if self._board[x, y, 0] == self.our_species.type:  # We are defending
                    self.our_species.remove_tile((x, y))
                    self.enemy_species.add_units((x, y), survivors)
                    species = self.enemy_species.type
                elif self._board[x, y, 0] == self.enemy_species.type:  # We are attacking the enemy
                    self.enemy_species.remove_units((x, y), self.board[x, y, 1] - survivors)
                    species = self.enemy_species.type
                else:  # Humans are being attacked
                    species = 1
            self.board[x, y, 1] = survivors
            self.board[x, y, 0] = species

    def __remove_unit(self, n, x, y):
        # Remove n units in (x,y) position.
        species = self._board[x, y, 0]
        if species == 1:
            self.human_species.remove_units((x, y), n)
        elif species == self.our_species.type:
            self.our_species.remove_units((x, y), n)
        else:
            self.enemy_species.remove_units((x, y), n)

    def next_state(self, moves, species):
        # Given a list of moves, outputs the next board state.
        for move in moves:
            x_init, y_init = move[0], move[1]
            n = move[2]
            x_end, y_end = move[3], move[4]
            self.__remove_unit(n, x_init, y_init)
            self.__add_unit(n, x_end, y_end, species)

    def copy_state(self):
        """
        return a copy of self as a new State object
        
        :return: State object
        """
        copy = State(("set", (self._nb_rows, self._nb_columns)), set_species=False)

        copy._nb_rows = self._nb_rows
        copy._nb_columns = self._nb_columns
        copy._board = np.copy(self._board)
        copy._house_list = np.copy(self._house_list)
        copy._starting_square = np.copy(self._starting_square)
        copy.our_species = Species(self.our_species.type, self.our_species.tile_contents())
        copy.enemy_species = Species(self.enemy_species.type, self.enemy_species.tile_contents())
        copy.human_species = Species(1, self.human_species.tile_contents())
        return copy
