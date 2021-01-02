from gblend.variables import x, y, z, rxy
from sympy.algebras.quaternion import Quaternion
from sympy import symbols, cos, sin, sqrt, N, lambdify, exp


def sigmoid(s, k):
    return 1 / (1 + exp(-(s / k)))


#
# General Geometry Types. No sigmoid functions here!
#
class Geometry:
    def __init__(self, f, dim):
        """
        Creates a geometry in type associated to the input function
        :param f: a function
        :param dim: the number of independent variable of the function
        """
        self.dim = dim
        self.f = f

    def geometry(self, f):
        if self.dim == 2:
            return Geometry2D(f)
        elif self.dim == 3:
            return Geometry3D(f)

        return Geometry(self, f)

    def __and__(self, b):
        return self.geometry(self.f * b.f)

    def __or__(self, b):

        return self.geometry(self.f + b.f - self.f * b.f)

    def __invert__(self):
        return self.geometry(1 - self.f)

    def __add__(self, b):
        """
        Computes the smooth union of this set with b
        :param b:
        :return:
        """
        return self.geometry(self.f + b.f - self.f * b.f)

    def __sub__(self, b):
        """
        Computes the smooth subtraction of this set with b
        :param b:
        :return:
        """
        return self.geometry(self.f * (1 - b.f))

    def __neg__(self):
        return self.geometry(1 - self.f)

    def get_lambda(self):
        if self.dim == 3:
            return lambdify((x, y, z), self.f, 'numpy')
        elif self.dim == 2:
            return lambdify((x, y), self.f, 'numpy')

        return None


class Geometry3D(Geometry):

    def __init__(self, f):
        Geometry.__init__(self, f, 3)

    @staticmethod
    def subs_3d(f, x_new, y_new, z_new):
        xx, yy, zz = symbols("xx yy zz", real=True)
        xx_new = x_new.subs({x: xx, y: yy, z: zz})
        yy_new = y_new.subs({x: xx, y: yy, z: zz})
        zz_new = z_new.subs({x: xx, y: yy, z: zz})
        tmp = f.subs({x: xx_new, y: yy_new, z: zz_new})
        return tmp.subs({xx: x, yy: y, zz: z})

    def translated(self, dx, dy, dz):
        """
        Returns a translated version of this object
        :param dx: distance translates in the x-direction
        :param dy: distance translates in the y-direction
        :param dz: distance translates in the z-direction
        :return: a translated version of this object
        """
        return Geometry3D(Geometry3D.subs_3d(self.f, x - dx, y - dy, z - dz))

    def displaced(self, f, axis='z'):
        """
        Returns this object displaced by one of the formulas

        (x,y,z) -> (x+f(y,z),y,z)
        
        (x,y,z) -> (x,f(x,z),z)
        
        (x,y,z) -> (x,y,z+f(x,y))
        
        depending on whether axis is "x", "y" or "z".

        :param f: a function in 2-variables none of which is the axis variable
        :param axis: the axis along which the object will be displaced
        :return: the displaced object
        """
        # TODO: Check for f variables dependencies
        if axis == 'x':
            return Geometry3D(self.subs_3d(self.f, x - f, y, z))
        elif axis == 'y':
            return Geometry3D(self.subs_3d(self.f, x, y - f, z))
        elif axis == 'z':
            return Geometry3D(self.subs_3d(self.f, x, y, z - f))

        return None

    def scaled(self, sx: float, sy: float, sz: float):
        """
        Returns a scaled version of this object

        :param sx: scale factor in the x-direction
        :param sy: scale factor in the y-direction
        :param sz: scale factor in the y-direction
        :return: a scaled version of this object
        """
        return Geometry3D(Geometry3D.subs_3d(self.f, x / sx, y / sy, z / sz))

    def rotated(self, nx: float, ny: float, nz: float, theta: float):
        """
        Returns a rotated version of this object

        :param nx: x-component of the rotation axis
        :param ny: y-component of the rotation axis
        :param nz: z-component of the rotation axis
        :param theta: rotation angle
        :return: a rotated version of this object
        """
        nrm = N(sqrt(nx ** 2 + ny ** 2 + nz ** 2))
        sn2 = N(sin(theta / 2))
        cs2 = N(cos(theta / 2))
        q = Quaternion(cs2, sn2 * nx / nrm, sn2 * ny / nrm, sn2 * nz / nrm)
        q_inv = q.conjugate()
        r = q_inv * Quaternion(0, x, y, z) * q
        return Geometry3D(self.subs_3d(self.f, r.b, r.c, r.d))

    def displace(self, f, axis='z'):
        self.f = self.displaced(f, axis).f

    def translate(self, dx: float, dy: float, dz: float):
        self.f = self.translated(dx, dy, dz).f

    def scale(self, sx, sy, sz):
        self.f = self.scaled(sx, sy, sz).f

    def rotate(self, nx, ny, nz, theta):
        self.f = self.rotated(nx, ny, nz, theta).f


