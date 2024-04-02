def test():
    pass
from math import inf
import svg_handler as svgh
import numpy as np
import svgpathtools as svgpt
from tqdm import tqdm
#import stitch_base as sb

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

    res = res - np_norm2(edge1[0], edge1[1]) - np_norm2(edge2[1], edge2[0])

    return res

def edges(graph):
    '''
    out: array (n,2,2), n le nombre d'edges dans le graphe
    '''
    array_de_points, array_d_adjacence, array_indice_depart = graph
    E = np.empty((array_de_points.shape[0],2,2))
    for i in range(array_d_adjacence.shape[0]):
        E[i,0] = array_de_points[i]
        E[i,1] = array_de_points[array_d_adjacence[i,0]]
    return E

def vectorial_energy(edge:np.array,E:np.array):
    '''
    E:ensemble d'edges dans le fichier (n-1,2,2)
    avec n le nombre d'edges dans le fichier, il n imclus pas l edge qu on passe en arg
    edge: l'edge qu'on veut stitcher (2,2)
    '''
    norm_edge = np_norm2(edge[0],edge[1])
    N = np.empty((E.shape[0],1))
    val1 = np.empty((E.shape[0],1))
    val2 = np.empty((E.shape[0],1))

    for i in range(E.shape[0]):
        N[i] = np_norm2(E[i,0],E[i,1])
        val1[i] = np_norm2(edge[0],E[i,1]) + np_norm2(edge[1],E[i,0])
        val2[i] = np_norm2(edge[0],E[i,0]) + np_norm2(edge[1],E[i,1])

    #print(np.minimum(val1,val2))
    return np.minimum(val1,val2) - norm_edge - N

