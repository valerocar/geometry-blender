# Geometry Blender

![Double Torus](images/tdt.png)

The library **geometry-blender** is designed to smoothly blend geometric objects 
using the following operations

- Union
- Intersection
- Subtraction
- Global Deformations

Solid objects in 3-dimensional are represented using 
smooth mathematical functions  `f = f(x,y,z)`, so that a point `(x,y,z)` belongs to
the object if and only if it satisfies the inequality

```python
f(x,y,z) <= 1/2
```

The border of such an object is a surface that consists of  set 
of points `(x,y,z)` that satisfy the equality

```python
f(x,y,z) == 1/2
```

We can mesh this *level set* using  algorithms like 
[Marching Cubes](https://en.wikipedia.org/wiki/Marching_cubes)
or 
[Marching Tetrahedra](https://en.wikipedia.org/wiki/Marching_tetrahedra), 
and then render into the screen by using a graphing system 
(like [plotly](https://plotly.com/python/)).

---
## Example: Double Torus in 3-dimensional space
(See Jupyter notebook [DoubleTorus.ipynb](demos/DoubleTorus.ipynb) )

We can create a *double torus* as follows. First, we join two lenticular shaped objects using the code

```python
b1 = Ball3D()
b1.scale(1/2,1/2,1/3)
b1.translate(-1/2,0,0)

b2 = Ball3D()
b2.scale(1/2,1/2,1/3)
b2.translate(1/2,0,0)

obj1 = b1 + b2
```

- The ball ``b1`` represent a ball radius `1` centered at the origin. We scale `b1` 
by a factor 
``1/2`` along the `x` and `y` plane and by a factor of `1/3` along the `z` axis; This 
produces a lenticular shaped object which is thinner in the ``z``-direction.
Next, we translate  `b1` by an amount of `-1/2` in the `x`-direction. 

- The object `b2` 
is constructed in a similar way, but is translated by an amount of `1/2` in the `x`-direction.

- Finally, we construct `obj1` as the blended sum (union) of `b1` and `b2` 
  (see Figure below)

![Double Torus](images/tdt0.png)


We now construct a new object `obj2` by making two holes to `obj1`. We
do this by subtracting  two cylinders `c1`
and `c2` from `obj1`. 

```python
c1 = Cylinder3D()
c1.scale(1/8,1/8,1)
c1.translate(-1/2,0,0)

c2 = Cylinder3D()
c2.scale(1/8,1/8,1)
c2.translate(1/2,0,0)

obj2 = obj1-(c1+c2)
```

![Double Torus](images/tdt1.png)

We can twist one of the  of *handles* of the double torus as follows

```python 
theta = pi/2
b2r = b2.rotated(1,0,0,theta)
c2r = c2.rotated(1,0,0,theta)
obj3 = (b1+b2r)-(c1+c2r)
```

The above code constructs `b2r` and `c2r` by rotating ``b2`` and ``c2`` an angle of ``pi/2``;
using the vector ``(1,0,0)`` as the axis of rotation. The resulting object `obj3` is shown in
the figure below. 

![Double Torus](images/tdt.png)
---
## Requirements and installation
To avoid package conflicts it is recommended to create a 
*Python Virtual Environment* 
for installation. This can be done at a terminal a follows

- Anaconda : `conda create --name geometry python=3`

We then need to activate this environment as follows:

- Anaconda : `conda activate geometry`


The packages *numpy*, *sympy* and *scikit-image* need to be present in the virtual 
environment. This can be achieved by typing (at a terminal)

- Anaconda : `conda install numpy sympy scikit-image`

Finally,  install the geometry-blender package by typing

`pip install geometry-blender`

---

# Jupyter notebook demos


The [demos](demos) folder contain Jupyter Notebooks that illustrate the usage of 
the library.



