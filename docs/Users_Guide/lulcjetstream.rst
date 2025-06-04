:orphan:

.. _lulcjetstream:

Running I-WRF On Jetstream2 with Land Use/Land Cover (LULC) Data
****************************************************************

Overview
========

The following instructions can be used to run elements of
the `I-WRF weather simulation framework <https://i-wrf.org>`_
from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_
and the `Cornell Center for Advanced Computing <https://cac.cornell.edu/>`_.
The steps below run the `Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ and `WRF Pre-Processing System (WPS) <https://github.com/wrf-model/WPS>`_
models with data from `The High-Resolution Rapid Refresh (HRRR) <https://rapidrefresh.noaa.gov/hrrr/>`_ 
and modified meteorological data on the  `Jetstream2 cloud computing platform <https://jetstream-cloud.org/>`_.
This science use case focuses on a deep convection system that passed over the Dallas-Fort Worth (DFW) metropolitan region on July 4th, 2017, and the simulations follow Zhou et al. 2024. This exercise provides an introduction to using cloud computing platforms, running computationally complex simulations and analyses, and using containerized applications.

Simulations like WRF often require greater computing resources
than you may have on your personal computer,
but a cloud computing platform can provided the needed computational power.
Jetstream2 is a national cyberinfrastructure resource that is easy to use
and is available to researchers and educators.
This exercise runs the I-WRF programs as Docker "containers",
which simplifies the setup work needed to run the simulation.

It is recommended that you follow the instructions in each section in the order presented
to avoid encountering issues during the process.
Most sections refer to external documentation to provide details about the necessary steps
and to offer additional background information.

Reference
---------
Zhou, X., Letson, F., Crippa, P. and Pryor, S.C., 2024. Urban effect on precipitation and deep convective systems over Dallas-Fort Worth. Journal of Geophysical Research: Atmospheres, 129(10), p.e2023JD039972. 

Get an ACCESS Account and Add an Allocation to It
=================================================

To `get started with Jetstream2 <https://jetstream-cloud.org/get-started>`_,
you will need to create an account with the `National Science Foundation (NSF) <https://www.nsf.gov/>`_'s `ACCESS program <https://access-ci.org/>`_.
If you do not already have one, `register for an ACCESS account <https://operations.access-ci.org/identity/new-user>`_.
When registering your account, you can either choose to associate your existing University/Organizational account or
create an entirely new ACCESS account when registering.
The Jetstream2 team strongly recommends that you create a new ACCESS account,
as your organizational affiliation may change in the future.

Once you have an account you will need to have a computational "allocation" added to that account.
Allocations provide the credits you will spend when running instances on Jetstream2.
If there are no allocation owners who can add you to their allocation and you are interested in obtaining your own,
you may `request an allocation <https://allocations.access-ci.org/get-your-first-project>`_
that will allow you to use an ACCESS-affiliated cyberinfrastructure resource.
Note that allocations may only be requested by faculty, staff and graduate researchers,
so undergraduates must work with a faculty sponsor to requeste an allocation.

Be sure to read all of the information on the request page so that you make a suitable request.
Note that you will need to describe the project for which the allocation is intended
and provide a CV or resume for the principal investigator.
An "Explore" project (400,000 credits) will be much more than enough to work with this exercise.
You will want to work with the resource "Indiana Jetstream2 CPU" (*not* **GPU**).
The typical turnaround time for allocation requests is one business day.

Log in to Jetstream2's Exosphere Web Site
=========================================

Once you have an ACCESS account and an allocation has been added to it,
you can log in to Jetstream's `Exosphere web dashboard <https://jetstream2.exosphere.app>`_.
The process of identifying your allocation and ACCESS ID to use Jetstream2
is described on `this page <https://cvw.cac.cornell.edu/jetstream/intro/jetstream-login>`__ of the
`Introduction to Jetstream2 <https://cvw.cac.cornell.edu/jetstream>`_ Cornell Virtual Workshop,
and on `this page <https://docs.jetstream-cloud.org/ui/exo/login>`__
of the `Jetstream2 documentation <https://docs.jetstream-cloud.org>`_.

