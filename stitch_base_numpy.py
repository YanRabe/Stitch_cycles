from math import inf
import svg_handler as svgh
import numpy as np
import svgpathtools as svgpt

'''
Cycle

'''
def np_norm2(point_a, point_b):
    '''
    point : vecteur 1,2
    norme euclidienne avec numpy
    '''
    return np.sqrt(np.sum((point_a-point_b)**2))

def np_energyid_cycle_Alc(edge1, edge2):
    '''
    edge : 2,2
    calcul energie de 'patch'
    '''
    res = min(np_norm2(edge1[0], edge2[1])+ np_norm2(edge1[1], edge2[0]),
              np_norm2(edge1[0], edge2[0]) + np_norm2(edge1[1], edge2[1]))

    res -= np_norm2(edge1[0], edge1[1]) - np_norm2(edge2[0], edge2[1])

    return res


