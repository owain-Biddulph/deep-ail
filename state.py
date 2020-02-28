from typing import List, Tuple
import numpy as np


class State:
    """Class to represent the board state
    The board is a nb_rows x nb_columns x 2 numpy array, the first 2D layer represents the species, the 2nd the number
    """

    def __init__(self, set_message: Tuple[str, Tuple[int, int]]) -> None:
        self._nb_rows: int = set_message[1][0]
        self._nb_columns: int = set_message[1][1]
<<<<<<< HEAD
        self._board: np.ndarray = np.zeros((self.nb_columns, self.nb_rows, 2), dtype=int)
        self._house_list: List[Tuple[int, int]] = []
        self._starting_square = None
        self.our_species = None
        self.our_troops: int = 0
        self.ennemy_troops: int = 0

        self.our_tiles: List[List[int]] = list()
        self.ennemy_tiles: List[List[int]] = list()
        self.human_tiles: List[List[int]] = list()
=======
        self._board: np.ndarray = np.zeros((2, self.nb_columns, self.nb_rows), dtype=int)
        self._house_list: List[Tuple[int, int]] = []
        self._starting_square = None
        self.our_species = None
        self.our_troops : int = 0
        self.ennemy_troops : int = 0

        self.our_tiles : List[List[int]] = list()
        self.ennemy_tiles : List[List[int]] = list()
        self.human_tiles : List[List[int]] = list()


>>>>>>> b79637a2849f9dfb723572b2015ce052da079d48

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
        print(f"in function update with message : {message}")
        if message[0] == "hum":
            self._house_list = message[1]
<<<<<<< HEAD

        elif message[0] == "hme":
            self._starting_square = message[1]

=======
            print(f"set house list to: {self._house_list}")
        elif message[0] == "hme":
            self._starting_square = message[1]

            print(f"set starting square to: {self._starting_square}")

>>>>>>> b79637a2849f9dfb723572b2015ce052da079d48
        elif message[0] == "map":
            x_home, y_home = self._starting_square
            werewolf_tiles = list()
            vampire_tiles = list()
            werewolf_troops = 0
            vampire_troops = 0
<<<<<<< HEAD

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
                    vampire_tiles.append([change[0], change[1], change[3]])
                    vampire_troops += change[3]
                    if (change[0], change[1]) == (x_home, y_home):
                        self.our_species = 2

                # il y a des loups garous
                if change[4] != 0:
                    self._board[change[0], change[1], 0] = 3
                    self._board[change[0], change[1], 1] = change[4]
                    werewolf_tiles.append([change[0], change[1], change[4]])
                    werewolf_troops += change[4]
                    if (change[0], change[1]) == (x_home, y_home):
                        self.our_species = 3

        elif message[0] == "upd":
            for change in message[1]:
                # il y a des humains
                if change[2] != 0:
                    self._board[change[0], change[1], 0] = 1
                    self._board[change[0], change[1], 1] = change[2]
=======
            for change in message[1]:
                print(f"change {change}")

                #il y a des humains
                if change[2]!=0:
                    self._board[0, change[0], change[1]] = 1
                    self._board[1, change[0], change[1]] = change[2]
                    self.human_tiles.append([change[0], change[1], change[2]])

                #il y a des vampires
                if change[3]!=0:
                    self._board[0, change[0], change[1]] = 2
                    self._board[1, change[0], change[1]] = change[3]
                    vampire_tiles.append([change[0], change[1], change[3]])
                    vampire_troops+=change[3]
                    if (change[0], change[1]) == (x_home, y_home):
                        self.our_species = 2

                #il y a des loups garous
                if change[4]!=0:
                    self._board[0, change[0], change[1]] = 3
                    self._board[1, change[0], change[1]] = change[4]
                    werewolf_tiles.append([change[0], change[1], change[4]])
                    werewolf_troops+=change[4]
                    if (change[0], change[1]) == (x_home, y_home):
                        self.our_species = 3

            if self.our_species == 2:
                self.our_troops = vampire_troops
                self.our_tiles = vampire_tiles

                self.ennemy_troops = werewolf_troops
                self.ennemy_tiles = werewolf_tiles
            else : 
                self.our_troops = werewolf_troops
                self.our_tiles = werewolf_tiles

                self.ennemy_troops = vampire_troops
                self.ennemy_tiles = vampire_tiles

            print(f"our species is {self.our_species}")

        elif message[0] == "upd":
            for change in message[1]:
                #il y a des humains
                if change[2]!=0:
                    self._board[0, change[0], change[1]] = 1
                    self._board[1, change[0], change[1]] = change[2]
