from utils import species_coordinates, distance
import math

##liste des faits: positions nous/ennemie, distance, variation distance, nb unité nous/ennemie, différence nb unité, variation différence
## nombre de groupe d'unité nous/ennemie, différence du nombre de groupe, variation de cette différence

Faits_actuels = {"position nous": None, "position ennemie": None, "distance": 5, "variation distance": None,
                 "nb unité nous": None, "nb unité ennemie": None, "diff nb unité": None,
                 "variation diff nb unité": None,
                 "nb de groupe nous": None, "nb de groupe ennemie": None, "variation nb de groupe ennemie": None,
                 "variation nb de groupe nous": None,
                 "strategy": None, "refus de combat": False}

Faits_precedents = {"position nous": None, "position ennemie": None, "distance": None, "variation distance": None,
                    "nb unité nous": None, "nb unité ennemie": None, "diff nb unité": None,
                    "variation diff nb unité": None,
                    "nb de groupe nous": None, "nb de groupe ennemie": None, "variation nb de groupe ennemie": None,
                    "variation nb de groupe nous": None,
                    "strategy": None, "refus de combat": False}

Faits_precedents_2 = {"position nous": None, "position ennemie": None, "distance": None, "variation distance": None,
                      "nb unité nous": None, "nb unité ennemie": None, "diff nb unité": None,
                      "variation diff nb unité": None,
                      "nb de groupe nous": None, "nb de groupe ennemie": None, "variation nb de groupe ennemie": None,
                      "variation nb de groupe nous": None,
                      "strategy": None, "refus de combat": False}

Faits_precedents_3 = {"position nous": None, "position ennemie": None, "distance": None, "variation distance": None,
                      "nb unité nous": None, "nb unité ennemie": None, "diff nb unité": None,
                      "variation diff nb unité": None,
                      "nb de groupe nous": None, "nb de groupe ennemie": None, "variation nb de groupe ennemie": None,
                      "variation nb de groupe nous": None,
                      "strategy": None, "refus de combat": False}


Faits = [Faits_actuels, Faits_precedents, Faits_precedents_2, Faits_precedents_3]


def observation_faits(state, Faits):
    Faits[1], Faits[2], Faits[3] = Faits[0].copy(), Faits[1].copy(), Faits[2].copy()
    Faits[0]["position nous"] = state.our_species.tile_contents()
    Faits[0]["position ennemie"] = state.enemy_species.tile_contents()
    Faits[0]["nb unité nous"] = state.our_species.units
    Faits[0]["nb unité ennemie"] = state.enemy_species.units
    Faits[0]["diff nb unité"] = Faits[0]["nb unité nous"] - Faits[0]["nb unité ennemie"]
    # Faits[0]["variation diff nb unité"] = Faits[0]["diff nb unité"] - Faits[1]["diff nb unité"]
    Faits[0]["nb de groupe nous"] = len(state.our_species.tile_coordinates())
    # Faits[0]["variation nb de groupe nous"] = Faits[0]["nb de groupe nous"] - Faits[1]["nb de groupe nous"]
    Faits[0]["nb de groupe ennemie"] = len(species_coordinates(state, state.enemy_species))
    # Faits[0]["variation nb de groupe ennemie"] = Faits[0]["nb de groupe ennemie"] - Faits[1]["nb de groupe ennemie"]
    Faits[0]["refus de combat"] = None


class Regle:

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = []
        self.premisses_precedents = []
        self.premisses_precedents_2 = []
        self.premisses_precedents_3 = []

    def reset_applicable(self):
        self.appliquee = False


    def applicable(self, faits):
        if self.appliquee:
            return False

        for premisse in self.premisses_actuels:
            print(f"premisse actuel {premisse}: {faits[0][premisse]}")
            if faits[0][premisse] is None:
                return False

        for premisse in self.premisses_precedents:
            print(f"premisse precedent {premisse}: {faits[1][premisse]}")
            if faits[1][premisse] is None:
                return False

        return True

    def appliquer(self, faits):
        pass


class r_distance(Regle):
    """
    calcule la distance au sens des ensemble entre nous et eux.
    """

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["position nous", "position ennemie"]
        self.premisses_precedents = []

    def appliquer(self, faits):
        distances = []
        ## on calcule pour toutes nos unités, les distances minimums avec des unités ennemies et on dit que notre
        ## distance est le min de ces distances
        for position_nous in faits[0]["position nous"]:
            distance_cette_unité = math.inf
            for position_ennemie in faits[0][self.premisses_actuels[1]]:
                if distance(position_ennemie, position_nous) < distance_cette_unité:
                    distance_cette_unité = distance(position_ennemie, position_nous)
            distances.append(distance_cette_unité)

        faits[0]["distance"] = min(distances)
        self.appliquee = True


class r_variation_distance(Regle):
    """
    les ennemis s'approchent-ils ou s'éloignent-ils
    """

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["distance"]
        self.premisses_precedents = ["distance"]

    def appliquer(self, faits):
        faits_actuels = faits[0]
        faits_precedents = faits[1]

        if faits_actuels["distance"] != faits_precedents["distance"]:
            faits[0]["variation distance"] = abs(faits_actuels["distance"] - faits_precedents["distance"])
        else:
            faits[0]["variation distance"] = 0

        self.appliquee = True


