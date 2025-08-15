.. _use-case-lulc:

Land Use/Land Cover Change
==========================

Scientific Objective
--------------------

The Land Use/Land Cover Change (LULC) use case examines how changes in
land surface characteristics impact weather patterns and atmospheric dynamics
through idealized modeling scenarios.
This science use case focuses on a deep convection system that passed over
the Dallas-Fort Worth (DFW) metropolitan region on July 4th, 2017,
and the simulations follow Zhou et al. 2024.
This exercise provides an introduction to running computationally complex
simulations and analyses using containerized applications.
METplus provides statistical analysis and evaluation tools to quantify these
meteorological impacts, making this verification workflow valuable for studies
in urban meteorology, land-atmosphere interactions,
and climate change impact assessment.

**Reference**

Zhou, X., Letson, F., Crippa, P. and Pryor, S.C., 2024. Urban effect on precipitation and deep convective systems over Dallas-Fort Worth. Journal of Geophysical Research: Atmospheres, 129(10), p.e2023JD039972.

Version Added
-------------

0.3

Datasets
--------

This use case runs the
`Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_
and `WRF Pre-Processing System (WPS) <https://github.com/wrf-model/WPS>`_
models with data from
`The High-Resolution Rapid Refresh (HRRR) <https://rapidrefresh.noaa.gov/hrrr/>`_
and modified meteorological data.

Running This I-WRF Use Case
---------------------------

Instructions a provided below for running the Land Use/Land Cover Change
use case for each :ref:`compute-platform` on which it has been tested.

.. include:: lulc/nsf-ncar.rst

.. include:: lulc/red-cloud.rst

.. include:: lulc/jetstream2.rst
