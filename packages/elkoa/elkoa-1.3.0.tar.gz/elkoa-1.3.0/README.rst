Elk Optics Analyzer (ElkOA)
---------------------------

|Python version| |PyPi version| |Code style: black| |License: GPL v3+|

Description
~~~~~~~~~~~

Elk Optics Analyzer (ElkOA) helps to analyze optics output data from
`The Elk Code <http://elk.sourceforge.net>`__.

Features
~~~~~~~~

Elk Optics Analyzer…

-  Comes with a GUI as well as a python CLI
-  Supports Elk tasks 121, 187, 320 and 330
-  Recognizes available tasks / (tensor) fields automatically
-  Is easily extendable

Users can…

-  Visualize real and imaginary parts of Elk optics output data in
   various ways
-  Import additional data files, e.g. experimental measurements Ctrl+O
-  Convert response functions via `Universal Response
   Relations <https://arxiv.org/abs/1401.6800>`__, e.g. ε ➙ σ Ctrl+C
-  Convert dielectric tensors into (extra-)ordinary refractive indices
   for arbitrary wavevectors Ctrl+C
-  Select tensor elements to plot individually via dialog Ctrl+T
-  Use global tensor elements settings for all plots Ctrl+G
-  Batch-load parameter studies to visually analyze the impact of
   different parameter settings Ctrl+B
-  Write out displayed data in different formats Ctrl+W

Soon to come:

-  3D-plotting of index ellipsoids
-  Batch-convert for a set of different q-points
-  Sample/geometry-dependent (i.e. thin films) conversions of response
   functions

Requirements
~~~~~~~~~~~~

-  `Python 3.x <https://www.python.org>`__
-  `numpy <https://www.numpy.org/>`__
-  `matplotlib <https://matplotlib.org>`__
-  `PyQt5 <http://pyqt.sourceforge.net/Docs/PyQt5/installation.html>`__
-  `pbr <https://docs.openstack.org/pbr/latest/>`__

You should use the packages provided by your linux distribution. On
recent Debian systems for example, you can get all requirements by
running

.. code:: bash

   apt install python3-numpy python3-matplotlib python3-pyqt5 python3-pbr

Alternatively, you can get the latest PyPI versions of each package
automatically by installing via pip (see below).

For testing purposes, you additionally need the following packages: \*
pytest \* pytest-qt \* pytest-mpl \* nose

Installation
~~~~~~~~~~~~

The easiest way to install ElkOA is via pip, either from PyPI directly

.. code:: bash

   pip install elkoa

or, if you want the latest git version,

.. code:: bash

   git clone https://github.com/PandaScience/ElkOpticsAnalyzer.git
   cd ElkOpticsAnalyzer
   pip install .

This will also install all required but absent python packages
automatically from PyPI.

If you like to install ElkOA only for the current user, add the flag
``--user``. If you want to take care of the required python packages
yourself (i.e. by using the ones provided by your Linux distribution),
add ``--no-deps``. If you like to run a developer installation (no
copying of files, instead use git repo files directly), add ``-e``.

In any case, after installation you can run the ElkOA GUI from
everywhere in a terminal using either ``elkoa`` or
``ElkOpticsAnalyzer``.

Another way to install is by cloning the repo as above and instead of
installing via pip, put something like

.. code:: bash

   export PATH=$PATH:/path/to/ElkOpticsAnalyzer/elkoa/gui
   export PYTHONPATH=$PYTHONPATH:/path/to/ElkOpticsAnalyzer/

to your ``.bashrc`` or ``.bash_profile``. Then you can start the ElkOA
GUI with ``ElkOpticsAnalyzer.py``.

Tests
~~~~~

Testing is done using the ``pytest`` library. Make sure you installed
all additional requirements beforehand.

1. Download and extract the sample data

   -  TODO

2. Run (–mpl flag is mandatory!)

.. code:: python

       pytest test_figures.py --mpl

Python CLI
~~~~~~~~~~

In an Elk output directory containing e.g. the files

.. code:: bash

   elk.in INFO.OUT EPSILON_11.OUT EPSILON_12.OUT EPSILON_13.OUT EPSILON_21.OUT
   EPSILON_22.OUT EPSILON_23.OUT EPSILON_31.OUT EPSILON_32.OUT EPSILON_33.OUT

you can run in a python3 interpreter:

.. code:: python

   from elkoa.utils import elk, io, convert
   # parse Elk input file
   elk_input = elk.ElkInput()
   # read specific input parameter
   eta = elk.readElkInputParameter("swidth")
   # read tensorial Elk optics output (ij = dummy for 11, 12, etc.)
   freqs, epsilon = io.readTenElk("EPSILON_TDDFT_ij.OUT")
   # create converter instance
   q = [0, 0, 0]
   converter = convert.Converter(q, freqs, eta, opticalLimit=True)
   # convert dielectric tensor to optical conductivity
   sigma = converter.epsilonToSigma(epsilon)
   # write out converted tensor
   io.writeTensor("sigma_ij_test.dat", freqs, sigma, threeColumn=True)
   # write out 11-element of converted tensor
   io.writeScalar("sigma_11-scalar.dat", freqs, sigma[0, 0, :], threeColumn=True)

Misc
~~~~

-  Auto-converting filenames to tex-labels

   -  For this feature to work, filenames must follow the pattern
      ``root``\ +\ ``_sub``\ +\ ``.ext``, which will show up as rootsub.
   -  In case ``root`` contains a case-insensitive substring like eps,
      EPSILON, Sig, SIGma etc., corresponding greek letters will be
      used, i.e. eps_ex.dat ➙ εex.

-  Additional data plots

   -  Number is restricted to 6, but in return we use consistent
      coloring after consecutively adding more plots.

Usage Examples GUI
~~~~~~~~~~~~~~~~~~

|see https://github.com/PandaScience/ElkOpticsAnalyzer/| |and
https://github.com/PandaScience/ElkOpticsAnalyzer/|

.. |Python version| image:: https://img.shields.io/pypi/pyversions/elkoa.svg?style=flat-square
   :target: pypi.org/project/elkoa/
.. |PyPi version| image:: https://img.shields.io/pypi/v/elkoa.svg?style=flat-square
   :target: pypi.org/project/elkoa/
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square
   :target: https://github.com/python/black
.. |License: GPL v3+| image:: https://img.shields.io/pypi/l/elkoa.svg?style=flat-square
   :target: http://www.gnu.org/licenses/gpl-3.0
.. |see https://github.com/PandaScience/ElkOpticsAnalyzer/| image:: screenshots/basic.gif
.. |and https://github.com/PandaScience/ElkOpticsAnalyzer/| image:: screenshots/batchload.gif

