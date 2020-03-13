import math
from typing import List

from state import State
import utils


def evaluate(state: State) -> float:
    """
    Evaluates the score of a given state

    :param state: State, state to evaluate
    :return: float, score
    """
    all_occupied_tile_us = []
    all_occupied_tile_other = []
    race_pop = 0
    adverse_pop = 0
    ponderation = [4, 1]

    for x in range(state.nb_columns):
        for y in range(state.nb_rows):
            if state.board[x][y][0] == state.our_species:
                all_occupied_tile_us += [[x, y, state.board[x][y][1]]]
                race_pop += state.board[x][y][1]
            elif state.board[x][y][0] == state.enemy_species:
                all_occupied_tile_other += [[x, y, state.board[x][y][1]]]
                adverse_pop += state.board[x][y][1]
            elif state.board[x][y][0] == 1:
                all_occupied_tile_other += [[x, y, state.board[x][y][1]]]

    return simple_score(state, all_occupied_tile_us, all_occupied_tile_other, race_pop, adverse_pop, ponderation)


def simple_score(state: State, all_occupied_tile_us: List[List[int]], all_occupied_tile_other: List[List[int]],
                 our_population: int, enemy_population: int, ponderation=None) -> float:
    """
    Returns a score for a given state
    
    :param state: State, state to evaluate
    :param all_occupied_tile_us: list, list of squares that are occupied by our units
    :param all_occupied_tile_other: list, list of squares that are occupied by other units
    :param our_population: int, our total population
    :param enemy_population: int, enemy total population
    :param ponderation: weight given to population values and unit disposition
    :return: 
    """
    # all_occupied_tile assumed to be with format : [x_position, y_position, number]
    if ponderation is None:
        ponderation = [4, 1]
    if enemy_population == 0:
        return math.inf
    current_state_score: float = our_population - enemy_population

    potential_score: int = 0
    for tile_1 in all_occupied_tile_us:
        for tile_2 in all_occupied_tile_other:
            distance_factor = 1 / utils.distance(tile_1[0:2], tile_2[0:2])
            potential_score += distance_factor * tile_score(
                tile_1[2], tile_2[2], state.board[tile_2[0]][tile_2[1]][0])
    score: float = ponderation[0] * current_state_score + ponderation[1] * potential_score
    return score


def tile_score(our_troops: int, their_troops: int, their_species: int) -> float:
    """
    Returns a score for a given enemy tile when comparing to a friendly tile

    :param our_troops: int, number of friendly units
    :param their_troops: int, number of enemy units
    :param their_species: int, enemy species
    :return: float, score between -1 and 1
    """
    if their_species == 1:
        return utils.win_probability(our_troops, their_troops, their_species)
    else:
        if our_troops > their_troops:
            return utils.win_probability(our_troops, their_troops, their_species)
        else:
            # approche prudente (si moins d'une chance sur deux de gagner ça devient négatif)
            return utils.win_probability(our_troops, their_troops, their_species) - 1
