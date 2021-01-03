from skimage import measure
import numpy as np


def function_level(f, level, domain, resolutions):
    res_x, res_y, res_z = resolutions
    x_min, x_max, y_min, y_max, z_min, z_max = domain
    x_inc = (x_max - x_min) / (res_x - 1)
    y_inc = (y_max - y_min) / (res_y - 1)
    z_inc = (z_max - z_min) / (res_z - 1)
    xs, ys, zs = np.meshgrid(np.linspace(x_min, x_max, res_x), np.linspace(y_min, y_max, res_y),
                             np.linspace(z_min, z_max, res_z))
    #print("Evaluating function at vertices\n")
    fs = f(xs, ys, zs)
    #print("Marching cubes starts\n")
    vs, ts, normals, values = measure.marching_cubes(fs, level, spacing=(x_inc, y_inc, z_inc))
    #print("Marching cubes ends\n")
    vs[:, 0] += x_min
    vs[:, 1] += y_min
    vs[:, 2] += z_min
    return vs, ts, normals, values


def geometry_level(geometry, box, res):
    return function_level(geometry.get_lambda(), .5, box, res)