While adding an allocation to your account, it is recommended that you choose
the "Indiana University" region of Jetstream2 for completing this exercise.

Create a Cloud Instance on Jetstream2
=====================================

After you have logged in to Jetstream2 and added your allocation to your account,
you are ready to create the cloud instance where you will run the simulation and verification.
If you are not familiar with the cloud computing terms "image" and "instance",
it is recommended that you `read about them <https://cvw.cac.cornell.edu/jetstream/intro/imagesandinstances>`__
before proceeding.

For this tutorial, you will be able to log in to your instance using Exosphere's Web Desktop or Web Shell functionalities.
If you would rather log in using the "ssh" command from a shell on your own computer,
you will need to create an SSH key pair and upload it to Jetstream2 before creating your instance.
Optional information about doing those things is available here:

.. dropdown:: Creating an SSH Key and uploading it to Jetstream2

    You may choose to upload a public SSH key to Jetstream2 before creating your instance.
    Jetstream2 will inject that public key into an instance's default user account,
    and you will need to provide the matching private SSH key to log in to the instance.
    If you are not familiar with "SSH key pairs", you should
    `read about them <https://cvw.cac.cornell.edu/jetstream/keys/about-keys>`__ before continuing.

    * First, `create an SSH Key on your computer <https://cvw.cac.cornell.edu/jetstream/keys/ssh-create>`_ using the "ssh-keygen" command.  That command allows you to specify the name and location of the private key file it creates, with the default being "id_rsa".  The matching public key file is saved to the same location and name with ".pub" appended to the filename.  Later instructions will assume that your private key file is named "id_rsa", but you may choose a different name now and use that name in those later instructions.
    * Then, `upload the public key to Jetstream2 <https://cvw.cac.cornell.edu/jetstream/keys/ssh-upload>`_ through the Exosphere web interface.

The Cornell Virtual Workshop topic `Creating an Instance <https://cvw.cac.cornell.edu/jetstream/create-instance>`_
provides detailed information about creating a Jetstream2 instance.
While following those steps for this tutorial, be sure to make the following choices for this instance:

* When choosing an image as the instance source, if viewing "By Type", select the "Ubuntu 24.04" image.  If viewing "By Image", choose the "Featured-Ubuntu24" image.
* Choose the "Flavor" m3.2xl (64 CPUs) to provide a faster simulation run-time.
* Select a custom disk size of 1500 GB, which is large enough to hold this exercise's data and results.
* For "Enable web desktop?", select Yes.
* For "Choose an SSH public key", select None unless you want to use your own SSH key that you uploaded previously.
* You do not need to set any of the Advanced Options.

After clicking the "Create" button, wait for the instance to enter the "Ready" state (it takes several minutes).
Note that the instance will not only be created, but will be running so that you can log in right away.

Log in to the Instance
======================

The Exosphere web dashboard provides two easy-to-use methods for logging in to your instance through a web browser.
The "Web Shell" button will open a terminal to your instance,
and the "Wed Desktop" button will open a view of the instance's graphical desktop (if enabled).
Both views open in a new browser tab, and Exosphere automatically logs you in to the instance.
For this tutorial you should open a Web Desktop so that you will be able to view
the plots that are generated from the simulation output.

If you wish to log in to the instance from a shell on your computer,
you can do so following the information in this optional content:

.. dropdown:: Logging in to a Jetstream2 Instance using SSH From a Shell

    You can use the SSH command to access your instance from a shell on your computer.
    The instructions for `connecting to Jetstream2 using SSH <https://cvw.cac.cornell.edu/jetstream/instance-login/sshshell>`_
    can be executed in the Command Prompt on Windows (from the Start menu, type "cmd" and select Command Prompt)
    or from the Terminal application on a Mac.

    In either case you will need to know the location and name of the private SSH key created on your computer (see SSH section, above),
    the IP address of your instance (found in the Exosphere web dashboard)
    and the default username on your instance, which is "exouser".


