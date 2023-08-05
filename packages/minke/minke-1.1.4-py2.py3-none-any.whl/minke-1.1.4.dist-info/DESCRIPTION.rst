===============================
Minke: The Burst MDC Factory
===============================

.. image:: https://zenodo.org/badge/53331163.svg
   :target: https://zenodo.org/badge/latestdoi/53331163
..

   .. image:: https://img.shields.io/pypi/v/minke.svg
	   :target: https://pypi.python.org/pypi/minke

.. image:: https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg
	   :target: https://singularity-hub.org/collections/504
	   :alt: Singularity image 

.. image:: https://git.ligo.org/daniel-williams/minke/badges/master/pipeline.svg
	   :target: https://git.ligo.org/daniel-williams/minke/commits/master
	   :alt: Pipeline Status

.. image:: https://code.daniel-williams.co.uk/minke/_images/minke.png
	   :alt: Project Minke Logo

.. image:: https://git.ligo.org/daniel-williams/minke/badges/master/coverage.svg
	   :target: https://git.ligo.org/daniel-williams/minke/commits/master"
	   :alt: Coverage report



Minke is a Python package to produce Mock Data Challenge data sets for LIGO interferometers.

* Free software: ISC license
* Documentation: https://code.daniel-williams.co.uk/minke

Features
--------

* Produces burst MDCs with Gaussian, SineGaussian, and White Noise Burst ad-hoc waveforms
* Produces ringdown waveforms for MDCs
* Produces numerical relativity burst MDCs for supernovae
* Produces numerical relativity burst MDCs for long duration searches
* Produces GWF frame files for MDCs
* Produces GravEn-format log files for MDCs
* Produces hardware-injection ready data files
* Produces SimBurstTable XML files for MDCs



=======
History
=======

1.1.1 (2018-03-27)
------------------
* Made a change to the package meta data to allow upload to PYPI.

1.1.0 (2018-03-27)
------------------
"Luce Bay"

* Added full support for hardware injection production
* Added Yakunin Supernova waveform family
* Added Ringdow waveform support
* Added support for all lscsoft table formats
* Added support for editing xml files
* Added support for String Cusp waveforms

1.0.1 (2017-01-23)
------------------
* Added provisional support for hardware injection production

1.0.0 (2016-09-14)
------------------
The Anniversary Update.

* ER10 and O2 Readiness
* Fully capable of producing supernova injections
* Fully capable of producing lalsimulation-burst waveforms
* Extensible interface for parameter distributions

0.1.0 (2016-3-14)
------------------

* First release on PyPI.


