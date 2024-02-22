import svg_handler_numpy as svgh_np
import svg_handler as svgh
import stitch_base as sb
from svgpathtools import Path, Line

#path = svgh.pointCoord("svg_entries\svg\simple.svg")
#print(path)
#svgh.pathsToSvg(path)
path = svgh.pointCoord("svg_entries\svg\simple.svg")
# print(path)
# svgh.pathsToSvg(path)
# print(len(svgh.pointCoord("svg_entries\svg\simple.svg")[1]))

filename = "brain_cycles_test"
graph = svgh.cyclesToGraph(f"svg_entries\svg\{filename}.svg")
# test = sb.nearestCycle(graph, 0)

new_path = sb.stitchEdges_2(graph)
svgh.pathsToSvg(new_path, filename)