Once you are logged in to the instance, your shell prompt will have the form ``exouser@instance-name:~$``,
which indicates your username, the instance name, and your current working directory, followed by "$".

Managing Your Jetstream2 Instance
=================================

In order to use cloud computing resources efficiently, you must know how to
`manage your instances <https://cvw.cac.cornell.edu/jetstream/manage-instance/states-actions>`_.
Instances incur costs whenever they are running (on Jetstream2, this is when they are "Ready").
"Shelving" an instance stops it from using the cloud's CPUs and memory,
and therefore stops it from incurring any charges against your allocation.

When you are through working on this exercise, you should shelve your instance.
Note that any programs that are running when you shelve the instance will be terminated,
but the contents of the disk are preserved when shelving.

To shelve, you need to be in the details page for your instance (with the "Actions" menu in the upper right).
If you are on the Instances page, click and instance's name to be taken to its details page.
From the Actions menu, select Shelve.
You will be prompted in that location to confirm the shelve action - click Yes to complete the action.
In the Instances page your instance will briefly be listed as "Shelving",
and then as "Shelved" when the operation is complete.

When you later return to the dashboard and want to use the instance again,
use the Action menu's "Unshelve" option to start the instance up again.
You can also use the "Resize" action to change the flavor (number of CPUs and amount of RAM) of the instance.
Increasing the number of CPUs can make your computations finish more quickly,
but doubling the number of CPUs doubles the cost per hour to run the instance,
so Shelving as soon as you are done becomes even more important!

Preparing the Environment
=========================

With your instance created and running and you logged in to it through SSH,
you can now create the run folders, install Docker software and download the data to run the simulation and verification.
You will only need to perform these steps once,
as they essentially change the contents of the instance's disk
and those changes will remain even after the instance is shelved and unshelved.

The following sections instruct you to issue numerous Linux commands in your shell.
If you are not familiar with Linux, you may want to want to refer to
`An Introduction to Linux <https://cvw.cac.cornell.edu/Linux>`_ when working through these steps.
The commands in each section can be copied using the button in the upper right corner
and then pasted into your shell by right-clicking.

If your shell ever becomes unresponsive or disconnected from the instance,
you can recover from that situation by opening a new Web Desktop (if available) or rebooting the instance.
In the Exosphere dashboard page for your instance, in the Actions menu, select "Reboot".
The process takes several minutes, after which the instance status will return to "Ready".


Access Data for WPS and WRF
===========================

Install and Enable CephFS
-------------------------

You need to access the data used in this exercise. In total, the data are close to 90 GB in size. Usually, such large datasets cannot be shared easily. However, Jetstream2 has a Ceph cluster, a distributed file system that stores the data locally at Jetstream2. Any Linux machine on Jetstream2 can access this data using the following steps. 

First, update the package list::

    sudo apt update

Install CephFS client::

    sudo apt install ceph-common

The CephFS mounting steps are slightly more complicated. When a CephFS share is created, access rules must be set for writing or reading the data. This credential is called a keyring, which consists of an entity name (accessTo) and a key (accessKey). For this exercise, copy and paste the credentials for read-only access::

    accessTo="iwrf-lulc-read-only"
    accessKey="AQCLixNooPVSGBAASckRTu+xrJeDzaoQQEv6SQ=="

The following commands set up the keyring::

    mkdir -p /etc/ceph
    echo -e "[client.${accessTo}]\n    key = ${accessKey}" | sudo tee /etc/ceph/ceph.client.${accessTo}.keyring

The keyring file must be only readable to root::

    sudo chown root:root /etc/ceph/ceph.client.${accessTo}.keyring
    sudo chmod 600 /etc/ceph/ceph.client.${accessTo}.keyring

Choose the mount point for the CephFS share, which will be in the home directory::

    cephfsPath="149.165.158.38:6789,149.165.158.22:6789,149.165.158.54:6789,149.165.158.70:6789,149.165.158.86:6789:/volumes/_nogroup/6e81fe46-b69e-4d33-be08-a2580b420b81/6cc28fc1-35f3-41b4-8652-f14555097810"
    mountPoint="/home/exouser/lulc_input"

