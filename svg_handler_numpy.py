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
    array_de_points = np.empty((0,2))

    for path_discontinuous in paths:
        
        for path in path_discontinuous.continuous_subpaths():

            cycle_de_point = np.array([path[0][0].real,path[0][0].imag])
            for point in path:
                point_np = np.array([point[1].real,point[1].imag])
                cycle_de_point = np.vstack((cycle_de_point,point_np))

            array_de_points = np.vstack((array_de_points,cycle_de_point))

    return  array_de_points


def cyclesToGraph(paths):
    """_summary_
    recupere le nom du fichier en entree et renvoie 3 listes:
    -une liste contenant la totalite des points complexes
    -une liste d'adajcence contenant une liste par point contenant l'indice du point suivant et du point precedent
    -une liste contenant une liste par cycle, avec l'indice du point de depart et le nombre de points du cycle
    """
    array_de_points = pointCoord(paths) #contient tous les points du cycle
    liste_d_adjacence =np.empty((0,2)) 
    liste_indice_depart = np.empty((0,2))  #continent une liste par cycle avec l'indice de depart et le nombre de points du cycle
        
    for indice_cycle in range(len(array_de_points)):
        
        liste_indice_depart=np.vstack((liste_indice_depart,np.array(len(array_de_points),len(array_de_points[indice_cycle]))))
        
        delta_nb_point = len(array_de_points)
        
        array_de_points += array_de_points[indice_cycle]
        
        for indice_point in range(len(array_de_points[indice_cycle])):
            if indice_point == len(array_de_points[indice_cycle])-1:
                indice_suivant = 0 
            else:
                indice_suivant = indice_point + 1
                
            if indice_point == 0:
                indice_precedent = len(array_de_points[indice_cycle])-1
            else:
                indice_precedent = indice_point -1
                
            liste_d_adjacence.append([indice_suivant + delta_nb_point,indice_precedent+delta_nb_point])
        
    return array_de_points,liste_d_adjacence,liste_indice_depart
                

def pathsToSvg(points):
    """Prend des coordonnées complexes.

    les transforme en path

    Renvoie un fichier svg.
    
    """
    global number_outputs
    lines_list = [[Line(points[i][j-1], points[i][j]) for j in range(len(points[i]))] for i in range(len(points))]
    print(*lines_list)
    paths = [Path(*lines_list[i]) for i in range(len(lines_list))]
    paths2svg.wsvg(paths, filename=f'outputs\output{number_outputs + 1}.svg')
