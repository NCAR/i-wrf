:orphan:

.. _lulcncarhpc:

***************************************************************
Running I-WRF on NCAR HPCs with Land Use/Land Cover Change Data
***************************************************************

Overview
========

Update section with an overview of the following instructions.

Prepare to Use NCAR HPCs
========================

Update section with instructions on how to set up the system to run i-wrf.

Examples include:

* Gaining access to the system
* Creating instances
* Managing instances.

Preparing the Environment
=========================

Load the apptainer module::

   module load apptainer

Create a working directory in the scratch area::

   IWRF_WORK_DIR=${SCRATCH}/iwrf_work

Create a directory to store the METplus output::

   LOCAL_OUTPUT_DIR=${IWRF_WORK_DIR}/metplus_out
   mkdir -p ${LOCAL_OUTPUT_DIR}

Create a directory to store temporary Apptainer files
($TMPDIR is set automatically for all users on NCAR HPC machines)::

   export APPTAINER_TMPDIR=${TMPDIR}
   mkdir -p ${APPTAINER_TMPDIR}

Clone the I-WRF GitHub repository to get the configuration files::

   git clone https://github.com/NCAR/i-wrf ${IWRF_WORK_DIR}/i-wrf

Install Docker and Pull Docker Objects
======================================

Update section with instructions on how to install Docker and pull docker images needed.

Download Data for WRF
=====================

Update section with instructions on how to download the data needed to run WRF.

Run WRF
=======

Update section with instructions on how to run WRF.

Run METplus
===========

Pull the METplus and input data containers from DockerHub. ::

   apptainer pull ${IWRF_WORK_DIR}/iwrf-metplus.sif docker://ncar/iwrf-metplus:latest
   apptainer pull ${IWRF_WORK_DIR}/data-lulc-input-obs.sif docker://ncar/iwrf-data:lulc-input-obs-d03.apptainer
   apptainer pull ${IWRF_WORK_DIR}/data-lulc-input-wrf.sif docker://ncar/iwrf-data:lulc-input-wrf-d03.apptainer

Set environment variables to bind directories to the container

* Input data directories for WRF and radar observation input data
   * WRF:
      * Local: From data-lulc-input-wrf.sif
      * Container: /data/input/wrf
   * OBS:
      * Local: From data-lulc-input-obs.sif
      * Container: /data/input/obs
* Config directory containing METplus use case configuration file
   * Local: ${IWRF_WORK_DIR}/i-wrf/use_cases/Land_Use_Land_Cover/METplus
   * Container: /config
* Plot script directory containing METplotpy configuration files
   * Local: ${IWRF_WORK_DIR}/i-wrf/use_cases/Land_Use_Land_Cover/Visualization
   * Container: /plot_scripts
* Output directory to write output
   * Local: ${IWRF_WORK_DIR}/metplus_out
   * Container: /data/output
* Apptainer temp directory
   * Local: ${APPTAINER_TMPDIR}
   * Container: ${APPTAINER_TMPDIR}

::

   LOCAL_METPLUS_CONFIG_DIR=${IWRF_WORK_DIR}/i-wrf/use_cases/Land_Use_Land_Cover/METplus
   LOCAL_PLOT_SCRIPT_DIR=${IWRF_WORK_DIR}/i-wrf/use_cases/Land_Use_Land_Cover/Visualization

   export APPTAINER_BIND="${IWRF_WORK_DIR}/data-lulc-input-obs.sif:/data/input/obs:image-src=/,${LOCAL_METPLUS_CONFIG_DIR}:/config,${IWRF_WORK_DIR}/data-lulc-input-wrf.sif:/data/input/wrf:image-src=/,${LOCAL_OUTPUT_DIR}:/data/output,${LOCAL_PLOT_SCRIPT_DIR}:/plot_scripts,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"

Execute the run_metplus.py command inside the container to run the use case

* Accumulated Precipitation::

   apptainer exec ${IWRF_WORK_DIR}/iwrf-metplus.sif /metplus/METplus/ush/run_metplus.py /config/GridStat_apcp_lulc.conf

* Reflectivity::

   apptainer exec ${IWRF_WORK_DIR}/iwrf-metplus.sif /metplus/METplus/ush/run_metplus.py /config/GridStat_refc_lulc.conf

Check that the output data was created locally::

   ls ${LOCAL_OUTPUT_DIR}/grid_stat/* -1

Check that the METplotpy plots were created locally::

   ls ${LOCAL_OUTPUT_DIR}/met_plot/*/*.png -1

Visualize the Results
=====================

In the near future, this exercise will be extended to include instructions to visualize the results.