Mount to the location::

    echo "${cephfsPath} ${mountPoint} ceph name=${accessTo},x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw 0 2" | sudo tee -a /etc/fstab
    sudo systemctl daemon-reload
    mkdir -p ${mountPoint}
    sudo mount ${mountPoint}

Run the following command to test if mount is successful::

    df -h ${mountPoint}

If the CephFS share is mounted correctly, the following output is shown:

..

    Filesystem                                                                                                                                                                                       Size  Used Avail Use% Mounted on
    149.165.158.38:6789,149.165.158.22:6789,149.165.158.54:6789,149.165.158.70:6789,149.165.158.86:6789:/volumes/_nogroup/6e81fe46-b69e-4d33-be08-a2580b420b81/6cc28fc1-35f3-41b4-8652-f14555097810  100G   85G   16G  85% /home/exouser/lulc_input


Pull Docker Objects
===================

As mentioned above, the WRF and WPS software are provided as a Docker image that will run as a
`"container" <https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/>`_
on your cloud instance.
To run a Docker container, the Docker Engine must be installed on your instance.
You can then "pull" (download) the image that will be run as a container.
The Ubuntu instance you created already has the Docker Engine installed and running.

Get the Docker Image
--------------------

You must pull the correct versions of the image that will be used in this exercise onto your instance::

    sudo docker pull ncar/iwrf:lulc-2024-10-04


Using Screen in Linux
=====================
This exercise will take about 4 days to run, and during this time, any disconnects from the instance will interrupt the simulation. For this reason, it's almost necessary to use the Linux command ``screen``. By using ``screen``, you create and enter a screen session. Within it, you may run commands as if you were in a normal terminal. You can disconnect from the screen session or the instance, and any ongoing process will continue in the background. At any time, SSH back into the instance and connect to the screen session to check the progress. Disconnecting from and connecting to a screen session is called "detaching" and "attaching". In this exercise, we will only use part of the functionalities of ``screen``. You may see the full documentation of ``screen`` at `GNU Screen <https://www.gnu.org/software/screen/manual/screen.html>`_.

To start a screen session with ``lulc`` as the session name, enter the following into your terminal::

    screen -S lulc

To show all running screen sessions and see if you are attached to any screen sessions, enter the following (if you started a screen session, it displays that you are attached to one)::

    screen -ls

Inside a screen session, if you want to detach from it, you would need to press a combination of keys::
    
    Ctrl+A, D

To attach to the screen session ``lulc``, enter the following:: 

    screen -r lulc


Set Input and Output Paths
--------------------------

Copy and paste the following lines to set up paths of the input and output files::

    mkdir ~/lulc_output
    WRF_OUTPUT=~/lulc_output
    WRF_INPUT=~/lulc_input


(Optional) Exercise Script
--------------------------

Later in this instruction, you will have the option to run this exercise manually (copy lines by lines into the shell) or you could run a script to do the same thing. If you want to run the entire exercise with one script, download the script::

    wget https://raw.githubusercontent.com/NCAR/i-wrf/refs/heads/main/use_cases/Land_Use_Land_Cover/WRF/run.sh
    chmod +x run.sh
    mkdir ~/lulc_script
    WRF_SCRIPT=~/lulc_script
    mv run.sh $WRF_SCRIPT


Start WPS and WRF with a Script
===============================

You are now ready to run the Docker container that will perform the simulation. First, make sure you are in a screen session. If you would like to run the entire process in one command, you just have to run the script. If you had used a different flavor than m3.2xl (64 CPUs) on this instance, adjust the CPU core count to a suitable number in the script (e.g. ``mpiexec -n 60 -ppn 60 ./main/wrf.exe`` to ``mpiexec -n 28 -ppn 28 ./main/wrf.exe`` for the m3.xl (32 CPUs) flavor).

