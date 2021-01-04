"""
Some useful variables to define functions in 3-dimensional space. The x,y and z are symbolic variables
used to construct functions to  represent geometric objects. The rxy variable is used to represent
the distance to the z axis (i.e sqrt(x**2+y**2)). The variable k is used as the smoothing parameter in the blending process of
geometrical objects.
"""
from sympy import symbols, Symbol


x, y, z, rxy, k = symbols("x y z rxy k", real=True)


