import svg_handler_numpy as svgh_np
import svg_handler as svgh
import stitch_base as sb
import stitch_base_numpy as sbn
from svgpathtools import Path, Line
import time

liste_names = ["simple", "simple_reverse", "brain_cycles", "bunny_small_cycles", "square_cycles", "dragon_cycles", "bunny_big_cycles"]


def conversion(time):
    res = [0, 0, time]
    if res[2] >= 60:
        res[1] = res[2] // 60
        res[2] -= res[1] * 60
        
        if res[1] >= 60:
            res[0] = res[1] // 60
            res[1] -= res[0] * 60
    return f"{res[0]} h, {res[1]} min, {res[2]} s"

#path = svgh.pointCoord("svg_entries\svg\simple.svg")
#print(path)
#svgh.pathsToSvg(path)
path = svgh.pointCoord("svg_entries\svg\simple.svg")
# print(path)
# svgh.pathsToSvg(path)
# print(len(svgh.pointCoord("svg_entries\svg\simple.svg")[1]))

"""
debut = time.time()
filename = "brain_cycle"
graph = svgh_np.cyclesToGraph(f"svg_entries\svg\{filename}.svg")
# test = sb.nearestCycle(graph, 0)


new_path = sbn.stitchEdges_2(graph)
fin = time.time()
svgh_np.pathsToSvg(new_path, filename)
tempsStr = conversion(fin-debut)

print(tempsStr)



"""
"""
monF = open("times.txt", "a", encoding="utf-8")

for i in range(1,-1,-1):
    filename = liste_names[i]
    debut = time.time()
    graph = svgh.cyclesToGraph(f"svg_entries\svg\{filename}.svg")

    new_path = sb.stitchEdges_2(graph)
    svgh.pathsToSvg(new_path, filename)
    fin = time.time()
    print(fin-debut)
    tempsStr = conversion(fin-debut)
    monF.write(filename + " : " + tempsStr + " \n")
    print(filename, "est fini")

monF.write("\n\n")
monF.close()
print("fini :)")

"""

monF = open("times_numpy.txt", "a", encoding="utf-8")
""""""
for i in range(2,3):
    filename = liste_names[i]
    debut = time.time()
    graph = svgh_np.cyclesToGraph(f"svg_entries\svg\{filename}.svg")

    new_path = sbn.stitchEdges_2(graph)
    svgh_np.pathsToSvg(new_path, filename)
    fin = time.time()
    print(fin-debut)
    tempsStr = conversion(fin-debut)
    monF.write(filename + " : " + tempsStr + " \n")
    print(filename, "est fini")

monF.write("\n\n")
monF.close()
print("fini :)")