The script runs inside the container, prints lots of status information, and creates output files in the output directory you created. Execute this command to start a container with the image we pulled::

    sudo docker run --shm-size 100G -it \
    -v $WRF_INPUT:/home/wrfuser/lulc_input \
    -v $WRF_OUTPUT:/home/wrfuser/lulc_output \
    -v $WRF_SCRIPT:/home/wrfuser/lulc_script \
    ncar/iwrf:lulc-2024-10-04 /home/wrfuser/lulc_script/run.sh

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 100 -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:lulc-2024-10-04`` is the Docker image to use when creating the container.

The simulation will take a long time to run, and when the results are ready, the terminal will become available again. The output files will be in the ``lulc_output`` directory in the home directory. See the "View Output" section below for instructions on how to view the outputs.


Run WPS and WRF Manually (Alternative)
======================================

The instructions below will run WPS and WRF manually; it is not a continuation of "Start WPS and WRF with a Script". With everything in place, you are ready to run the Docker container that will perform the simulation. First, make sure you are in a screen session. The command below is similar to the one above, but it does not run the script. Instead, it starts the container and provides a shell prompt. From there, we will run each command one by one::

    sudo docker run --shm-size 100G -it \
    -v $WRF_INPUT:/home/wrfuser/lulc_input \
    -v $WRF_OUTPUT:/home/wrfuser/lulc_output \
    ncar/iwrf:lulc-2024-10-04 bash

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 100 -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:lulc-2024-10-04`` is the Docker image to use when creating the container.

Setting Up
----------
Set the container environment, ensure all required executables are in ``$PATH``, and address memory limits. First, source ``/etc/bashrc`` to load the environment, then allow unlimited stack size::

    source /etc/bashrc
    ulimit -s unlimited

And define some environment variables for input and output paths::

    WPS=/home/wrfuser/WPS
    WRF=/home/wrfuser/WRF
    LULC_OUTPUT=/home/wrfuser/lulc_output
    LULC_WPS_INPUT=/home/wrfuser/lulc_input/WPS_input
    LULC_WRF_INPUT=/home/wrfuser/lulc_input/WRF_input


Run WPS
-------

Note that 'Run WPS' will take several hours to finish. The first half of the instruction is to run **WRF Preprocessing Systems (WPS)** on geographic data and meteorological data. The WPS software is located at ``/home/wrfuser/WPS`` and the geographic data and meteorological data are in ``/home/wrfuser/lulc_input/WPS_input``, as ``WPS_GEOG`` and ``HRRR_PRS``, respectively.

In WPS, the program ``geogrid.exe`` creates terrestrial data from static geographic data and defines the simulation domains. The section ``&geogrid`` in the ``namelist.wps`` directs ``geogrid.exe`` to read domain configuration parameters from ``WPS_GEOG``::

    cd $WPS
    cp $LULC_WPS_INPUT/namelist/namelist_PRS.wps $WPS/namelist.wps
    ln -fs $LULC_WPS_INPUT/WPS_GEOG $WPS
    ./geogrid.exe

Next, the program ``ungrib.exe`` unpacks the meteorological data into WRF intermediate format. ``Vtable`` is used to specify which fields to unpack, by linking the Vtable file to ``$WPS/Vtable``. The meteorological data consists of two formats, ``wrfprs`` and ``wrfnat``, which are linked and unpacked separately. The ``&ungrib`` section in ``namelist.wps`` specifies which files to use. Link the files and run ``ungrib.exe`` on ``wrfprs`` files to generate files with "HRRR_PRS" headers::

    cd $WPS
    cp $LULC_WPS_INPUT/namelist/Vtable.hrrr.modified $WPS/ungrib/Variable_Tables/
    ln -sf $WPS/ungrib/Variable_Tables/Vtable.hrrr.modified $WPS/Vtable
    ./link_grib.csh $LULC_WPS_INPUT/HRRR_0703/hrrr.*.wrfprs
    ./ungrib.exe