class r_refus_combat(Regle):

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["distance"]
        self.premisses_precedents = ["distance", "refus de combat"]

        self.premisses_precedents_2 = ["position nous", "position ennemie", "distance", "variation distance",
                 "nb unité nous", "nb unité ennemie", "diff nb unité", "variation diff nb unité",
                 "nb de groupe nous", "nb de groupe ennemie", "variation nb de groupe ennemie", "variation nb de groupe nous"]

        self.premisses_precedents_3 = ["position nous", "position ennemie", "distance", "variation distance",
                 "nb unité nous", "nb unité ennemie", "diff nb unité", "variation diff nb unité",
                 "nb de groupe nous", "nb de groupe ennemie", "variation nb de groupe ennemie", "variation nb de groupe nous"]

    def appliquer(self, faits):
        # on considere qu'un ennemi nous fuit s'il a eu l'occasion de nous attaquer
        # mais qu'il ne l'a pas fait
        faits_actuels = faits[0]
        faits_precedents = faits[1]
        faits_precedents_2 = faits[2]
        faits_precedents_3 = faits[3]
        if (faits_precedents["refus de combat"] or (
                faits_actuels["distance"] >= 2 and faits_precedents["distance"] == 2)):
            print(f"faits_precedents : refus de combat : {faits_precedents['refus de combat']}")
            print(f"faits_actuels : distance : {faits_actuels['distance']}")
            print(f"faits_precedents : distance {faits_precedents['distance']}")
            faits[0]["refus de combat"] = True
        else:
            faits[0]["refus de combat"] = False

        self.appliquee = True


class r_strategy(Regle):

    def __init__(self):
        self.appliquee = False
        # self.premisses_actuels = ["refus de combat""position nous", "position ennemie", "distance", "variation distance",
        #         "nb unité nous", "nb unité ennemie", "diff nb unité", "variation diff nb unité",
        #         "nb de groupe nous", "nb de groupe ennemie", "variation nb de groupe ennemie", "variation nb de groupe nous"]

        # self.premisses_precedents = ["position nous", "position ennemie", "distance", "variation distance",
        #         "nb unité nous", "nb unité ennemie", "diff nb unité", "variation diff nb unité",
        #         "nb de groupe nous", "nb de groupe ennemie", "variation nb de groupe ennemie", "variation nb de groupe nous"]

        # self.premisses_precedents_2 = ["position nous", "position ennemie", "distance", "variation distance",
        #         "nb unité nous", "nb unité ennemie", "diff nb unité", "variation diff nb unité",
        #         "nb de groupe nous", "nb de groupe ennemie", "variation nb de groupe ennemie", "variation nb de groupe nous"]

        # self.premisses_precedents_3 = ["position nous", "position ennemie", "distance", "variation distance",
        #         "nb unité nous", "nb unité ennemie", "diff nb unité", "variation diff nb unité",
        #         "nb de groupe nous", "nb de groupe ennemie", "variation nb de groupe ennemie", "variation nb de groupe nous"]

        self.premisses_actuels = ["nb unité nous", "nb unité ennemie", "nb de groupe nous", "refus de combat"]
        self.premisses_precedents = []

    def appliquer(self, faits):
        faits_actuels = faits[0]
        faits_precedents = faits[1]
        faits_precedents_2 = faits[2]
        faits_precedents_3 = faits[3]

        # on est desesperes
        if 1.5 * faits_actuels["nb unité nous"] < faits_actuels["nb unité ennemie"]:
            Faits[0]["strategy"] = "split"
            print(f"choosing {Faits[0]['strategy']}")

        # si on n'est pas groupes, il faut le faire
        elif faits_actuels["nb de groupe nous"] > 1:
            Faits[0]["strategy"] = "agglo"
            print(f"choosing {Faits[0]['strategy']}")

        # le cas ou on gagne de toute facon
        elif faits_actuels["nb unité nous"] > 1.5 * faits_actuels["nb unité ennemie"]:
            Faits[0]["strategy"] = "straightattack"
            print(f"choosing {Faits[0]['strategy']}")

        # le cas ou on est just un peu plus nombreux : il faut tenter d'attaquer, mais s'ils fuient, les laisser fuir
        elif faits_actuels["nb unité nous"] > faits_actuels["nb unité ennemie"]:
            Faits[0]["strategy"] = "firstattack"
            print(f"choosing {Faits[0]['strategy']}")

        # le cas ou on est un peu moins nombreux : il faut se battre à tout prix : si on peut les attaquer tant mieux
        # sinon, il faut tenter quand meme
        elif faits_actuels["nb unité nous"] < faits_actuels["nb unité ennemie"] and 1.5 * faits_actuels[
            "nb unité nous"] > faits_actuels["nb unité ennemie"]:
            if not faits_actuels["refus de combat"]:
                Faits[0]["strategy"] = "firstattack"
                print(f"choosing {Faits[0]['strategy']}")
            else:
                Faits[0]["strategy"] = "straightattack"
                print(f"choosing {Faits[0]['strategy']}")

        self.appliquee = True


distance_instance = r_distance()
# variation_distance_instance = r_variation_distance()
refus_combat_instance = r_refus_combat()
strategy_instance = r_strategy()
Regles = [distance_instance, refus_combat_instance, strategy_instance]

