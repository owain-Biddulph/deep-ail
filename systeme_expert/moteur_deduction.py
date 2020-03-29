from systeme_expert.regles_expert import observation_faits
from systeme_expert.strategies import AttackFirst, StraightAttack, AggloStrategy, SplitStrategy


def chainage(F, R, state):
    for regle in R:
        regle.reset_applicable()

    observation_faits(state, F)

    print(f"faits precedents {F[1]}")

    while True:
        regles_applicables = []
        for regle in R:
            if regle.applicable(F):
                regles_applicables.append(regle)

        if len(regles_applicables) == 0:
            break

        for regle in regles_applicables:
            print(regle)
            regle.appliquer(F)

    print(f"chosen strategy : {F[0]['strategy']}")

    if F[0]["strategy"] == "firstattack":
        strat = AttackFirst()
        return strat

    if F[0]["strategy"] == "straightattack":
        strat = StraightAttack()
        return strat

    if F[0]["strategy"] == "agglo":
        strat = AggloStrategy()
        return strat

    if F[0]["strategy"] == "split":
        strat = SplitStrategy()
        return strat

