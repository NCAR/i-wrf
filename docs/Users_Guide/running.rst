************************
Running I-WRF Containers
************************

On an HPC Cluster with Apptainer
================================

WRF
---

METplus
-------

The following commands were run on Casper.

Load the apptainer module::

   module load apptainer

Create a working directory in the scratch area::

   IWRF_WORK_DIR=${SCRATCH}/iwrf_work

.. note::

   If an error is displayed when attempting to pull the METplus image,
   creating a DockerHub account and authenticating through apptainer may be
   necessary.

   ::

      apptainer remote login --username {USERNAME} docker://docker.io

   where **{USERNAME}** is your DockerHub username.

Create a directory to store the output::

   LOCAL_OUTPUT_DIR=${IWRF_WORK_DIR}/metplus_out
   mkdir -p ${LOCAL_OUTPUT_DIR}

Create a directory to store temporary Apptainer files::

   export APPTAINER_TMPDIR=${IWRF_WORK_DIR}/tmp
   mkdir -p ${APPTAINER_TMPDIR}

Change directory to working directory and pull the containers from DockerHub.
This will create a `.sif` file in the current directory::

   apptainer pull ${IWRF_WORK_DIR}/iwrf-metplus.sif docker://ncar/iwrf:metplus-latest
   apptainer pull ${IWRF_WORK_DIR}/data-matthew-input-obs.sif oras://registry-1.docker.io/ncar/iwrf:data-matthew-input-obs

Clone the I-WRF GitHub repository to get the configuration files::

   git clone https://github.com/NCAR/i-wrf ${IWRF_WORK_DIR}/i-wrf

Set environment variable to bind directories to container
(note: this can also be accomplished by passing the value on the command line
using the --bind argument)

* Input data directories for WRF, raob, and metar input data
   * WRF:
      * Local: /glade/derecho/scratch/jaredlee/nsf_i-wrf/matthew
      * Container: /data/input/wrf
   * RAOB:
      * Local: From data-matthew-input-obs.sif
      * Container: /data/input/obs/raob
   * METAR:
      * Local: From data-matthew-input-obs.sif
      * Container: /data/input/obs/metar
* Config directory containing METplus use case configuration file
   * Local: ${IWRF_WORK_DIR}/i-wrf/use_cases/Hurricane_Matthew/METplus
   * Container: /config
* Plot script directory containing WRF plotting scripts
   * Local: ${SCRATCH}/i-wrf/use_cases/Hurricane_Matthew/Visualization
   * Container: /plot_scripts
* Output directory to write output
   * Local: ${IWRF_WORK_DIR}/metplus_out
   * Container: /data/output
* Apptainer temp directory
   * Local: ${APPTAINER_TMPDIR}
   * Container: ${APPTAINER_TMPDIR}

::

   LOCAL_METPLUS_CONFIG_DIR=${IWRF_WORK_DIR}/i-wrf/use_cases/Hurricane_Matthew/METplus
   LOCAL_PLOT_SCRIPT_DIR=${IWRF_WORK_DIR}/i-wrf/use_cases/Hurricane_Matthew/Visualization
   LOCAL_FCST_INPUT_DIR=/glade/derecho/scratch/jaredlee/nsf_i-wrf/matthew

   export APPTAINER_BIND="${SCRATCH}/data-matthew-input-obs.sif:/data/input/obs:image-src=/,${LOCAL_METPLUS_CONFIG_DIR}:/config,${LOCAL_FCST_INPUT_DIR}:/data/input/wrf,${LOCAL_OUTPUT_DIR}:/data/output,${LOCAL_PLOT_SCRIPT_DIR}:/plot_scripts,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"

Execute the run_metplus.py command inside the container to run the use case::

   apptainer exec ${SCRATCH}/iwrf-metplus.sif /metplus/METplus/ush/run_metplus.py /config/PointStat_matthew.conf

Check that the output data was created locally::

   ls ${IWRF_WORK_DIR}/metplus_out/point_stat -1


Visualization
-------------

On AWS
======

WRF
---

METplus
-------

Visualization
-------------
