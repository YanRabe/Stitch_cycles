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

cycle_A = graph1[0:6]
cycle_B = graph1[6:12]

#print(sb.nearestEdge3(cycle_A, cycle_B))

cycle_A_np = graph1_np[0:6]
cycle_B_np = graph1_np[6:12]

array_de_point, array_d_adjacence, array_indice_depart = graph1_np
res = np.empty((0,2))
act = array_indice_depart[0,0]
prueba = array_de_point[act]
inter = np.vstack((res,prueba))

# #print(sb_np.np_nearestEdge3(cycle_A_np, cycle_B_np))
# print(sb.nearestCycle(graph1,0))
#
# print(sb_np.np_nearestCycle(graph1_np,0))

##
import numpy as np
a = np.array([[1,2],[3,4],[4,4],[5,6],[4,4]])
print(np.where(a==[4,4]))
