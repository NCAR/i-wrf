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

Change directory to scratch and pull the container from DockerHub.
This will create a `.sif` file in the current directory::

   cd ${SCRATCH}
   apptainer pull docker://dtcenter/metplus:6.0.0-beta4

Create a directory to store the output::

   mkdir ${SCRATCH}/metplus_out

Set environment variable to bind directories to container
(note: this can also be accomplished by passing the value on the command line
using the --bind argument)

* Input data directories for WRF, raob, and metar input data
   * WRF: /glade/derecho/scratch/jaredlee/nsf_i-wrf/matthew to /data/input/wrf
   * RAOB: /glade/campaign/ral/wsap/i-wrf/data/hurr-matthew/madis/point/raob/netcdf to /data/input/obs/raob
   * METAR: /glade/campaign/ral/wsap/i-wrf/data/hurr-matthew/madis/point/metar/netcdf to /data/input/obs/metar
* Config directory containing METplus use case configuration file
   * /glade/u/home/mccabe/i-wrf/use_cases/Hurricane_Matthew/METplus to /config
* Output directory to write output
   * ${SCRATCH}/metplus_out to /data/output

::

   LOCAL_METPLUS_CONFIG_DIR=/glade/u/home/mccabe/i-wrf/use_cases/Hurricane_Matthew/METplus
   LOCAL_FCST_INPUT_DIR=/glade/derecho/scratch/jaredlee/nsf_i-wrf/matthew
   LOCAL_UPPER_AIR_OBS_INPUT_DIR=/glade/campaign/ral/wsap/i-wrf/data/hurr-matthew/madis/point/raob/netcdf
   LOCAL_SURFACE_OBS_INPUT_DIR=/glade/campaign/ral/wsap/i-wrf/data/hurr-matthew/madis/point/metar/netcdf
   LOCAL_OUTPUT_DIR=${SCRATCH}/metplus_out

   export APPTAINER_BIND="${LOCAL_METPLUS_CONFIG_DIR}:/config,${LOCAL_FCST_INPUT_DIR}:/data/input/wrf,${LOCAL_UPPER_AIR_OBS_INPUT_DIR}:/data/input/obs/raob,${LOCAL_SURFACE_OBS_INPUT_DIR}:/data/input/obs/metar,${LOCAL_OUTPUT_DIR}:/data/output"

Execute the run_metplus.py command inside the container to run the use case::

   apptainer exec metplus_6.0.0-beta4.sif /metplus/METplus/ush/run_metplus.py /config/PointStat_matthew.conf

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
