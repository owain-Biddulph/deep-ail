from systeme_expert.regles_expert import Regles, Faits
from systeme_expert.strategies import AttackFirst, StraightAttack, AggloStrategy, SplitStrategy

def chainage(F, R):
    for regle in R:
        regle.reset_applicable()

    while True:
        regles_applicables = []
        for regle in R:
            if regle.applicable(F):
                regles_applicables.append(regle)
        
        if len(regles_applicables) == 0:
            break

        for regle in regles_applicables:
            regle.appliquer(F)

    if Faits[0]["strategy"] == "firstattack":
        strat = AttackFirst()
        return strat

    if Faits[0]["strategy"] == "straightattack":
        strat = StraightAttack()
        return strat

    if Faits[0]["strategy"] == "agglo":
        strat = AggloStrategy()
        return strat

    if Faits[0]["strategy"] == "split":
        strat = SplitStrategy()
        return strat

