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

Change directory to scratch and pull the containers from DockerHub.
This will create a `.sif` file in the current directory::

   cd ${SCRATCH}
   apptainer pull docker://dtcenter/metplus-dev:feature_1514_madis2nc-pull_request
   apptainer pull data-matthew-input-obs.sif oras://registry-1.docker.io/ncar/iwrf:data-matthew-input-obs

Create a directory to store the output::

   mkdir ${SCRATCH}/metplus_out

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
   * Local: /glade/u/home/mccabe/i-wrf/use_cases/Hurricane_Matthew/METplus
   * Container: /config
* Output directory to write output
   * Local: ${SCRATCH}/metplus_out
   * Container: /data/output

::

   LOCAL_METPLUS_CONFIG_DIR=/glade/u/home/mccabe/i-wrf/use_cases/Hurricane_Matthew/METplus
   LOCAL_FCST_INPUT_DIR=/glade/derecho/scratch/jaredlee/nsf_i-wrf/matthew
   LOCAL_OUTPUT_DIR=${SCRATCH}/metplus_out

   export APPTAINER_BIND="data-matthew-input-obs.sif:/data/input/obs:image-src=/,${LOCAL_METPLUS_CONFIG_DIR}:/config,${LOCAL_FCST_INPUT_DIR}:/data/input/wrf,${LOCAL_OUTPUT_DIR}:/data/output"

Execute the run_metplus.py command inside the container to run the use case::

   apptainer exec metplus-dev_feature_1514_madis2nc-pull_request.sif /metplus/METplus/ush/run_metplus.py /config/PointStat_matthew.conf

Check that the output data was created locally::

   ls ${SCRATCH}/metplus_out/point_stat -1


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
