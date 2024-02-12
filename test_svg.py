import svg_handler as svgh
import stitch_base as sb
from svgpathtools import Path, Line

# path = svgh.pointCoord("svg_entries\svg\simple.svg")
# print(path)
#svgh.pathsToSvg(path)
# path = svgh.pointCoord("svg_entries\svg\simple.svg")
# print(path)
# svgh.pathsToSvg(path)
# print(len(svgh.pointCoord("svg_entries\svg\simple.svg")[1]))

graph = svgh.cyclesToGraph("svg_entries\svg\simple_reverse.svg")
# print("XXXXXXXXXXXXXXXXXXXX")
# print(a)
# print("")
# print(b)
# print("")
# print(c)
test = sb.nearestCycle(graph, 0)

new_path = sb.stitchEdges_2(graph)
print(new_path)
svgh.pathsToSvg(new_path)