from math import inf
import svgpathtools as svgpt
from tqdm import tqdm

"""
Cycles --> liste:
    -coord points
    -ind points suiv - préc
    -ind point de départ + nb de points par cycle
"""
def energyid_cycle_Calc(edge1, edge2):
    """
    Prend en entrée deux lignes (type liste)

    et renvoie l'énergie de 'patch' selon la formule pg 8.
    """
    res = min(norm2(edge1[0], edge2[1])+ norm2(edge1[1], edge2[0]),
              norm2(edge1[0], edge2[0]) + norm2(edge1[1], edge2[1]))

    res -= norm2(edge1[0], edge1[1]) - norm2(edge2[0], edge2[1])

    return res

def calcul_energie_2(edge1, edge2):
    """
    Prend en entrée deux lignes (type liste)

    et renvoie l'énergie de 'patch' selon la formule pg 8.
    """

    global liste_points

    val1 = norm2(liste_points[edge1[0]], liste_points[edge2[1]]) + norm2(liste_points[edge1[1]], liste_points[edge2[0]])
    val2 = norm2(liste_points[edge1[0]], liste_points[edge2[0]]) + norm2(liste_points[edge1[1]], liste_points[edge2[1]])

    if val1 < val2:
        res = val1
        # [[0,1], [1,0]]
        link = 'pattern_2'
        if not intersection_segments([edge1[0], edge2[1]], [edge1[1], edge2[0]]):
            reverse = False
        else:
            reverse = True
    else:
        res = val2
        # [[0,0], [1,1]]
        link = 'pattern_1'
        if not intersection_segments([edge1[0], edge2[0]], [edge1[1], edge2[1]]):
            reverse = True

    res = res - norm2(liste_points[edge1[0]], liste_points[edge1[1]]) - norm2(liste_points[edge2[0]], liste_points[edge2[1]])
    return res, reverse, link

def norm2(point_a, point_b):
    """
    Prend deux points complexes en entrée

    id_cycle_Calcule la différence

    Renvoie la distance avec la norme euclidienne.
    """
    difference = (point_a.real - point_b.real, point_a.imag - point_b.imag) #différence des points a et b
    res = (difference[0]**2+difference[1]**2)**0.5 #distance entre a et b (norme 2)
    return res

def listCoord(id_cycle_A):
    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle;
    """
    global liste_adjacence
    global liste_indice_depart
    # liste_points, liste_adjacence, liste_indice_depart = graph
    res = [0.] * liste_indice_depart[id_cycle_A][1]
    act = liste_indice_depart[id_cycle_A][0]
    for i in range(liste_indice_depart[id_cycle_A][1]):
        res[i] = act
        act = liste_adjacence[act][0]
    return res


def nearestCycle(id_cycle_A):

    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle dont on cherche le voisin le + proche;
    """

    global liste_indice_depart


    cycle_A = listCoord(id_cycle_A)
    min_energy_cycle = inf
    edge_A, edge_B = None, None
    reversed = None

    for id_cycle_B in range(len(liste_indice_depart)):


        if id_cycle_B != id_cycle_A:

            cycle_B = listCoord(id_cycle_B)

            temp = nearestEdge4(cycle_A, cycle_B)

            if temp[2] < min_energy_cycle:

                min_energy_cycle = temp[2]
                edge_A = [temp[0][0], temp[0][1]]
                edge_B = [temp[1][0], temp[1][1]]
                reversed = temp[3]
                patch_pattern = temp[4]

    return reversed, edge_A, edge_B, patch_pattern#, min_energy_cycle

