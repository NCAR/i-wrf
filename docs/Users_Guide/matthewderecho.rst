:orphan:

.. _matthewderecho:

Running I-WRF On Derecho with Hurricane Matthew Data
****************************************************

Overview
========

The following instructions can be used to run elements of
the `I-WRF weather simulation framework <https://i-wrf.org>`_
from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_
and the `Cornell Center for Advanced Computing <https://cac.cornell.edu/>`_.
The steps below run the `Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ model
with data from `Hurricane Matthew <https://en.wikipedia.org/wiki/Hurricane_Matthew>`_
on NCAR's `Derecho computing platform <https://www.cisl.ucar.edu/capabilities/derecho/>`_.
This exercise provides an introduction to using NCAR's Derecho HPC computing platform,
running computationally complex simulations and analyses, and using containerized applications.

Simulations like WRF often require greater computing resources
than you may have on your personal computer,
but an HPC platform can provided the needed computational power.
Jetstream2 is a national cyberinfrastructure resource that is easy to use
and is available to researchers and educators.
This exercise runs the I-WRF programs as Docker "containers",
which simplifies the set-up work needed to run the simulation and verification.

It is recommended that you follow the instructions in each section in the order presented
to avoid encountering issues during the process.
Most sections refer to external documentation to provide details about the necessary steps
and to offer additional background information.

Prepare to Use Derecho
======================

To `get started with Derecho <https://arc.ucar.edu/docs>`_,:

* You must be a U.S.-based researcher
* Your research must be in the Earth system sciences or related to Earth system science.
* Most projects require an NSF award, but we do offer access to graduate students, postdocs, new faculty, and for classroom use or data analysis without NSF funding.

The sections below will guide you through this process.

Logging In To Derecho
=====================

To log in, start your terminal or Secure Shell client and run an ssh command as shown here::

    ssh -X username@derecho.hpc.ucar.edu

The ``-X`` is optional and requests simple X11 graphics forwarding to your client. You can omit username in the command above if your Derecho username is the same as your username on your local computer.

With your successful login to Derecho through SSH,
you can now create the run folders, install Docker software and download the data to run the simulation and verification.
You will only need to perform these steps once as they will be stored on the disk.

The following sections instruct you to issue numerous Linux commands in your shell.
If you are not familiar with Linux, you may want to want to refer to
`An Introduction to Linux <https://cvw.cac.cornell.edu/Linux>`_ when working through these steps.
The commands in each section can be copied using the button in the upper right corner
and then pasted into your shell by right-clicking.

Pull The Docker Hub Image As A Singularity Image File (.sif)
------------------------------------------------------------

Derecho uses the ``modules`` command to make it easy to load various software libraries.  We
need to load a few modules to make basic commands available to the environment and then
the container image can be pulled from Docker Hub::

    module load charliecloud apptainer gcc cuda ncarcompilers
    mkdir ${HOME}/iwrf ; cd ${HOME}/iwrf
    singularity pull docker://ncar/iwrf:latest

Check that there is a file named ``iwrf_latest.sif`` if the current directory to confirm
that the image was pulled successfully.

Gain Interactive Access To A Compute Node
-----------------------------------------

Tasks that are resource intensive should not be run on the login nodes, so a compute node
should be accessed through Derecho's job queue before starting the container.  The following
command will submit an interactive job in the `develop` queue.::

    qsub -l select=1:ncpus=8:mpiprocs=8 -A <account_id> -l walltime=01:00:00 -I -q develop

The above command should be modified with your specific account ID for charging computing time.
The number of processors needed can also be specified here.  The full documentation for the `qsub`
command can be found on `Adaptive Computing's <http://docs.adaptivecomputing.com/torque/4-0-2/Content/topics/commands/qsub.htm>`_ website.

Running WRF In The Container
----------------------------
Once the interactive job has started, the container can be started and WRF can run.

To simplify the WRF execution process, there is a script that will download case study data for Hurricane Matthew (2016),
run Ungrib, Geogrid, Metgrid, REAL, and WRF processes.  Use the following command to download the script.::

    wget https://raw.githubusercontent.com/NCAR/i-wrf/feature/hurricane-matthew-script/run_hurricane_matthew_case.sh

Now the singularity container can be started.::

    module load charliecloud apptainer gcc cuda ncarcompilers
    singularity run --bind /glade/work/wrfhelp/WPS_GEOG:/terrestrial_data --bind /var/spool/pbs:/var/spool/pbs iwrf_latest.sif /bin/bash

The ``--bind /glade/work/wrfhelp/WPS_GEOG:/terrestrial_data`` option will make the terrestrial data available to the container,
which is pre-installed on Derecho.  This data set is required by the Geogrid step that will be running.
The ``--bind /var/spool/pbs:/var/spool/pbs`` option will make the job queue information available to the container, which provides
the available hosts and number of compute cores.  This information is required by the ``mpirun`` command in the script.

Now that we are running inside the container, we can execute the ``run_hurricane_matthew_case.sh`` script to run the model.::

    bash ./run_hurricane_matthew_case.sh

After the script finishes running the WRF output data will be in ``/tmp/hurricane_matthew/wrfout_d01*``.  If these files exist,
it indicates that the WRF run was successful.  If these files do not appear, you can check ``/tmp/hurricane_matthew/rsl.error.*``
files for errors.
