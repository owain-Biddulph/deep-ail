from utils import species_coordinates, distance
import math

##liste des faits: positions nous/ennemie, distance, variation distance, nb unité nous/ennemie, différence nb unité, variation différence
## nombre de groupe d'unité nous/ennemie, différence du nombre de groupe, variation de cette différence

Faits_actuels = {"position nous": None, "position ennemie": None, "distance": None, "variation distance": None,
                 "nb unité nous": None, "nb unité ennemie": None, "diff nb unité": None, "variation diff nb unité": None
                 "nb de groupe nous": None, "nb de groupe ennemie": None, "variation nb de groupe ennemie": None, "variation nb de groupe nous": None
                 "strategy": "firstattack"}

Faits_precedents = {"position nous": None, "position ennemie": None, "distance": None, "variation distance": None,
                 "nb unité nous": None, "nb unité ennemie": None, "diff nb unité": None, "variation diff nb unité": None
                 "nb de groupe nous": None, "nb de groupe ennemie": None, "variation nb de groupe ennemie": None, "variation nb de groupe nous": None,
                    "strategy": None}

Faits = [Faits_actuels, Faits_precedents]

distance = r_distance()
variation_distance = r_variation_distance()
strategy = r_strategy()

Regles = [distance, variation_distance, strategy]

def observation_faits(state, Faits):
    Faits[1], Faits[0] = Faits[0], Faits[1]
    Faits[0]["position nous"] = state.our_species.tile_contents
    Faits[0]["position ennemie"] = state.enemy_species.tile_contents
    Faits[0]["nb unité nous"] = state.our_species.units
    Faits[0]["nb unité ennemie"] = state.ennemy_species.units
    Faits[0]["diff nb unité"] = Faits[0]["nb unité nous"] - Faits[0]["nb unité ennemie"]
    Faits[0]["variation diff nb unité"] = Faits[0]["diff nb unité"] - Faits[1]["diff nb unité"]
    Faits[0]["nb de groupe nous"] = len(species_coordinates(state, state.our_species))
    Faits[0]["variation nb de groupe nous"] = Faits[0]["nb de groupe nous"] - Faits[1]["nb de groupe nous"]
    Faits[0]["nb de groupe ennemie"] = len(species_coordinates(state, state.enemy_species))
    Faits[0]["variation nb de groupe ennemie"] = Faits[0]["nb de groupe ennemie"] - Faits[1]["nb de groupe ennemie"]


class Regle:

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = []
        self.premisses_precedents = []

    def applicable(self, faits):
        if self.appliquee:
            return False

        for premisse in self.premisses_actuels:
            if faits[0][premisse] is None:
                return False

        for premisse in self.premisses_precedents:
            if faits[1][premisse] is None:
                return False

        return True

    def appliquer(self, faits):
        pass


class r_distance(Regle):

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["position nous", "position ennemie"]

    def appliquer(self, faits):
        distances = []
        ## on calcule pour toutes nos unités, les distances minimums avec des unités ennemies et on dit que notre
        ## distance est le min de ces distances
        for position_nous in faits[0][self.premisses_actuels[0]]:
            distance_cette_unité = math.inf
            for position_ennemie in faits[0][self.premisses_actuels[1]]:
                if distance(position_ennemie,  position_nous) < distance_cette_unité:
                    distance_cette_unité = distance(position_ennemie,  position_nous)
            distances.append(distance_cette_unité)

        faits[0]["distance"] = min(distances)
        self.appliquee = True


class r_variation_distance(Regle):

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["distance"]
        self.premisses_precedents = ["distance"]

    def appliquer(self, faits):
        faits_actuels = faits[0]
        faits_precedents = faits[1]
        
        if faits_actuels["distance"] != faits_precedents["distance"]:
            faits["variation distance"] = abs(faits_actuels["distance"] - faits_precedents["distance"])
        else:
            faits["variation distance"] = 0

        self.appliquee = True


class r_strategy(Regle):

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["position nous", "position ennemie", "distance", "variation distance",
                 "nb unité nous", "nb unité ennemie", "diff nb unité", "variation diff nb unité",
                 "nb de groupe nous", "nb de groupe ennemie", "variation nb de groupe ennemie", "variation nb de groupe nous"]
        self.premisses_precedents = ["position nous", "position ennemie", "distance", "variation distance",
                 "nb unité nous", "nb unité ennemie", "diff nb unité", "variation diff nb unité",
                 "nb de groupe nous", "nb de groupe ennemie", "variation nb de groupe ennemie", "variation nb de groupe nous"]

    def appliquer(self, faits):
        faits_actuels = faits[0]
        faits_precedents = faits[1]

        ##TODO

        self.appliquee = True


