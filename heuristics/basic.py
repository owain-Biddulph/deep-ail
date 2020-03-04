import math
from typing import List


def evaluate(state):
    all_occupied_tile_us = []
    all_occupied_tile_other = []
    race_pop = 0
    adverse_pop = 0
    ponderation = [1,1]

    for x in range(state.nb_columns):
        for y in range(state.nb_rows):
            if state.board[x][y][0] == state.our_species:
                all_occupied_tile_us += [[x, y, state.board[x][y][1]]]
                race_pop += state.board[x][y][1]
            if state.board[x][y][0] == state.enemy_species:
                all_occupied_tile_other += [[x, y, state.board[x][y][1]]]
                adverse_pop += state.board[x][y][1]

    return simple_score(all_occupied_tile_us, all_occupied_tile_other, race_pop, adverse_pop, ponderation)


def simple_score(all_occupied_tile_us: List[List[int]], all_occupied_tile_other: List[List[int]],
                 race_pop: int, adverse_pop: int, ponderation: List[int] = list((1, 1))):
    # all_occupied_tile assumed to be with format : [x_position, y_position, number]

    if adverse_pop == 0:
        return math.inf

    current_state_score: float = race_pop + 1 / adverse_pop

    potential_score: int = 0
    for tile_1 in all_occupied_tile_us:
        for tile_2 in all_occupied_tile_other:
            distance_factor = 1 / distance(tile_1[0], tile_1[1], tile_2[0], tile_2[1])
            potential_score += distance_factor * get_proba_of_success(tile_1[2], tile_2[2])

    score: float = ponderation[0] * current_state_score + ponderation[1] * potential_score
    return score


def distance(tile1_x, tile1_y, tile2_x, tile2_y):
    return min(abs(tile1_x - tile2_x), abs(tile1_y - tile2_y))


def get_proba_of_success(our_troops, our_type, their_troops, their_type):
    if their_type == 1:
        return compute_proba_of_success(our_troops, their_troops, their_type)
    else:
        if our_troops >= their_troops:
            return compute_proba_of_success(our_troops, their_troops, their_type)
        else:
            # approche prudente (si moins d'une chance sur deux de gagner ça devient négatif)
            return -compute_proba_of_success(their_troops, our_troops, our_type)


def compute_proba_of_success(attack_troops: int, defense_troops: int, defense_type: int):
    if defense_type == 1:
        if attack_troops >= defense_troops:
            return 1
        else:
            return random_battle(attack_troops, defense_troops)
    else:
        if attack_troops >= 1.5 * defense_troops:
            return 1
        elif defense_troops >= 1.5 * defense_troops:
            return 0
        else:
            return random_battle(attack_troops, defense_troops)


def random_battle(attack_troops: int, defense_troops: int):
    if attack_troops >= defense_troops:
        return float(attack_troops) / float(defense_troops) - 0.5
    else:
        return float(attack_troops) / (2 * float(defense_troops))
