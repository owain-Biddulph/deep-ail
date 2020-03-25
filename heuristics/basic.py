import math
from typing import List


from state import State
import utils


class Heuristic:
    def __init__(self):
        self.cached_scores = {}

    def evaluate(self, state: State, maximizing_player: bool, times) -> float:
        """
        Evaluates the score of a given state

        :param state: State, state to evaluate
        :return: float, score
        """
        board_hash = utils.hash_array(state._board)
        score = self.cached_scores.get(board_hash, None)
        if score is None:
            if len(state.human_species.tile_coordinates()) != 0:
                score = in_game_score(state, state.our_species.tile_contents(), state.enemy_species.tile_contents(),
                                      state.human_species.tile_contents(), state.our_species.units,
                                      state.enemy_species.units, maximizing_player, [10, 1, 1]), times
            else:
                score = end_game_score(state.our_species.tile_contents(), state.our_species.units,
                                       state.enemy_species.units), times
            self.cached_scores[board_hash] = score
        return score


def in_game_score(state: State, all_occupied_tile_us: List[List[int]], all_occupied_tile_opponent: List[List[int]],
                  all_occupied_tile_human: List[List[int]], our_population: int,
                  enemy_population: int, maximizing_player: bool, ponderation=None) -> float:
    """
    Returns a score for a given state
    
    :param state: State, state to evaluate
    :param all_occupied_tile_us: list, list of squares that are occupied by our units
    :param all_occupied_tile_opponent: list, list of squares that are occupied by opponent units
    :param all_occupied_tile_human: list, list of squares that are occupied by human
    :param our_population: int, our total population
    :param enemy_population: int, enemy total population
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
        min_us: int = math.inf
        min_opponent: int = math.inf
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
            another_score += 1/min_us * tile_score(first_to_reach[2], human[2], 1) * human[2]
        else:
            another_score += 0
    score: float = ponderation[0] * current_state_score + ponderation[1] * potential_score + ponderation[2]*another_score
    return score


def end_game_score(all_occupied_tile_us: List[List[int]],  our_population: int, enemy_population: int) -> float:
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
    l = 1
    for i in range(len(all_occupied_tile_us)):
        for j in range(i):
            proximity_score += utils.distance((all_occupied_tile_us[i][0], all_occupied_tile_us[i][1]),
                                              (all_occupied_tile_us[j][0], all_occupied_tile_us[j][1]))
            l += 1
    proximity_score += proximity_score/l

    groups_score: int = -len(all_occupied_tile_us)
    score: int = ponderation[0] * current_state_score + ponderation[1] * groups_score + ponderation[2] * proximity_score
    return score


def split_score(all_occupied_tile_us: List[List[int]], all_occupied_tile_opponent: List[List[int]], our_population: int, enemy_population: int) -> float:
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

    split_score: int = 0
    l = 1
    for tile_us in range(len(all_occupied_tile_us)):
        for tile_opponent in range(len(all_occupied_tile_opponent)):
            split_score += -abs(4- utils.distance((tile_us[0], tile_us[1]),
                                          (tile_opponent[0], tile_opponent[1])))
            l += 1
    split_score += split_score/l

    groups_score: int = len(all_occupied_tile_us)
    score: int = ponderation[0] * current_state_score + ponderation[1] * groups_score + ponderation[2] * split_score
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


class HeuristicAgglo:

    def __init__(self):
        self.cached_scores = {}

    def evaluate(self, state: State, maximizing_player: bool, times) -> float:
        """
        Evaluates the score of a given state

        :param state: State, state to evaluate
        :return: float, score
        """
        board_hash = utils.hash_array(state._board)
        score = self.cached_scores.get(board_hash, None)

        score = end_game_score(state.our_species.tile_contents(), state.our_species.units,
                                       state.enemy_species.units)
        self.cached_scores[board_hash] = score
        return score, times


class HeuristicSplit:

    def __init__(self):
        self.cached_scores = {}

    def evaluate(self, state: State, maximizing_player: bool, times) -> float:
        """
        Evaluates the score of a given state

        :param state: State, state to evaluate
        :return: float, score
        """
        board_hash = utils.hash_array(state._board)
        score = self.cached_scores.get(board_hash, None)
        print("score", score)
        score = split_score(state.our_species.tile_contents(), state.enemy_species.tile_contents(),
                            state.our_species.units, state.enemy_species.units)
        self.cached_scores[board_hash] = score
        return score, times

