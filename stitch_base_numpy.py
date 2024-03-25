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
    """
    # print(id_cycle_A, liste_indice_depart)
    array_de_point, array_d_adjacence,array_indice_depart = graph
    res = np.empty((array_indice_depart[id_cycle_A,1]),dtype=int)
    act = array_indice_depart[id_cycle_A][0]
    for i in range(res.shape[0]):
        res[i] = act
        act = array_d_adjacence[act][0]
    return res

def edges(graph):
    '''
    out: array (n,2,2), n le nombre d'edges dans le graphe
    '''
    array_de_point, array_d_adjacence, array_indice_depart = graph
    E = np.empty((array_de_point.shape[0],2,2))
    for i in range(array_d_adjacence.shape[0]):
        E[i,0] = array_de_point[i]
        E[i,1] = array_de_point[array_d_adjacence[i,0]]
    return E

def np_nearestEdge4(graph, id_cycle_A,E):
    '''
    trouve les deux edges a stitcher
    '''
    array_de_point, array_d_adjacence, array_indice_depart = graph
    cycle_A = np_listCoord(graph, id_cycle_A)
    print(cycle_A,cycle_A.shape)
    research_edge = np.empty((cycle_A.shape[0],2,2))
    energy_edgeB = np.empty_like(cycle_A)
    #print('energy_edgeB:',energy_edgeB)

    for i in cycle_A:
        edgeA = np.array([array_de_point[i],array_de_point[array_d_adjacence[i,0]]])
        #print('edgeA',edgeA)
        energy = vectorial_energy(edgeA,np.delete(E,cycle_A,0))
        #print('nrj',energy)
        temp_edgeB_id = np.argmin(energy)
        #print('temp',temp_edgeB_id)
        research_edge[i] = edgeA
        energy_edgeB[i] = energy[temp_edgeB_id]

    edgeB_id = np.argmin(energy_edgeB)

    return research_edge[edgeB_id], E[edgeB_id + cycle_A.shape[0]]

# def stitchEdges_2(graph):
#     '''
#     Récupère la liste de coordonnées des deux cycles, ainsi que les deux edges à stitch.
#
#     Recrée un objet de type path avec la liaison effectuée.
#     '''
#     global array_de_point
#     global array_d_adjacence
#     global array_indice_depart
#
#     array_de_point, array_d_adjacence, array_indice_depart = graph
#
#     '''trouver le premier cycle a stitch'''
#     #necessaire??
#
#     # min_cycle = array_indice_depart[0]
#     # for cycle in array_indice_depart:
#     #     if cycle[1] <= min_cycle[1]:
#     #         min_cycle = cycle
#     # id_cycle_depart = liste_indice_depart.index(min_cycle)
#     """
#     print(liste_indice_depart, len(array_de_point))
#     test = len(liste_indice_depart)
#     print(array_de_point[82], array_de_point[83], array_de_point[100], array_de_point[101])
#     print(norm2(array_de_point[82], array_de_point[83]), norm2(array_de_point[100], array_de_point[101]))
#     print(norm2(array_de_point[82], array_de_point[100]), norm2(array_de_point[83], array_de_point[101]))
#     print(norm2(array_de_point[82], array_de_point[101]), norm2(array_de_point[83], array_de_point[100]))
#     """
#     #for i in tqdm(range(array_indice_depart.shape[0]-1)):
#     #while len(liste_indice_depart) > 1:
#         reversed, edge1_ids, edge2_ids = nearestCycle(graph, id_cycle_depart)
#
#         cycle_A_id, cycle_B_id = selectIdCycle(edge1_ids[0]), selectIdCycle(edge2_ids[0])
#
#         id_first_point = edge2_ids[0]
#
#         if reversed:
#             reverse_2(edge1_ids[0])
#             patch_pattern = 'pattern_1'
#         else:
#             patch_pattern = 'pattern_2'
#         #patch_pattern = selectCorrectPatchPattern_3(edge1_ids, edge2_ids)
#
#         # si on met liste_adjacence en global pk la mettre en paramètre de la fonction ?
#         liste_adjacence = changeAdjacence_2(edge1_ids, edge2_ids, patch_pattern, liste_adjacence)
#
#         cycle_B_id = merge_Cycles(cycle_B_id, cycle_A_id)
#         id_cycle_depart = cycle_B_id
#         # ou on pred l'indice du cycle avec le - de points (+ complexe)
#
#     # print(liste_indice_depart)
#
#
#     first_stitch_id = liste_adjacence[id_first_point][0]
#     # print(id_first_point, liste_adjacence, first_stitch_id)
#     lines = [0.] *(len(liste_points))
#     lines[0] = svgpt.Line(liste_points[id_first_point], liste_points[first_stitch_id])
#     current_point_id = first_stitch_id
#     next_point_id = liste_adjacence[current_point_id][0]
#     # print(lines[-1])
#
#     for i in range(len(liste_points)):
#         lines[i] = svgpt.Line(liste_points[current_point_id], liste_points[next_point_id])
#         current_point_id = next_point_id
#         next_point_id = liste_adjacence[current_point_id][0]
#         # print(lines[-1])
#
#     print(lines)
#
#     new_path = svgpt.Path(*lines)
#     return new_path