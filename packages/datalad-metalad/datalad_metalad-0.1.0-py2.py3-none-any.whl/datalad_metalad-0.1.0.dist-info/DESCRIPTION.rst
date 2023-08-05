DataLad extension for semantic metadata handling
================================================

`Travis tests status <https://travis-ci.org/datalad/datalad-metalad>`__
`Build status <https://ci.appveyor.com/project/mih/datalad-metalad>`__
`codecov.io <https://codecov.io/github/datalad/datalad-metalad?branch=master>`__
`GitHub
release <https://GitHub.com/datalad/datalad-metalad/releases/>`__ `PyPI
version fury.io <https://pypi.python.org/pypi/datalad-metalad/>`__
`Documentation <http://docs.datalad.org/projects/metalad>`__

This software is a `DataLad <http://datalad.org>`__ extension that
equips DataLad with an alternative command suite for metadata handling
(extraction, aggregation, reporting). It is backward-compatible with the
metadata storage format in DataLad proper, while being substantially
more performant (especially on large dataset hierarchies). Additionally,
it provides new metadata extractors and improved variants of DataLad’s
own ones that are tuned for better performance and richer, JSON-LD
compliant metadata reports.

Command(s) currently provided by this extension

-  ``meta-extract`` – new and improved dedicated command to run any and
   all of DataLad’s metadata extractors.
-  ``meta-aggregate`` – complete reimplementation of metadata
   aggregation, with stellar performance benefits, in particular on
   large dataset hierarchies.
-  ``meta-report`` – new command to specifically access the aggregated
   metadata present in a dataset, much faster and more predictable
   behavior than the ``metadata`` command in datalad-core.

Additional metadata extractor implementations

-  ``metalad_core`` – enriched variant of the ``datalad_core`` extractor
   that yields valid JSON-LD
-  ``metalad_annex`` – refurbished variant of the ``annex`` extractor
   using the metalad extractor API
-  ``metalad_custom`` – read pre-crafted metadata from shadow/side-care
   files for a dataset and/or any file in a dataset.

Installation
------------

Before you install this package, please make sure that you `install a
recent version of
git-annex <https://git-annex.branchable.com/install>`__. Afterwards,
install the latest version of ``datalad-metalad`` from
`PyPi <https://pypi.org/project/datalad-metalad>`__. It is recommended
to use a dedicated `virtualenv <https://virtualenv.pypa.io>`__:

::

   # create and enter a new virtual environment (optional)
   virtualenv --system-site-packages --python=python3 ~/env/datalad
   . ~/env/datalad/bin/activate

   # install from PyPi
   pip install datalad_metalad

Support
-------

For general information on how to use or contribute to DataLad (and this
extension), please see the `DataLad website <http://datalad.org>`__ or
the `main GitHub project page <http://datalad.org>`__. The documentation
is found here: http://docs.datalad.org/projects/metalad

All bugs, concerns and enhancement requests for this software can be
submitted here: https://github.com/datalad/datalad-metalad/issues

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


