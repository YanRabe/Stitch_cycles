from svgpathtools import svg2paths, paths2svg
import numpy as np

###FIchier où on va mettre les fonctions pour ouvrir et renvoyer les svg
#Req: svgpathtools

def pointCoord(svgpath):
    '''Récupère en entrée le nom du fichier
    
    Divise en assemblage de chemins les cycles;
     Un chemin est composé de lignes partant d'un point de départ jusqu'à un point d'arrivée
     Puis récupère les coordonnées individuelles du chemin
     Renvoie une liste de liste contenant les coordonnees complexes de chaque point d'un cycle.
      '''
    paths = svg2paths(svgpath)[0]
    # print(f"paths:{paths}")

    liste_de_point = []
    nb_path = 0 
    for path_discontinuous in paths:
        #print(f"path discontinuous: {path_discontinuous}")
        #print(f"continuous subpath: {path_discontinuous.continuous_subpaths()}")
        for path in path_discontinuous.continuous_subpaths():
            #print(f'path: {path}')
            liste_de_point.append([])
            for i in range(len(path)):
                # print(path[i][0])
                liste_de_point[nb_path].append(path[i][0])
            nb_path += 1
    return liste_de_point


def energyCalc(edge1, edge2):
    """
    Prend en entrée deux lignes (type liste) 

    et renvoie l'énergie de 'patch' selon la formuleb pg 8.
    """
    res = min(norm2(edge1[0] - edge2[1])+ norm2(edge1[1] - edge2[0]), 
              norm2(edge1[0] - edge2[0]) + norm2(edge1[1] - edge2[1])) 
    
    res -= norm2(edge1[0] - edge1[1]) - norm2(edge2[0]- edge2[1])
    
    return res

def norm2(point_a, point_b):
    """
    Prend deux points complexes en entrée

    calcule la différence

    Renvoie la distance avec la norme euclidienne.
    """
    difference = (point_a.real - point_b.real, point_a.imag - point_b.imag) #différence des points a et b
    res = np.sqrt(difference[0]**2+difference[1]**2) #distance entre a et b (norme 2)
    return res

def stitchEdges(A, B):
    """créer un objet Line du package svgpathtools pour lier deux points.
    
    
    """
    pass

def cyclesToGraph(paths):
    pass

def pathsToSvg(paths):
    pass