###################################
#                                 #
#      Concrete Geometry Types    #
#     (sigmoid functions here!    #
#                                 #
###################################

class Ball3D(Geometry3D):
    def __init__(self, x0=0, y0=0, z0=0, r_val=1, k=1 / 2):
        """
        A ball in 3-dimensional space

        :param x0: the x-component of the center of the ball
        :param y0: the y-component of the center of the ball
        :param z0: the z-component of the center of the ball
        :param r_val: the radius of the ball
        :param k: smoothing factor
        """
        Geometry3D.__init__(self, sigmoid(r_val ** 2 - (x - x0) ** 2 - (y - y0) ** 2 - (z - z0) ** 2, k))


class Cylinder3D(Geometry3D):
    def __init__(self, x0=0, y0=0, r_val=1, k=1 / 2):
        """
        A cylinder in 3-dimensional space

        :param x0: the x-component of the cylinder's center
        :param y0: the y-component of the cylinder's center
        :param r_val: the y-component of the cylinder's center
        :param k: the smoothing factor
        """
        Geometry3D.__init__(self, sigmoid(r_val ** 2 - (x - x0) ** 2 - (y - y0) ** 2, k))


class RevolutionSurface3D(Geometry3D):
    def __init__(self, curve_eq, k=1 / 2):
        """
        A surface obtained by rotating a curve around the z-axis

        :param curve_eq:  equation of curve in the r and z variables
        :param k:  smoothing parameter
        """
        Geometry3D.__init__(self, sigmoid(RevolutionSurface3D.compute_f(curve_eq), k))

    @staticmethod
    def compute_f(curve_eq):
        return curve_eq.subs({rxy: sqrt(x ** 2 + y ** 2)})


class Torus3D(RevolutionSurface3D):
    def __init__(self, r_min=1, r_max=2, k=1 / 2):
        """
        A torus in 3-dimensional space

        :param r_min: radius of the torus circular cross sections
        :param r_max: radius to the center of the torus circular cross section
        :param k: smoothing parameter
        """
        RevolutionSurface3D.__init__(self, r_min ** 2 - (rxy - r_max) ** 2 - z ** 2, k)


##########################
#                        #
#      Geometry  2D      #
#                        #
##########################

# TODO: Complete this!
class Geometry2D(Geometry):

    def __init__(self, f):
        Geometry.__init__(self, f, 2)

    def translated(self, dx, dy):
        return Geometry2D(self.subs_2d(self.f, x - dx, y - dy))

    def scaled(self, sx, sy):
        return Geometry2D(self.subs_2d(self.f, x / sx, y / sy))

    def rotated(self, theta):
        return Geometry2D(self.subs_2d(self.f, x * cos(theta) + y * sin(theta), -x * sin(theta) + y * cos(theta)))

    def translate(self, dx, dy):
        self.f = self.translated(dx, dy).f

    def scale(self, sx, sy):
        self.f = self.scaled(sy, sx).f

    def rotate(self, theta):
        self.f = self.rotated(theta).f

    @staticmethod
    def subs_2d(f, x_new, y_new):
        xx, yy = symbols("xx yy", real=True)
        xx_new = x_new.subs({x: xx, y: yy})
        yy_new = y_new.subs({x: xx, y: yy})
        tmp = f.subs({x: xx_new, y: yy_new})
        return tmp.subs({xx: x, yy: y})


class Disk2D(Geometry2D):
    def __init__(self, x0=0, y0=0, r=1, k=1 / 2):
        Geometry2D.__init__(self, sigmoid(r ** 2 - (x - x0) ** 2 - (y - y0) ** 2, k))


class HalfPlane2D(Geometry2D):
    def __init__(self, x0, y0, x1, y1, k=1 / 2):
        Geometry2D.__init__(self, sigmoid(HalfPlane2D.compute_f(x0, y0, x1, y1), k))

    @staticmethod
    def compute_f(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        return -dy * (x - x0) + dx * (y - y0)

# TODO: Create HalfPlane2D and HalfSpace3D Classes
