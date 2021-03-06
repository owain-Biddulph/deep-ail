from itertools import product
import numpy as np
from typing import List, Tuple
import math
import time

from state import State, Species

import utils


def alphabeta(state, depth: int, alpha: int, beta: int, maximizing_player: bool, heuristic, time_message_received,
              always_split: bool):
    if depth == 0:
        eval = heuristic.evaluate(state, maximizing_player)
        return eval, None, False

    if maximizing_player:
        current_value = -math.inf
        possible_moves = all_possible_moves(state, state.our_species, state.enemy_species, always_split)

        if possible_moves is None:
            return -math.inf, None  # No more friendly units, we have lost
        best_move = None
        for move in possible_moves:
            child_state = state.copy_state()
            child_state.next_state(move, state.our_species.type)
            alphabeta_result, _, _ = alphabeta(
                child_state, depth - 1, alpha, beta, False, heuristic, time_message_received, always_split)
            if current_value < alphabeta_result:
                current_value = alphabeta_result
                best_move = move
            alpha = max(alpha, current_value)
            if alpha >= beta:
                break  # beta cut-off
            try:
                check_time(time_message_received)
            except TimeError:
                if best_move is None:
                    best_move = move
                return current_value, best_move, True
        return current_value, best_move, False
    else:
        current_value = math.inf
        possible_moves = all_possible_moves(state, state.enemy_species, state.our_species, always_split)
        if possible_moves is None:
            return math.inf, None  # No more enemy units, we have won
        best_move = None
        for move in possible_moves:
            child_state = state.copy_state()
            child_state.next_state(move, state.enemy_species.type)
            alphabeta_result, _, _ = alphabeta(
                child_state, depth - 1, alpha, beta, True, heuristic, time_message_received, always_split)

            if current_value > alphabeta_result:
                current_value = alphabeta_result
                best_move = move

            beta = min(beta, current_value)
            if alpha >= beta:
                break  # alpha cut-off
            try:
                check_time(time_message_received)
            except TimeError:
                if best_move is None:
                    best_move = move
                return current_value, best_move, True
        return current_value, best_move, False


def possibly_worth_splitting(friendly_squares: List[Tuple[int, int]],
                             other_squares: List[Tuple[int, int]]) -> bool:
    """ Checks if there is any point splitting at all given the number of friendly tiles and other occupied tiles.

    :param friendly_squares: The squares occupied by the species who’s turn it is
    :param other_squares: The squares occupied by humans or the other species
    :return: bool, True if we have fewer squares, False otherwise
    """
    if len(friendly_squares) >= len(other_squares):
        return False
    return True


def all_possible_moves(state: State, moving_species: Species, other_species: Species, always_split) -> List[
    List[Tuple[int, int, int, int, int]]]:
    """Returns all the possible moves, limits number of splits to 2 in total.

    :param state:
    :param species:
    :return:
    """
    moving_species_squares: List[Tuple[int, int]] = moving_species.tile_coordinates()
    human_squares: List[Tuple[int, int]] = state.human_species.tile_coordinates()
    other_species_squares: List[Tuple[int, int]] = other_species.tile_coordinates()
    adverse_squares: List[Tuple[int, int]] = human_squares + other_species_squares

    other_contents = other_species.tile_contents()
    human_contents = state.human_species.tile_contents()
    adverse_square_contents = sorted(other_contents + human_contents, key=lambda t: t[-1])
    moving_species_squares_content = moving_species.tile_contents()

    worth_splitting: bool = possibly_worth_splitting(moving_species_squares, adverse_squares)
    square_moves = []
    possible_moves = []
    for square_content in moving_species_squares_content:
        this_square_moves = []
        x, y = square_content[:2]
        nb_units = square_content[2]

        #  Legal squares
        possible_squares = order_target_squares(state, possible_target_squares(
            state.nb_rows, state.nb_columns, x, y), moving_species)

        # No split moves
        this_square_moves += [[(x, y, nb_units, target_x, target_y)]
                              for target_x, target_y in possible_squares]
        if len(human_squares) == 0:
            possible_moves.extend(this_square_moves)

        # Split moves
        if worth_splitting or always_split:
            min_size = adverse_square_contents[0][-1]
            second_min_size = adverse_square_contents[1][-1]

            half_size = int(np.ceil(square_content[2] / 2))
            # No point splitting if there are no enemy squares with fewer units than the 2 split sizes
            if min_size + second_min_size <= square_content[2]:
                for i in range(min_size, half_size + (square_content[2] % 2 == 0) * 1):
                    size_first_split = i
                    size_second_split = square_content[2] - i
                    # size_second_split is always the max
                    adv_tiles = [tile for tile in adverse_square_contents if tile[-1] <= size_second_split]
                    if len(adv_tiles) < 2:
                        break
                    for adv_tile in adv_tiles:
                        np.append(adv_tile, utils.distance(square_content[:2], adv_tile[:2]))

                    if size_first_split >= adv_tiles[0][2]:
                        target_first_split = adv_tiles[0][:2]
                        target_second_split = adv_tiles[1][:2]
                    else:
                        target_second_split = adv_tiles[0][:2]
                        for j in range(1, len(adv_tiles)):
                            if size_first_split >= adv_tiles[j][2]:
                                target_first_split = adv_tiles[0][2]
                                break

                    result = []

                    if target_first_split[0] > x:
                        if target_first_split[1] > y:
                            result.append(
                                (x, y, size_first_split, x + 1, y + 1))
                        elif target_first_split[1] < y:
                            result.append(
                                (x, y, size_first_split, x + 1, y - 1))
                        else:
                            result.append((x, y, size_first_split, x + 1, y))

                    elif target_first_split[0] < x:
                        if target_first_split[1] > y:
                            result.append(
                                (x, y, size_first_split, x - 1, y + 1))
                        elif target_first_split[1] < y:
                            result.append(
                                (x, y, size_first_split, x - 1, y - 1))
                        else:
                            result.append((x, y, size_first_split, x - 1, y))

                    else:
                        if target_first_split[1] > y:
                            result.append((x, y, size_first_split, x, y + 1))
                        elif target_first_split[1] < y:
                            result.append((x, y, size_first_split, x, y - 1))
                        else:
                            result.append((x, y, size_first_split, x, y))

                    if target_second_split[0] > x:
                        if target_second_split[1] > y:
                            result.append(
                                (x, y, size_second_split, x + 1, y + 1))
                        elif target_second_split[1] < y:
                            result.append(
                                (x, y, size_second_split, x + 1, y - 1))
                        else:
                            result.append(
                                (x, y, size_second_split, x + 1, y))

                    elif target_second_split[0] < x:
                        if target_second_split[1] > y:
                            result.append(
                                (x, y, size_second_split, x - 1, y + 1))
                        elif target_second_split[1] < y:
                            result.append(
                                (x, y, size_second_split, x - 1, y - 1))
                        else:
                            result.append(
                                (x, y, size_second_split, x - 1, y))

                    else:
                        if target_second_split[1] > y:
                            result.append(
                                (x, y, size_second_split, x, y + 1))
                        elif target_second_split[1] < y:
                            result.append(
                                (x, y, size_second_split, x, y - 1))
                        else:
                            result.append((x, y, size_second_split, x, y))

                    if result[0][3] == result[1][3] and result[0][4] == result[1][4]:
                        break

                    this_square_moves.append(result)
        square_moves.append(this_square_moves)
        if len(human_squares) == 0:
            possible_moves.extend(this_square_moves)
    possible_moves += list(map(merge, product(*square_moves)))
    possible_moves = remove_illegal_moves(possible_moves)
    return possible_moves


