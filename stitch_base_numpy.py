def test():
    pass
from math import inf
import svg_handler as svgh
import numpy as np
import svgpathtools as svgpt

'''
Cycle

'''
def np_norm2(point_a, point_b):
    '''
    point : vecteur 1,2
    norme euclidienne avec numpy
    '''
    return np.sqrt(np.sum((point_a-point_b)**2))

def np_energyid_cycle_Alc(edge1, edge2):
    '''
    edge : 2,2
    calcul energie de 'patch'
    '''
    res = min(np_norm2(edge1[0], edge2[1])+ np_norm2(edge1[1], edge2[0]),
              np_norm2(edge1[0], edge2[0]) + np_norm2(edge1[1], edge2[1]))

    res -= np_norm2(edge1[0], edge1[1]) - np_norm2(edge2[0], edge2[1])

    return res

def listCoord(graph,id_cycle_A):
    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle;

    renvoie un un tableau de dim N,2 avec contenant les points d'un seul cycle dont l'indice est passe en argument
    """
    liste_points, liste_adjacence, liste_indice_depart = graph
    res = np.empty((0,2))
    act = liste_indice_depart[id_cycle_A][0]

    for i in range(liste_indice_depart[id_cycle_A][1]):
        res = np.vstack((res,liste_points[act]))
        act = liste_adjacence[act][0]
    return res