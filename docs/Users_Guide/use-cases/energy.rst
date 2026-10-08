.. _use-case-energy:

Renewable Energy Forecasting
============================

Objective
---------

This use case demonstrates WRF simulations configured for renewable energy
forecasting applications, including solar and wind energy research.
WRF is initialized and forced at the boundaries using hourly HRRR
(High-Resolution Rapid Refresh) data downloaded from the NOAA AWS archive.
The physics configuration includes coupled farm radiation, topographic shading,
and aerosol-aware microphysics suited for energy applications.

Version Added
-------------

Update section with the version of i-wrf this use case was added to.

Datasets
--------

* **Initial and boundary conditions**: HRRR pressure-level GRIB2 files
  (``wrfprsf*``) downloaded from the NOAA AWS public archive.
* **Geographic data**: WPS_GEOG high-resolution mandatory dataset.
* **Aerosol climatology**: QNWFA/QNIFA/QNBCA monthly climatology file
  required for Thompson aerosol-aware microphysics.

Running This I-WRF Use Case
---------------------------

Instructions are provided below for running the Renewable Energy use case
on each :ref:`compute-platform` on which it has been tested.

.. include:: energy/nsf-ncar.rst
.. include:: energy/jetstream2.rst
