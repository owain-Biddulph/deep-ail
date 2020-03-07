def win_probability(attack_troops: int, defense_troops: int, defense_type: int):
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
        expected_outcome += (attacking_species_units > defending_species_units) * attacking_species_units
    return expected_outcome
