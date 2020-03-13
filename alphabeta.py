from itertools import combinations, product
import numpy as np
from typing import List, Tuple
import math

from state import State
from heuristics.basic import evaluate


def alphabeta(state, depth: int, alpha: int, beta: int, maximizing_player: bool):
    if depth == 0:
        return [evaluate(state, maximizing_player), None]

    if maximizing_player:
        current_value = -math.inf
        possible_moves = all_possible_moves(state, state.our_species)
        if possible_moves is None:
            return [-math.inf, None]  # No more friendly units, we have lost
        best_move = None
        for move in possible_moves:
            child_state = state.copy_state()
            child_state.next_state(move, state.our_species)
            alphabeta_result = alphabeta(
                child_state, depth - 1, alpha, beta, False)[0]
            if current_value < alphabeta_result:
                current_value = alphabeta_result
                best_move = move
            alpha = max(alpha, current_value)
            if alpha >= beta:
                break  # beta cut-off

        return current_value, best_move
    else:
        current_value = math.inf
        possible_moves = all_possible_moves(state, state.enemy_species)
        if possible_moves is None:
            return [math.inf, None]  # No more enemy units, we have won
        best_move = None
        for move in possible_moves:
            child_state = state.copy_state()
            child_state.next_state(move, state.enemy_species)
            alphabeta_result = alphabeta(
                child_state, depth - 1, alpha, beta, True)[0]
            if current_value > alphabeta_result:
                current_value = alphabeta_result
                best_move = move

            beta = min(beta, current_value)
            if alpha >= beta:
                break  # alpha cut-off
        return current_value, best_move


def all_possible_moves(state: State, species: int) -> List[List[Tuple[int, int, int, int, int]]]:
    """Returns all the possible moves, limits number of splits to 2 in total

    :param state:
    :param species:
    :return:
    """

    active_squares = list(zip(*np.where(state.board[:, :, 0] == species)))
    adverse_squares = list(
        zip(*np.where(state.board[:, :, 0] not in [0, species])))

    adverse_squares_content = []
    for coordinates in adverse_squares:
        temp = [coordinates[0], coordinates[1]]
        temp.extend(state.board[coordinates[0], coordinates[1]])
        adverse_squares_content.append(temp)
    adverse_squares_content = np.array(adverse_squares_content)

    square_moves = []
    for square in active_squares:
        this_square_moves = []
        x, y = square
        nb_units = state.board[x, y, 1]

        #  Legal squares
        possible_squares = possible_target_squares(
            state.nb_rows, state.nb_columns, x, y)

        # Combinations of 2 possible squares
        square_combinations = combinations(possible_squares, 2)

        # No split moves
        this_square_moves += [[(x, y, nb_units, target_x, target_y)]
                              for target_x, target_y in possible_squares]

        # Split moves
        a = len(active_squares)
        b = len(adverse_squares)

        if a < b:
            adverse_squares_content = adverse_squares_content[adverse_squares_content[:, -1].argsort(
            )]
            min_size = adverse_squares_content[0, -1]
            second_min_size = adverse_squares_content[1, -1]

            for tile in active_squares:
                half_size = tile[4]//2 + tile[4] % 2
                if second_min_size <= half_size:
                    for i in range(min_size, half_size):
                        size_first_split = i
                        size_second_split = tile[4]-i

                        # size_second_split is always the max
                        adv_tiles = adverse_squares_content[adverse_squares_content[:, -1]
                                                            < size_second_split]

                        for adv_tile in adv_tiles:
                            adv_tile.append(utils.distance(
                                tile[:2], adv_tile[:2]))

                        adv_tiles = adv_tiles[adv_tiles[:, -1].argsort()]

                        if size_first_split >= adv_tiles[0]:
                            target_first_split = adv_tiles[0, :2]
                            target_second_split = adv_tiles[1, :2]
                        else:
                            target_second_split = adv_tiles[0, :2]
                            for i in range(1, len(adv_tiles)):
                                if size_first_split >= adv_tiles[i]:
                                    target_first_split = adv_tiles[0, :2]
                                    break

                        result = []

                        if target_first_split[0] > x:
                            if target_first_split[1] > y:
                                result.append(
                                    (x, y, size_first_split, x+1, y+1))
                            elif target_first_split[1] < y:
                                result.append(
                                    (x, y, size_first_split, x+1, y-1))
                            else:
                                result.append((x, y, size_first_split, x+1, y))

                        elif target_first_split[0] < x:
                            if target_first_split[1] > y:
                                result.append(
                                    (x, y, size_first_split, x-1, y+1))
                            elif target_first_split[1] < y:
                                result.append(
                                    (x, y, size_first_split, x-1, y-1))
                            else:
                                result.append((x, y, size_first_split, x-1, y))

                        else:
                            if target_first_split[1] > y:
                                result.append((x, y, size_first_split, x, y+1))
                            elif target_first_split[1] < y:
                                result.append((x, y, size_first_split, x, y-1))
                            else:
                                result.append((x, y, size_seo_split, x, y))

                        if target_second_split[0] > x:
                            if target_second_split[1] > y:
                                result.append(
                                    (x, y, size_second_split, x+1, y+1))
                            elif target_second_split[1] < y:
                                result.append(
                                    (x, y, size_second_split, x+1, y-1))
                            else:
                                result.append(
                                    (x, y, size_second_split, x+1, y))

                        elif target_second_split[0] < x:
                            if target_second_split[1] > y:
                                result.append(
                                    (x, y, size_second_split, x-1, y+1))
                            elif target_second_split[1] < y:
                                result.append(
                                    (x, y, size_second_split, x-1, y-1))
                            else:
                                result.append(
                                    (x, y, size_second_split, x-1, y))

                        else:
                            if target_second_split[1] > y:
                                result.append(
                                    (x, y, size_second_split, x, y+1))
                            elif target_second_split[1] < y:
                                result.append(
                                    (x, y, size_second_split, x, y-1))
                            else:
                                result.append((x, y, size_second_split, x, y))

                        if result[0, 3] == result[1, 3] and result[0, 4] == result[1, 4]:
                            break

                        this_square_moves += result
                        square_moves.append(this_square_moves)

    possible_moves = list(map(merge, product(*square_moves)))
    return possible_moves


def possible_target_squares(nb_rows: int, nb_columns: int, x: int, y: int) -> List[Tuple[int, int]]:
    """Returns the legal squares to move to from a given square

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
    """ Merge all the lists within a given iterable

    :param lists: iterable containing the lists to merge
    :return: Merged list
    """
    output = []
    for list_ in lists:
        output += list_
    return output
