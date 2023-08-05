A Python Interface to Conic Optimization Solvers
================================================

PICOS is a user friendly Python API to several conic and integer programming
solvers, very much like [YALMIP](http://users.isy.liu.se/johanl/yalmip/) or
[CVX](http://cvxr.com/cvx/) under [MATLAB](http://www.mathworks.com/).

PICOS allows you to enter a mathematical optimization problem as a **high level
model**, with painless support for **(complex) vector and matrix variables** and
**multidemensional algebra**. Your model will be transformed to the standard
form understood by an appropriate solver that is available at runtime. This
makes your application **portable** as users have the choice between several
commercial and open source solvers.

Features
--------

PICOS runs under both **Python 2** and **Python 3** and supports the following
solvers and problem types. To use a solver, you need to seperately install it
along with the Python interface listed here.

| Solver | Interface | [LP](https://en.wikipedia.org/wiki/Linear_programming) | [SOCP](https://en.wikipedia.org/wiki/Second-order_cone_programming) | [SDP](https://en.wikipedia.org/wiki/Semidefinite_programming) | [QCQP](https://en.wikipedia.org/wiki/Quadratically_constrained_quadratic_program) | [EXP](https://docs.mosek.com/modeling-cookbook/expo.html) | [MIP](https://en.wikipedia.org/wiki/Integer_programming) | License |
| --------------------------------------------------------- | ---------------------------------------------------------- | --- | --- | --- | --- | --- | --- | -------- |
| [CPLEX](https://www.ibm.com/analytics/cplex-optimizer)    | included                                                   | Yes | Yes |     | Yes |     | Yes | non-free |
| [CVXOPT](https://cvxopt.org/)                             | native                                                     | Yes | Yes | Yes | Yes | Yes¹|     | [GPL-3](https://www.gnu.org/licenses/gpl-3.0.html) |
| [ECOS](https://www.embotech.com/ECOS)                     | [ecos-python](https://github.com/embotech/ecos-python)     | Yes | Yes |     | Yes | Yes | Yes | [GPL-3](https://www.gnu.org/licenses/gpl-3.0.html) |
| [GLPK](https://www.gnu.org/software/glpk/)                | [swiglpk](https://github.com/biosustain/swiglpk)           | Yes |     |     |     |     | Yes | [GPL-3](https://www.gnu.org/licenses/gpl-3.0.html) |
| [Gurobi](http://www.gurobi.com/products/gurobi-optimizer) | included                                                   | Yes | Yes |     | Yes |     | Yes | non-free |
| [MOSEK](https://www.mosek.com/)                           | included                                                   | Yes | Yes | Yes | Yes |     | Yes | non-free |
| [SMCP](http://smcp.readthedocs.io/en/latest/)             | native                                                     | Yes²| Yes²| Yes | Yes²|     |     | [GPL-3](https://www.gnu.org/licenses/gpl-3.0.html) |
| [SCIP](http://scip.zib.de/)                               | [PySCIPOpt](https://github.com/SCIP-Interfaces/PySCIPOpt/) | Yes | Yes |     | Yes |     | Yes | [ZIB](https://scip.zib.de/academic.txt)/[MIT](https://github.com/SCIP-Interfaces/PySCIPOpt/blob/master/LICENSE) |

¹ only [geometric programming](https://en.wikipedia.org/wiki/Geometric_programming),
² experimental

### Example

This is what it looks like to solve a multidimensional mixed integer program
with PICOS:

```python
>>> import picos
>>> P = picos.Problem()
>>> x = P.add_variable("x", 2, vtype="integer")
>>> C = P.add_constraint(x <= 5.5)
>>> P.set_objective("max", 1|x) # 1|x is the sum over x
>>> solution = P.solve(verbose = 0)
>>> print(solution["status"])
'integer optimal solution'
>>> print(P.obj_value())
10.0
>>> print(x)
[ 5.00e+00]
[ 5.00e+00]
>>> print(C.slack)
[ 5.00e-01]
[ 5.00e-01]
```

### Documentation & Source

- The full documentation can be browsed
[online](https://picos-api.gitlab.io/picos/)
or downloaded
[in PDF form](https://gitlab.com/picos-api/picos/-/jobs/artifacts/master/raw/picos.pdf?job=pdfdoc).
- The API documentation without the tutorial and examples is also available as a
[separate PDF](https://gitlab.com/picos-api/picos/-/jobs/artifacts/master/raw/picos-api.pdf?job=pdfdoc).
- The source code lives on [GitLab](https://gitlab.com/picos-api/picos).

Installation
------------

### Via pip

If you are using [pip](https://pypi.org/project/pip/) you can run
``pip install picos`` to get the latest version.

### Via Anaconda

If you are using [Anaconda](https://anaconda.org/) you can run
``conda install -c picos picos`` to get the latest version.

### Via your system's package manager

On **Arch Linux**, there are seperate packages in the AUR for the
[latest version](https://aur.archlinux.org/packages/python-picos-git/) and the
[latest release](https://aur.archlinux.org/packages/python-picos/). Both are
split packages that ship both Python 2 and Python 3 versions of PICOS.

If you are packaging PICOS for additional systems, please tell us so we can list
your package here!

### From source

If you are installing PICOS manually, you can choose between a number of
[development versions](https://gitlab.com/picos-api/picos/branches) and
[source releases](https://gitlab.com/picos-api/picos/tags).
You will need to have at least the following Python packages installed:

- [NumPy](http://www.numpy.org/)
- [CVXOPT](https://cvxopt.org/)

Credits
-------

### Developers

- [Guillaume Sagnol](http://page.math.tu-berlin.de/~sagnol/) is PICOS' initial
  author and primary developer since 2012.
- [Maximilian Stahlberg](about:blank) is extending and maintaining PICOS since
  2017.

### Contributors

For an up-to-date list of all code contributors, please refer to the
[contributors page](https://gitlab.com/picos-api/picos/graphs/master).
Should a reference from before 2019 be unclear, you can refer to the
[old contributors page](https://github.com/gsagnol/picos/graphs/contributors)
on GitHub as well.

License
-------

PICOS is free and open source software and available to you under the terms of
the [GNU GPL v3](https://gitlab.com/picos-api/picos/raw/master/LICENSE.txt).
