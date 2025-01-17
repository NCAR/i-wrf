:orphan:

.. _matthewredcloud:

Running I-WRF On Red Cloud with LULC Data
******************************************************

Overview
========

The following instructions can be used to run elements of
the `I-WRF weather simulation framework <https://i-wrf.org>`_
from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_
and the `Cornell Center for Advanced Computing <https://cac.cornell.edu/>`_.
The steps below run the `Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ model with data fom `The High-Resolution Rapid Refresh (HRRR) <https://rapidrefresh.noaa.gov/hrrr/>`_ 
on the `Red Cloud cloud computing platform <https://www.cac.cornell.edu/services/cloudservices.aspx/>`_ 
provided by Cornell Center for Advanced Computing (CAC).
This exercise provides an introduction to using cloud computing platforms,
running computationally complex simulations and analyses, and using containerized applications.

Simulations like WRF often require greater computing resources
than you may have on your personal computer,
but a cloud computing platform can provide the needed computational power.
Red Cloud is a subscription-based Infrastructure as a Service cloud that provides 
root access to virtual servers and on-demand storage to Cornell researchers.
This exercise runs the I-WRF program as a Docker "container",
which simplifies the set-up work needed to run the simulation.

It is recommended that you follow the instructions in each section in the order presented
to avoid encountering issues during the process.
Most sections refer to external documentation to provide details about the necessary steps
and to offer additional background information.

Prepare to Use Red Cloud
========================

To `get started with Red Cloud <https://www.cac.cornell.edu/services/projects.aspx>`_,
you will need to:

* Get a CAC account by doing one of the following:

  * Start a new project by making a `project request <https://www.cac.cornell.edu/services/projects/project.aspx>`_ (Only available for Cornell Faculty and Staff).
  * Join an existing project by `request to be added to a project <https://www.cac.cornell.edu/services/external/RequestCACid.aspx>`_.
  * Request an exploratory account by `submitting a request <https://www.cac.cornell.edu/cu/explore.aspx>`_.

* Log in to Red Cloud's OpenStack interface.

The sections below will guide you through this process. 
For an overview of Red Cloud, read Cornell TechDocs `Red Cloud documentation <https://www.cac.cornell.edu/techdocs/redcloud/#red-cloud>`_.

Start a Project
---------------

One way to create a CAC account is to request a project. 
Note that you must be a Cornell faculty member or a staff member to view the pages below and start a project. 
You may submit a `project request <https://www.cac.cornell.edu/services/projects/project.aspx>`_ at the CAC website.
Thoroughly review the `rates <https://www.cac.cornell.edu/services/projects/rates.aspx>`_ page to understand the Red Cloud subscription service.
Once your project is approved, you can `manage your project <https://www.cac.cornell.edu/services/projects/manage.aspx>`_, and  
read `this page <https://www.cac.cornell.edu/services/projects/project.aspx>`_ to learn how to manage a project.

Join a Project
--------------

To join an existing project, submit a `join request <https://www.cac.cornell.edu/services/external/RequestCACid.aspx>`_. 
You should only do this if your PI has requested you to submit the request. 
Once the PI of the project approves the request, an email is sent to you with the login information.

Open an Exploratory Account
---------------------------

You may also request an exploratory account if you have not made one already. 
This account has limited computing hours and storage but is sufficient for this exercise. 
To request an exploratory account, submit a `request <https://www.cac.cornell.edu/cu/explore.aspx>`_.
You are also given one hour of free consulting for any help you may need.

Log in to Red Cloud OpenStack Interface
---------------------------------------

Once you are given a CAC account login information,
you can log into the `Red Cloud OpenStack web interface <https://redcloud.cac.cornell.edu/>`_.
Note that you need to be on a project with a subscription to log in successfully.

Create a Cloud Instance and Log In
==================================

After you have logged in to the Red Cloud OpenStack interface,
you are ready to create the cloud instance where you will run the I-WRF simulation.
If you are not familiar with the cloud computing terms "image" and "instance",
it is recommended that you read about them `here <https://www.cac.cornell.edu/techdocs/openstack/images/>`__ 
and `here <https://www.cac.cornell.edu/techdocs/redcloud/Red_Cloud_Linux_Instances/>`__ before proceeding.

Create an SSH Key
-----------------

You can either upload a public SSH key to Red Cloud or generate an SSH key pair on Red Cloud before creating your instance.
Red Cloud injects the uploaded public key or generated public key into the instance's default user account,
and you will need to provide the matching private SSH key to log in to the instance.
If you are not familiar with "SSH key pairs", you should
`read about them <https://www.cac.cornell.edu/techdocs/openstack/keypairs/>`__ before continuing.

