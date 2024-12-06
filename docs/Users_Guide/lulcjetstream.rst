:orphan:

.. _matthewjetstream:

Running I-WRF On Jetstream2 with LULC
*******************************************************

Overview
========

The following instructions can be used to run elements of the `I-WRF weather simulation framework <https://i-wrf.org>`_ from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_ and the `Cornell Center for Advanced Computing <https://cac.cornell.edu/>`_. The steps below run the `Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ model with data fom `The High-Resolution Rapid Refresh <https://rapidrefresh.noaa.gov/hrrr/>(HRRR)`_ on the `Jetstream2 cloud computing platform <https://jetstream-cloud.org/>`_. This exercise provides an introduction to using cloud computing platforms, running computationally complex simulations and analyses, and using containerized applications.

Simulations like WRF often require greater computing resources than you may have on your personal computer, but a cloud computing platform can provided the needed computational power. Jetstream2 is a national cyberinfrastructure resource that is easy to use and is available to researchers and educators.This exercise runs the I-WRF programs as Docker "containers", which simplifies the set-up work needed to run the simulation and verification.

It is recommended that you follow the instructions in each section in the order presented to avoid encountering issues during the process. Most sections refer to external documentation to provide details about the necessary steps and to offer additional background information.

Get an ACCESS Account and Add an Allocation to It
=================================================

To `get started with Jetstream2 <https://jetstream-cloud.org/get-started>`_, you will need to create an account with the `National Science Foundation (NSF) <https://www.nsf.gov/>`_'s `ACCESS program <https://access-ci.org/>`_. If you do not already have one, `register for an ACCESS account <https://operations.access-ci.org/identity/new-user>`_. When registering your account, you can either choose to associate your existing University/Organizational account or create an entirely new ACCESS account when registering. The Jetstream2 team strongly recommends that you create a new ACCESS account, as your organizational affiliation may change in the future.

Once you have an account you will need to have a computational "allocation" added to that account. Allocations provide the credits you will spend when running instances on Jetstream2. If there are no allocation owners who can add you to their allocation and you are interested in obtaining your own, you may `request an allocation <https://allocations.access-ci.org/get-your-first-project>`_ that will allow you to use an ACCESS-affiliated cyberinfrastructure resource. Note that allocations may only be requested by faculty, staff and graduate researchers, so undergraduates must work with a faculty sponsor to requeste an allocation.

Be sure to read all of the information on the request page so that you make a suitable request. Note that you will need to describe the project for which the allocation is intended and provide a CV or resume for the principal investigator. An "Explore" project (400,000 credits) will be much more than enough to work with this exercise. You will want to work with the resource "Indiana Jetstream2 CPU" (*not* **GPU**). The typical turnaround time for allocation requests is one business day.

Log in to Jetstream2's Exosphere Web Site
=========================================

Once you have an ACCESS account and an allocation has been added to it, you can log in to Jetstream's `Exosphere web dashboard <https://jetstream2.exosphere.app>`_. The process of identifying your allocation and ACCESS ID to use Jetstream2 is described on `this page <https://cvw.cac.cornell.edu/jetstream/intro/jetstream-login>`__ of the `Introduction to Jetstream2 <https://cvw.cac.cornell.edu/jetstream>`_ Cornell Virtual Workshop, and on `this page <https://docs.jetstream-cloud.org/ui/exo/login>`__ of the `Jetstream2 documentation <https://docs.jetstream-cloud.org>`_.

While adding an allocation to your account, it is recommended that you choose the "Indiana University" region of Jetstream2 for completing this exercise.

Create a Cloud Instance on Jetstream2
=====================================

After you have logged in to Jetstream2 and added your allocation to your account, you are ready to create the cloud instance where you will run the simulation and verification. If you are not familiar with the cloud computing terms "image" and "instance", it is recommended that you `read about them <https://cvw.cac.cornell.edu/jetstream/intro/imagesandinstances>`__ before proceeding.

For this tutorial, you will be able to log in to your instance using Exosphere's Web Desktop or Web Shell functionalities. If you would rather log in using the "ssh" command from a shell on your own computer, you will need to create an SSH key pair and upload it to Jetstream2 before creating your instance. Optional information about doing those things is available here:

.. dropdown:: Creating an SSH Key and uploading it to Jetstream2

    You may choose to upload a public SSH key to Jetstream2 before creating your instance. Jetstream2 will inject that public key into an instance's default user account, and you will need to provide the matching private SSH key to log in to the instance. If you are not familiar with "SSH key pairs", you should `read about them <https://cvw.cac.cornell.edu/jetstream/keys/about-keys>`__ before continuing.

    * First, `create an SSH Key on your computer <https://cvw.cac.cornell.edu/jetstream/keys/ssh-create>`_ using the "ssh-keygen" command.  That command allows you to specify the name and location of the private key file it creates, with the default being "id_rsa".  The matching public key file is saved to the same location and name with ".pub" appended to the filename.  Later instructions will assume that your private key file is named "id_rsa", but you may choose a different name now and use that name in those later instructions.
    * Then, `upload the public key to Jetstream2 <https://cvw.cac.cornell.edu/jetstream/keys/ssh-upload>`_ through the Exosphere web interface.

