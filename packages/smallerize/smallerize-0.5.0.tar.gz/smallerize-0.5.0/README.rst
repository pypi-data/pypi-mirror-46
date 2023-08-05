==========
smallerize
==========


.. image:: https://img.shields.io/pypi/v/smallerize.svg
        :target: https://pypi.python.org/pypi/smallerize
        :alt: pip version

.. image:: https://gitlab.com/warsquid/smallerize/badges/master/pipeline.svg
        :target: https://gitlab.com/warsquid/smallerize/commits/master
        :alt: pipeline status
        
.. image:: https://gitlab.com/warsquid/smallerize/badges/master/coverage.svg
        :alt: Coverage

.. image:: https://readthedocs.org/projects/smallerize/badge/?version=latest
        :target: https://smallerize.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A Python implementation of minimisation for clinical trials


* Open source: Mozilla Public License 2.0
* Documentation: https://smallerize.readthedocs.io.
* Source: https://gitlab.com/warsquid/smallerize.


Features
--------

* Implements minimization as described in Pocock + Simon (1975): *Sequential
  treatment assignment with balancing for prognostic factors in the
  controlled clinical trial*
* Tested using ``pytest`` to ensure the results match the original
  implementation.
* Pure Python module with no dependencies (``pandas`` is useful when conducting
  simulations but is optional)
* Includes all functions described in the article: range, standard deviation,
  variance, etc.
* Also implements the biased-coin minimization method described in Han et al. (2009):
  *Randomization by minimization for unbalanced treatment allocation*, to
  allow for unequal allocation ratios.
* Allows pure random assignment for comparison
* Simulation module to allow simulating the effects of different assignment
  schemes.

Example
-------

Comparing minimization to purely random assignment by simulation:

.. image:: https://gitlab.com/warsquid/smallerize/raw/master/examples/ps1975_factor_imbalance.png
        :width: 1350
        :height: 600
        :scale: 50%
        :alt: Simulation results

See the example `notebook`_  for details of the simulation.

.. _notebook: https://gitlab.com/warsquid/smallerize/blob/master/examples/ps1975_simulations.ipynb

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