* First, `create an SSH Key on your computer <https://www.cac.cornell.edu/techdocs/openstack/keypairs/#creating-a-passphrase-protected-key-pair-recommended>`_ using the "ssh-keygen" command.  That command allows you to specify the name of the private key file it creates, with the default being "id_rsa".  The matching public key file is saved and named with ".pub" appended to the filename. 
* Then, `import the public key to Red Cloud <https://www.cac.cornell.edu/techdocs/openstack/keypairs/#importing-a-key-pair>`_ through the Red Cloud web interface.

Alternatively, you can `create a key pair on Red Cloud <https://www.cac.cornell.edu/techdocs/openstack/keypairs/#creating-a-key-pair-without-a-passphrase>`_. Be sure to follow the steps and save the private key it generated with the correct format and permission before proceeding. 

Create an Instance
------------------

The Cornell TechDocs `Creating a New Linux Instance <https://www.cac.cornell.edu/techdocs/redcloud/Red_Cloud_Linux_Instances/#creating-a-new-linux-instance>`_
provides detailed information about creating a Linux instance on Red Cloud.
While following those steps, be sure to make the following choices for this instance:

* When choosing an image as the instance source:
  
  * Select Boot from Source is "Image"
  * Volume Size (GB) is 1000
  * Delete Volume on Instance Delete is "Yes"
  * Select the "ubuntu-24.04-LTS" image

* In Flavor, choose the "Flavor" c64.m120 (64 Virtual CPUs) to provide a faster simulation run-time. Note that this will consume subscriptions very fast.
* In Network, select "public".
* In Key Pair, select the SSH public key that you uploaded previously.

When all the required options are selected, click on the "Launch Instance" button, and wait for the instance to enter the "Active" state.
Note that the instance will not only be created, but will be running so that you can log in right away.

Log in to the Instance
----------------------

The instructions for `connecting to Red Cloud Linux instances using SSH <https://www.cac.cornell.edu/techdocs/redcloud/Red_Cloud_Linux_Instances/#accessing-instances>`_
can be executed in the Command Prompt on Windows (from the Start menu, type "cmd" and select Command Prompt)
or from the Terminal application on a Mac.

In either case, you will need to know the location and name of the private SSH key created on your computer (see above),
the IP address of your instance (found in the Red Cloud OpenStack interface)
and the default username on your instance, which is "ubuntu".

Once you are logged in to the instance you can proceed to the
"Install Software and Download Data" section below.
You will know that your login has been successful when the prompt has the form ``ubuntu@instance-name:~$``,
which indicates your username, the instance name, and your current working directory, followed by "$"

Managing a Red Cloud Instance
------------------------------

In order to use cloud computing resources efficiently, you must know how to
`manage your instances <https://www.cac.cornell.edu/techdocs/openstack/#instance-states>`_.
Instances incur costs whenever they are running (on Red Cloud, this is when they are "Active").
"Shelving" an instance stops it from using the cloud's CPUs and memory,
and therefore stops it from incurring any charges against your project.

When you are through working on this exercise,
be sure to use the instance's dropdown menu in the web interface to
"Shelve" the instance so that it is no longer spending your computing hours.
If you later return to the web interface and want to use the instance again,
Use the dropdown menu's "Unshelve Instance" option to start the instance up again.
Note that any programs that were running when you shelve the instance will be lost,
but the contents of the disk are preserved when shelving.

You may also want to try the "Resize" action to change the number of CPUs of the instance.
Increasing the number of CPUs (say, to flavor "c8.m64") can make your computations finish more quickly.
But of course, doubling the number of CPUs doubles the cost per hour to run the instance,
so Shelving as soon as you are done becomes even more important!

Preparing the Environment
=========================

With your instance created and running and you logged in to it through SSH,
you can now install the necessary software and download the data to run the simulation.
You will only need to perform these steps once,
as they essentially change the contents of the instance's disk
and those changes will remain even after the instance is shelved and unshelved.

The following sections instruct you to issue numerous Linux commands in your shell.
If you are not familiar with Linux, you may want to want to refer to
`An Introduction to Linux <https://cvw.cac.cornell.edu/Linux>`_ when working through these steps.
The commands in each section can be copied using the button in the upper right corner
and then pasted into your web shell by right-clicking.


Download Data for WPS and WRF
=============================

To run WRF on the HRRR and LULC data set, you need to have several data sets to support the computation. The commands in these sections download archive files containing that data, then uncompress the archives into folders. The geographic data is large and takes several minutes to acquire, while the other dataset should already be in the attached volume. 


Get the geographic data representing the terrain in the area of the simulation::

    cd ~
    wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
    tar -xzf geog_high_res_mandatory.tar.gz
    rm geog_high_res_mandatory.tar.gz
    WPS_GEOG="~/WPS_GEOG"

