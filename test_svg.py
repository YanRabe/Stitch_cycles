import svg_handler as svgh
from svgpathtools import Path, Line

path = svgh.pointCoord("svg_entries\svg\simple.svg")
# print(path)
svgh.pathsToSvg(path)
# print(len(svgh.pointCoord("svg_entries\svg\simple.svg")[1]))

