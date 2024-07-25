:orphan:

.. _matthewredcloud:

Running I-WRF On Red Cloud with Hurricane Matthew Data
******************************************************

Overview
========

The following instructions can be used to run elements of
the `I-WRF weather simulation framework <https://i-wrf.org>`_
from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_
and the `Cornell Center for Advanced Computing <https://cac.cornell.edu/>`_.
The steps below run the `Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ model
and the  `METplus <https://https://dtcenter.org/community-code/metplus>`_ verification framework
with data from `Hurricane Matthew <https://en.wikipedia.org/wiki/Hurricane_Matthew>`_
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
  * Volume Size (GB) is 100
  * Delete Volume on Instance Delete is "Yes"
  * Select the "ubuntu-22.04-LTS" image

* In Flavor, choose the "Flavor" c4.m32 (4 Virtual CPUs) to provide a faster simulation run-time.
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

Define Environment Variables
----------------------------

We will be using some environment variables throughout this exercise to
make sure that we refer to the same resource names and file paths wherever they are used.
Copy and paste the definitions below into your shell to define the variables before proceeding::

    WRF_IMAGE=ncar/iwrf:latest
    METPLUS_IMAGE=dtcenter/metplus-dev:develop
    WORKING_DIR=/home/ubuntu
    WRF_DIR=${WORKING_DIR}/wrf/20161006_00
    METPLUS_DIR=${WORKING_DIR}/metplus
    WRF_CONFIG_DIR=${WORKING_DIR}/i-wrf/use_cases/Hurricane_Matthew/WRF
    METPLUS_CONFIG_DIR=${WORKING_DIR}/i-wrf/use_cases/Hurricane_Matthew/METplus
    OBS_DATA_VOL=data-matthew-input-obs

Any time you open a new shell on your instance, you will need to perform this action
to redefine the variables before executing the commands that follow.

Create the WRF and METplus Run Folders
--------------------------------------

The simulation is performed using a script that expects to run in a folder where it can create result files.
The first command below creates a folder (named "wrf") under the user's home directory,
and a sub-folder within "wrf" to hold the output of this simulation.
The subfolder is named "20161006_00", which is the beginning date and time of the simulation.
Similarly, a run folder named "metplus" must be created for the METplus process to use::

    mkdir -p ${WRF_DIR}
    mkdir -p ${METPLUS_DIR}

Download Configuration Files
----------------------------

Both WRF and METplus require some configuration files to direct their behavior,
and those are downloaded from the I-WRF GitHub repository.
Some of those configuration files are then copied into the run folders.
These commands perform the necessary operations::

    git clone https://github.com/NCAR/i-wrf ${WORKING_DIR}/i-wrf
    cp ${WRF_CONFIG_DIR}/namelist.* ${WRF_DIR}
    cp ${WRF_CONFIG_DIR}/vars_io.txt ${WRF_DIR}
    cp ${WRF_CONFIG_DIR}/run.sh ${WRF_DIR}

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

    sudo docker pull ${WRF_IMAGE}
    sudo docker pull ${METPLUS_IMAGE}

METplus is run to perform verification of the results of the WRF simulation using
observations gathered during Hurricane Matthew.
We download that data by pulling a Docker volume that holds it,
and then referencing that volume when we run the METplus Docker container.
The commands to pull and create the volume are::

    sudo docker pull ncar/iwrf:${OBS_DATA_VOL}.docker
    sudo docker create --name ${OBS_DATA_VOL} ncar/iwrf:${OBS_DATA_VOL}.docker

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

    cd ${WORKING_DIR}
    wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
    tar -xzf geog_high_res_mandatory.tar.gz
    rm geog_high_res_mandatory.tar.gz

Get the case study data (GRIB2 files)::

    cd ${WRF_DIR}
    wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_1deg.tar.gz
    tar -xvzf matthew_1deg.tar.gz
    rm -f matthew_1deg.tar.gz

Get the SST (Sea Surface Temperature) data::

    cd ${WRF_DIR}
    wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_sst.tar.gz
    tar -xzvf matthew_sst.tar.gz
    rm -f matthew_sst.tar.gz

Run WRF
=======

With everything in place, you are now ready to run the Docker container that will perform the simulation.
The downloaded script runs inside the container, prints lots of status information,
and creates output files in the run folder you created.
Execute this command to run the simulation in your shell::

    sudo docker run --shm-size 14G -it \
      -v ${WORKING_DIR}:/home/wrfuser/terrestrial_data \
      -v ${WRF_DIR}:/tmp/hurricane_matthew \
      ${WRF_IMAGE} /tmp/hurricane_matthew/run.sh

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 14G -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:latest`` is the Docker image to use when creating the container.
* ``/tmp/hurricane_matthew/run.sh`` is the location within the container of the script that it runs.

The simulation initially prints lots of information while initializing things, then settles in to the computation.
The provided configuration simulates 48 hours of weather and takes about 26 minutes to finish on a c4.m32 Red Cloud instance.
Once completed, you can view the end of an output file to confirm that it succeeded::

    tail ${WRF_DIR}/rsl.out.0000

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

    sudo docker run --rm -it \
      --volumes-from ${OBS_DATA_VOL} \
      -v ${METPLUS_CONFIG_DIR}:/config \
      -v ${WORKING_DIR}/wrf:/data/input/wrf \
      -v ${METPLUS_DIR}:/data/output ${METPLUS_IMAGE} \
      /metplus/METplus/ush/run_metplus.py /config/PointStat_matthew.conf

Progress information is displayed while the verification is performed.
**WARNING** log messages are expected because observations files are not available for every valid time and METplus is
configured to allow some missing inputs. An **ERROR** log message indicates that something went wrong.
METplus first converts the observation data files to a format that the MET tools can read using the MADIS2NC wrapper.
Point-Stat is run to generate statistics comparing METAR observations to surface-level model fields and
RAOB observations to "upper air" fields.
METplus will print its completion status when the processing finishes.

The results of the METplus verification can be found in ``${WORKING_DIR}/metplus/point_stat``.
These files contain tabular output that can be viewed in a text editor. Turn off word wrapping for better viewing.
Refer to the MET User's Guide for more information about the
`Point-Stat output <https://met.readthedocs.io/en/latest/Users_Guide/point-stat.html#point-stat-output>`_.
In the near future, this exercise will be extended to include instructions to visualize the results.