Get the HRRR data and namelists (GRIB2 files)::

    TODO: Find a way to share the HRRR data and the namelists.
    Currently, it's a volume in JetStream2, in /media/volume/I-WRF_input.
    WRF_INPUT="/mnt/I-WRF_input"

If you would like to want to run the entire procedure with one script::

    TODO: Change this from issue 68 to main
    wget https://raw.githubusercontent.com/NCAR/i-wrf/refs/heads/feature_68_LULC_Instruction/use_cases/Land_Use_Land_Cover/WRF/run.sh
    chmod +x run.sh
    mv run.sh $WRF_INPUT

Create a folder for the output::

    mkdir output
    WRF_OUTPUT="~/output"

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


Get the WRF Docker Image
------------------------

Once Docker is running, you must pull the correct versions of the WRF and METplus images onto your instance::

    docker pull ncar/iwrf:lulc-2024-10-04
    

Start WRF with script
=====================

With everything in place, you are now ready to run the Docker container that will perform the simulation. If you would like to run the entire script in one command, we just have to run the script. The downloaded script runs inside the container, prints lots of status information, and creates output files in the run folder you created. Execute this command start a container with the image we pulled earlier::

    docker run --shm-size 200G -it \
    -v $WRF_INPUT:/home/wrfuser/input \
    -v $WRF_OUTPUT:/home/wrfuser/output \
    -v $WPS_GEOG:/home/wrfuser/WPS_GEOG \
    ncar/iwrf:lulc-2024-10-04 /home/wrfuser/input/run.sh

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 200 -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:lulc-2024-10-04`` is the Docker image to use when creating the container.

The simulation will take a long time to run, and when the results are ready, the terminal would become available again. The output files will be in the output folder. 


Start WPS and WRF Manually
==========================

With everything in place, you are now ready to run the Docker container that will perform the simulation. The command below is similar to the one above, but it does not run the script. Instead, it starts the container and provides a shell prompt. From there, we will run each command one by one::

    docker run --shm-size 200G -it \
    -v $WRF_INPUT:/home/wrfuser/input \
    -v $WRF_OUTPUT:/home/wrfuser/output \
    -v $WPS_GEOG:/home/wrfuser/WPS_GEOG \
    ncar/iwrf:lulc-2024-10-04 


Run WPS
=======

We now need to set up the environment in the container to ensure proper files and programs are found and there will not be memory issues. First, "source" bashrc to load the environment and then allow unlimited memory to be used in this container:: 

    source /etc/bashrc
    ulimit -s unlimited


The first step of LULC is to run a few commands with WRF Pre-Processing System (WPS). The geogrid.exe in the WPS should be run with the correct namelist::
    
    cd /home/wrfuser/WPS
    cp /home/wrfuser/input/namelist/WPS/namelist1.wps /home/wrfuser/WPS/namelist.wps
    ./geogrid.exe


Next, link the files from the Vtable and link the HRRR files wit Vtable. Call ungrib.exe to generate files with HRRR_PRS headers::

    cp /home/wrfuser/input/namelist/WPS/Vtable.hrrr.modified /home/wrfuser/WPS/ungrib/Variable_Tables/
    ln -sf ./ungrib/Variable_Tables/Vtable.hrrr.modified Vtable
    ./link_grib.csh /home/wrfuser/input/HRRR/0703/hrrr.*.wrfprs
    ./ungrib.exe

We need to do the same steps to genereate HRRR_NAT files. So we copy another namelist and link the HRRR data, and run ungrib.exe to generate files with HRRR_NAT headers:: 

    cp /home/wrfuser/input/namelist/WPS/namelist2.wps /home/wrfuser/WPS/namelist.wps
    ./link_grib.csh /home/wrfuser/input/HRRR/0703/hrrr.*.wrfnat
    ./ungrib.exe

Finally, we can finalize the WPS process by calling metgrid.exe, which will read both HRRR_PRS and HRRR_NAT files::

    ./metgrid.exe


Run WRF
=======

To run the simulation with LULC modifications, we need to link WRF/run and the met_ems files we generated from WPS and copy the new namelist::

    cd /home/wrfuser/WRF
    ln -sf /home/wrfuser/WRF/run/* .
    cp /home/wrfuser/input/namelist/WRF/namelist.input .
    cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d01.txt .
    cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d02.txt .
    cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d03.txt .
    ln -sf /home/wrfuser/WPS/met_em* .

Run real.exe to generate boundary conditions for WRF input::

    ./main/real.exe

Create a folder named "wrfdata" and run WRF simulations with 60 CPU cores::
    
    mkdir wrfdata
    mpiexec -n 60 -ppn 60 ./main/wrf.exe

This step will take about 2 days to run. When it's finished, copy the output from wrfdata to the output folder::

    mv -r wrfdata/* /home/wrfuser/output

You can now exit the container by entering "exit", and the output files will be in the output folder.