>>>>>>> b79637a2849f9dfb723572b2015ce052da079d48

                # il y a des vampires
                elif change[3] != 0:
                    self._board[change[0], change[1], 0] = 2
                    self._board[change[0], change[1], 1] = change[3]

                # il y a des loups garous
                elif change[4] != 0:
                    self._board[change[0], change[1], 0] = 3
                    self._board[change[0], change[1], 1] = change[4]

                # il n'y a rien
                else:
                    self._board[change[0], change[1], 0] = 0
                    self._board[change[0], change[1], 1] = 0

    def get_probability(self, E1, E2):
        # Given the number of units, measures the probability of winning.
        if E1 == E2:
            p = .5
        elif E1 < E2:
            p = E1 / (2 * E2)
        else:
            p = E1 / E2 - .5
        return p

    def battle(self, E1, E1_species, E2, E2_species):
        # Simulates a battle between E1 and E2.
        if ((E2_species == 1) & (E1 < E2)) | ((E2_species != 1) & (E1 < 1.5 * E2)):

            p = self.get_probability(E1, E2)
            rd = np.random.random()
            victory = p > rd

            if victory:
                # Every winner's unit has a probability p of surviving.
                winner = 'E1'
                survivors_E1 = [p > np.random.random() for k in range(E1)]
                if E2_species == 1:
                    # If losers are humans, every one of them has a probability p of being transformed.
                    transformed = [p > np.random.random() for k in range(E2)]
                    return winner, [sum(survivors_E1) + sum(transformed), E1_species]
                else:
                    return winner, [sum(survivors_E1), E1_species]
            else:
                # Every winner's unit has a probability 1-p of surviving
                winner = 'E2'
                survivors_E2 = [p > np.random.random() for k in range(E2)]
                return winner, [sum(survivors_E2), E2_species]
        else:
            winner = 'E1'
            return winner, [E1, E1_species]

    def add_unit(self, move_board, n, x, y):
        # Add n units in (x,y) position.
        if move_board[0, x, y] == 0:
            # No unit in (x,y). Settlement of n units.
            move_board[1, x, y] = n
            move_board[0, x, y] = self.our_species
        else:
            # One or several units in (x,y). There will be blood.
            winner, (survivors, species) = self.battle(
                E1=n, E1_species=self.our_species,
                E2=move_board[1, x, y], E2_species=move_board[0, x, y])
            move_board[1, x, y] = survivors
            move_board[0, x, y] = species

        return move_board

    def remove_unit(self, move_board, n, x, y):
        # Remove n units in (x,y) position.
        if n < move_board[1, x, y]:
            # Removing n units.
            move_board[1, x, y] -= n
        elif n == move_board[1, x, y]:
            # Removing all the units and cleaning the board.
            move_board[:, x, y] = 0
        else:
            raise Exception('nope')
        return move_board

    def next_state(self, moves):
        # Given a list of moves, outputs the next board state.
        # self.display_board()
        move_board = np.array(self._board, copy=True)
        for move in moves:
            x_init, y_init = move[0], move[1]
            n = move[2]
            x_end, y_end = move[3], move[4]
            self.remove_unit(move_board, n, x_init, y_init)
            self.add_unit(move_board, n, x_end, y_end)
        # self.display_board()

<<<<<<< HEAD
=======
        self.display_board()


    def get_probability(self, E1, E2):
        # Given the number of units, measures the probability of winning.
        if E1 == E2:
            p = .5
        elif E1 < E2:
            p = E1 / (2 * E2)
        else:
            p = E1 / E2 - .5
        return p


    def battle(self, E1, E1_species, E2, E2_species):
        # Simulates a battle between E1 and E2.
        if ((E2_species == 1) & (E1 < E2)) | ((E2_species != 1) & (E1 < 1.5 * E2)):

            p = self.get_probability(E1, E2)
            rd = np.random.random()
            victory = p > rd

            if victory:
                # Every winner's unit has a probability p of surviving.
                winner = 'E1'
                survivors_E1 = [p > np.random.random() for k in range(E1)]
                if E2_species == 1:
                    # If losers are humans, every one of them has a probability p of being transformed.
                    transformed = [p > np.random.random() for k in range(E2)]
                    return winner, [sum(survivors_E1) + sum(transformed), E1_species]
                else:
                    return winner, [sum(survivors_E1), E1_species]
            else:
                # Every winner's unit has a probability 1-p of surviving
                winner = 'E2'
                survivors_E2 = [p > np.random.random() for k in range(E2)]
                return winner, [sum(survivors_E2), E2_species]
        else:
            winner = 'E1'
            return winner, [E1, E1_species]


    def add_unit(self, move_board, n, x, y):
        # Add n units in (x,y) position.
        if move_board[0, x, y] == 0:
            # No unit in (x,y). Settlement of n units.
            move_board[1, x, y] = n
            move_board[0, x, y] = self.our_species
        else:
            # One or several units in (x,y). There will be blood.
            winner, (survivors, species) = self.battle(
                E1=n, E1_species=self.our_species,
                E2=move_board[1, x, y], E2_species=move_board[0, x, y])
            move_board[1, x, y] = survivors
            move_board[0, x, y] = species

        return move_board


    def remove_unit(self, move_board, n, x, y):
        # Remove n units in (x,y) position.
        if n < move_board[1, x, y]:
            # Removing n units.
            move_board[1, x, y] -= n
        elif n == move_board[1, x, y] :
            # Removing all the units and cleaning the board.
            move_board[:, x, y] = 0
        else:
            raise Exception('nope')
        return move_board


    def next_state(self, moves):
        # Given a list of moves, outputs the next board state.
        # self.display_board()
        move_board = np.array(self._board, copy=True)
        for move in moves:
            x_init, y_init = move[0], move[1]
            n = move[2]
            x_end, y_end = move[3], move[4]
            self.remove_unit(move_board, n, x_init, y_init)
            self.add_unit(move_board, n, x_end, y_end)
        # self.display_board()

>>>>>>> b79637a2849f9dfb723572b2015ce052da079d48
        return move_board
