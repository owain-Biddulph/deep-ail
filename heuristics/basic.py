import math


def simple_score(all_occupied_tile_us, all_occupied_tile_other, race_pop: int, adverse_pop: int,  ponderation=[1, 1]):

    # all_occupied_tile assumed to be with format : [x_position, y_position, number, type]

    if adverse_pop == 0:
        return math.inf

    current_state_score: int = race_pop + 1/adverse_pop

    potential_score: int = 0
    for tile_1 in all_occupied_tile_us:
        for tile_2 in all_occupied_tile_other:
            distance_factor = 1/distance(tile_1[0]tile_1[1], tile_2[0]tile_2[1])
            potential_score += distance_factor * \
                getProbaOfSuccess(tile_1[2], tile_2[2])

    score: int = ponderation[0]*current_state_score+ponderation[1]*potential_score
    return score


def distance(tile1_x, tile1_y, tile2_x, tile2_y):
    return min(abs(tile1_x-tile2_x), abs(tile1_y-tile2_y))


def getProbaOfSuccess(our_troops, their_troops):
    if our_troops > 1.5*their_troops:
        return 1
    else if 1.5*our_troops < their_troops:
        return -1
    else:
        return 0
