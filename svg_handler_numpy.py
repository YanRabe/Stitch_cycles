from svgpathtools import svg2paths, paths2svg, Line, Path
import os
import numpy as np
###FIchier où on va mettre les fonctions pour ouvrir et renvoyer les svg
#Req: svgpathtools

outputs_list = os.listdir("outputs") #list des outputs
global number_outputs
number_outputs = len(outputs_list)

def pointCoord(svgpath):
    '''Récupère en entrée le nom du fichier
    
    Divise en assemblage de chemins les cycles;
     Un chemin est composé de lignes partant d'un point de départ jusqu'à un point d'arrivée
     Puis récupère les coordonnées individuelles du chemin
     
     Renvoie une array de dimmension N,2 contenant les coordonnees complexes de chaque point
     avec la partie réelle dans la colonne 0 et la partie imaginaire dans la colonne 1.
      '''
    paths = svg2paths(svgpath)[0]
    liste_de_point = np.empty((0,2))

    for path_discontinuous in paths:
        
        for path in path_discontinuous.continuous_subpaths():

            cycle_de_point = np.array([path[0][0].real,path[0][0].imag])
            for point in path:
                point_np = np.array([point[1].real,point[1].imag])
                cycle_de_point = np.vstack((cycle_de_point,point_np))

            liste_de_point = np.vstack((liste_de_point,cycle_de_point))

    return  liste_de_point


def pointCoordList(svgpath):
    '''Récupère en entrée le nom du fichier
    
    Divise en assemblage de chemins les cycles;
     Un chemin est composé de lignes partant d'un point de départ jusqu'à un point d'arrivée
     Puis récupère les coordonnées individuelles du chemin
     
     Renvoie une liste par cycle, d'array de dimmension N,2 contenant les coordonnees complexes de chaque point du cycle
     avec la partie réelle dans la colonne 0 et la partie imaginaire dans la colonne 1.
      '''
    paths = svg2paths(svgpath)[0]
    liste_d_array = []

    for path_discontinuous in paths:
        
        for path in path_discontinuous.continuous_subpaths():

            cycle_de_point = np.array([path[0][0].real,path[0][0].imag])
            for point in path[:-1]:
                point_np = np.array([point[1].real,point[1].imag])
                cycle_de_point = np.vstack((cycle_de_point,point_np))
                
            liste_d_array.append(cycle_de_point)

    return liste_d_array