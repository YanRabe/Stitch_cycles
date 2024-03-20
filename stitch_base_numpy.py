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

def np_listCoord(graph,id_cycle_A):
    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle;

    renvoie un un tableau de dim N,2 avec contenant les points d'un seul cycle dont l'indice est passe en argument
    """
    array_de_point, array_d_adjacence, array_indice_depart = graph
    res = np.empty((0,2))
    act = array_indice_depart[id_cycle_A,0]

    for i in range(array_indice_depart[id_cycle_A,1]):
        inter = np.vstack((res,array_de_point[act]))
        act = array_d_adjacence[act][0]
    return inter

def np_nearestCycle(graph, id_cycle_A):

    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle dont on cherche le voisin le + proche;
    """
    array_de_point, _, array_indice_depart = graph
    """
    print(len(liste_indice_depart), id_cycle_A)

    if len(liste_indice_depart) < id_cycle_A:
        print(liste_indice_depart)
    """

    cycle_A = np_listCoord(graph, id_cycle_A)
    min_energy_cycle = inf
    edge_A, edge_B = None, None

    for id_cycle_B in range(array_indice_depart.shape[0]):


        if id_cycle_B != id_cycle_A:

            cycle_B = np_listCoord(graph, id_cycle_B)

            temp = np_nearestEdge3(cycle_A, cycle_B)

            if temp[2] < min_energy_cycle:

                min_energy_cycle = temp[2]
                edge_A = np.where(array_de_point==temp[0][0])
                edge_B = np.where(array_de_point==temp[1][0])

            """
            liste_energy.append(min_energy_cycle)
            indice_A1, indice_A2 = liste_de_point.index(edge_A[0]), liste_de_point.index(edge_A[1])
            indice_B1, indice_B2 = liste_de_point.index(edge_B[0]), liste_de_point.index(edge_B[1])
            liste_edges.append([[indice_A1,indice_A2],[indice_B1,indice_B2]])

        else:

            liste_energy.append(min_energy_cycle)
            liste_edges.append([None,None])
            """
    """
    minId = liste_energy.index(min(liste_energy))
    return liste_energy[minId], *liste_edges[minId]
    """
    return min_energy_cycle, edge_A, edge_B

def np_nearestEdge3(cycle_A, cycle_B):
    '''
    renvoie les deux edges les + proches entre cycle A et cycle B
    '''
    edge_A, edge_B = np.array([cycle_A[-1], cycle_A[0]]), np.array([cycle_B[-1], cycle_B[0]])
    min_energy = np_energyid_cycle_Alc(edge_A, edge_B)

    for id_point_A in range(cycle_A.shape[0]-1):
        for id_point_B in range(cycle_A.shape[1]-1):
            temp = np_energyid_cycle_Alc([cycle_A[id_point_A], cycle_A[id_point_A + 1]], [cycle_B[id_point_B], cycle_B[id_point_B + 1]])
            if temp < min_energy:
                min_energy = temp
                edge_A, edge_B = np.array([cycle_A[id_point_A], cycle_A[id_point_A + 1]]), np.array([cycle_B[id_point_B], cycle_B[id_point_B + 1]])

    return edge_A, edge_B, min_energy

def isPrecedent(point_1, point_2):
    """
    La fonction revoie True si le point_1 est le premier du segment
    point_1 est l'indice d'un point du cycle dans array_de_point
    point_2 est l'indice d'un point du cycle dans array_de_point
    """
    global array_d_adjacence
    return array_d_adjacence[point_1][0] == point_2