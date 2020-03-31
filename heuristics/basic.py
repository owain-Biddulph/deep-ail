import math
from typing import List, Tuple

from state import State
import utils


class Heuristic:
    """A global heuristic that chooses the appropriate heuristic to use depending on the context"""

    def __init__(self):
        self.cached_scores = {}

    def evaluate(self, state: State, maximizing_player: bool) -> float:
        """Evaluates the score of a given state

        :param state: State, state to evaluate
        :param maximizing_player: bool, tracks who turn it is
        :return: float, score
        """
        board_hash = utils.hash_array(state.board)
        score = self.cached_scores.get(board_hash, None)
        if score is None:
            if len(state.human_species.tile_coordinates()) != 0:
                score = in_game_score(state, state.our_species.tile_contents(), state.enemy_species.tile_contents(),
                                      state.human_species.tile_contents(), state.our_species.units,
                                      state.enemy_species.units, maximizing_player, [10, 1, 1])
            else:
                score = end_game_score(state.our_species.tile_contents(), state.our_species.units,
                                       state.enemy_species.units)
            self.cached_scores[board_hash] = score
        return score * state.probability


def in_game_score(state: State, all_occupied_tile_us: List[List[int]], all_occupied_tile_opponent: List[List[int]],
                  all_occupied_tile_human: List[List[int]], our_population: int,
                  enemy_population: int, maximizing_player: bool, ponderation=None) -> float:
    """Returns a score for a given state

    :param state: State, state to evaluate
    :param all_occupied_tile_us: list, list of squares that are occupied by our units
    :param all_occupied_tile_opponent: list, list of squares that are occupied by opponent units
    :param all_occupied_tile_human: list, list of squares that are occupied by human
    :param our_population: int, our total population
    :param enemy_population: int, enemy total population
    :param maximizing_player: bool, tracks who turn it is
    :param ponderation: weight given to population values and unit disposition
    :return: 
    """
    # all_occupied_tile assumed to be with format : [x_position, y_position, number]
    if ponderation is None:
        ponderation = [100, 1, 1]
    if enemy_population == 0:
        return math.inf
    if our_population == 0:
        return -math.inf
    current_state_score: int = our_population - enemy_population

    potential_score: float = 0
    for tile_1 in all_occupied_tile_us:
        for tile_2 in all_occupied_tile_opponent:
            distance_factor = 1 / utils.distance(tile_1, tile_2)
            potential_score += distance_factor * (tile_score(
                tile_1[2], tile_2[2], state.board[tile_2[0]][tile_2[1]][0]) - 0.5)

    another_score: float = 0
    for human in all_occupied_tile_human:
        min_us: float = math.inf
        min_opponent: float = math.inf
        first_to_reach_us = []
        first_to_reach_opponent = []
        first_to_reach = []
        got_there_first = False
        for our_troop in all_occupied_tile_us:
            if min_us > utils.distance(human, our_troop):
                min_us = utils.distance(human, our_troop)
                first_to_reach_us = our_troop
        for opponent_troop in all_occupied_tile_opponent:
            if min_opponent > utils.distance(human, opponent_troop):
                min_opponent = utils.distance(human, opponent_troop)
                first_to_reach_opponent = opponent_troop
        if min_us > min_opponent:
            first_to_reach = first_to_reach_opponent
            got_there_first = False
        elif min_opponent > min_us:
            first_to_reach = first_to_reach_us
            got_there_first = True
        elif min_us == min_opponent:
            if maximizing_player:
                first_to_reach = first_to_reach_us
                got_there_first = True
            else:
                first_to_reach = first_to_reach_opponent
                got_there_first = False

        if got_there_first:
            another_score += 1 / min_us * \
                             tile_score(first_to_reach[2], human[2], 1) * human[2]
        else:
            another_score += 0
    score: float = ponderation[0] * current_state_score + ponderation[1] * potential_score + ponderation[
        2] * another_score
    return score


