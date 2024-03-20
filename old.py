from math import inf
import svg_handler as svgh
import numpy as np
import svgpathtools as svgpt
from tqdm import tqdm







# Fonctions non utilisées


def checkIfIntersecting(edge1, edge2):
    """solves the linear system verified by objects s and t.
    
    This linear system allows us to know if two edges under format (x1+y1j, x2+y2j) 
    intersect:
        
        if s >= 0 and t <= 1, they do. 

    Return True if so, else False.
    
    """
   
    x1, x2 = edge1[0].real, edge1[1].real
    y1, y2 = edge1[0].imag, edge1[1].imag
    x3, x4 = edge2[0].real, edge2[1].real
    y3, y4 = edge2[0].imag, edge2[1].imag

    membre_gauche = np.array([[x2 - x1, -x4 + x3], [y2 - y1, -y4 + y3]])
    membre_droit = np.array([x3 - x1, y3 - y1])
    s, t= np.linalg.solve(membre_gauche, membre_droit)

    if s >= 0 and t <= 1:
        return True
    return False

def selectCorrectPatchPattern(edge1, edge2):
    '''
    
    '''
    if checkIfIntersecting(edge1, edge2):
        return 'pattern_2'
    
    else:
        return 'pattern_1'
    
 
def changeAdjacence(edge1_id,edge2_id,patch_pattern, liste_d_adjacence):
    '''
    change la liste d'adjacence pour sticher
    '''
    global liste_points
    global liste_adjacence
    """
    print(liste_adjacence)
    print()
    print()
    print()
    print(patch_pattern)
    print(f"edge 1:\n point 1 id: {edge1_id[0]} / coord : {liste_points[edge1_id[0]]} / adjacence id: {liste_adjacence[edge1_id[0]]} / adjacence coord: {liste_points[liste_adjacence[edge1_id[0]][0]]}, {liste_points[liste_adjacence[edge1_id[0]][1]]}")
    print(f"edge 1:\n point 2 id: {edge1_id[1]} / coord : {liste_points[edge1_id[1]]} / adjacence id: {liste_adjacence[edge1_id[1]]} / adjacence coord: {liste_points[liste_adjacence[edge1_id[1]][0]]}, {liste_points[liste_adjacence[edge1_id[1]][1]]}")
    print(f"edge 2:\n point 1 id: {edge2_id[0]} / coord : {liste_points[edge2_id[0]]} / adjacence id: {liste_adjacence[edge2_id[0]]} / adjacence coord: {liste_points[liste_adjacence[edge2_id[0]][0]]}, {liste_points[liste_adjacence[edge2_id[0]][1]]}")
    print(f"edge 2:\n point 2 id: {edge2_id[1]} / coord : {liste_points[edge2_id[1]]} / adjacence id: {liste_adjacence[edge2_id[1]]} / adjacence coord: {liste_points[liste_adjacence[edge2_id[1]][0]]}, {liste_points[liste_adjacence[edge2_id[1]][1]]}")
    print()
    print()
    print()
    """

    if patch_pattern == 'pattern_2':    #Comment on sait le sens des 2 formes ?
        liste_d_adjacence[edge1_id[0]][0], liste_d_adjacence[edge1_id[1]][1] = edge2_id[1], edge2_id[0]

        liste_d_adjacence[edge2_id[0]][0], liste_d_adjacence[edge2_id[1]][1] = edge1_id[1], edge1_id[0]
    else:
        liste_d_adjacence[edge1_id[0]][0], liste_d_adjacence[edge1_id[1]][1] = edge2_id[0], edge2_id[1]

        liste_d_adjacence[edge2_id[0]][0], liste_d_adjacence[edge2_id[1]][1] = edge1_id[0], edge1_id[1] 
    
    """
    print(f"edge 1:\n point 1 id: {edge1_id[0]} / coord : {liste_points[edge1_id[0]]} / adjacence id: {liste_adjacence[edge1_id[0]]} / adjacence coord: {liste_points[liste_adjacence[edge1_id[0]][0]]}, {liste_points[liste_adjacence[edge1_id[0]][1]]}")
    print(f"edge 1:\n point 2 id: {edge1_id[1]} / coord : {liste_points[edge1_id[1]]} / adjacence id: {liste_adjacence[edge1_id[1]]} / adjacence coord: {liste_points[liste_adjacence[edge1_id[1]][0]]}, {liste_points[liste_adjacence[edge1_id[1]][1]]}")
    print(f"edge 2:\n point 1 id: {edge2_id[0]} / coord : {liste_points[edge2_id[0]]} / adjacence id: {liste_adjacence[edge2_id[0]]} / adjacence coord: {liste_points[liste_adjacence[edge2_id[0]][0]]}, {liste_points[liste_adjacence[edge2_id[0]][1]]}")
    print(f"edge 2:\n point 2 id: {edge2_id[1]} / coord : {liste_points[edge2_id[1]]} / adjacence id: {liste_adjacence[edge2_id[1]]} / adjacence coord: {liste_points[liste_adjacence[edge2_id[1]][0]]}, {liste_points[liste_adjacence[edge2_id[1]][1]]}")
    print()
    print()
    print()
    print(liste_adjacence)
    """
        
    return liste_d_adjacence

