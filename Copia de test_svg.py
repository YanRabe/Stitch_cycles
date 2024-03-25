import os
os.chdir('/Users/teresa/z-Cours/Stitch_cycles')
import svg_handler as svgh
import svg_handler_numpy as svgh_np
import stitch_base as sb
import stitch_base_numpy as sb_np
from svgpathtools import Path, Line

##
path = svgh.pointCoord("svg_entries/svg/simple.svg")
#print(path)
#svgh.pathsToSvg(path)
# path = svgh.pointCoord("svg_entries\svg\simple.svg")
# print(path)
# svgh.pathsToSvg(path)
# print(len(svgh.pointCoord("svg_entries\svg\simple.svg")[1]))

graph1 = svgh.cyclesToGraph("svg_entries/svg/simple.svg")[0]
graph2 = svgh_np.cyclesToGraph("svg_entries/svg/simple.svg")[0]
#print(graph1)
#print(graph2)
edge1 = graph1[0:2]
edge2 = graph1[2:4]
print(sb.norm2(edge1[0],edge2[0]))
print(sb.energyid_cycle_Alc(edge1,edge2))

edge1_g2 = graph2[:2,:]
edge2_g2 = graph2[2:4,:]
print(sb_np.np_norm2(edge1_g2[0],edge2_g2[0]))
print(sb_np.np_senergyid_cycle_Alc(edge1_g2,edge2_g2))



##
import brouillon

test1=[[1,2],[2,0],[0,1],[4,5],[5,3],[3,4]]
l_indice_dep=[[0,3],[3,3]]

edge1=[1,2]
edge2=[3,4]
print(test1)
print('test1',changeAdjacence(edge1,edge2,'pattern_2',test1))

test2=[[1,2],[2,0],[0,1],[5,4],[3,5],[4,3]]
print(test2)
print('test2', changeAdjacence(edge1,edge2,'pattern_2',test2))

##
liste_indice_depart=[[0,5],[6,8],[15,2],[18,5]]
min_cycle = liste_indice_depart[0]
for cycle in liste_indice_depart:
    if cycle[1] <= min_cycle[1]:
        min_cycle = cycle
id_cycle_depart = liste_indice_depart.index(min_cycle)

##
liste_adjacence=[[1,2],[2,0],[0,1],[4,5],[5,3],[3,4]]
liste_indice_depart=[[0,3],[3,3]]

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