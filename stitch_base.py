from math import inf
import svg_handler as svgh
"""
Cycles --> liste: 
    -coord points 
    -ind points suiv - préc
    -ind point de départ + nb de points par cycle
"""

def listCoord(graph,cA):
    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    cA est l'indice du cycle;
    """
    liste_points, liste_adjacence, liste_indice_depart = graph
    res = []
    act = liste_indice_depart[cA]
    for i in range(liste_indice_depart[cA][1]):
        res.append(liste_points[act])
        act = liste_adjacence[act][0]
    return res


def nearestCycle(graph, cA):
    
    """
    graph est le resultat de la fonction cyclesToGraph (à changer peut-être pour 3 variables différentes);
    cA est l'indice du cycle dont on cherche le voisin le + proche;
    """
    liste_points, liste_adjacence, liste_indice_depart = graph
    liste_dist = []
    liste_edges = []
    cycleA = svgh.listCoord(graph, cA)
    for cB in range(len(liste_indice_depart)):
        min_Energy_Cyc = inf
        if cB != cA:
            cycleB = svgh.listCoord(graph, cB)
            edgeA, edgeB = None, None
            for coord in cycleB:
                temp = nearestEdge2(cycleA,cycleA[:2],cycleB)
                if temp[2] < min_Energy_Cyc:
                    edgeA, edgeB, min_Energy_Cyc = temp
            liste_dist.append(min_Energy_Cyc)
            liste_edges.append([edgeA,edgeB])
        else:
            liste_dist.append(min_Energy_Cyc)
            liste_edges.append([None,None])

    minId = liste_dist.index(min(liste_dist))
    return liste_dist[minId], liste_edges[minId]

def nearestEdge2(Ca, edgeA, Cb, expected = None):
    """
    edgeA = liste de 2 complexes (coords);
    Ca = liste des coords du cycle A;
    Cb = liste des coords du cycle B;
    expected = les coordonnées du plus proche trouvé avant chez B;
    """
    
    choixB = [Cb[-1],Cb[0]]
    minE = energyCalc(edgeA,choixB)
    for sommet in range(len(Cb)-1):
        temp = energyCalc(edgeA,[Cb[sommet],Cb[sommet+1]])
        if temp < minE:
            minE = temp
            choixB = [Cb[sommet],Cb[sommet+1]]
    
    if choixB == expected:
        return edgeA, choixB, minE
    return nearestEdge2(Cb, choixB, Ca, edgeA)