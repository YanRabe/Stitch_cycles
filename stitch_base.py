from math import inf
import svg_handler as svgh
import numpy as np
import svgpathtools as svgpt
"""
Cycles --> liste: 
    -coord points 
    -ind points suiv - préc
    -ind point de départ + nb de points par cycle
"""
def energyid_cycle_Alc(edge1, edge2):
    """
    Prend en entrée deux lignes (type liste) 

    et renvoie l'énergie de 'patch' selon la formule pg 8.
    """
    res = min(norm2(edge1[0], edge2[1])+ norm2(edge1[1], edge2[0]), 
              norm2(edge1[0], edge2[0]) + norm2(edge1[1], edge2[1])) 
    
    res -= norm2(edge1[0], edge1[1]) - norm2(edge2[0], edge2[1])
    
    return res

def norm2(point_a, point_b):
    """
    Prend deux points complexes en entrée

    id_cycle_Calcule la différence

    Renvoie la distance avec la norme euclidienne.
    """
    difference = (point_a.real - point_b.real, point_a.imag - point_b.imag) #différence des points a et b
    res = np.sqrt(difference[0]**2+difference[1]**2) #distance entre a et b (norme 2)
    return res
    
def listCoord(graph,id_cycle_A):
    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle;
    """
    liste_points, liste_adjacence, liste_indice_depart = graph
    res = []
    act = liste_indice_depart[id_cycle_A][0]
    for i in range(liste_indice_depart[id_cycle_A][1]):
        res.append(liste_points[act])
        act = liste_adjacence[act][0]
    return res


def nearestCycle(graph, id_cycle_A):
    
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

def nearestEdge2(id_cycle_A, edge_A, id_cycle_B, expected = None):
    """
    edge_A = liste de 2 complexes (coords);
    id_cycle_A = liste des coords du cycle A;
    id_cycle_B = liste des coords du cycle B;
    expected = les coordonnées du plus proche trouvé avant chez B;
    """
    
    choix_B = [id_cycle_B[-1],id_cycle_B[0]]
    min_energy = energyid_cycle_Alc(edge_A,choix_B)
    for sommet in range(len(id_cycle_B)-1):
        temp = energyid_cycle_Alc(edge_A,[id_cycle_B[sommet],id_cycle_B[sommet+1]])
        if temp < min_energy:
            min_energy = temp
            choix_B = [id_cycle_B[sommet],id_cycle_B[sommet+1]]
    
    if choix_B == expected:
        return edge_A, choix_B, min_energy
    return nearestEdge2(id_cycle_B, choix_B, id_cycle_A, edge_A)

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

    # patching_order = [id_first_point]
    # i = 0
    # while patching_order[-1] != edge2_ids[1]:
    #     res = liste_d_adjacence[patching_order[i]][0]
    #     i += 1
    #     patching_order.append(res)
    #     print(f'each {patching_order}')
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

def isPrecedent(point_1, point_2):
    """
    La fonction revoie True si le point_1 est le premier du segment
    point_1 est l'indice d'un point du cycle dans liste_points
    point_2 est l'indice d'un point du cycle dans liste_points
    """
    global liste_adjacence
    return liste_adjacence[point_1][0] == point_2


def isSuivant(point_1, point_2):
    """
    La fonction revoie True si le point_1 est le deuxième du segment
    point_1 est l'indice d'un point du cycle dans liste_points
    point_2 est l'indice d'un point du cycle dans liste_points
    """
    global liste_adjacence
    return liste_adjacence[point_1][1] == point_2

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


def reverse_2(point):
    """
    Inverse la partie de la liste de points appartenant au cycle de point
    point : indice du point appartenant au cycle à inverser
    """
    global liste_points
    global liste_adjacence
    
    # print(liste_adjacence)
    id_depart = point
    point_actuel = point
    prochain_point = liste_adjacence[point_actuel][0]
    liste_adjacence[point_actuel][0], liste_adjacence[point_actuel][1] = liste_adjacence[point_actuel][1], liste_adjacence[point_actuel][0]
    
    while prochain_point != id_depart:
        point_actuel = prochain_point
        prochain_point = liste_adjacence[point_actuel][0]
        liste_adjacence[point_actuel][0], liste_adjacence[point_actuel][1] = liste_adjacence[point_actuel][1], liste_adjacence[point_actuel][0]

    # print(liste_adjacence)


def selectCorrectPatchPattern_2(edge1, edge2):
    """
    vérifie que le sens actuel des 2 formes est correct pour un stitch
    edge1 est la liste des indices des sommets du segment 1 dans la liste de point de graph
    edge2 est la liste des indices des sommets du segment 2 dans la liste de point de graph
    """
    global liste_points
    global liste_adjacence
    """
    print(f"edge1 : point 1 {edge1[0]} / {liste_adjacence[edge1[0]]}, point 2 {edge1[1]} / {liste_adjacence[edge1[1]]}")
    print(f"edge2 : point 1 {edge2[0]} / {liste_adjacence[edge2[0]]}, point 2 {edge2[1]} /{liste_adjacence[edge2[1]]}")
    """

    if norm2(liste_points[edge1[0]], liste_points[edge2[0]]) < norm2(liste_points[edge1[0]], liste_points[edge2[1]]):
        # print("a")
        if isPrecedent(edge1[0], edge1[1]) == isPrecedent(edge2[0], edge2[1]):
            reverse_2(edge2[0])
        return 'pattern_1'
    else:
        # print("b")
        if isPrecedent(edge1[0], edge1[1]) == isPrecedent(edge2[1], edge2[0]):
            reverse_2(edge2[0])
        return 'pattern_2'
    
def selectIdCycle(id_Point):
    
    global liste_indice_depart

    indice_cycle_actuel = 0
    depart, longueur_cycle = liste_indice_depart[indice_cycle_actuel][0], liste_indice_depart[indice_cycle_actuel][1]
    while id_Point >= depart + longueur_cycle:
        indice_cycle_actuel += 1
        depart, longueur_cycle = liste_indice_depart[indice_cycle_actuel][0], liste_indice_depart[indice_cycle_actuel][1]
    return indice_cycle_actuel


def stitchEdges_2(graph):
    '''
    Récupère la liste de coordonnées des deux cycles, ainsi que les deux edges à stitch. 

    Recrée un objet de type path avec la liaison effectuée.
    '''
    global liste_points
    global liste_adjacence
    global liste_indice_depart
    liste_points, liste_adjacence, liste_indice_depart = graph

    edge1_ids, edge2_ids = nearestCycle(graph, 0)[1:]
    id_first_point = edge2_ids[0]
    patch_pattern = selectCorrectPatchPattern_2(edge1_ids, edge2_ids)

    # si on met liste_adjacence en global pk la mettre en paramètre de la fonction ?
    liste_adjacence = changeAdjacence_2(edge1_ids, edge2_ids, patch_pattern, liste_adjacence)
    # print(liste_d_adjacence)
    
    first_stitch_id = liste_adjacence[id_first_point][0]
    # print(id_first_point, liste_adjacence, first_stitch_id)
    lines = [svgpt.Line(liste_points[id_first_point], liste_points[first_stitch_id])]
    current_point_id = first_stitch_id
    next_point_id = liste_adjacence[current_point_id][0]
    # print(lines[-1])

    for i in range(liste_indice_depart[selectIdCycle(edge1_ids[0])][1] + liste_indice_depart[selectIdCycle(edge2_ids[0])][1]):
        lines.append(svgpt.Line(liste_points[current_point_id], liste_points[next_point_id]))
        current_point_id = next_point_id
        next_point_id = liste_adjacence[current_point_id][0]
        # print(lines[-1])
        
    # print(lines)
    new_path = svgpt.Path(*lines)
    return new_path

def changeAdjacence_2(edge1_id,edge2_id,patch_pattern, liste_d_adjacence):
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
        if isPrecedent(edge1_id[0], edge1_id[1]):
            liste_adjacence[edge1_id[0]][0], liste_adjacence[edge2_id[1]][1] = edge2_id[1], edge1_id[0]

            liste_adjacence[edge2_id[0]][0], liste_adjacence[edge1_id[1]][1] = edge1_id[1], edge2_id[0]
        
        else:
            liste_adjacence[edge1_id[0]][1], liste_adjacence[edge2_id[1]][0] = edge2_id[1], edge1_id[0]

            liste_adjacence[edge2_id[0]][1], liste_adjacence[edge1_id[1]][0] = edge1_id[1], edge2_id[0]

    else:
        if isPrecedent(edge1_id[0], edge1_id[1]):
            liste_adjacence[edge1_id[0]][0], liste_adjacence[edge2_id[0]][1] = edge2_id[0], edge1_id[0]

            liste_adjacence[edge2_id[1]][0], liste_adjacence[edge1_id[1]][1] = edge1_id[1], edge2_id[1]
        
        else:
            liste_adjacence[edge1_id[0]][1], liste_adjacence[edge2_id[0]][0] = edge2_id[0], edge1_id[0]

            liste_adjacence[edge2_id[1]][1], liste_adjacence[edge1_id[1]][0] = edge1_id[1], edge2_id[1]
            
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