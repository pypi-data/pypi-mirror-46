Revolutionary DataLad extension
===============================

`Travis tests
status <https://travis-ci.org/datalad/datalad-revolution>`__ `Build
status <https://ci.appveyor.com/project/mih/datalad-revolution>`__
`codecov.io <https://codecov.io/github/datalad/datalad-revolution?branch=master>`__
`GitHub
release <https://GitHub.com/datalad/datalad-revolution/releases/>`__
`PyPI version
fury.io <https://pypi.python.org/pypi/datalad-revolution/>`__
`Documentation <http://docs.datalad.org/projects/revolution>`__

This software is a `DataLad <http://datalad.org>`__ extension that
equips DataLad with alternative and additional core commands that are
leaner and written specifically with enhanced cross-platform
compatibility and speed in mind. Please see the `extension
documentation <http://docs.datalad.org/projects/revolution>`__ for a
description on additional commands and functionality.

**Note:** There is *no support* for `git-annex direct mode
repositories <https://git-annex.branchable.com/direct_mode>`__. Users
that previously relied on this mode, and Windows users in particular,
are recommended to use `git-annex V7
mode <https://git-annex.branchable.com/upgrades>`__. DataLad can be
instructed to always use this mode by running:

::

   git config --global --add datalad.repo.version 6

Command(s) currently provided by this extension

-  ``rev-extract-metadata`` – new and improved dedicated command to run
   any and all of DataLad’s metadata extractors. Much improved versions
   of the core extractor implementations also ship with this extension.
-  ``rev-aggregate-metadata`` – complete reimplementation of metadata
   aggregation, with stellar performance benefits, in particular on
   large dataset hierarchies.
-  ``query-metadata`` – new command to specifically access the
   aggregated metadata present in a dataset, much faster and more
   predictable behavior than the ``metadata`` command in datalad-core.

Installation
------------

Before you install this package, please make sure that you `install a
recent version of
git-annex <https://git-annex.branchable.com/install>`__. Afterwards,
install the latest version of ``datalad-revolution`` from
`PyPi <https://pypi.org/project/datalad-revolution>`__. It is
recommended to use a dedicated
`virtualenv <https://virtualenv.pypa.io>`__:

::

   # create and enter a new virtual environment (optional)
   virtualenv --system-site-packages --python=python3 ~/env/datalad
   . ~/env/datalad/bin/activate

   # install from PyPi
   pip install datalad_revolution

Support
-------

For general information on how to use or contribute to DataLad (and this
extension), please see the `DataLad website <http://datalad.org>`__ or
the `main GitHub project page <http://datalad.org>`__. The documentation
is found here: http://docs.datalad.org/projects/revolution

All bugs, concerns and enhancement requests for this software can be
submitted here: https://github.com/datalad/datalad-revolution/issues

If you have a problem or would like to ask a question about how to use
DataLad, please `submit a question to
NeuroStars.org <https://neurostars.org/tags/datalad>`__ with a
``datalad`` tag. NeuroStars.org is a platform similar to StackOverflow
but dedicated to neuroinformatics.

All previous DataLad questions are available here:
http://neurostars.org/tags/datalad/

Acknowledgements
----------------

DataLad development is supported by a US-German collaboration in
computational neuroscience (CRCNS) project “DataGit: converging
catalogues, warehouses, and deployment logistics into a federated ‘data
distribution’” (Halchenko/Hanke), co-funded by the US National Science
Foundation (NSF 1429999) and the German Federal Ministry of Education
and Research (BMBF 01GQ1411). Additional support is provided by the
German federal state of Saxony-Anhalt and the European Regional
Development Fund (ERDF), Project: Center for Behavioral Brain Sciences,
Imaging Platform. This work is further facilitated by the ReproNim
project (NIH 1P41EB019936-01A1).


