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

def vectorial_energy(edge:np.array,E:np.array):
    '''
    E:ensemble d'edges dans le fichier (n,2,2)
    avec n le nombre d'edges dans le fichier
    edge: l'edge qu'on veut stitcher (2,2)
    '''
    norm_edge = norm2(edge[0],edge[1])
    N = np.empty((E.shape[0],1))
    norm_1_2 = np.empty((E.shape[0],1))
    norm_1_1 = np.empty((E.shape[0],1))

    for i in range(E.shape[0]):
        N[i] = norm2(E[i,0],E[i,1])
        norm_1_2[i] = norm2(edge[0],E[i,1]) + norm2(edge[1],E[i,0])
        norm_1_1[i] = norm2(edge[0],E[i,0]) + norm2(edge[1],E[i,1])

    #print(np.minimum(norm_1_2,norm_1_1))
    return np.minimum(norm_1_2,norm_1_1) - norm_edge - N

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

def stitchEdges_2(graph):
    '''
    Récupère la liste de coordonnées des deux cycles, ainsi que les deux edges à stitch.

    Recrée un objet de type path avec la liaison effectuée.
    '''
    global liste_points
    global liste_adjacence
    global liste_indice_depart

    array_de_point, array_d_adjacence, array_indice_depart = graph

    '''trouver le premier cycle a stitch'''
    #necessaire??

    # min_cycle = array_indice_depart[0]
    # for cycle in array_indice_depart:
    #     if cycle[1] <= min_cycle[1]:
    #         min_cycle = cycle
    # id_cycle_depart = liste_indice_depart.index(min_cycle)
    """
    print(liste_indice_depart, len(liste_points))
    test = len(liste_indice_depart)
    print(liste_points[82], liste_points[83], liste_points[100], liste_points[101])
    print(norm2(liste_points[82], liste_points[83]), norm2(liste_points[100], liste_points[101]))
    print(norm2(liste_points[82], liste_points[100]), norm2(liste_points[83], liste_points[101]))
    print(norm2(liste_points[82], liste_points[101]), norm2(liste_points[83], liste_points[100]))
    """
    for i in tqdm(range(array_indice_depart.shape[0]-1)):
    #while len(liste_indice_depart) > 1:
        reversed, edge1_ids, edge2_ids = nearestCycle(graph, id_cycle_depart)

        cycle_A_id, cycle_B_id = selectIdCycle(edge1_ids[0]), selectIdCycle(edge2_ids[0])

        id_first_point = edge2_ids[0]

        if reversed:
            reverse_2(edge1_ids[0])
            patch_pattern = 'pattern_1'
        else:
            patch_pattern = 'pattern_2'
        #patch_pattern = selectCorrectPatchPattern_3(edge1_ids, edge2_ids)

        # si on met liste_adjacence en global pk la mettre en paramètre de la fonction ?
        liste_adjacence = changeAdjacence_2(edge1_ids, edge2_ids, patch_pattern, liste_adjacence)

        cycle_B_id = merge_Cycles(cycle_B_id, cycle_A_id)
        id_cycle_depart = cycle_B_id
        # ou on pred l'indice du cycle avec le - de points (+ complexe)

    # print(liste_indice_depart)


    first_stitch_id = liste_adjacence[id_first_point][0]
    # print(id_first_point, liste_adjacence, first_stitch_id)
    lines = [0.] *(len(liste_points))
    lines[0] = svgpt.Line(liste_points[id_first_point], liste_points[first_stitch_id])
    current_point_id = first_stitch_id
    next_point_id = liste_adjacence[current_point_id][0]
    # print(lines[-1])

    for i in range(len(liste_points)):
        lines[i] = svgpt.Line(liste_points[current_point_id], liste_points[next_point_id])
        current_point_id = next_point_id
        next_point_id = liste_adjacence[current_point_id][0]
        # print(lines[-1])

    print(lines)

    new_path = svgpt.Path(*lines)
    return new_path