import os
os.chdir('/Users/teresa/z-Cours/Stitch_cycles')
import svg_handler as svgh
import svg_handler_numpy as svgh_np
import stitch_base as sb
import stitch_base_numpy as sb_np
from svgpathtools import Path, Line
import numpy as np

path = svgh.pointCoord("svg_entries/svg/simple.svg")
graph1 = svgh.cyclesToGraph("svg_entries/svg/simple.svg")
graph1_np = svgh_np.cyclesToGraph("svg_entries/svg/simple.svg")

# cycle_A = graph1[0:6]
# cycle_B = graph1[6:12]

#print(sb.nearestEdge3(cycle_A, cycle_B))
# print('python:',sb.listCoord(graph1,1))
#print('numpy',sb_np.np_listCoord(graph1_np,1))


# cycle_A_np = graph1_np[0:6]
# cycle_B_np = graph1_np[6:12]
liste_points, liste_adjacence, liste_indice_depart = graph1
array_de_point, array_d_adjacence, array_indice_depart = graph1_np
#print(array_de_point[8],array_de_point[array_d_adjacence[8,0]])

#print(sb_np.np_nearestEdge3(cycle_A_np, cycle_B_np))
#print(sb.nearestCycle(graph1,0))

#print(sb_np.np_nearestCycle(graph1_np,0))

# test fonction edges
#E = np.zeros((3,2,2))
# E[0,0] = array_de_point[0]
# E[0,1] = array_de_point[array_d_adjacence[0,0]]
# E = sb_np.edges(graph1_np)
# edge = np.array([array_de_point[0],array_de_point[array_d_adjacence[0,0]]])
# modif_E = np.delete(E,0,0)
#energy = sb_np.vectorial_energy(edge,np.delete(E,0,axis=0))
#print('numpy:', sb_np.np_nearestEdge4(graph1_np,0,sb_np.edges(graph1_np)))
#print('python:', sb.nearestCycle(graph1,0))

#print(sb.energyid_cycle_Calc_2([(3.0681859+13.0285j ),(7.4997739+13.0285j )],[(7.6670039+10.01837j ),(2.9845719+10.01837j )],liste_points))
