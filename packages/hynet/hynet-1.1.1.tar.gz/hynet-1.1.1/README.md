# Welcome to *hynet*

*hynet* is a package for the calculation of the optimal power flow (OPF) in hybrid AC/DC power systems. It supports power systems that comprise an arbitrary interconnection of AC grids and radial DC grids, i.e., point-to-point and radial multi-terminal HVDC systems. With respect to OPF methods, it supports the solution of the nonconvex quadratically constrained quadratic program (QCQP) as well as its semidefinite relaxation (SDR) and second-order cone relaxation (SOCR). Especially the SOCR is a computationally highly efficient approach for OPF and locational marginal pricing in power systems with the [hybrid architecture](http://ieeexplore.ieee.org/document/7997734/). For more information, please refer to *hynet*'s documentation ([HTML](https://hynet.readthedocs.io)/[PDF](https://readthedocs.org/projects/hynet/downloads/pdf/latest/)) and [this paper](https://arxiv.org/abs/1811.10496).

*hynet* uses [SQLite](https://www.sqlite.org/)-based SQL databases to store grid infrastructure and scenario information. Several grid databases are provided [here](https://gitlab.com/tum-msv/hynet-databases), including a hybrid AC/DC adaptation of the [PJM test system](https://ieeexplore.ieee.org/document/5589973) and a model of the [German transmission grid](https://ieeexplore.ieee.org/document/8278744/), both with several different scenarios, as well as an import of all test cases of the [Power Grid Lib - Optimal Power Flow](https://github.com/power-grid-lib/pglib-opf).


## Installation

*hynet* was developed for Python 3.5 and higher and requires [NumPy](http://www.numpy.org/), [SciPy](https://www.scipy.org/), [pandas](https://pandas.pydata.org/), [SQLAlchemy](https://www.sqlalchemy.org/), [Matplotlib](https://matplotlib.org/), [h5py](https://www.h5py.org/) as well as at least one of the supported [solvers](#solvers). For a convenient installation, the Python distribution [Anaconda](http://www.anaconda.com/download/) (or the stripped-down [Miniconda](https://conda.io/miniconda.html)) may be used, where the included package manager [Conda](https://conda.io) supports a straightforward installation of the supported solvers.


To install *hynet* using Python's package management system, run

```sh
pip install hynet
```

The installation of *hynet* and the installed [solvers](#solvers) can be tested with

```sh
python -m hynet test
```

To install *hynet* from its sources, get the latest source code by cloning the *hynet* repository with [Git](https://git-scm.com/) via

```sh
git clone https://gitlab.com/tum-msv/hynet.git
```

and initiate the installation with

```sh
python setup.py install
```


### Solvers

In the following, the supported solvers are listed. **Currently, the utilization of the following solvers is recommended: [IPOPT](#ipopt) for the QCQP, [MOSEK](#mosek) for the SDR, and [MOSEK](#mosek) or [CPLEX](#ibm-ilog-cplex) for the SOCR.** Regarding the latter, it was found empirically that CPLEX is more robust while MOSEK is computationally more efficient. Please note that **even if only QCQPs are solved, it is recommended to install MOSEK or CPLEX**, as they enable the efficient computation an initial point for QCQP solvers.


#### IPOPT

[IPOPT](https://projects.coin-or.org/Ipopt) is an open-source software package for large-scale nonlinear optimization and [CYIPOPT](https://github.com/matthias-k/cyipopt) is a Python wrapper for IPOPT. With [Conda](https://conda.io), both can be installed as follows.

* Linux and MAC OS X:

```sh
conda install -c conda-forge cyipopt
```

* Windows:

```sh
conda install -c pycalphad cyipopt
```

#### MOSEK

[MOSEK](http://www.mosek.com) is an interior-point optimizer for large-scale conic optimization problems. It is commercial, but offers a **[free academic license](https://www.mosek.com/products/academic-licenses/)**. With [Conda](https://conda.io), MOSEK can be installed with

```sh
conda install -c mosek mosek
```


#### IBM ILOG CPLEX

[CPLEX](http://www.ibm.com/analytics/cplex-optimizer) is a high-performance mathematical programming solver for linear, mixed integer, quadratic, and quadratically constrained programming problems. It is commercial, but offers a **[free academic license](http://www.ibm.com/products/ilog-cplex-optimization-studio)** through the [IBM Academic Initiative](http://developer.ibm.com/academic/accessresources/). For the installation, please refer to the instructions provided with CPLEX and the section "Setting up the Python API of CPLEX" of the CPLEX documentation.


#### PICOS

*hynet* supports the solution of the SDR and SOCR with [PICOS](http://picos.zib.de/index.html). However, the additional modeling layer causes a performance drawback. [PICOS](http://picos.zib.de/index.html) is an open-source Python-based modeling language for linear and conic optimization problems. It supports several solvers, including the open-source solver [CVXOPT](http://cvxopt.org). With Python's package management system, PICOS and CVXOPT can be installed with

```sh
pip install picos cvxopt
```


#### PYOMO

*hynet* supports the solution of the QCQP with [Pyomo](http://www.pyomo.org/). However, the additional modeling layer causes a performance drawback. Furthermore, the import of Pyomo is demanding and **slows down the import** of *hynet* significantly, thus the installation is only recommended if Pyomo is actually utilized. [Pyomo](http://www.pyomo.org/) is an open-source optimization modeling language and includes support for the solver [IPOPT](https://projects.coin-or.org/Ipopt). With [Conda](https://conda.io), both can be installed with

```sh
conda install -c conda-forge pyomo
conda install -c cachemeorg ipopt_bin
```


## Usage

Open a terminal, navigate to the directory that contains the [grid databases](https://gitlab.com/tum-msv/hynet-databases), and start a Python shell, either the standard shell (``python``) or a more convenient one like [IPython](https://ipython.org) or [ptpython](https://github.com/jonathanslenders/ptpython). At the Python command prompt, import *hynet* via

```python
import hynet as ht
```

To access the data of the system in the file ``pjm_hybrid.db``, connect to this database using

```python
database = ht.connect('pjm_hybrid.db')
```

The optimal power flow for the default scenario of this system can then be calculated with

```python
result = ht.calc_opf(database)
```

The object ``result`` contains all result data. For example, to print a summary, print details of the solution, and access the determined bus voltages, type

```python
print(result)
print(result.details)
result.bus['v']
```

By default, *hynet* selects the most appropriate solver among those installed. To specify the type of solver explicitly, set the ``solver_type`` as illustrated below.

```python
ht.calc_opf(database, solver_type=ht.SolverType.QCQP)
ht.calc_opf(database, solver_type=ht.SolverType.SDR)
ht.calc_opf(database, solver_type=ht.SolverType.SOCR)
```

In case that the scenario shall be modified prior to the OPF calculation, it can be loaded explicitly via

```python
scenario = ht.load_scenario(database)
```

For example, to set the load at bus 2 to 100MW and 50Mvar, use

```python
scenario.bus.at[2, 'load'] = 100 + 50j
```

The optimal power flow for this modified scenario can be calculated with

```python
ht.calc_opf(scenario)
```

For more information and usage examples, please refer to the tutorials in [USAGE.md](https://gitlab.com/tum-msv/hynet/blob/master/USAGE.md), *hynet*'s documentation ([HTML](https://hynet.readthedocs.io)/[PDF](https://readthedocs.org/projects/hynet/downloads/pdf/latest/)), and [this paper](https://arxiv.org/abs/1811.10496).


## Contributing

Contributions to *hynet* are very welcome.  Please refer to [CONTRIBUTING.md](https://gitlab.com/tum-msv/hynet/blob/master/CONTRIBUTING.md) for more information. In case that *hynet* is useful to you, we would appreciate if you star this project.


## Credits

This software was developed at the [Professur für Methoden der Signalverarbeitung](http://www.msv.ei.tum.de/), [Technische Universität München](https://www.tum.de/) (TUM). The principal developer and project maintainer is Matthias Hotz (@matthias_hotz), who would like to recognize the highly appreciated support of the following contributors:

- Vincent Bode (TUM): Database management, network graph export
- Michael Mitterer (TUM): Distributed computation, MATPOWER import, database management
- Christian Wahl (TUM): Capability region visualizer, CI configuration
- Yangyang He (TUM): CVXPY and PICOS solver interface
- Julia Sistermanns (TUM): Feature- and structure-preserving network reduction


## Citation

In case that *hynet* is used in the preparation of a scientific publication, we would appreciate the citation of the following work:

> M. Hotz and W. Utschick, "*hynet:* An optimal power flow framework for hybrid AC/DC power systems," arXiv:1811.10496, Nov. 2018. \[Online\]. Available: [http://arxiv.org/abs/1811.10496](http://arxiv.org/abs/1811.10496)

The corresponding BibTeX entry is provided below.

```
@article{Hotz2018,
    Author = {Matthias Hotz and Wolfgang Utschick},
    Journal = {arXiv:1811.10496},
    Month = {Nov.},
    Title = {\textit{{hynet}:} {A}n Optimal Power Flow Framework for Hybrid {AC}/{DC} Power Systems},
    Url = {http://arxiv.org/abs/1811.10496v1},
    Year = {2018}}
```

Furthermore, in case that the feature- and structure-preserving network reduction functionality in *hynet* is utilized, we would appreciate the citation of the following work:

> J. Sistermanns, M. Hotz, D. Hewes, R. Witzmann, and W. Utschick, "[Feature- and Structure-Preserving Network Reduction for Large-Scale Transmission Grids](http://arxiv.org/abs/1903.11590)," 13th IEEE PES PowerTech Conf., Milano, Italy, Jun. 2019.


## License

[BSD 3-clause license](https://gitlab.com/tum-msv/hynet/blob/master/LICENSE)
