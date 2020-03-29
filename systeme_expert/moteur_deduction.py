from systeme_expert.regles_expert import fact_observation
from systeme_expert.strategies import AttackFirst, StraightAttack, AggloStrategy, SplitStrategy


def chainage(F, R, state):
    for regle in R:
        regle.reset_applicable()

def chainage(facts, rules, state):
    for rule in rules:
        rule.reset_applicable()

    fact_observation(state, facts)

    print(f"faits precedents {facts[1]}")

    while True:
        regles_applicables = []
        for rule in rules:
            if rule.applicable(facts):
                regles_applicables.append(rule)
        
        if len(regles_applicables) == 0:
            break

        for rule in regles_applicables:
            print(rule)
            rule.apply(facts)

    print(f"chosen strategy : {facts[0]['strategy']}")

    if facts[0]["strategy"] == "firstattack":
        strat = AttackFirst()
        return strat

    if facts[0]["strategy"] == "straightattack":
        strat = StraightAttack()
        return strat

    if facts[0]["strategy"] == "agglo":
        strat = AggloStrategy()
        return strat

    if facts[0]["strategy"] == "split":
        strat = SplitStrategy()
        return strat

