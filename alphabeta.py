

def MaxValue(state, alpha, beta):
    if successeurs(state) == None:
        return eval(state)
    for states in successeurs(state):
        alpha = max(alpha, MinValue(states, alpha, beta))
        if alpha >= beta:
            return beta
    return alpha


def MinValue(state, alpha, beta):
    if successeurs(state) == None:
        return eval(state)
    for states in successeurs(state):
        alpha = min(alpha, MaxValue(states, alpha, beta))
        if alpha >= beta:
            return beta
    return alpha
##Todo
## faire les states, et  calculer les states successeurs, et eval (coté nico avec l'heuristique)