def order_target_squares(state: State, target_squares: List[Tuple[int, int]], moving_species: int):
    """Returns an ordered list of target squares to optimise the alpha-beta

    :param state: Current state
    :param target_squares: list of target squares as returned by the possible_target_squares function
    :return: ordered target squares, human squares first, then our squares, then enemy squares, then empty squares
    """
    order = []
    for square in target_squares:
        if state.board[square[0], square[1], 0] == 1:
            order.append((square, 1))
        elif state.board[square[0], square[1], 0] == moving_species:
            order.append((square, 2) )
        elif state.board[square[0], square[1], 0] > 0:
            order.append((square, 3))
        else:
            order.append((square, 4))
    return list(map(lambda x: x[0], sorted(order, key=lambda x: x[-1])))


def possible_target_squares(nb_rows: int, nb_columns: int, x: int, y: int) -> List[Tuple[int, int]]:
    """Returns the legal squares to move to from a given square.

    :param nb_rows: int, number of rows on the board
    :param nb_columns: int, number of columns on the board
    :param x: int, column coordinate of original square
    :param y: int, row coordinate of original square
    :return: list of squares
    """
    if x == 0:
        if y == 0:
            possible_squares = [(x + 1, y + 1), (x + 1, y), (x, y + 1)]
        elif y == nb_rows - 1:
            possible_squares = [(x + 1, y - 1), (x + 1, y), (x, y - 1)]
        else:
            possible_squares = [(x + 1, y), (x + 1, y + 1),
                                (x + 1, y - 1), (x, y + 1), (x, y - 1)]
    elif x == nb_columns - 1:
        if y == 0:
            possible_squares = [(x - 1, y + 1), (x - 1, y), (x, y + 1)]
        elif y == nb_rows - 1:
            possible_squares = [(x - 1, y - 1), (x - 1, y), (x, y - 1)]
        else:
            possible_squares = [(x - 1, y), (x - 1, y + 1),
                                (x - 1, y - 1), (x, y + 1), (x, y - 1)]
    elif y == 0:
        possible_squares = [(x, y + 1), (x + 1, y + 1),
                            (x - 1, y + 1), (x + 1, y), (x - 1, y)]
    elif y == nb_rows - 1:
        possible_squares = [(x, y - 1), (x + 1, y - 1),
                            (x - 1, y - 1), (x + 1, y), (x - 1, y)]
    else:
        possible_squares = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y), (x + 1, y + 1), (x - 1, y - 1),
                            (x + 1, y - 1), (x - 1, y + 1)]
    return possible_squares


def merge(lists: Tuple) -> List:
    """ Merge all the lists within a given iterable.

    :param lists: iterable containing the lists to merge
    :return: Merged list
    """
    output = []
    for list_ in lists:
        output += list_
    return output


def remove_illegal_moves(moves: List[List[Tuple]]) -> List[List[Tuple[int, int, int, int, int]]]:
    """ This function removes the illegal moves from the list of possible moves.

    Illegal moves are defined by the game rules.
    :param moves: List of possible moves
    :return: List of legal moves
    """
    legal_moves = []
    for move in moves:
        if len(move) == 1:
            legal_moves.append(move)
        else:
            c = 0
            for m1 in move:
                for m2 in move:
                    if m1[:2] == m2[3:]:
                        c += 1
                        break
            if c == 0:
                legal_moves.append(move)
    return legal_moves


def check_time(time_message_received):
    """Checks how much time has elapsed since the update message"""
    elapsed_time = time.time() - time_message_received
    if elapsed_time >= 1.90:
        raise TimeError


class TimeError(Exception):
    pass