def stitchEdges(graph):
    '''
    Récupère la liste de coordonnées des deux cycles, ainsi que les deux edges à stitch. 

    Recrée un objet de type path avec la liaison effectuée.
    '''
    liste_de_point,liste_d_adjacence,liste_indice_depart = graph
    edge1_ids, edge2_ids = nearestCycle(graph, 0)[1:]
    id_first_point = edge2_ids[0]
    patch_pattern = selectCorrectPatchPattern([liste_de_point[edge1_ids[0]], liste_de_point[edge2_ids[0]]],
                                              [liste_de_point[edge1_ids[1]], liste_de_point[edge2_ids[1]]])


    liste_d_adjacence = changeAdjacence(edge1_ids, edge2_ids, patch_pattern, liste_d_adjacence)
    # print(liste_d_adjacence)
    
    if patch_pattern == 'pattern_1':
        id_stitch_point = edge1_ids[1]
    else:
        id_stitch_point = edge1_ids[0]
    """
    patching_order = [id_first_point]
    i = 0
    while patching_order[-1] != edge2_ids[1]:
        res = liste_d_adjacence[patching_order[i]][0]
        i += 1
        patching_order.append(res)
        print(f'each {patching_order}')
    """
    first_stitch_id = liste_d_adjacence[id_first_point][0]
    lines = [svgpt.Line(liste_de_point[id_first_point], liste_de_point[first_stitch_id])]
    current_point_id = first_stitch_id
    next_point_id = liste_d_adjacence[current_point_id][0]

    for i in range(len(liste_de_point)): 
        lines.append(svgpt.Line(liste_de_point[current_point_id], liste_de_point[next_point_id]))
        current_point_id = next_point_id
        next_point_id = liste_d_adjacence[current_point_id][0]
        
    #print(lines)
    new_path = svgpt.Path(*lines)
    return new_path


def reverse(point):
    """
    Inverse la partie de la liste de points appartenant au cycle de point
    point : indice du point appartenant au cycle à inverser
    """
    global liste_points
    global liste_indice_depart
    
    # print(liste_points)
    id_cycle = selectIdCycle(point)
    depart = liste_indice_depart[id_cycle][0]
    longueur_cycle = liste_indice_depart[id_cycle][1]
    liste_cycle = liste_points[depart:depart + longueur_cycle]
    liste_cycle = liste_cycle[::-1].copy()
    liste_points[depart:depart+longueur_cycle] = liste_cycle
    print()
    # print(liste_points)


def selectCorrectPatchPattern_2(edge1, edge2):
    """
    vérifie que le sens actuel des 2 formes est correct pour un stitch
    edge1 est la liste des indices des sommets du segment 1 dans la liste de point de graph
    edge2 est la liste des indices des sommets du segment 2 dans la liste de point de graph
    """
    global liste_points
    global liste_adjacence
    global liste_indice_depart
    """
    print(f"edge1 : point 1 {edge1[0]} / {liste_adjacence[edge1[0]]}, point 2 {edge1[1]} / {liste_adjacence[edge1[1]]}")
    print(f"edge2 : point 1 {edge2[0]} / {liste_adjacence[edge2[0]]}, point 2 {edge2[1]} /{liste_adjacence[edge2[1]]}")
    """

    if norm2(liste_points[edge1[0]], liste_points[edge2[0]]) < norm2(liste_points[edge1[0]], liste_points[edge2[1]]):
        if isPrecedent(edge1[0], edge1[1]) == isPrecedent(edge2[0], edge2[1]):
            if liste_indice_depart[selectIdCycle(edge2[0])][1] < liste_indice_depart[selectIdCycle(edge2[0])][1]:
                reverse_2(edge2[0])
            else:
                reverse_2(edge1[0])
        return 'pattern_1'
    else:
        if isPrecedent(edge1[0], edge1[1]) == isPrecedent(edge2[1], edge2[0]):
            if liste_indice_depart[selectIdCycle(edge2[0])][1] < liste_indice_depart[selectIdCycle(edge2[0])][1]:
                reverse_2(edge2[0])
            else:
                reverse_2(edge1[0])
        return 'pattern_2'
    
def nearestCycle_old(graph, id_cycle_A):
    
    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle dont on cherche le voisin le + proche;
    """
    liste_de_point, liste_d_adjacence, liste_indice_depart = graph
    liste_dist = []
    liste_edges = []
    cycle_A = listCoord(graph, id_cycle_A)

    for id_cycle_B in range(len(liste_indice_depart)):

        min_energy_cycle = inf

        if id_cycle_B != id_cycle_A:

            cycle_B = listCoord(graph, id_cycle_B)
            edge_A, edge_B = None, None
            
            for coord in range(len(cycle_B)):

                temp = nearestEdge2(cycle_B,[cycle_B[coord-1],cycle_B[coord]],cycle_A)

                if temp[2] < min_energy_cycle:

                    edge_A, edge_B, min_energy_cycle = temp

            liste_dist.append(min_energy_cycle)
            indice_A1, indice_A2 = liste_de_point.index(edge_A[0]), liste_de_point.index(edge_A[1])
            indice_B1, indice_B2 = liste_de_point.index(edge_B[0]), liste_de_point.index(edge_B[1])
            liste_edges.append([[indice_A1,indice_A2],[indice_B1,indice_B2]])

        else:

            liste_dist.append(min_energy_cycle)
            liste_edges.append([None,None])

    minId = liste_dist.index(min(liste_dist))
    return liste_dist[minId], *liste_edges[minId]
