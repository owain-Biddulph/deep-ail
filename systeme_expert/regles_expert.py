from utils import species_coordinates
Faits_actuels = {"delta distance": 0, "delta nombre d unité": 0, "delta nombre de groupe d unité": 0, "nombre de groupe allié":0,
                "nombre de groupe ennemie":0, "enemy explosion": -1}

Faits_precedents = {"delta distance": 0, "delta nombre d unité": 0, "delta nombre de groupe d unité": 0, "nombre de groupe allié":0,
                "nombre de groupe ennemie":0, "enemy explosion": -1}
Faits = [Faits_actuels, Faits_precedents]

Regles = [r_enemy_split]

def observation_faits(state, Faits):
    Faits[1], Faits[0] = Faits[0], Faits[1]
    Faits[0]["nombre de groupe allié"] = len(species_coordinates(state, state.our_species))
    Faits[0]["nombre de groupe ennemie"] = len(species_coordinates(state, state.enemy_species))

class Regle:

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = []
        self.premisses_precedents = []

    def applicable(self, faits):
        if self.appliquee:
            return False

        for premisse in self.premisses_actuels:
            if faits[0][premisse] == -1:
                return False

        for premisse in self.premisses_precedents:
            if faits[1][premisse] == -1:
                return False

        return True

    def appliquer(self, faits):
        pass

class r_enemy_split(Regle):

    def __init__(self):
        self.appliquee = False
        self.premisses_actuels = ["nombre de groupe ennemie"]
        self.premisses_precedents = ["nombre de groupe ennemie"]

    def appliquer(self, faits):
        faits_actuels = Faits[0]
        faits_precedents = Faits[1]
        if (faits_actuels["nombre de groupe ennemie"] > faits_precedents["nombre de groupe ennemie"] ):
            faits_actuels["enemy explosion"] = 1
        else:
            faits_actuels["enemy explosion"] = 0
        self.appliquee = True