def np_listCoord(graph,id_cycle_A):
    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle;
    out : array avec indices dess points du cycle A
    """
    # print(id_cycle_A, liste_indice_depart)
    array_de_points, array_d_adjacence,array_indice_depart = graph
    res = np.empty((array_indice_depart[id_cycle_A,1]),dtype=int)
    act = array_indice_depart[id_cycle_A][0]
    for i in range(res.shape[0]):
        res[i] = act
        act = array_d_adjacence[act][0]
    return res

def np_equation_droite(edge):
    """
    Calcule l'équation de droite du segment donné en argument
    Equation de la forme : y = ax + b
    si droite verticale alors equation : x = c
    renvoie a,b,c avec inf sur les valeurs non utilisées
    """
    x1, x2 = edge[0,0], edge[1,0]
    y1, y2 = edge[0,1], edge[1,1]
    if x1 == x2:
        a, b, c = inf, inf, x1
    else:
        a = (y1 - y2) / (x1 - x2)
        b = y1 - a * x1
        c = inf
    return a, b, c

def np_intersection_segments(edge1, edge2):
    """
    Prends 2 segments, calcule leur équation paramétrique de segment
    puis vérifie que le point d'intersection des droites n'est pas sur les segments
    """
    a1, _, _ = np_equation_droite(edge1)
    a2, _, _ = np_equation_droite(edge2)
    if a1 == a2:
        """
        vérifie si les droites sont parallèles
        """
        return False

    x1, x2 = edge1[0,0], edge1[1,0]
    y1, y2 = edge1[0,1], edge1[1,1]
    x3, x4 = edge2[0,0], edge2[1,0]
    y3, y4 = edge2[0,1], edge2[1,1]
    """
    2 équations:
    m * x - n * y = k1
    p * x - q * y = k2
    """

    m, n = x2 - x1, x4 - x3
    p, q = y2 - y1, y4 - y3
    k1, k2 = x3 - x1, y3 - y1

    x = (k1 * (-q) - (-n) * k2) / (m * (-q) - (-n) * p)
    y = (m * k2 - k1 * p) / (m * (-q) - (-n) * p)

    if 0 <= x <= 1 and 0 <= y <= 1:
        return True
    return False

def np_nearestEdge4(graph, id_cycle_A,E):
    '''
    trouve les deux edges a stitcher, comment les stitcher et reversed
    out: equivalent a nearestCycle
    '''
    array_de_points, array_d_adjacence, array_indice_depart = graph
    cycle_A = np_listCoord(graph, id_cycle_A)
    E[cycle_A] = 1000
    #print(E)
    #print(cycle_A,cycle_A.shape)
    research_edge = np.empty((cycle_A.shape[0],2,2))
    energy_edgeB = np.empty((cycle_A.shape[0]))
    energy_id = np.empty((cycle_A.shape[0]),dtype=int)
    #print('energy_edgeB:',energy_edgeB)

    for i in cycle_A:
        edgeA = np.array([array_de_points[i],array_de_points[array_d_adjacence[i,0]]])
        #print('edgeA',edgeA)
        energy = vectorial_energy(edgeA,E)
        #print('nrj',energy)
        temp_edgeB_id = np.argmin(energy)
        #print('temp',temp_edgeB_id)
        if i >= cycle_A.shape[0]:
            #print(i-cycle_A.shape[0])
            research_edge[i-cycle_A.shape[0]] = edgeA
            energy_edgeB[i-cycle_A.shape[0]] = energy[temp_edgeB_id]
            energy_id[i-cycle_A.shape[0]] = temp_edgeB_id
        else:
            research_edge[i] = edgeA
            energy_edgeB[i] = energy[temp_edgeB_id]
            energy_id[i] = temp_edgeB_id

    #print(energy_edgeB)
    edgeB_id = energy_id[np.argmin(energy_edgeB)]
    #print(edgeB_id)
    edgeA, edgeB = research_edge[np.argmin(energy_edgeB)] , E[edgeB_id]

    reversed = True

    if np_norm2(edgeA[0], edgeB[1])+ np_norm2(edgeA[1], edgeB[0]) < np_norm2(edgeA[0], edgeB[0]) + np_norm2(edgeA[1], edgeB[1]):

        link = 'pattern_2'
        if not np_intersection_segments(np.array([edgeA[0],edgeB[1]]),np.array([edgeA[1],edgeB[0]])):
            reversed = False
    else:

        link = 'pattern1'
        if np_intersection_segments(np.array([edgeA[0],edgeB[0]]),np.array([edgeA[1],edgeB[1]])):
            print('d')
            reversed = False

    return reversed, np.array([np.argmin(energy_edgeB),array_d_adjacence[np.argmin(energy_edgeB),0]]), np.array([edgeB_id,array_d_adjacence[edgeB_id,0]]), link

def np_selectIdCycle(id_Point):
    '''
    trouver a quel cycle appartient le point
    '''
    global array_d_adjacence
    global array_indice_depart

    indice_cycle_actuel = 0
    for cycle in array_indice_depart:
        point_actuel = cycle[0]
        for i in range(cycle[1]):
            if array_d_adjacence[point_actuel,0] == id_Point:
                return indice_cycle_actuel
            point_actuel = array_d_adjacence[point_actuel,0]
        indice_cycle_actuel += 1
    return indice_cycle_actuel

def reverse_2(point):
    """
    Inverse la partie de la liste de points appartenant au cycle de point
    point : indice du point appartenant au cycle à inverser
    """
    #global liste_points
    global array_d_adjacence

    # print(array_d_adjacence)
    id_depart = point
    point_actuel = point
    prochain_point = array_d_adjacence[point_actuel][0]
    array_d_adjacence[point_actuel][0], array_d_adjacence[point_actuel][1] = array_d_adjacence[point_actuel][1], array_d_adjacence[point_actuel][0]

    while prochain_point != id_depart:
        point_actuel = prochain_point
        prochain_point = array_d_adjacence[point_actuel][0]
        array_d_adjacence[point_actuel][0], array_d_adjacence[point_actuel][1] = array_d_adjacence[point_actuel][1], array_d_adjacence[point_actuel][0]

def np_isPrecedent(idpoint_1, idpoint_2):
    """
    La fonction revoie True si le point_1 est le premier du segment
    point_1 est l'indice d'un point du cycle dans liste_points
    point_2 est l'indice d'un point du cycle dans liste_points
    """
    global array_d_adjacence
    return array_d_adjacence[idpoint_1,0] == idpoint_2


def np_isSuivant(idpoint_1, idpoint_2):
    """
    La fonction revoie True si le point_1 est le deuxième du segment
    point_1 est l'indice d'un point du cycle dans liste_points
    point_2 est l'indice d'un point du cycle dans liste_points
    """
    global array_d_adjacence
    return array_d_adjacence[idpoint_1,1] == point_2

def np_changeAdjacence_2(edge1_id,edge2_id,patch_pattern, array_d_adjacence):
    '''
    change la liste d'adjacence pour sticher
    '''
    global array_de_points
    #global array_d_adjacence
    """
    print(array_d_adjacence)
    print()
    print()
    print()
    print(patch_pattern)
    print(f"edge 1:\n point 1 id: {edge1_id[0]} / coord : {array_de_points[edge1_id[0]]} / adjacence id: {array_d_adjacence[edge1_id[0]]} / adjacence coord: {array_de_points[array_d_adjacence[edge1_id[0]][0]]}, {array_de_points[array_d_adjacence[edge1_id[0]][1]]}")
    print(f"edge 1:\n point 2 id: {edge1_id[1]} / coord : {array_de_points[edge1_id[1]]} / adjacence id: {array_d_adjacence[edge1_id[1]]} / adjacence coord: {array_de_points[array_d_adjacence[edge1_id[1]][0]]}, {array_de_points[array_d_adjacence[edge1_id[1]][1]]}")
    print(f"edge 2:\n point 1 id: {edge2_id[0]} / coord : {array_de_points[edge2_id[0]]} / adjacence id: {array_d_adjacence[edge2_id[0]]} / adjacence coord: {array_de_points[array_d_adjacence[edge2_id[0]][0]]}, {array_de_points[array_d_adjacence[edge2_id[0]][1]]}")
    print(f"edge 2:\n point 2 id: {edge2_id[1]} / coord : {array_de_points[edge2_id[1]]} / adjacence id: {array_d_adjacence[edge2_id[1]]} / adjacence coord: {array_de_points[array_d_adjacence[edge2_id[1]][0]]}, {array_de_points[array_d_adjacence[edge2_id[1]][1]]}")
    print()
    print()
    print()
    """

    if patch_pattern == 'pattern_2':
        if np_isPrecedent(edge1_id[0], edge1_id[1]):
            array_d_adjacence[edge1_id[0],0], array_d_adjacence[edge2_id[1],1] = edge2_id[1], edge1_id[0]

            array_d_adjacence[edge2_id[0],0], array_d_adjacence[edge1_id[1],1] = edge1_id[1], edge2_id[0]

        else:
            array_d_adjacence[edge1_id[0],1], array_d_adjacence[edge2_id[1],0] = edge2_id[1], edge1_id[0]

            array_d_adjacence[edge2_id[0],1], array_d_adjacence[edge1_id[1],0] = edge1_id[1], edge2_id[0]

    else:
        if np_isPrecedent(edge1_id[0], edge1_id[1]):
            array_d_adjacence[edge1_id[0],0], array_d_adjacence[edge2_id[0],1] = edge2_id[0], edge1_id[0]

            array_d_adjacence[edge2_id[1],0], array_d_adjacence[edge1_id[1],1] = edge1_id[1], edge2_id[1]

        else:
            array_d_adjacence[edge1_id[0],1], array_d_adjacence[edge2_id[0],0] = edge2_id[0], edge1_id[0]

            array_d_adjacence[edge2_id[1],1], array_d_adjacence[edge1_id[1],0] = edge1_id[1], edge2_id[1]

    """
    print(f"edge 1:\n point 1 id: {edge1_id[0]} / coord : {array_de_points[edge1_id[0]]} / adjacence id: {array_d_adjacence[edge1_id[0]]} / adjacence coord: {array_de_points[array_d_adjacence[edge1_id[0]][0]]}, {array_de_points[array_d_adjacence[edge1_id[0]][1]]}")
    print(f"edge 1:\n point 2 id: {edge1_id[1]} / coord : {array_de_points[edge1_id[1]]} / adjacence id: {array_d_adjacence[edge1_id[1]]} / adjacence coord: {array_de_points[array_d_adjacence[edge1_id[1]][0]]}, {array_de_points[array_d_adjacence[edge1_id[1]][1]]}")
    print(f"edge 2:\n point 1 id: {edge2_id[0]} / coord : {array_de_points[edge2_id[0]]} / adjacence id: {array_d_adjacence[edge2_id[0]]} / adjacence coord: {array_de_points[array_d_adjacence[edge2_id[0]][0]]}, {array_de_points[array_d_adjacence[edge2_id[0]][1]]}")
    print(f"edge 2:\n point 2 id: {edge2_id[1]} / coord : {array_de_points[edge2_id[1]]} / adjacence id: {array_d_adjacence[edge2_id[1]]} / adjacence coord: {array_de_points[array_d_adjacence[edge2_id[1]][0]]}, {array_de_points[array_d_adjacence[edge2_id[1]][1]]}")
    print()
    print()
    print()
    print(array_d_adjacence)
    """

    return array_d_adjacence

def np_merge_Cycles(id_Cycle_A,id_Cycle_B):
    """
    Fusionne 2 cycles dans la liste de cycles
    id_cycle_A/B sont les indices des cycles dans liste_indice_depart
    """
    #print('a')
    global  array_indice_depart
    #print('id_cA',id_Cycle_A)
    depart_cycle_A = array_indice_depart[id_Cycle_A,0]
    longueur_cycle_B = array_indice_depart[id_Cycle_B,1]
    array_indice_depart[id_Cycle_A,1] += longueur_cycle_B
    np.delete(array_indice_depart,id_Cycle_B,axis=0)
    return np_selectIdCycle(depart_cycle_A)

def stitchEdges_2(graph):
    '''
    Récupère la liste de coordonnées des deux cycles, ainsi que les deux edges à stitch.

    Recrée un objet de type path avec la liaison effectuée.
    '''
    global array_de_points
    global array_d_adjacence
    global array_indice_depart

    array_de_points, array_d_adjacence, array_indice_depart = graph

    id_cycle_depart = 0
    """
    print(liste_indice_depart, len(array_de_points))
    test = len(liste_indice_depart)
    print(array_de_points[82], array_de_points[83], array_de_points[100], array_de_points[101])
    print(norm2(array_de_points[82], array_de_points[83]), norm2(array_de_points[100], array_de_points[101]))
    print(norm2(array_de_points[82], array_de_points[100]), norm2(array_de_points[83], array_de_points[101]))
    print(norm2(array_de_points[82], array_de_points[101]), norm2(array_de_points[83], array_de_points[100]))
    """
    for i in tqdm(range(array_indice_depart.shape[0]-1)):
    #while array_indice_depart.shape[0] > 1:
        reversed, edge1_ids, edge2_ids, patch_pattern = np_nearestEdge4(graph, id_cycle_depart,edges(graph))

        cycle_A_id, cycle_B_id = np_selectIdCycle(edge1_ids[0]), np_selectIdCycle(edge2_ids[0])

        id_first_point = edge2_ids[0]

        if reversed:
            reverse_2(edge1_ids[0])
            patch_pattern = 'pattern_1'
        else:
            patch_pattern = 'pattern_2'
        #patch_pattern = selectCorrectPatchPattern_3(edge1_ids, edge2_ids)

        # si on met liste_adjacence en global pk la mettre en paramètre de la fonction ?
        array_d_adjacence = np_changeAdjacence_2(edge1_ids, edge2_ids, patch_pattern, array_d_adjacence)

        #print('id:',cycle_B_id)

        cycle_B_id = np_merge_Cycles(cycle_B_id, cycle_A_id)
        id_cycle_depart = cycle_B_id
        # ou on pred l'indice du cycle avec le - de points (+ complexe)

    # print(liste_indice_depart)


    first_stitch_id = array_d_adjacence[id_first_point,0]
    # print(id_first_point, liste_adjacence, first_stitch_id)
    lines = [0.]* array_de_points.shape[0]
    lines[0] = svgpt.Line(array_de_points[id_first_point], array_de_points[first_stitch_id])
    current_point_id = first_stitch_id
    next_point_id = array_d_adjacence[current_point_id,0]
    # print(lines[-1])

    for i in range(array_de_points.shape[0]):
        lines[i] = svgpt.Line(array_de_points[current_point_id], array_de_points[next_point_id])
        current_point_id = next_point_id
        next_point_id = array_d_adjacence[current_point_id,0]
        # print(lines[-1])

    print(lines)

    new_path = svgpt.Path(*lines)
    return new_path