def end_game_score(all_occupied_tile_us: List[List[int]], our_population: int, enemy_population: int) -> float:
    """
    Returns a score for a given state
    :param all_occupied_tile_us: list, list of squares that are occupied by our units
    :param our_population: int, our total population
    :param enemy_population: int, enemy total population
    :return:
    """
    # all_occupied_tile assumed to be with format : [x_position, y_position, number]
    ponderation = [100, 1, 1]
    if enemy_population == 0:
        return math.inf
    if our_population == 0:
        return -math.inf
    current_state_score: int = our_population - enemy_population

    proximity_score: int = 0
    number_of_tile_combinations = 1
    for i in range(len(all_occupied_tile_us)):
        for j in range(i):
            proximity_score += - utils.distance((all_occupied_tile_us[i][0], all_occupied_tile_us[i][1]),
                                                (all_occupied_tile_us[j][0], all_occupied_tile_us[j][1]))
            number_of_tile_combinations += 1
    proximity_score += proximity_score / number_of_tile_combinations

    groups_score: int = -len(all_occupied_tile_us)
    score: int = ponderation[0] * current_state_score + ponderation[1] * groups_score + ponderation[2] * proximity_score

    return score


def tile_score(our_troops: int, their_troops: int, their_species: int) -> float:
    """Returns a score for a given enemy tile when comparing to a friendly tile

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


def split_score(all_occupied_tile_us: List[List[int]], all_occupied_tile_opponent: List[List[int]], our_population: int,
                enemy_population: int) -> float:
    """Returns a score for a given state

    :param all_occupied_tile_us: list, list of squares that are occupied by our units
    :param all_occupied_tile_opponent: list, list of squares that are occupied by enemy units
    :param our_population: int, our total population
    :param enemy_population: int, enemy total population
    :return:
    """
    # all_occupied_tile assumed to be with format : [x_position, y_position, number]
    ponderation = [100, 1, 1]
    if enemy_population == 0:
        return math.inf
    if our_population == 0:
        return -math.inf
    current_state_score: int = our_population - enemy_population

    split_score_: int = 0
    number_of_tile_combinations = 1
    for tile_us in all_occupied_tile_us:
        for tile_opponent in all_occupied_tile_opponent:
            split_score_ += -abs(4 - utils.distance((tile_us[0], tile_us[1]), (tile_opponent[0], tile_opponent[1])))
            number_of_tile_combinations += 1
    split_score_ += split_score_ / number_of_tile_combinations

    groups_score: int = len(all_occupied_tile_us)
    score: int = ponderation[0] * current_state_score + ponderation[1] * groups_score + ponderation[2] * split_score_
    return score


class HeuristicAgglo(Heuristic):
    """Heuristic to get our units to merge back together."""

    def evaluate(self, state: State, maximizing_player: bool) -> float:
        """Evaluates the score of a given state

        :param state: State, state to evaluate
        :param maximizing_player: bool, tracks who turn it is
        :return: float, score
        """
        board_hash = utils.hash_array(state.board)
        score = self.cached_scores.get(board_hash, None)
        if score is None:
            score = end_game_score(state.our_species.tile_contents(), state.our_species.units,
                                   state.enemy_species.units)
            self.cached_scores[board_hash] = score
        return score


class HeuristicSplit(Heuristic):
    """Heuristic to spit as effectively as possible to slow opponent move calculation .

    The aim of this it to try and make the opponents miss their turn. It is used as a last resort.
    """

    def evaluate(self, state: State, maximizing_player: bool) -> float:
        """Evaluates the score of a given state

        :param state: State, state to evaluate
        :param maximizing_player: bool, tracks who turn it is
        :return: float, score
        """
        board_hash = utils.hash_array(state.board)
        score = self.cached_scores.get(board_hash, None)
        if score is None:
            score = split_score(state.our_species.tile_contents(), state.enemy_species.tile_contents(),
                                state.our_species.units, state.enemy_species.units)
            self.cached_scores[board_hash] = score
        return score
