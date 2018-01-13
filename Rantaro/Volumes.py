# sphere, cube, cone

from math import pi
from math import pow

def sphere_vol(r):
    return (4/3) * pi * pow(r, 3)

def cube_vol(l, w, h):
    return l * w * h

def cone_vol(r, h):
    return (pi * pow(r, 2)) * h/3