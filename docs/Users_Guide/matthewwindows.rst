:orphan:

.. _matthewwindows:

Running I-WRF On Windows (Intel CPU) with Hurricane Matthew Data
****************************************************************

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
so the Windows 10 or 11 computer you use must contain an Intel processor
(note that these instructions are not intended for use on a system running Windows Server).
Your Windows account will also need to have administrative privileges in order to perform all necessary steps.

It is recommended that you follow the instructions in each section in the order presented
to avoid encountering issues during the process.
Most sections refer to external documentation to provide details about the necessary steps
and to offer additional background information.

Preparing the Environment
=========================

You will now create the run folders, install the software and download the data
that are needed to run the simulation and verification.
You will only need to perform these steps once.
The following sections instruct you to issue numerous DOS commands in a Windows "Command Prompt" shell.
To open such a shell:

* Click the Start icon and then type "cmd" to display matching commands.
* Right click on the "Command Prompt" option that is shown and select "Run as administrator".
* A black shell window should open.

Define Environment Variables
----------------------------

We will be using some environment variables throughout this exercise to
make sure that we refer to the same resource names and file paths wherever they are used.
The first variable you need to define will specify the location of the "working directory" for the data and run folders.
The example command below specifies that the working directory is the home directory of a hypothetical username "exercise".
You will need to enter a command similar to this that either specifies *your* user account name instead of "exercise",
or changes the path entirely to use a different location on your computer::

    set WORKING_DIR=C:\Users\exercise

Now you can copy and paste the definitions below into your shell to define the other variables before proceeding::

    set WRF_IMAGE=ncar/iwrf:latest
    set METPLUS_IMAGE=ncar/iwrf-metplus:latest
    set WRF_DIR=%WORKING_DIR%\wrf\20161006_00
    set METPLUS_DIR=%WORKING_DIR%\metplus
    set WRF_CONFIG_DIR=%WORKING_DIR%\i-wrf-main\use_cases\Hurricane_Matthew\WRF
    set METPLUS_CONFIG_DIR=%WORKING_DIR%\i-wrf-main\use_cases\Hurricane_Matthew\METplus
    set PLOT_SCRIPT_DIR=%WORKING_DIR%\i-wrf-main\use_cases\Hurricane_Matthew\Visualization
    set OBS_DATA_VOL=matthew-input-obs

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
* After the ZIP file has been downloaded, open it and extract its contents to the working directory you have selected as a folder named "i-wrf-main" (the default).  Be careful not to include two levels of "i-wrf-main" folders in the path!

Now, some of the configuration files must be copied into the WRF run folder.
These commands perform the necessary operations::

    copy /y %WRF_CONFIG_DIR%\namelist.* %WRF_DIR%
    copy /y %WRF_CONFIG_DIR%\vars_io.txt %WRF_DIR%
    copy /y %WRF_CONFIG_DIR%\run.sh %WRF_DIR%

Install Docker and Pull Docker Objects
======================================

As mentioned above, the WRF and METplus software are provided as Docker images that will run as a
`"container" <https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/>`_
on your cloud instance.
To run a Docker container, you must first install the Docker Engine on your instance.
You can then "pull" (download) the WRF and METplus images that will be run as containers.

Install Docker Desktop
----------------------

In order to install Docker on your Windows computer, one or more Windows services must be enabled
(these services allow virtualization and running of containers).
The `process for performing this setup and installation <https://learn.microsoft.com/en-us/virtualization/windowscontainers/quick-start/set-up-environment>`_
is outlined below.
During the setup process your computer may reboot one or more times,
so be sure to save all work and close your other applications before beginning the setup.

To install Docker and enable the required components on Windows 10/11,
you will install the Docker Desktop for Windows application by following these steps:

* In a web browser, visit `Install Docker Desktop on Windows <https://docs.docker.com/desktop/install/windows-install/>`_.
* Click on ``Docker Desktop for Windows - x86_64`` to download the installer.
* Run the installer file "Docker Desktop Installer.exe", which will require a system restart.
* Leave the "Use WSL 2 instead of Hyper-V" option checked in the dialog that appears.
* After the installation is complete, use the Start menu to find and run Docker Desktop, then agree to the terms and complete the other steps in the "first use" wizard.

The Docker Desktop app should now show a green "Engine running" status in the lower left corner.
If your engine isn't running or you encounter any other issues,
visit the `Troubleshoot Docker Desktop page <https://docs.docker.com/desktop/troubleshoot/overview/>`_.

Get the WRF and METplus Docker Images and the Observed Weather Data
-------------------------------------------------------------------

Once Docker is running, you must pull the correct versions of the WRF and METplus images onto your instance.
Open a Command Prompt shell as done before, execute the commands to define the environment variables, and then issue these commands::

    docker pull %WRF_IMAGE%
    docker pull %METPLUS_IMAGE%

