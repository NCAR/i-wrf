:orphan:

.. _matthewjetstream:

Running I-WRF On Windows (Intel CPU) with Hurricane Matthew Data
**********************************************************************

Overview
========

The following instructions can be used to run elements of
the `I-WRF weather simulation framework <https://i-wrf.org>`_
from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_
and the `Cornell Center for Advanced Computing <https://cac.cornell.edu/>`_.
The steps below run the `Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ model
and the  `METplus <https://https://dtcenter.org/community-code/metplus>`_ verification framework
with data from `Hurricane Matthew <https://en.wikipedia.org/wiki/Hurricane_Matthew>`_
on a Windows computer with an Intel CPU.
This exercise provides an introduction to using cloud computing platforms,
running computationally complex simulations and analyses, and using containerized applications.

Simulations like WRF often require significant computing resources,
so it is recommended that the computer you use have at least four cores, 32 GB of RAM, and 50 Gb of available disk space.
This exercise runs the I-WRF programs as Docker "containers",
which simplifies the set-up work needed to run the simulation and verification.
However, the code used to build those Docker containers was compiled expressly for use on
`Intel CPUs <https://www.intel.com/content/www/us/en/products/details/processors.html>`_,
so the Windows computer you use must contain an Intel processor.
Your Windows account will also need to have administrative privileges in order to perform all necessary steps.

It is recommended that you follow the instructions in each section in the order presented
to avoid encountering issues during the process.
Most sections refer to external documentation to provide details about the necessary steps
and to offer additional background information.

Preparing the Environment
=========================

You can now create the run folders, install the software and download the data
that are needed to run the simulation and verification.
You will only need to perform these steps once.
The following sections instruct you to issue numerous DOS commands in a Windows "Command Prompt" shell.
To open such a shell, click the Start icon and then type "cmd" to display matching commands.
Right click on the "Command Prompt" option that is shown and select "Run as administrator".
A black shell window should open.

Define Environment Variables
----------------------------

We will be using some environment variables throughout this exercise to
make sure that we refer to the same resource names and file paths wherever they are used.
The first variable you need to define will specify the location of the "working directory" for the data and run folders.
The example command below specifies that the working directory is the home directory of user account "exercise".
You will need to enter a command similar to this that either specifies your user account name instead of "exercise",
or changes the path entirely to use a different location on your computer::

    set WORKING_DIR=C:\Users\exercise

Now you can copy and paste the definitions below into your shell to define the other variables before proceeding::

    set WRF_IMAGE=ncar/iwrf:latest
    set METPLUS_IMAGE=dtcenter/metplus-dev:develop
    set WRF_DIR=%WORKING_DIR%\wrf\20161006_00
    set METPLUS_DIR=%WORKING_DIR%\metplus
    set WRF_CONFIG_DIR=%WORKING_DIR%\i-wrf-main\use_cases\Hurricane_Matthew\WRF
    set METPLUS_CONFIG_DIR=%WORKING_DIR%\i-wrf-main\use_cases\Hurricane_Matthew\METplus
    set OBS_DATA_VOL=data-matthew-input-obs

Any time you open a new shell on your instance, you will need to perform this action
to redefine the variables before executing the commands that follow.

Create the WRF and METplus Run Folders
--------------------------------------

The simulation is performed using a script that expects to run in a folder where it can create result files.
The first command below creates a folder (named "wrf") under the user's home directory,
and a sub-folder within "wrf" to hold the output of this simulation.
The subfolder is named "20161006_00", which is the beginning date and time of the simulation.
Similarly, a run folder named "metplus" must be created for the METplus process to use::

    mkdir %WRF_DIR%
    mkdir %METPLUS_DIR%

Download Configuration Files
----------------------------

Both WRF and METplus require some configuration files to direct their behavior,
and those must be downloaded from GitHub:

* In a browser, visit the `I-WRF GitHub repository <https://github.com/NCAR/i-wrf>`_.
* Expand the green button ``<> Code`` button, and select Download ZIP.
* After the ZIP file has been downloaded, open it and extract its contents to the working directory you have selected.
* Do not change the name of the extracted folder, which should be "i-wrf-main".

Now, some of the configuration files must be copied into the run folders.
These commands perform the necessary operations::

    cp %WRF_CONFIG_DIR}%\namelist.* %WRF_DIR%
    cp %WRF_CONFIG_DIR%\vars_io.txt %WRF_DIR%
    cp %WRF_CONFIG_DIR%\run.sh %WRF_DIR%

Install Docker and Pull Docker Objects
======================================

Install Docker
--------------

As mentioned above, the WRF and METplus software are provided as Docker images that will run as a
`"container" <https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/>`_
on your cloud instance.
To run a Docker container, you must first install the Docker Engine on your instance.
You can then "pull" (download) the WRF and METplus images that will be run as containers.

The `instructions for installing Docker Engine on Ubuntu <https://docs.docker.com/engine/install/ubuntu/>`_
are very thorough and make a good reference, but we only need to perform a subset of those steps.
These commands run a script that sets up the Docker software repository on your instance,
then installs Docker::

    curl --location https://bit.ly/3R3lqMU > install-docker.sh
    source install-docker.sh
    rm install-docker.sh

If a text dialog is displayed asking which services should be restarted, type ``Enter``.
When the installation is complete, you can verify that the Docker command line tool works by asking for its version::

    docker --version

The Docker daemon should start automatically, but it sometimes runs into issues.
First, check to see if the daemon started successfully::

    sudo systemctl --no-pager status docker

