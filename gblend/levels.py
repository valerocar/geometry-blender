"""
Functions to extract surface geometry
"""
from skimage import measure
import numpy as np


def __function_level(f, level, domain, resolutions):
    res_x, res_y, res_z = resolutions
    x_min, x_max, y_min, y_max, z_min, z_max = domain
    x_inc = (x_max - x_min) / (res_x - 1)
    y_inc = (y_max - y_min) / (res_y - 1)
    z_inc = (z_max - z_min) / (res_z - 1)
    xs, ys, zs = np.meshgrid(np.linspace(x_min, x_max, res_x), np.linspace(y_min, y_max, res_y),
                             np.linspace(z_min, z_max, res_z))
    #fs = f(xs, ys, zs)
    # TODO: Explain this!
    fs = f(ys, xs, zs)
    ps, ts, normals, values = measure.marching_cubes(fs, level, spacing=(x_inc, y_inc, z_inc))
    ps[:, 0] += x_min
    ps[:, 1] += y_min
    ps[:, 2] += z_min
    return ps, ts, normals, values


def geometry_level(geometry, box, res=[120, 120, 120]):
    """
    Returns the mesh data for the level set geometry.f == 1/2
    :param geometry: The geometric object
    :param box: bounding box
    :param res: resolution of voxels for the marching algorithm
    :return: vertices coordinates, triangle indices, normals at vertices, f values at vertices
    """
    return __function_level(geometry.get_lambda(), .5, box, res)
