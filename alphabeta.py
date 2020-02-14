def MaxValue(state, alpha, beta):
    boucle = True
    k=0
    while boucle:
        if k == 10:
            return eval(state)
        for states in successeurs(state):
            alpha = max(alpha, MinValue(states, alpha, beta))
            if alpha >= beta:
                return beta
        return alpha
    boucle = False


def MinValue(state, alpha, beta):
    boucle = True
    k=0
    while boucle:
        if k == 10:
            return eval(state)
        for states in successeurs(state):
            alpha = min(alpha, MaxValue(states, alpha, beta))
            if alpha >= beta:
                return beta
        return alpha
    boucle = False
##Todo
## faire les states, et  calculer les states successeurs, et eval (coté nico avec l'heuristique)

