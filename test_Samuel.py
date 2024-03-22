import svg_handler_numpy as svgh_np
import svg_handler as svgh
import stitch_base_numpy as sb
from svgpathtools import Path, Line
a,b,c = svgh_np.cyclesToGraph("svg_entries\svg\simple.svg")
print(a)
#path = svgh.pointCoord("svg_entries\svg\simple.svg")
#print(path)
#svgh.pathsToSvg(path)
print("xxxxxxxxxxx")
print(sb.listCoord(svgh_np.cyclesToGraph("svg_entries\svg\simple.svg"),0))