def nearestCycle_2(graph, id_cycle_A):

    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    id_cycle_A est l'indice du cycle dont on cherche le voisin le + proche;
    """
    liste_de_point, liste_adjacence, liste_indice_depart = graph

    cycle_A = listCoord(graph, id_cycle_A)
    min_energy_cycle = inf
    edge_A, edge_B = None, None
    reversed = None

    for id_point_A in cycle_A:
        edge_A_test = [id_point_A, liste_adjacence[id_point_A][0]]

        for id_point_B in range(len(liste_de_point)):
            #id_cycle_B = selectIdCycle(id_point_B)

            if id_point_B not in cycle_A:
                edge_B_test = [id_point_B, liste_adjacence[id_point_B][0]]
                temp = calcul_energie_2(edge_A_test, edge_B_test)
                if temp[0] <= min_energy_cycle:
                    min_energy_cycle = temp[0]
                    edge_A = edge_A_test
                    edge_B = edge_B_test
                    reversed = temp[1]
                    patch_pattern = temp[2]

    return reversed, edge_A, edge_B, patch_pattern

def nearestEdge2(id_cycle_A, edge_A, id_cycle_B, expected = None):
    """
    edge_A = liste de 2 complexes (coords);
    id_cycle_A = liste des coords du cycle A;
    id_cycle_B = liste des coords du cycle B;
    expected = les coordonnées du plus proche trouvé avant chez B;
    """

    choix_B = [id_cycle_B[-1],id_cycle_B[0]]
    min_energy = energyid_cycle_Calc(edge_A,choix_B)
    for sommet in range(len(id_cycle_B)-1):
        temp = energyid_cycle_Calc(edge_A,[id_cycle_B[sommet],id_cycle_B[sommet+1]])
        if temp < min_energy:
            min_energy = temp
            choix_B = [id_cycle_B[sommet],id_cycle_B[sommet+1]]

    if choix_B == expected:
        return edge_A, choix_B, min_energy
    return nearestEdge2(id_cycle_B, choix_B, id_cycle_A, edge_A)

def nearestEdge3(cycle_A, cycle_B):
    """
    renvoie les deux edges les + proches entre cycle A et cycle B
    """

    edge_A, edge_B = [cycle_A[-1], cycle_A[0]], [cycle_B[-1], cycle_B[0]]
    min_energy = energyid_cycle_Calc(edge_A, edge_B)

    for id_point_A in range(len(cycle_A)-1):
        for id_point_B in range((len(cycle_B))-1):
            temp = energyid_cycle_Calc([cycle_A[id_point_A], cycle_A[id_point_A + 1]], [cycle_B[id_point_B], cycle_B[id_point_B + 1]])
            if temp < min_energy:
                min_energy = temp
                edge_A, edge_B = [cycle_A[id_point_A], cycle_A[id_point_A + 1]], [cycle_B[id_point_B], cycle_B[id_point_B + 1]]

    return edge_A, edge_B, min_energy


def nearestEdge4(cycle_A, cycle_B):
    """
    renvoie les deux edges les + proches entre cycle A et cycle B
    """

    global liste_adjacence

    edge_A, edge_B = [cycle_A[-1], cycle_A[0]], [cycle_B[-1], cycle_B[0]]
    min_energy, reversed, patch_pattern = calcul_energie_2(edge_A, edge_B)

    for id_point_A in range(len(cycle_A)):
        for id_point_B in range((len(cycle_B))):
            point_A = cycle_A[id_point_A - 1]
            point_B = cycle_B[id_point_B - 1]
            temp = calcul_energie_2([point_A, liste_adjacence[point_A][0]], [point_B, liste_adjacence[point_B][0]])
            if temp[0] < min_energy:
                min_energy = temp[0]
                reversed = temp[1]
                patch_pattern = temp[2]
                edge_A, edge_B = [point_A, liste_adjacence[point_A][0]], [point_B, liste_adjacence[point_B][0]]

    return edge_A, edge_B, min_energy, reversed, patch_pattern


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

def reverse_2(point):
    """
    Inverse la partie de la liste de points appartenant au cycle de point
    point : indice du point appartenant au cycle à inverser
    """
    global liste_points
    global liste_adjacence

    id_depart = point
    point_actuel = point
    prochain_point = liste_adjacence[point_actuel][0]
    liste_adjacence[point_actuel][0], liste_adjacence[point_actuel][1] = liste_adjacence[point_actuel][1], liste_adjacence[point_actuel][0]

    while prochain_point != id_depart:
        point_actuel = prochain_point
        prochain_point = liste_adjacence[point_actuel][0]
        liste_adjacence[point_actuel][0], liste_adjacence[point_actuel][1] = liste_adjacence[point_actuel][1], liste_adjacence[point_actuel][0]



def selectCorrectPatchPattern_3(edge1, edge2):
    """
    vérifie que le sens actuel des 2 formes est correct pour un stitch
    edge1 est la liste des indices des sommets du segment 1 dans la liste de point de graph
    edge2 est la liste des indices des sommets du segment 2 dans la liste de point de graph
    """
    global liste_points
    global liste_adjacence
    global liste_indice_depart


    if not intersection_segments([liste_points[edge1[0]], liste_points[edge2[0]]], [liste_points[edge1[1]], liste_points[edge2[1]]]):
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



def selectIdCycle(id_Point):
    '''
    trouver a quel cycle appartient le point
    '''
    global liste_adjacence
    global liste_indice_depart

    indice_cycle_actuel = 0
    for cycle in liste_indice_depart:
        point_actuel = cycle[0]
        for i in range(cycle[1]):
            if liste_adjacence[point_actuel][0] == id_Point:
                return indice_cycle_actuel
            point_actuel = liste_adjacence[point_actuel][0]
        indice_cycle_actuel += 1
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

    """trouver le premier cycle a stitch"""
    min_cycle = liste_indice_depart[0]
    for cycle in liste_indice_depart:
        if cycle[1] <= min_cycle[1]:
            min_cycle = cycle
    id_cycle_depart = liste_indice_depart.index(min_cycle)


    for i in tqdm(range(len(liste_indice_depart)-1)):
    #while len(liste_indice_depart) > 1:
        reversed, edge1_ids, edge2_ids, patch_pattern = nearestCycle(id_cycle_depart)

        cycle_A_id, cycle_B_id = id_cycle_depart, selectIdCycle(edge2_ids[0])

        id_first_point = edge2_ids[0]

        if reversed:
            reverse_2(edge2_ids[0])

        # liste_adjacence = changeAdjacence_2(edge1_ids, edge2_ids, patch_pattern, liste_adjacence)
        changeAdjacence_2(edge1_ids, edge2_ids, patch_pattern)

        id_cycle_depart = merge_Cycles(cycle_B_id, cycle_A_id)


    first_stitch_id = liste_adjacence[id_first_point][0]
    lines = [0.] * (len(liste_points))
    lines[0] = svgpt.Line(liste_points[id_first_point], liste_points[first_stitch_id])
    current_point_id = first_stitch_id
    next_point_id = liste_adjacence[current_point_id][0]

    for i in range(len(liste_points)):
        lines[i] = svgpt.Line(liste_points[current_point_id], liste_points[next_point_id])
        current_point_id = next_point_id
        next_point_id = liste_adjacence[current_point_id][0]

    new_path = svgpt.Path(*lines)
    return new_path

def changeAdjacence_2(edge1_id,edge2_id,patch_pattern):
    '''
    change la liste d'adjacence pour sticher
    '''
    global liste_points
    global liste_adjacence

    if patch_pattern == 'pattern_2':
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


def merge_Cycles(id_Cycle_A,id_Cycle_B):
    """
    Fusionne 2 cycles dans la liste de cycles
    id_cycle_A/B sont les indices des cycles dans liste_indice_depart
    """

    global  liste_indice_depart

    depart_cycle_A = liste_indice_depart[id_Cycle_A][0]
    longueur_cycle_B = liste_indice_depart[id_Cycle_B][1]
    liste_indice_depart[id_Cycle_A][1] += longueur_cycle_B
    del(liste_indice_depart[id_Cycle_B])
    return selectIdCycle(depart_cycle_A)



def equation_droite(edge):
    """
    Calcule l'équation de droite du segment donné en argument
    Equation de la forme : y = ax + b
    si droite verticale alors equation : x = c
    renvoie a,b,c avec inf sur les valeurs non utilisées
    """
    x1, x2 = edge[0].real, edge[1].real
    y1, y2 = edge[0].imag, edge[1].imag
    if x1 == x2:
        a, b, c = inf, inf, x1
    else:
        a = (y1 - y2) / (x1 - x2)
        b = y1 - a * x1
        c = inf
    return a, b, c



def intersection_segments(edge1, edge2):
    """
    Prends 2 segments, calcule leur équation paramétrique de segment
    puis vérifie que le point d'intersection des droites n'est pas sur les segments
    """
    a1, _, _ = equation_droite(edge1)
    a2, _, _ = equation_droite(edge2)
    if a1 == a2:
        """
        vérifie si les droites sont parallèles
        """
        return False
    x1, x2 = edge1[0].real, edge1[1].real
    y1, y2 = edge1[0].imag, edge1[1].imag
    x3, x4 = edge2[0].real, edge2[1].real
    y3, y4 = edge2[0].imag, edge2[1].imag
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


def intersection_droites(edge1, edge2):
    """
    Prend 2 segments en argument et vérifie que l'intersection des droites associées
    n'est pas inclus dans les segments
    """
    a1, b1, c1 = equation_droite(edge1)
    a2, b2, c2 = equation_droite(edge2)
    x1, x2 = edge1[0].real, edge1[1].real
    y1, y2 = edge1[0].imag, edge1[1].imag
    x3, x4 = edge2[0].real, edge2[1].real
    y3, y4 = edge2[0].imag, edge2[1].imag

    if x2 < x1 :
        x1, x2 = x2, x1
    if x4 < x3 :
        x3, x4 = x4, x3
    if y2 < y1 :
        y1, y2 = y2, y1
    if y4 < y3 :
        y3, y4 = y4, y3

    if a1 == a2:
        print("a")
        """
        vérifie si les droites sont parallèles
        """
        return False
    elif c1 == inf and c2 != inf:
        print("b")
        """
        il existe (x,y) vérifiant les 2 équations:
        y = a1 * x + b1
        x = c2
        """
        x = c2
        y = a1 * x + b1
    elif c1 != inf and c2 == inf:
        print("c")
        """
        il existe (x,y) vérifiant les 2 équations:
        x = c1
        y = a2 * x + b2
        """
        x = c1
        y = a2 * x + b2
    else:
        print("d")
        """
        il existe (x,y) vérifiant les 2 équations:
        y = a1 * x + b1
        y = a2 * x + b2
        """
        x = (b2 - b1)/(a1 - a2)
        y = a1 * x + b1

    if x1 <= x <= x2 and x3 <= x <= x4 and y1 <= y <= y2 and y3 <= y <= y4:
        return True
    return False