Link the files and run ``ungrib.exe`` on ``wrfnat`` files to generate files with "HRRR_NAT" headers using a new namelist containing a different ``&ungrib`` section::

    cd $WPS
    cp $LULC_WPS_INPUT/namelist/namelist_NAT.wps $WPS/namelist.wps
    ./link_grib.csh $LULC_WPS_INPUT/HRRR_0703/hrrr.*.wrfnat
    ./ungrib.exe

The last step is to call ``metgrid.exe`` to interpolate the meteorological data onto the simulation domain, and the outputs of ``metgrid.exe`` are used as inputs to ``WRF``. This process is guided by the ``&metgrid`` section of ``namelist.wps``::

    cd $WPS
    ./metgrid.exe


Run WRF
-------

The latter half of the exercise involves running two WRF simulations to investigate the impact of land use and land cover (LULC) on simulated deep convection over different sizes of the Dallas-Fort Worth (DFW) area. The first simulation is a control simulation using data generated from the previous WPS steps. The second simulation is a perturbed simulation with modified data, where the DFW area is expanded to four times its original size.


Control Simulation
^^^^^^^^^^^^^^^^^^

The control simulation runs WRF with the outputs generated from the previous WPS steps. Copy the relevant namelist, define environment variable, and link the ``met_em`` files from WPS::

    cd $WRF
    ln -sf $WRF/run/* $WRF
    cp $LULC_WRF_INPUT/namelist/namelist.input $WRF
    cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d01.txt $WRF
    cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d02.txt $WRF
    cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d03.txt $WRF
    ln -sf $WPS/met_em* $WRF


The WRF software is located at ``/home/wrfuser/WRF``, which contains two programs, ``real.exe`` and ``wrf.exe``. ``real.exe`` vertically interpolates the outputs of ``metgrid.exe`` and generates boundary and initial conditions: ``wrfbdy_d01``, ``wrfinput_d01``, ``wrfinput_d02``, and ``wrfinput_d03``::

    cd $WRF
    ./main/real.exe


Create a directory named ``wrfdata`` in the WRF directory to store the output from WRF and run WRF simulation with 60 CPU cores. If you had used a different flavor on this instance, adjust the CPU core count to a suitable number::
    
    cd $WRF
    mkdir $WRF/wrfdata
    mpiexec -n 60 -ppn 60 ./main/wrf.exe

This step will take about 2 days to run. When it's finished, move the outputs from ``wrfdata`` to the output directory::

    mv $WRF/wrfdata $LULC_OUTPUT/ctl


DFW4X Simulation
^^^^^^^^^^^^^^^^

The perturbed simulation will modify the inputs such that the DFW area is four times its original size. Instead of making modifications on our own, the modified data is provided. 

First, remove the files used for the control simulation::

    cd $WRF
    rm met_em*
    rm wrfbdy_d01
    rm wrfinput*

Link the appropriate files for DFW4X simulation::

    ln -sf $WRF/run/* $WRF
    ln -sf $LULC_WRF_INPUT/dfw4x/wrfbdy_d01 $WRF
    ln -sf $LULC_WRF_INPUT/dfw4x/wrfinput* $WRF
    ln -sf $LULC_WRF_INPUT/dfw4x/met_em* $WRF

Create a directory named ``wrfdata`` in the WRF directory to store the output from WRF and run WRF simulation with 60 CPU cores. If you had used a different flavor on this instance, adjust the CPU core count to a suitable number::
    
    cd $WRF
    mkdir $WRF/wrfdata
    mpiexec -n 60 -ppn 60 ./main/wrf.exe

When it's finished, move the outputs from ``wrfdata`` to the output directory::

    mv $WRF/wrfdata $LULC_OUTPUT/dfw4x

After moving the outputs, you may exit the container by entering ``exit``.


View Outputs
============

To view the outputs in the ``lulc_output`` directory, you must get read permission::

    sudo chmod -R a+r $WRF_OUTPUT

Use the ``ls`` command to list the files in the ``ctl`` or ``dfw4x`` directory::

    ls $WRF_OUTPUT/ctl
    ls $WRF_OUTPUT/dfw4x
