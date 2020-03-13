from typing import Tuple

import numpy as np


def win_probability(attack_troops: int, defense_troops: int, defense_type: int) -> float:
    """
    Return the probability of attacking troops winning a battle

    :param attack_troops:
    :param defense_troops:
    :param defense_type:
    :return:
    """
    if defense_type == 1:
        if attack_troops >= defense_troops:
            return 1
        else:
            return random_battle_win_probability(attack_troops, defense_troops)
    else:
        if attack_troops >= 1.5 * defense_troops:
            return 1
        elif defense_troops >= 1.5 * defense_troops:
            return 0
        else:
            return random_battle_win_probability(attack_troops, defense_troops)


def random_battle_win_probability(species_1_units: int, species_2_units: int) -> float:
    """
    Given the number of units, measures the probability that species 1 wins.

    :param species_1_units: int, number of units of species 1
    :param species_2_units: int, number of units of species 2
    :return: float, probability that species 1 wins
    """
    if species_1_units <= species_2_units:
        p = species_1_units / (2 * species_2_units)
    else:
        p = species_1_units / species_2_units - .5
    return p


def expected_battle_outcome(attacking_species_units: int, defending_species_type: int,
                            defending_species_units: int) -> int:
    """
    Returns the expected number of attacking species units to result from battle, note that this is not a simulation.

    :param attacking_species_units: int, number of units of attacking species
    :param defending_species_units: int, number of units of defending species
    :param defending_species_type: int, can be any species (1, 2, 3)
    :return: int
    """
    expected_outcome = 0
    # True if the battle is not an outright win
    if ((defending_species_units == 1) & (attacking_species_units < defending_species_units)) | (
            (defending_species_units != 1) & (attacking_species_units < 1.5 * defending_species_units)):

        probability_of_winning = random_battle_win_probability(attacking_species_units, defending_species_units)

        expected_outcome += int(probability_of_winning * attacking_species_units)  # Under estimate
        # If losers are humans, every one of them has a probability of being transformed.
        if defending_species_type == 1:
            expected_outcome += int(probability_of_winning * defending_species_units)  # Under estimate
    # If it is an outright win
    else:
        expected_outcome += (attacking_species_units >= defending_species_units) * attacking_species_units
        if defending_species_type == 1:
            expected_outcome += defending_species_units
    return expected_outcome


def distance(square_1: Tuple[int, int], square_2: Tuple[int, int]) -> int:
    """
    Returns the distance in number of moves between 2 squares

    :param square_1: tuple, square 1 coordinates
    :param square_2: tuple, square 2 coordinates
    :return: int, distance between squares
    """
    return max(abs(square_1[0] - square_2[0]), abs(square_1[1] - square_2[1]))


def battle_simulation(species_1_units: int, species_1_type: int, species_2_units: int,
                      species_2_type: int) -> Tuple[int, int]:
    """
    Simulates a battle between two species

    :param species_1_units: int, number of units of species 1
    :param species_1_type: int, species 1 type
    :param species_2_units: int, number of units of species 2
    :param species_2_type: int, species 2 type
    :return: tuple, battle outcome, winning species type and number of remaining units
    """
    if ((species_2_type == 1) & (species_1_units < species_2_units)) | (
            (species_2_type != 1) & (species_1_units < 1.5 * species_2_units)):

        p = random_battle_win_probability(species_1_units, species_2_units)
        # If species 1 wins
        if p >= np.random.random():
            # Every winner's unit has a probability p of surviving.
            winner = species_1_type
            remaining_units = np.random.binomial(species_1_units, p)
            if species_2_type == 1:
                # If losers are humans, every one of them has a probability p of being transformed.
                remaining_units += np.random.binomial(species_2_units, p)
        # If species 2 wins
        else:
            winner = species_2_type
            # Every winner's unit has a probability 1-p of surviving
            remaining_units = np.random.binomial(species_2_units, 1-p)
    else:
        winner = species_1_type if species_1_units >= species_2_units else species_2_type
        remaining_units = species_1_units + (species_2_type == 1) * species_2_units
    return winner, remaining_units