The Cornell Virtual Workshop topic `Creating an Instance <https://cvw.cac.cornell.edu/jetstream/create-instance>`_ provides detailed information about creating a Jetstream2 instance. While following those steps for this tutorial, be sure to make the following choices for this instance:

TODO: Find an appropiate flavor and disk size. Current setup is very pricy!

* When choosing an image as the instance source, if viewing "By Type", select the "Ubuntu 24.04" image.  If viewing "By Image", choose the "Featured-Ubuntu24" image.
* Choose the "Flavor" r3.large (64 CPUs) to provide a faster simulation run-time. 
* Select a custom disk size of 800 GB, which is large enough to hold this exercise's data and results.
* For "Enable web desktop?", select Yes.
* For "Choose an SSH public key", select None unless you want to use your own SSH key that you uploaded previously.
* You do not need to set any of the Advanced Options.

After clicking the "Create" button, wait for the instance to enter the "Ready" state (it takes several minutes). Note that the instance will not only be created, but will be running so that you can log in right away.

Log in to the Instance
======================

The Exosphere web dashboard provides two easy-to-use methods for logging in to your instance through a web browser. The "Web Shell" button will open a terminal to your instance, and the "Wed Desktop" button will open a view of the instance's graphical desktop (if enabled). Both views open in a new browser tab, and Exosphere automatically logs you in to the instance. For this tutorial you should open a Web Desktop so that you will be able to view the plots that are generated from the simulation output.

If you wish to log in to the instance from a shell on your computer, you can do so following the information in this optional content:

.. dropdown:: Logging in to a Jetstream2 Instance using SSH From a Shell

    You can use the SSH command to access your instance from a shell on your computer. The instructions for `connecting to Jetstream2 using SSH <https://cvw.cac.cornell.edu/jetstream/instance-login/sshshell>`_ can be executed in the Command Prompt on Windows (from the Start menu, type "cmd" and select Command Prompt) or from the Terminal application on a Mac.

    In either case you will need to know the location and name of the private SSH key created on your computer (see SSH section, above), the IP address of your instance (found in the Exosphere web dashboard) and the default username on your instance, which is "exouser".

    Once you are logged in to the instance you can proceed to the  "Install Software and Download Data" section below.

Once you are logged in to the instance, your shell prompt will have the form ``exouser@instance-name:~$``, which indicates your username, the instance name, and your current working directory, followed by "$".

Preparing the Environment
=========================

With your instance created and running and you logged in to it through SSH, you can now install Docker software and download the data to run the simulation. You will only need to perform these steps once, as they essentially change the contents of the instance's disk and those changes will remain even after the instance is shelved and unshelved.

The following sections instruct you to issue numerous Linux commands in your shell. If you are not familiar with Linux, you may want to want to refer to `An Introduction to Linux <https://cvw.cac.cornell.edu/Linux>`_ when working through these steps. The commands in each section can be copied using the button in the upper right corner and then pasted into your shell by right-clicking.

If your shell ever becomes unresponsive or disconnected from the instance, you can recover from that situation by opening a new Web Desktop (if available) or rebooting the instance. In the Exosphere dashboard page for your instance, in the Actions menu, select "Reboot". The process takes several minutes, after which the instance status will return to "Ready".


Pull Docker Objects
===================

As mentioned above, the WRF software are provided as Docker images that will run as a `"container" <https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/>`_ on your cloud instance. To run a Docker container, the Docker Engine must be installed on your instance. You can then "pull" (download) the WRF image that will be run as containers. The Ubuntu instance you created already has the Docker Engine installed and running.

Get the WRF Docker Images
-------------------------------------------------------------------

You must pull the correct versions of the WRF image onto your instance::

    docker pull ncar/iwrf:lulc-2024-10-04


Download Data for WPS and WRF
=============================

To run WRF on the HRRR and LULC data set, you need to have several data sets to support the computation. The commands in these sections download archive files containing that data, then uncompress the archives into folders. The geographic data is large and takes several minutes to acquire, while the other dataset should already be in the attached volume. 

TODO: Find a way to share the HRRR data and namelists.

Get the geographic data representing the terrain in the area of the simulation::

    cd ~
    wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
    tar -xzf geog_high_res_mandatory.tar.gz
    rm geog_high_res_mandatory.tar.gz

