from systeme_expert.regles_expert import Regles, Faits

def chainage(F, R):

    while True:
        regles_applicables = []
        for regle in R:
            if regle.applicable(F):
                regles_applicables.append(regle)
        
        if len(regles_applicables) == 0:
            break

        for regle in regles_applicables:
            regle.appliquer(F)