If you see a message saying the daemon failed to start because a "Start request repeated too quickly",
wait a few minutes and issue this command to try again to start it::

    sudo systemctl start docker

If the command seems to succeed, confirm that the daemon is running using the status command above.
Repeat these efforts as necessary until it is started.

Get the WRF and METplus Docker Images and the Observed Weather Data
-------------------------------------------------------------------

Once Docker is running, you must pull the correct versions of the WRF and METplus images onto your instance::

    docker pull %WRF_IMAGE%
    docker pull %METPLUS_IMAGE%

METplus is run to perform verification of the results of the WRF simulation using
observations gathered during Hurricane Matthew.
We download that data by pulling a Docker volume that holds it,
and then referencing that volume when we run the METplus Docker container.
The commands to pull and create the volume are::

    docker pull ncar/iwrf:%OBS_DATA_VOL%.docker
    docker create --name %OBS_DATA_VOL% ncar/iwrf:%OBS_DATA_VOL%.docker

Download Data for WRF
=====================

To run WRF on the Hurricane Matthew data set, you need to have
several data sets to support the computation.
The commands in these sections download archive files containing that data,
then uncompress the archives into folders.
The geographic data is large and takes several minutes to acquire,
while the other two data sets are smaller and are downloaded directly into the WRF run folder,
rather than the user's home directory.

Get the geographic data representing the terrain in the area of the simulation::

    cd %WORKING_DIR%
    wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
    tar -xzf geog_high_res_mandatory.tar.gz
    rm geog_high_res_mandatory.tar.gz

Get the case study data (GRIB2 files)::

    cd %WORKING_DIR%
    wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_1deg.tar.gz
    tar -xvzf matthew_1deg.tar.gz
    rm -f matthew_1deg.tar.gz

Get the SST (Sea Surface Temperature) data::

    cd %WORKING_DIR%
    wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_sst.tar.gz
    tar -xzvf matthew_sst.tar.gz
    rm -f matthew_sst.tar.gz

Run WRF
=======

With everything in place, you are now ready to run the Docker container that will perform the simulation.
The downloaded script runs inside the container, prints lots of status information,
and creates output files in the run folder you created.
Execute this command to run the simulation in your shell::

    docker run --shm-size 14G -it \
      -v %WORKING_DIR%:/home/wrfuser/terrestrial_data \
      -v %WRF_DIR%:/tmp/hurricane_matthew \
      %WRF_IMAGE% /tmp/hurricane_matthew/run.sh

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 14G -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:latest`` is the Docker image to use when creating the container.
* ``/tmp/hurricane_matthew/run.sh`` is the location within the container of the script that it runs.

The simulation initially prints lots of information while initializing things, then settles in to the computation.
The provided configuration simulates 48 hours of weather and takes about 12 minutes to finish on an m3.quad Jetstream2 instance.
Once completed, you can view the end of an output file to confirm that it succeeded::

    tail %WRF_DIR%\rsl.out.0000

The output should look something like this::

    Timing for main: time 2016-10-06_11:42:30 on domain   1:    0.23300 elapsed seconds
    Timing for main: time 2016-10-06_11:45:00 on domain   1:    0.23366 elapsed seconds
    Timing for main: time 2016-10-06_11:47:30 on domain   1:    2.77688 elapsed seconds
    Timing for main: time 2016-10-06_11:50:00 on domain   1:    0.23415 elapsed seconds
    Timing for main: time 2016-10-06_11:52:30 on domain   1:    0.23260 elapsed seconds
    Timing for main: time 2016-10-06_11:55:00 on domain   1:    0.23354 elapsed seconds
    Timing for main: time 2016-10-06_11:57:30 on domain   1:    0.23345 elapsed seconds
    Timing for main: time 2016-10-06_12:00:00 on domain   1:    0.23407 elapsed seconds
    Timing for Writing wrfout_d01_2016-10-06_12:00:00 for domain        1:    0.32534 elapsed seconds
    d01 2016-10-06_12:00:00 wrf: SUCCESS COMPLETE WRF

Run METplus
===========

After the WRF simulation has finished, you can run the METplus verification to compare the simulated results
to the actual weather observations during the hurricane.
The verification takes about five minutes to complete.
We use command line options to tell the METplus container several things, including where the observed data is located,
where the METplus configuration can be found, where the WRF output data is located, and where it should create its output files::

    docker run --rm -it \
      --volumes-from %OBS_DATA_VOL% \
      -v %METPLUS_CONFIG_DIR%:/config \
      -v %WORKING_DIR%\wrf:/data/input/wrf \
      -v %METPLUS_DIR%:/data/output %METPLUS_IMAGE% \
      /metplus/METplus/ush/run_metplus.py /config/PointStat_matthew.conf

Progress information is displayed while the verification is performed.
**WARNING** log messages are expected because observations files are not available for every valid time and METplus is
configured to allow some missing inputs. An **ERROR** log message indicates that something went wrong.
METplus first converts the observation data files to a format that the MET tools can read using the MADIS2NC wrapper.
Point-Stat is run to generate statistics comparing METAR observations to surface-level model fields and
RAOB observations to "upper air" fields.
METplus will print its completion status when the processing finishes.

The results of the METplus verification can be found in ``%WORKING_DIR%\metplus\point_stat``.
These files contain tabular output that can be viewed in a text editor. Turn off word wrapping for better viewing.
Refer to the MET User's Guide for more information about the
`Point-Stat output <https://met.readthedocs.io/en/latest/Users_Guide/point-stat.html#point-stat-output>`_.
In the near future, this exercise will be extended to include instructions to visualize the results.