Get the HRRR data and namelists (GRIB2 files)::

    It's in /media/volume/I-WRF_input. Similarly, there is a /media/volume/I-WRF_output volume.


Start WRF
=========

With everything in place, you are now ready to run the Docker container that will perform the simulation. The downloaded script runs inside the container, prints lots of status information, and creates output files in the run folder you created. Execute this command start a container with the image we pulled earlier::

TODO: change arguments as necessary.

    docker run --shm-size 400G -it \
    -v /media/volume/I-WRF_input:/home/wrfuser/input \
    -v /media/volume/I-WRF_output:/home/wrfuser/output \
    -v /home/exouser/WPS_GEOG:/home/wrfuser/WPS_GEOG \
    ncar/iwrf:lulc-2024-10-04

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 400G -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:lulc-2024-10-04`` is the Docker image to use when creating the container.

Since we didn't provide a script at the end, it creates a container from the image and our shell is replaced with the container's environment. This container has the necessary files to run both WPS and WRF from the data we downloaded. 

Run WPS
=======

We now set up the environment in the container to ensure proper files are found and there will not be memoruy issues. First "source" bashrc to load the environment and then allow unlimited memory to be used in this container:: 

    source /etc/bashrc
    ulimit -s unlimited

To start simulation, we need to run a few commands with WRF Pre-Processing System (WPS). The geogrid.exe must be run with the correct namelist::
    
    cd /home/wrfuser/WPS
    cp /home/wrfuser/input/namelist/WPS/namelist1.wps /home/wrfuser/WPS/namelist.wps
    ./geogrid.exe


Next, link the files from our attached volumes and link the HRRR data. Call ungrib.exe to generate files with HRRR_PRS headers::

    cp /home/wrfuser/input/namelist/WPS/Vtable.hrrr.modified /home/wrfuser/WPS/ungrib/Variable_Tables/
    ln -sf ./ungrib/Variable_Tables/Vtable.hrrr.modified Vtable
    ./link_grib.csh /home/wrfuser/input/HRRR/0703/hrrr.*.wrfprs
    ./ungrib.exe

We need to do the same for WRFNAT files, so we copy a new namelist, link the HRRR data, and run ungrib.exe to generate files with HRRR_NAT headers:: 

    cp /home/wrfuser/input/namelist/WPS/namelist2.wps /home/wrfuser/WPS/namelist.wps
    ./link_grib.csh /home/wrfuser/input/HRRR/0703/hrrr.*.wrfnat
    ./ungrib.exe

Finally, we can finalize the WPS process by calling metgrid.exe, which will read both HRRR_PRS and HRRR_NAT files::

    ./metgrid.exe


Run WRF
=======

To run the simulation with LULC modifications, we need to link the met_ems files we generated from WPS and copy the new namelist. 

    cd /home/wrfuser/WRF
    cp /home/wrfuser/input/namelist/WRF/namelist.input /home/wrfuser/WRF
    cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d01.txt /home/wrfuser/WRF
    cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d02.txt /home/wrfuser/WRF
    cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d03.txt /home/wrfuser/WRF
    ln -sf /home/wrfuser/WPS/met_em* .

Run real.exe to generate boundary conditions for WRF input::

    ./main/real.exe

TODO change core number as needed. 
Run WRF simulations with 60 CPU cores::
    
    mpiexec -n 60 -ppn 60 ./main/wrf.exe


Managing Your Jetstream2 Instance
=================================

In order to use cloud computing resources efficiently, you must know how to `manage your instances <https://cvw.cac.cornell.edu/jetstream/manage-instance/states-actions>`_. Instances incur costs whenever they are running (on Jetstream2, this is when they are "Ready"). "Shelving" an instance stops it from using the cloud's CPUs and memory, and therefore stops it from incurring any charges against your allocation.

When you are through working on this exercise, you should shelve your instance. Note that any programs that are running when you shelve the instance will be terminated, but the contents of the disk are preserved when shelving.

To shelve, you need to be in the details page for your instance (with the "Actions" menu in the upper right). If you are on the Instances page, click and instance's name to be taken to its details page. From the Actions menu, select Shelve. You will be prompted in that location to confirm the shelve action - click Yes to complete the action. In the Instances page your instance will briefly be listed as "Shelving", and then as "Shelved" when the operation is complete.

When you later return to the dashboard and want to use the instance again, use the Action menu's "Unshelve" option to start the instance up again. You can also use the "Resize" action to change the flavor (number of CPUs and amount of RAM) of the instance. Increasing the number of CPUs can make your computations finish more quickly, but doubling the number of CPUs doubles the cost per hour to run the instance, so Shelving as soon as you are done becomes even more important!
