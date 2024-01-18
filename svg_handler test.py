from svgpathtools import svg2paths, paths2svg

###FIchier où on va mettre les fonctions pour ouvrir et renvoyer les svg
#Req: svgpathtools

#yan aime les zizis
def pointCoord(svgpath):
    '''Récupère en entrée le nom du fichier
    
    Divise en assemblage de chemins les cycles;
     Un chemin est composé de lignes partant d'un point de départ jusqu'à un point d'arrivée
     Puis récupère les coordonnées individuelles du chemin

     Renvoie les coordonnées (complexes) de chaque point du chemin/cycle.
      '''
    paths = svg2paths(svgpath)[0]
    print(f"paths:{paths}")

    for path_discontinuous in paths:
        print(f"path discontinuous: {path_discontinuous}")
        print(f"continuous subpath: {path_discontinuous.continuous_subpaths()}")
        for path in path_discontinuous.continuous_subpaths():
            print(f'path: {path}')
            for i in range(len(path)):
                print(path[i][0])

def stitchEdges(A, B):
    """créer un objet Line du package svgpathtools pour lier deux points.
    Ne renvoie rien."""
    pass
def cyclesToGraph(paths):
    pass

def pathsToSvg(paths):
    pass