METplus is run to perform verification of the results of the WRF simulation using
observations gathered during Hurricane Matthew.
We download that data by pulling a Docker volume on which the data resides,
then creating a container from that volume,
and then referencing that volume when we run the METplus Docker container.
The commands to pull the volume and create a container for it are::

    docker pull ncar/iwrf-data:%OBS_DATA_VOL%.docker
    docker create --name %OBS_DATA_VOL% ncar/iwrf-data:%OBS_DATA_VOL%.docker

Download Data for WRF
=====================

To run WRF on the Hurricane Matthew data, you need to have
three data sets to support the computation.
The commands in this section download archive files containing that data,
then uncompress the archives into folders.
The geographic data is large and takes several minutes to acquire,
while the other two data sets are smaller and are downloaded directly into the WRF run folder,
rather than the main working directory.

The steps to process each data set are the same:

* Visit the data set's URL in a web browser, which will download the .tar.gz file.
* Unzip the .tar.gz file contents into the destination folder.
* Remove the downloaded .tar.gz file.

Begin by download all of the data sets in this table:

+-------------------+----------------------------------------------------------------------------+---------------+
| Data Set          | URL                                                                        | Destination   |
+===================+============================================================================+===============+
| Terrain           | https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz | %WORKING_DIR% |
+-------------------+----------------------------------------------------------------------------+---------------+
| Case study        | https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_1deg.tar.gz            | %WRF_DIR%     |
+-------------------+----------------------------------------------------------------------------+---------------+
| Sea Surface Temps | https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_sst.tar.gz             | %WRF_DIR%     |
+-------------------+----------------------------------------------------------------------------+---------------+

Now, in your command prompt window, change directory ("cd") to the folder where those files were downloaded.
Then, copy/paste the commands below to unzip the data and delete the downloaded files::

    tar -xzf geog_high_res_mandatory.tar.gz -C %WORKING_DIR%
    del geog_high_res_mandatory.tar.gz

    tar -xzf matthew_1deg.tar.gz -C %WRF_DIR%
    del -f matthew_1deg.tar.gz

    tar -xzf matthew_sst.tar.gz -C %WRF_DIR%
    del -f matthew_sst.tar.gz

Run WRF
=======

With everything in place, you are now ready to run the Docker container that will perform the simulation.
The downloaded script runs inside the container, prints lots of status information,
and creates output files in the run folder you created.
Execute this command to run the simulation in your shell::

    docker run --shm-size 14G -it ^
      -v %WORKING_DIR%:/home/wrfuser/terrestrial_data ^
      -v %WRF_DIR%:/tmp/hurricane_matthew ^
      %WRF_IMAGE% /tmp/hurricane_matthew/run.sh

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 14G -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:latest`` is the Docker image to use when creating the container.
* ``/tmp/hurricane_matthew/run.sh`` is the location within the container of the script that it runs.

The simulation initially prints lots of information while initializing things, then settles in to the computation.
The provided configuration simulates 48 hours of weather and should take less than 30 minutes to finish,
depending on your CPU's number of cores and clock speed.
Once completed, you can view the end of an output file to confirm that it succeeded::

    powershell -command "& {Get-Content %WRF_DIR%\rsl.out.0000 | Select-Object -last 10}"

The output should look something like this::

    Timing for main: time 2016-10-07_23:50:00 on domain 1: 0.25548 elapsed seconds
    Timing for main: time 2016-10-07_23:52:30 on domain 1: 0.25495 elapsed seconds
    Timing for main: time 2016-10-07_23:55:00 on domain 1: 0.25066 elapsed seconds
    Timing for main: time 2016-10-07_23:57:30 on domain 1: 0.25231 elapsed seconds
    Timing for main: time 2016-10-08_00:00:00 on domain 1: 0.25795 elapsed seconds
    Timing for Writing wrfout_d01_2016-10-08_00:00:00 for domain 1: 0.68666 elapsed seconds
    Timing for Writing wrfout_zlev_d01_2016-10-08_00:00:00 for domain 1: 0.47411 elapsed seconds
    Timing for Writing wrfout_plev_d01_2016-10-08_00:00:00 for domain 1: 0.47619 elapsed seconds
    Timing for Writing restart for domain 1: 1.54598 elapsed seconds
    d01 2016-10-08_00:00:00 wrf: SUCCESS COMPLETE WRF

Run METplus
===========

After the WRF simulation has finished, you can run the METplus verification to compare the simulated results
to the actual weather observations during the hurricane.
The verification takes about five minutes to complete.
We use command line options to tell the METplus container several things,
including where the observed data is located,
where the METplus configuration can be found,
where the plotting scripts can be found,
where the WRF output data is located,
and where it should create its output files::

    docker run --rm -it ^
      --volumes-from %OBS_DATA_VOL% ^
      -v %METPLUS_CONFIG_DIR%:/config ^
      -v %PLOT_SCRIPT_DIR%:/plot_scripts ^
      -v %WORKING_DIR%\wrf:/data/input/wrf ^
      -v %METPLUS_DIR%:/data/output %METPLUS_IMAGE% ^
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
