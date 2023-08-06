hiPhive
=======

**hiPhive** is a tool for efficiently extracting high-order force constants
from atomistic simulations, most commonly density functional theory
calculations. A detailed description of the functionality provided as well as an
extensive tutorial can be found in the
`user guide <https://hiphive.materialsmodeling.org/>`_

**hiPhive** is written in Python, which allows
easy integration with countless first-principles codes and analysis tools
accessible in Python, and allows for a simple and intuitive user interface. For
example using the following snippet one can train a force constant potential:

.. code-block:: python

   cs = ClusterSpace(primitive_cell, cutoffs)
   sc = StructureContainer(cs, list_of_training_structure)
   opt = Optimizer(sc.get_fit_data())
   opt.train()
   fcp = ForceConstantPotential(cs, opt.parameters)

after wich it can be used in various ways, e.g., for generating phonon
dispersions, computing phonon lifetimes, or running molecular dynamics
simulations.


Installation
------------
**hiPhive** can be installed via `pip`::

    pip3 install hiphive

If you want to get the absolutely latest (development) version you can clone the repo and then install **hiPhive** via::

  git clone git@gitlab.com:materials-modeling/hiphive.git
  cd hiphive
  python3 setup.py install --user

**hiPhive** requires Python3 and invokes functionality from
several external libraries including the
`atomic simulation environment <https://wiki.fysik.dtu.dk/ase>`_,
`spglib <https://atztogo.github.io/spglib/>`_ and
`SymPy <http://www.sympy.org/en/index.html>`_.
Please note that the dependency on
`scikit-learn <http://scikit-learn.org/>`_
is not enforced during installation via `pip`.
Please consult the
`installation section of the user guide <https://hiphive.materialsmodeling.org/installation.html>`_
for details.


Authors
-------
* Fredrik Eriksson
* Erik Fransson
* Paul Erhart

**hiPhive** has been developed at Chalmers University of Technology in
Gothenburg, Sweden, in the
`Materials and Surface Theory division <http://www.materialsmodeling.org>`_
at the Department of Physics.
