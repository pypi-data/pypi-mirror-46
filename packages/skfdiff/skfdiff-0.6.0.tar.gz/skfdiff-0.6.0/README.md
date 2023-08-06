# Scikit-fdiff / skfdiff (formerly Triflow)

The full documentation is available on [read the doc.](https://scikit-fdiff.readthedocs.io/en/latest/)

|                                                                       master                                                                       |                                                                     dev                                                                      |
| :------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------: |
| [![pipeline status](https://gitlab.com/celliern/scikit-fdiff/badges/master/pipeline.svg)](https://gitlab.com/celliern/scikit-fdiff/commits/master) | [![pipeline status](https://gitlab.com/celliern/scikit-fdiff/badges/dev/pipeline.svg)](https://gitlab.com/celliern/scikit-fdiff/commits/dev) |

- [Scikit-fdiff / skfdiff (formerly Triflow)](#scikit-fdiff--skfdiff-formerly-triflow)
  - [Installation](#installation)
    - [External requirements](#external-requirements)
    - [via PyPI](#via-pypi)
    - [via github](#via-github)
  - [Introduction](#introduction)
    - [Rational](#rational)
  - [Model writing](#model-writing)
    - [Toy examples (more ambitious one are in the doc)](#toy-examples-more-ambitious-one-are-in-the-doc)
      - [1D advection / diffusion system, Dirichlet boundary](#1d-advection--diffusion-system-dirichlet-boundary)
      - [2D advection / diffusion system, mixed robin / periodic boundary](#2d-advection--diffusion-system-mixed-robin--periodic-boundary)
    - [Contributing](#contributing)
    - [Code of Conduct](#code-of-conduct)

## Installation

### External requirements

This library is written for python &gt;= 3.6.

On v0.6.0, it is possible to choose between numpy and numba
(which provide similar features). numpy will be slower but with
no compilation time, which is handy for testing and prototyping.
On other hand, numba use a JIT compilation, and give access to
faster and parallized routines in the cost of an extra dependency
and a warm-up time.

### via PyPI

```bash
pip install skfdiff[numba,interactive]
```

will install the package and

```bash
pip install skfdiff --upgrade
```

will update an old version of the library.

### via github

You can install the latest version of the library
using pip and the github repository:

```bash
pip install git+git://github.com/locie/skfdiff.git
```

## Introduction

### Rational

The aim of this library is to have a (relatively) easy way to write
transient dynamic systems finite difference discretization, with
fast temporal solvers.

The main two parts of the library are:

- symbolic tools defining the spatial discretization, with boundary
    taking into account in a separated part
- a fast temporal solver written in order to use the sparsity of the
    finite difference method to reduce the memory and CPU usage during
    the solving

Moreover, extra tools are provided and the library is written in a
modular way, allowing an easy extension of these different parts (see
the plug-in module of the library.)

The library fits well with an interactive usage (in a jupyter notebook).
The dependency list is actually larger, but on-going work target a
reduction of the stack complexity.

## Model writing

All the models are written as function generating the F
vector and the Jacobian matrix of the model defined as ``dtU = F(U)``.

The symbolic model is written as a simple mathematic equation. For
example, a diffusion advection model can be written as:

```python
from skfdiff import Model

equation_diff = "k * dxxU - c * dxU"
dependent_var = "U"
physical_parameters = ["k", "c"]

model = Model(equation_diff, dependent_var,
              physical_parameters)
```

### Toy examples (more ambitious one are in the doc)

#### 1D advection / diffusion system, Dirichlet boundary

```python
>>> import pylab as pl
>>> import numpy as np
>>> from skfdiff import Model, Simulation

>>> model = Model("k * dxxU - c * dxU",
...               "U(x)", ["k", "c"],
...               boundary_conditions={("U", "x"): ("dirichlet", "dirichlet")}
...               )

>>> x, dx = np.linspace(0, 1, 200, retstep=True)
>>> U = np.cos(2 * np.pi * x * 5)

# The fields are ``xarray.Dataset`` objects, and all the
# tools / methods available in the ``xarray`` lib can be
# applied to the skfdiff.Fields.
>>> fields = model.Fields(x=x, U=U, k=0.001, c=0.3)

# fix the boundary values for the dirichlet condition
>>> fields["U"][0] = 1
>>> fields["U"][-1] = 0

>>> t = 0
>>> dt = 5E-1
>>> tmax = 2.5

>>> simul = Simulation(model, fields, dt, tmax=tmax)

# The containers are in-memory or persistant
# xarray Dataset with all or some time-steps available.
>>> container = simul.attach_container()
>>> simul.run()
(2.5, <xarray.Dataset>
 Dimensions:  (x: 200)
 Coordinates:
   * x        (x) float64 0.0 ... 1.0
 Data variables:
     U        (x) float64 ...
     k        float64 0.001
     c        float64 0.3)

>>> for t in container.data.t:
...     fig = pl.figure()
...     plot = container.data["U"].sel(t=t).plot()

```

#### 2D advection / diffusion system, mixed robin / periodic boundary

```python
>>> import pylab as pl
>>> import numpy as np
>>> from skfdiff import Model, Simulation

# some specialized scheme as the upwind scheme as been implemented.
# as the problem as a strong advective component, we can use it
# to reduce the numerical instabilities.
# the dirichlet condition mean that the boundary will stay fix,
# keeping the initial value.
>>> model = Model("k * (dxxU + dyyU) - (upwind(cx, U, x, 2) + upwind(cy, U, y, 2))",
...               "U(x, y)", ["k", "cx", "cy"],
...               boundary_conditions={("U", "x"): ("dxU - (U - sin(y) * cos(t))", "dxU - 5"),
...                                    ("U", "y"):  "periodic"})

>>> x = np.linspace(0, 10, 56)
>>> y = np.linspace(-np.pi, np.pi, 32)

>>> U = np.zeros((x.size, y.size))
>>> fields = model.Fields(x=x, y=y, U=U, k=0.001, cx=0.8, cy=0.3)

>>> dt = 1.
>>> tmax = 15.

>>> simul = Simulation(model, fields, dt, tmax=tmax, tol=5E-1)
>>> container = simul.attach_container()

>>> simul.run()
(15.0, <xarray.Dataset>
 Dimensions:  (x: 56, y: 32)
 Coordinates:
   * x        (x) float64 0.0 ... 10.0
   * y        (y) float64 -3.142 ... 3.142
 Data variables:
     U        (x, y) float64 ...
     k        float64 0.001
     cx       float64 0.8
     cy       float64 0.3)

>>> for t in np.linspace(0, tmax, 5):
...     fig = pl.figure()
...     plot = container.data["U"].sel(t=t, method="nearest").plot()

```

### Contributing

See [the contribute section of the doc](https://scikit-fdiff.readthedocs.io/en/latest/contribute.html).

### Code of Conduct

See [the dedicated page](COC.md).