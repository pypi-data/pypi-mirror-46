Rmdawn: a Python package for programmatic R markdown workflows
==============================================================

1. Create R markdown (Rmd) files from YAML, code, and markdown files.
2. Extract YAML, code, and markdown files from R markdown files.

|PyPI| |Updates|

The ``rmdawn`` Python package consists of 2 shell commands and
functions:

- ``rmdawn``, which concatenates input files to output an `R Markdown <https://rmarkdown.rstudio.com/authoring_quick_tour.html>`__ (Rmd) file.
- ``rmdusk``, which extracts 1) a YAML file, 2) Python or R scripts and 3) `Markdown <https://www.markdownguide.org/>`__ (md) files from Rmd files.


Installation
------------

.. code:: sh

    pip install rmdawn


.. |PyPI| image:: https://img.shields.io/pypi/v/rmdawn.svg
   :target: https://pypi.python.org/pypi/rmdawn
.. |Updates| image:: https://pyup.io/repos/github/marskar/rmdawn/shield.svg
   :target: https://pyup.io/repos/github/marskar/rmdawn/
