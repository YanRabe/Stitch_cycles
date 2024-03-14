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
     
     Renvoie une ndarray de dimmension N,2 contenant les coordonnees complexes de chaque point
     avec la partie réelle dans la colonne 0 et la partie imaginaire dans la colonne 1.
      '''
    paths = svg2paths(svgpath)[0]
    array_de_point = np.empty((0,2))
    print(array_de_point)
    for path_discontinuous in paths:
        
        for path in path_discontinuous.continuous_subpaths():

            cycle_de_point = np.array([path[0][0].real,path[0][0].imag])
            for point in path:
                point_np = np.array([point[1].real,point[1].imag])
                cycle_de_point = np.vstack((cycle_de_point,point_np))

            array_de_point = np.vstack((array_de_point,cycle_de_point))

    return  array_de_point


def pointCoordList(svgpath):
    '''Récupère en entrée le nom du fichier
    
    Divise en assemblage de chemins les cycles;
     Un chemin est composé de lignes partant d'un point de départ jusqu'à un point d'arrivée
     Puis récupère les coordonnées individuelles du chemin
     
     Renvoie une liste d'array de dimmension N,2 contenant les coordonnees complexes de chaque point du cycle
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


def cyclesToGraph(paths):
    """_summary_
    recupere le nom du fichier en entree et renvoie 3 array:
    -une array de dimension N,2 ontenant la totalite des points complexes
    -une array d'adajcence de dimension N,2 contenant l'indice du point suivant et du point precedent
    -une array de dimension M,2 (avec M le nombre de cycle), avec l'indice du point de depart et le nombre de points du cycle
    """
    array_de_point_initiale = pointCoordList(paths)
    array_d_adjacence = np.empty((0,2))
    array_indice_depart = np.empty((0,2)) #continent une array par cycle avec l'indice de depart et le nombre de points du cycle
    array_de_point = np.empty((0,2))#contient l'ensemble des points dans une seule array
    
    for indice_cycle in range(len(array_de_point_initiale)):
        
        array_indice_depart = np.vstack((array_indice_depart,np.array([len(array_de_point),array_de_point_initiale[indice_cycle].shape[0]])))
        
        delta_nb_point = array_de_point.shape[0]
        
        array_de_point = np.vstack((array_de_point,array_de_point_initiale[indice_cycle]))
        
        for indice_point in range(array_de_point_initiale[indice_cycle].shape[0]):
            
            if indice_point == array_de_point_initiale[indice_cycle].shape[0]-1:
                indice_suivant = 0 
            else:
                indice_suivant = indice_point + 1
                
            if indice_point == 0:
                indice_precedent = array_de_point_initiale[indice_cycle].shape[0]-1
            else:
                indice_precedent = indice_point -1
                
            array_d_adjacence = np.vstack((array_d_adjacence,np.array([indice_suivant + delta_nb_point,indice_precedent+delta_nb_point])))
        
    return array_de_point,array_d_adjacence,array_indice_depart
                

def pathsToSvg(points, filename):
    """Prend des coordonnées complexes.

    les transforme en path

    Renvoie un fichier svg.
    """
    global number_outputs
    print(points[0][0])
    lines_list = [Line(complex(*points[i][j-1]), complex(*points[i][j])) for i in range(len(points)) for j in range(len(points[i]))]
    print(*lines_list, sep='\n \n')
    paths = [Path(lines_list[i]) for i in range(len(lines_list))]
    paths2svg.wsvg(paths, filename=f'outputs\ numpy_output{number_outputs + 1}_{filename}.svg')
