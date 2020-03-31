from utils import species_coordinates, distance
import math


## liste des faits: positions nous/ennemie, distance, variation distance, nb unité nous/ennemie, différence nb unité, variation différence
# nombre de groupe d'unité nous/ennemie, différence du nombre de groupe, variation de cette différence
def fact_dict():
    dict_ = {"position nous": None, "position ennemie": None, "distance": None, "variation distance": None,
             "nb unité nous": None, "nb unité ennemie": None, "diff nb unité": None, "variation diff nb unité": None,
             "nb de groupe nous": None, "nb de groupe ennemie": None, "variation nb de groupe ennemie": None,
             "variation nb de groupe nous": None, "strategy": None, "refus de combat": False}
    return dict_


current_facts = {"position nous": None, "position ennemie": None, "distance": 5, "variation distance": None,
                 "nb unité nous": None, "nb unité ennemie": None, "diff nb unité": None,
                 "variation diff nb unité": None, "nb de groupe nous": None, "nb de groupe ennemie": None,
                 "variation nb de groupe ennemie": None, "variation nb de groupe nous": None, "strategy": None,
                 "refus de combat": False}

previous_facts = fact_dict()


Facts = [current_facts, previous_facts]


def fact_observation(state, facts):
    facts[1] = facts[0].copy()
    facts[0]["position nous"] = state.our_species.tile_contents()
    facts[0]["position ennemie"] = state.enemy_species.tile_contents()
    facts[0]["nb unité nous"] = state.our_species.units
    facts[0]["nb unité ennemie"] = state.enemy_species.units
    facts[0]["diff nb unité"] = facts[0]["nb unité nous"] - facts[0]["nb unité ennemie"]
    facts[0]["nb de groupe nous"] = len(state.our_species.tile_coordinates())
    facts[0]["nb de groupe ennemie"] = len(species_coordinates(state, state.enemy_species))
    facts[0]["refus de combat"] = None


class Rule:
    def __init__(self):
        self.applied = False
        self.current_premises = []
        self.previous_premises = []

    def reset_applicable(self):
        self.applied = False

    def applicable(self, facts):
        if self.applied:
            return False

        for premise in self.current_premises:
            if facts[0][premise] is None:
                return False

        for premise in self.previous_premises:
            if facts[1][premise] is None:
                return False

        return True

    def apply(self, facts):
        pass


class RDistance(Rule):
    """Calculates overall distance between enemy units and us"""

    def __init__(self):
        Rule.__init__(self)
        self.applied = False
        self.current_premises = ["position nous", "position ennemie"]
        self.previous_premises = []

    def apply(self, facts):
        distances = []
        ## on calcule pour toutes nos unités, les distances minimums avec des unités ennemies et on dit que notre
        ## distance est le min de ces distances
        for our_position in facts[0]["position nous"]:
            unit_distance = math.inf
            for enemy_position in facts[0][self.current_premises[1]]:
                if distance(enemy_position, our_position) < unit_distance:
                    unit_distance = distance(enemy_position, our_position)
            distances.append(unit_distance)

        facts[0]["distance"] = min(distances)
        self.applied = True


class RVariationDistance(Rule):
    """Checks whether the enemy is moving towards us or away from us."""

    def __init__(self):
        Rule.__init__(self)
        self.applied = False
        self.current_premises = ["distance"]
        self.previous_premises = ["distance"]

    def apply(self, facts):
        current_facts = facts[0]
        previous_facts = facts[1]

        if current_facts["distance"] != previous_facts["distance"]:
            facts[0]["variation distance"] = abs(current_facts["distance"] - previous_facts["distance"])
        else:
            facts[0]["variation distance"] = 0

        self.applied = True


class RRefuseCombat(Rule):
    def __init__(self):
        Rule.__init__(self)
        self.applied = False
        self.current_premises = ["distance"]
        self.previous_premises = ["distance", "refus de combat"]

    def apply(self, facts):
        # on considere qu'un ennemi nous fuit s'il a eu l'occasion de nous attaquer
        # mais qu'il ne l'a pas fait
        current_facts = facts[0]
        previous_facts = facts[1]
        if previous_facts["refus de combat"] or (current_facts["distance"] >= 2 and previous_facts["distance"] == 2):
            facts[0]["refus de combat"] = True
        else:
            facts[0]["refus de combat"] = False

        self.applied = True


class RStrategy(Rule):
    def __init__(self):
        self.applied = False
        self.current_premises = ["nb unité nous", "nb unité ennemie", "nb de groupe nous", "refus de combat"]
        self.previous_premises = []

    def apply(self, facts):
        current_facts = facts[0]

        # on est desesperes
        if 1.5 * current_facts["nb unité nous"] < current_facts["nb unité ennemie"]:
            facts[0]["strategy"] = "split"

        # si on n'est pas groupes, il faut le faire
        elif current_facts["nb de groupe nous"] > 1:
            facts[0]["strategy"] = "agglo"

        # le cas ou on gagne de toute facon
        elif current_facts["nb unité nous"] > 1.5 * current_facts["nb unité ennemie"]:
            facts[0]["strategy"] = "straightattack"

        # le cas ou on est just un peu plus nombreux : il faut tenter d'attaquer, mais s'ils fuient, les laisser fuir
        elif current_facts["nb unité nous"] >= current_facts["nb unité ennemie"]:
            facts[0]["strategy"] = "firstattack"

        # le cas ou on est un peu moins nombreux : il faut se battre à tout prix : si on peut les attaquer tant mieux
        # sinon, il faut tenter quand meme
        elif current_facts["nb unité nous"] < current_facts["nb unité ennemie"] and 1.5 * current_facts[
            "nb unité nous"] > current_facts["nb unité ennemie"]:
            if not current_facts["refus de combat"]:
                facts[0]["strategy"] = "firstattack"
            else:
                facts[0]["strategy"] = "straightattack"

        self.applied = True


distance_instance = RDistance()
refuse_combat_instance = RRefuseCombat()
strategy_instance = RStrategy()
Rules = [distance_instance, refuse_combat_instance, strategy_instance]
