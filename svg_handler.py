from svgpathtools import svg2paths, paths2svg, Line, Path
import os

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
    return  liste_de_point


def stitchEdges(edge1, edge2):
    '''
    
    '''

    pass

def cyclesToGraph(paths):
    """_summary_
    recupere le nom du fichier en entree et renvoie 3 listes:
    -une liste contenant la totalite des points complexes
    -une liste d'adajcence contenant une liste par point contenant l'indice du point suivant et du point precedent
    -une liste contenant une liste par cycle, avec l'indice du point de depart et le nombre de points du cycle
    """
    liste_de_point_initiale = pointCoord(paths)
    liste_d_adjacence = []
    liste_indice_depart = [] #continent une liste par cycle avec l'indice de depart et le nombre de points du cycle
    liste_de_point = [] #contient l'ensemble des points dans une seule liste
    
    for indice_cycle in range(len(liste_de_point_initiale)):
        
        liste_indice_depart.append([len(liste_de_point),len(liste_de_point_initiale[indice_cycle])])
        
        delta_nb_point = len(liste_de_point)
        
        liste_de_point += liste_de_point_initiale[indice_cycle]
        
        for indice_point in range(len(liste_de_point_initiale[indice_cycle])):
            if indice_point == len(liste_de_point_initiale[indice_cycle])-1:
                indice_suivant = 0 
            else:
                indice_suivant = indice_point + 1
                
            if indice_point == 0:
                indice_precedent = len(liste_de_point_initiale[indice_cycle])-1
            else:
                indice_precedent = indice_point -1
                
            liste_d_adjacence.append([indice_suivant + delta_nb_point,indice_precedent+delta_nb_point])
        
    return liste_de_point,liste_d_adjacence,liste_indice_depart
                

def pathsToSvg(points):
    """Prend des coordonnées svgpathtool.

    les transforme en path

    Renvoie un fichier svg.
    
    """
    global number_outputs
    lines_list = [[Line(points[i][j-1], points[i][j]) for j in range(len(points[i]))] for i in range(len(points))]
    print(*lines_list)
    paths = [Path(*lines_list[i]) for i in range(len(lines_list))]
    paths2svg.wsvg(paths, filename=f'outputs\output{number_outputs + 1}.svg')
