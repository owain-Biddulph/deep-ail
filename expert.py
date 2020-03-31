import numpy as np


def centroid(state, species):
    coords = np.nonzero(state.board[:, :, 0] == species)
    weights = np.where(state.board[:, :, 0] == species, state.board[:, :, 1], 0)
    centroid_ = np.zeros(2)
    for (x, y) in zip(coords[0], coords[1]):
        centroid_[0] += weights[x, y] * x
        centroid_[1] += weights[x, y] * y
    centroid_ /= np.sum(weights)
    return centroid_


def dist(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def measure_risk(state, our_species, enemy_species):
    our_ctr = centroid(state, our_species)
    enemy_ctr = centroid(state, enemy_species)
    return dist(our_ctr, enemy_ctr)


def measure_proximity(state, species):
    ctr = centroid(state, species)
    coords = np.nonzero(state.board[:, :, 0] == species)
    weights = np.where(state.board[:, :, 0] == species, state.board[:, :, 1], 0)
    proximity = 0
    for (x, y) in zip(coords[0], coords[1]):
        proximity += dist(ctr, [x, y])*weights[x, y]
    proximity /= np.sum(weights)
    return proximity


def next_move():
    groups = np.count_nonzero(state.board[:, :, 0] == state.our_species)
    
    # Si on est pas regroupé, on cherche à diminuer la distance entre chacune de nos unités.
    if groups > 1:
        group_units(state)
    
    # Si on est regroupé
    else:
        # Trouver une façon de mesurer le rapprochement des unités adverses aux nôtres.
        # On peut mesurer la distance moyenne entre les unités, ou la distance entre les barycentres.
        closer = ...
        # Si on est moins nombreux
        if state.our_troops < state.enemy_troops:
            # S'il se rapprochent
            if closer:
                # On attend
                wait()
            else:
                get_closer()
                # On se rapproche sans se mettre en danger
                
        # Si on est autant
        elif us == them:
            if closer:
#                 On se rapproche sans se mettre en danger
                get_closer()
            else:
#                 On se rapproche sans se mettre en danger
                get_closer()

        # Si on est plus nombreux:
        else:
            if closer:
#                 On attend sagement en s'éloignant du bord
                wait()
            else:
#                 WTF, on attend
                wait()
