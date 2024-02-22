import svg_handler_numpy as svgh_np
import svg_handler as svgh
import stitch_base as sb
from svgpathtools import Path, Line

#path = svgh.pointCoord("svg_entries\svg\simple.svg")
#print(path)
#svgh.pathsToSvg(path)
a,b,c = svgh_np.cyclesToGraph("svg_entries\svg\simple.svg")
u,v,w = svgh.cyclesToGraph("svg_entries\svg\simple.svg")
print(a)
print(u)
print("xxx")
print(b)
print(v)
print("xxx")
print(c)
print(w)
# svgh.pathsToSvg(path)
# print(len(svgh.pointCoord("svg_entries\svg\simple.svg")[1]))
print("XXXXXXXXXXXx")
