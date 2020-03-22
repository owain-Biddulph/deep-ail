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

Regles = [r_us_split, r_enemy_split, r_distance]

def observation_faits(state, Faits):
    Faits[1], Faits[0] = Faits[0], Faits[1]
    Faits[0]["position nous"] = state.our_species.tile_contents
    Faits[0]["position ennemie"] = state.enemy_species.tile_contents
    Faits[0]["distance"] =
    Faits[0]["nb unité nous"] = state.our_species.units
    Faits[0]["nb unité ennemie"] = state.ennemy_species.units
    Faits[0]["nb de groupe nous"] = len(species_coordinates(state, state.our_species))
    Faits[0]["nb de groupe ennemie"] = len(species_coordinates(state, state.enemy_species))


class Regle:

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = []
        self.premisses_precedents = []

    def applicable(self, faits):
        if self.appliquee:
            return False

        for premisse in self.premisses_actuels:
            if faits[0][premisse] == None:
                return False

        for premisse in self.premisses_precedents:
            if faits[1][premisse] == None:
                return False

        return True

    def appliquer(self, faits):
        pass


class r_us_split(Regle):

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["nb de groupe nous"]
        self.premisses_precedents = ["nb de groupe nous"]

    def appliquer(self, faits):
        faits_actuels = faits[0]
        faits_precedents = faits[1]
        if faits_actuels["nb de groupe nous"] > faits_precedents["nb de groupe nous"]:
            faits[0]["variation nb de groupe nous"] = faits_actuels["nb de groupe nous"] - faits_precedents["nb de groupe nous"]
        elif faits_actuels["nb de groupe nous"] < faits_precedents["nb de groupe nous"]:
            faits[0]["variation nb de groupe nous"] = faits_actuels["nb de groupe nous"] - faits_precedents["nb de groupe nous"]
        else:
            faits[0]["variation nb de groupe nous"] = 0
        self.appliquee = True


class r_enemy_split(Regle):

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["nb de groupe ennemie"] ##ça sert à rien ce qu'on a fait là, on utilise jamais self.premisses actuels
        self.premisses_precedents = ["nb de groupe ennemie"]

    def appliquer(self, faits):
        faits_actuels = faits[0]
        faits_precedents = faits[1]
        if faits_actuels["nb de groupe ennemie"] > faits_precedents["nb de groupe ennemie"] :
            faits[0]["variation nb de groupe ennemie"] = faits_actuels["nb de groupe ennemie"] - faits_precedents["nb de groupe ennemie"]
        elif  faits_actuels["nb de groupe ennemie"] < faits_precedents["nb de groupe ennemie"]:
            faits[0]["variation nb de groupe ennemie"] = faits_actuels["nb de groupe ennemie"] - faits_precedents["nb de groupe ennemie"]
        else:
            faits[0]["variation nb de groupe ennemie"] = 0
        self.appliquee = True


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
        self.premisses_actuels = ["distance"] ##a quoi ça sert ?
        self.premisses_precedents = ["distance"]

    def appliquer(self, faits):
        faits_actuels = faits[0]
        faits_precedents = faits[1]
        
        if faits_actuels["distance"] != faits_precedents["distance"]:
            faits["variation distance"] = faits_actuels["distance"] - faits_precedents["distance"]
        else:
            faits



        self.appliquee = True



