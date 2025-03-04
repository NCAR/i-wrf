:orphan:

.. _lulcredcloud:

Running I-WRF On Red Cloud with LULC Data
*****************************************


Overview
========

The following instructions can be used to run elements of
the `I-WRF weather simulation framework <https://i-wrf.org>`_
from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_
and the `Cornell Center for Advanced Computing <https://cac.cornell.edu/>`_.
The steps below run the `Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ 
model with data from `The High-Resolution Rapid Refresh (HRRR) <https://rapidrefresh.noaa.gov/hrrr/>`_ 
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

To `get started with Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud2/#getting-started-on-red-cloud-v2>`_,
you will need to:

* Go to the `CAC portal <https://portal.cac.cornell.edu/>`_ and log in. The instructions to log in are on the `CAC TechDocs page: Login <https://portal.cac.cornell.edu/techdocs/general/CACportal/#portal-login>`_.

* Get access to Red Cloud by doing one of the following options on the CAC portal:

  * Start a new project by making a project request. The instructions are on the `CAC TechDocs page: As a Cornell Faculty or Staff, How Do I Start a new Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#as-a-cornell-faculty-or-staff-how-do-i-start-a-new-project>`__ (Only available for Cornell Faculty and Staff)

  * Join an existing project. The instructions are on the `CAC TechDocs page: How Do I Join an Existing Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-join-an-existing-project>`__
  
  * Request an exploratory account. The instructions are on the `CAC TechDocs page: How Do I Request an Exploratory Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-request-an-exploratory-account>`__ Note that an exploratory project might not have enough compute hours to complete this set of instructions.

* For the new projects and the existing projects, make sure that the project has Red Cloud subscriptions. 

* Log in to Red Cloud's Horizon interface.

The sections below will guide you through this process. 
For an overview of Red Cloud, read Cornell CAC TechDocs `Red Cloud documentation <https://www.cac.cornell.edu/techdocs/redcloud2/#red-cloud-v2>`_.


Start a Project
---------------

One way to get a CAC account is to request a project. 
Note that you must be a Cornell faculty member or a staff member to view the pages below and start a project. 
You may submit a project request at the CAC portal.
Thoroughly review the `rates <https://www.cac.cornell.edu/services/projects/rates.aspx>`_ page to understand the Red Cloud subscription service.
Once your project is approved, you can manage your project on the CAC portal. Read `Portal Overview <https://www.cac.cornell.edu/techdocs/general/CACportal/#portal-overview>`_ to learn how to manage a project. Detailed instructions to start a project are available at the `CAC TechDocs page: As a Cornell Faculty or Staff, How Do I Start a new Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#as-a-cornell-faculty-or-staff-how-do-i-start-a-new-project>`__


Join a Project
--------------

To join an existing project, submit a request to join on the CAC portal. You should only do this if your PI has requested you to submit the request. Once the PI of the project approves the request, an email is sent to you with the login information. For the full instructions, read the `CAC TechDocs page: How Do I Join an Existing Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-join-an-existing-project>`__


Open an Exploratory Account
---------------------------

You may also request an exploratory account if you have not made one already. 
This account has limited computing hours and storage and may be insufficient for this exercise. 
To request an exploratory account, go to the CAC portal and submit an exploration account request. 
You are also given one hour of free consulting for any help you may need. For the full instructions, read the `CAC TechDocs page: How Do I Request an Exploratory Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-request-an-exploratory-project>`__


Log in to Red Cloud Horizon Web Interface
-----------------------------------------

Once you are in a project with Red Cloud subscription,
you can log into the `Red Cloud Horizon web interface <https://redcloud2.cac.cornell.edu/>`_.
Note that you need to be on a project with a subscription to log in successfully.


Create a Cloud Instance and Log In
==================================

After you have logged in to the Red Cloud Horizon web interface,
you are ready to create the cloud instance where you will run the I-WRF simulation.
If you are not familiar with the cloud computing terms "image" and "instance",
it is recommended that you read about them `here <https://www.cac.cornell.edu/techdocs/redcloud2/compute/#images>`__ 
and `here <https://www.cac.cornell.edu/techdocs/redcloud2/run_linux_instances/>`__ before proceeding.


Create an SSH Key
-----------------

You can either upload a public SSH key to Red Cloud or generate an SSH key pair on Red Cloud before creating your instance.
Red Cloud injects the uploaded public key or generated public key into the instance's default user account,
and you will need to provide the matching private SSH key to log in to the instance.
If you are not familiar with "SSH key pairs", you should
`read about them <https://www.cac.cornell.edu/techdocs/redcloud2/compute/#keypairs>`__ before continuing.

* First, `create an SSH Key on your computer <https://www.cac.cornell.edu/techdocs/openstack/keypairs/#creating-a-passphrase-protected-key-pair-recommended>`_ using the "ssh-keygen" command.  That command allows you to specify the name of the private key file it creates, with the default being "id_rsa".  The matching public key file is saved and named with ".pub" appended to the filename. 
* Then, `import the public key to Red Cloud <https://www.cac.cornell.edu/techdocs/redcloud2/horizon_ssh_keys/#import-a-public-key>`_ through the Red Cloud web interface.

Alternatively, you can `create a key pair on Red Cloud <https://www.cac.cornell.edu/techdocs/redcloud2/horizon_ssh_keys/#create-a-new-ssh-key-pair>`_. Be sure to follow the steps and save the private key it generated with the correct format and permission before proceeding. 


Create a Security Group
-----------------------

Security groups are firewalls that control inbound and outbound network traffic to your instances. To access a Linux instance, the rule SSH must be enabled in the security group. You can read more about security groups `here <https://www.cac.cornell.edu/techdocs/redcloud2/network/#security>`__. To create such a security group, follow the steps below:

* First, create a security group with `these instructions <https://www.cac.cornell.edu/techdocs/redcloud2/horizon_security_groups/#create-a-security-group>`__.

* Then, add the SSH rule to the security group to allow SSH traffic with `these instructions <https://www.cac.cornell.edu/techdocs/redcloud2/horizon_security_groups/#manage-your-security-group>`__.


Create an Instance
------------------

The Cornell TechDocs `Creating a New Linux Instance <https://www.cac.cornell.edu/techdocs/redcloud2/run_linux_instances/#creating-a-new-linux-instance>`_
provides detailed information about creating a Linux instance on Red Cloud.
While following those steps, be sure to make the following choices for this instance:

* When choosing an image as the instance source:
  
  * Select Boot from Source is "Image"
  * Volume Size (GB) is 1500
  * Delete Volume on Instance Delete is "Yes"
  * Select the "ubuntu-24.04-LTS" image

* In Flavor, choose the "Flavor" c64.m120 (64 Virtual CPUs) to provide a faster simulation run-time. Note that this will consume subscriptions very fast.
* In Network, select "public".
* In Security Groups, select the group with SSH rule enabled.
* In Key Pair, select the SSH public key that you uploaded previously.

When all the required options are selected, click on the "Launch Instance" button, and wait for the instance to enter the "Active" state.
Note that the instance will not only be created, but also running so that you can log in right away.


Log in to the Instance
----------------------

The instructions for `connecting to Red Cloud Linux instances using SSH <https://www.cac.cornell.edu/techdocs/redcloud2/run_linux_instances/#accessing-instances>`_
can be executed in the Command Prompt on Windows (from the Start menu, type "cmd" and select Command Prompt)
or from the Terminal application on a Mac.

In either case, you will need to know the location and name of the private SSH key created on your computer (see above),
the IP address of your instance (found in the Red Cloud OpenStack interface)
and the default username on your instance, which is "ubuntu".

Once you are logged in to the instance, you can proceed to the
"Install Software and Download Data" section below.
You will know that your login has been successful when the prompt has the form ``ubuntu@instance-name:~$``,
which indicates your username, the instance name, and your current working directory, followed by "$"


Managing a Red Cloud Instance
-----------------------------

In order to use cloud computing resources efficiently, you must know how to
`manage your instances <https://www.cac.cornell.edu/techdocs/redcloud2/compute/#instance-states>`_.
Instances incur costs whenever they are running (on Red Cloud, this is when they are "Active").
"Shelving" an instance stops it from using the cloud's CPUs and memory,
and therefore stops it from incurring any charges against your project.

When you are finished with this exercise,
be sure to use the instance's dropdown menu in the web interface to
"Shelve" the instance so that it is no longer spending your computing hours.
If you later return to the web interface and want to use the instance again,
Use the dropdown menu's "Unshelve Instance" option to start the instance up again.
Note that any programs that were running when you shelve the instance will be lost,
but the contents of the disk are preserved when shelving.

You may also want to try the "Resize" action to change the number of CPUs of the instance.
Decreasing the number of CPUs (say, to flavor "c8.m64") may slow down your computations, but it will also reduce the cost per hour to run the instance.
Nonetheless, it's important to shelve the instance as soon as you are done. 


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
and then pasted into your shell by right-clicking.


Download and Access Data for WPS and WRF
========================================

Install and Enable CephFS
-------------------------

For this exericse, you need to access the LULC use case data. In total, the LULC use case data are close to 90 GB in size. Usually, such massive data cannot be shared easily. However, Red Cloud now has a Ceph cluster, a distributed file system that stores the data locally at Cornell CAC. Any Linux machine on the Cornell network can access this data once CephFS is installed.
 
First, update your instance::

    sudo apt update

Then, install the CephFS client::

    sudo apt install ceph-common

The CephFS mounting steps are slightly more complicated. When a CephFS share is created, access rules must be set for writing or reading the data. This credential is called a keyring, which consists of an entity name (accessTo) and a key (accessKey). For this exercise, below is the credential for read-only access to the LULC data::

    accessTo="globus-public"
    accessKey="AQCewqNnk5WcOBAAngE0Ktm1SfPV1711Q82uVw==" 

The following commands set up the keyring::

    mkdir -p /etc/ceph
    echo -e "[client.${accessTo}]\n    key = ${accessKey}" | sudo tee /etc/ceph/ceph.client.${accessTo}.keyring

The keyring file must be only readable to root::

    sudo chown root:root /etc/ceph/ceph.client.${accessTo}.keyring
    sudo chmod 600 /etc/ceph/ceph.client.${accessTo}.keyring

Choose the mount location, which will be in the home directory::

    cephfsPath="128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/a33ce441-0ebd-4fab-b850-c0124bc46b70/89b3c9d9-b31c-4d64-9251-38b86a874c7d"
    mountPoint="/home/ubuntu/lulc_input"

Mount to the location::

    echo "${cephfsPath} ${mountPoint} ceph name=${accessTo},x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw 0 2" | sudo tee -a /etc/fstab
    sudo systemctl daemon-reload
    mkdir -p ${mountPoint}
    sudo mount ${mountPoint}

To test if mount is successful, run the following command::

    df -h ${mountPoint}

If CephFS is mounted correctly, the following output is shown::

    Filesystem                                                                                                                                                                             Size  Used Avail Use% Mounted on
    128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/a33ce441-0ebd-4fab-b850-c0124bc46b70/89b3c9d9-b31c-4d64-9251-38b86a874c7d  100G   85G   16G  85% /home/ubuntu/lulc_input


Set Input and Ouput Paths
-------------------------

Copy and paste the following lines to set up paths of the input and output files::

    mkdir ~/lulc_output
    WRF_OUTPUT=~/lulc_output
    WRF_INPUT=~/lulc_input


(Optional) Exercise Script
--------------------------

If you would like to want to run the entire exercise with one script::

    TODO: Change this from issue 68 to main
    wget https://raw.githubusercontent.com/NCAR/i-wrf/refs/heads/feature_68_LULC_Instruction/use_cases/Land_Use_Land_Cover/WRF/run.sh
    chmod +x run.sh
    mkdir ~/lulc_script
    WRF_SCRIPT=~/lulc_script
    mv run.sh $WRF_SCRIPT


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


Get the LULC Docker Image
-------------------------

Once Docker is running, you must pull the correct versions of the WRF image onto your instance::

    sudo docker pull ncar/iwrf:lulc-2024-10-04
    

Using screen in Linux
=====================
As the simulation will take a long time to run, any disconnects from the instance will interrupt the simulation. It's recommended to use the Linux command "screen" in this scenario to create a screen session. The advantage of screen is that even if you disconnect from a screen session, the task will be still running, you can reconnect to the screen session at any time to check the progress. Disconnecting and reconnecting are referred to as "detaching" and "attaching." 

To start a screen session with "lulc" as the session name, enter the following::

    screen -S lulc

At any time, enter the following to show the currently running sessions and attached sessions, if any::

    screen -ls

Inside a session, if you want to detach from it, you would need to press a combination of keys::
    
    Ctrl+A,  D

To attach to the screen session "lulc", enter the following:: 

    screen -r lulc


Start WPS and WRF with script
=============================

With everything in place, you are now ready to run the Docker container that will perform the simulation. First, make sure you are in a screen session. If you would like to run the entire script in one command, you just have to run the script. The downloaded script runs inside the container, prints lots of status information, and creates output files in the output folder you created. Execute this command to start a container with the image we pulled earlier::

    sudo docker run --shm-size 100G -it \
    -v $WRF_INPUT:/home/wrfuser/lulc_input \
    -v $WRF_OUTPUT:/home/wrfuser/lulc_output \
    -v $WRF_SCRIPT:/home/wrfuser/lulc_script \
    ncar/iwrf:lulc-2024-10-04 sudo /home/wrfuser/lulc_script/run.sh

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 100 -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:lulc-2024-10-04`` is the Docker image to use when creating the container.

The simulation will take a long time to run, and when the results are ready, the terminal will become available again. The output files will be in the "lulc_output" folder. See the "View Output" section below for instructions on how to view the output.


Run WPS and WRF Manually
========================

With everything in place, you are now ready to run the Docker container that will perform the simulation. The command below is similar to the one above, but it does not run the script. Instead, it starts the container and provides a shell prompt. From there, we will run each command one by one::

    sudo docker run --shm-size 100G -it \
    -v $WRF_INPUT:/home/wrfuser/lulc_input \
    -v $WRF_OUTPUT:/home/wrfuser/lulc_output \
    ncar/iwrf:lulc-2024-10-04 bash

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 100 -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:lulc-2024-10-04`` is the Docker image to use when creating the container.


Run WPS
=======

We now need to set up the environment in the container to ensure proper files and executables are in the path and resolve any memory issues. First, load the environment in "/etc/bashrc" with "source" and then allow unlimited memory to be used in this container:: 

    source /etc/bashrc
    ulimit -s unlimited

And define some environment variables for input and output paths::

    WPS=/home/wrfuser/WPS
    WRF=/home/wrfuser/WRF
    LULC_OUTPUT=/home/wrfuser/lulc_output
    LULC_WPS_INPUT=/home/wrfuser/lulc_input/WPS_input
    LULC_WRF_INPUT=/home/wrfuser/lulc_input/WRF_input

The first step of the LULC use case is to run the WRF Pre-Processing System (WPS). Start with running "geogrid.exe" with "WPS_GEOG" data. The file "namelist.wps" directs "geogrid.exe" to read domain configuration parameters from the WPS_GEOG data directory::
    
    cd $WPS
    cp $LULC_WPS_INPUT/namelist/namelist_PRS.wps $WPS/namelist.wps
    ln -fs $LULC_WPS_INPUT/WPS_GEOG $WPS
    ./geogrid.exe


Next, link the Vtable and link the HRRR files with the extension "wrfprs". Call "ungrib.exe" to generate files with HRRR_PRS headers::

    cd $WPS
    cp $LULC_WPS_INPUT/namelist/Vtable.hrrr.modified $WPS/ungrib/Variable_Tables/
    ln -sf $WPS/ungrib/Variable_Tables/Vtable.hrrr.modified $WPS/Vtable
    ./link_grib.csh $LULC_WPS_INPUT/HRRR_0703/hrrr.*.wrfprs
    ./ungrib.exe

Do the same with HRRR files with the extension "wrfnat" and generate files with HRRR_PRS headers. Note that we need a new "namelist.wps"::

    cd $WPS
    cp $LULC_WPS_INPUT/namelist/namelist_NAT.wps $WPS/namelist.wps
    ./link_grib.csh $LULC_WPS_INPUT/HRRR_0703/hrrr.*.wrfnat
    ./ungrib.exe

Finally, we can finalize the WPS process by calling "metgrid.exe", which will read both HRRR_PRS and HRRR_NAT files::

    cd $WPS
    ./metgrid.exe


Run WRF
=======

Control Simulation
------------------

The control simulation runs WRF with the files generated from WPS. First, copy the namelist and WRF variable files and link the "met_em" files from WPS::

    cd $WRF
    ln -sf $WRF/run/* $WRF
    cp $LULC_WRF_INPUT/namelist/namelist.input $WRF
    cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d01.txt $WRF
    cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d02.txt $WRF
    cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d03.txt $WRF
    ln -sf $WPS/met_em* $WRF

Run "real.exe" to generate boundary conditions for WRF input. The files generated from this step are "wrfbdy_d01", "wrfinput_d01", "wrfinput_d02", and "wrfinput_d03". Paste the following::

    cd $WRF
    ./main/real.exe

Create a folder named "wrfdata" in the WRF directory and run WRF simulation with 60 CPU cores::
    
    cd $WRF
    mkdir $WRF/wrfdata
    mpiexec -n 60 -ppn 60 ./main/wrf.exe

This step will take about 2 days to run. When it is finished, copy the output from "wrfdata" to the output folder::

    mv $WRF/wrfdata $LULC_OUTPUT/ctl


DFW4X Simulation
----------------

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

Create a folder named "wrfdata" in the WRF directory and run WRF simulation with 60 CPU cores::
    
    cd $WRF
    mkdir $WRF/wrfdata
    mpiexec -n 60 -ppn 60 ./main/wrf.exe

When it is finished, copy the output from "wrfdata" to the output folder::

    mv $WRF/wrfdata $LULC_OUTPUT/dfw4x


After the copying is done, you may exit the container by entering "exit".


View Output
===========

To view the outputs in the "lulc_output" folder, you must first give view permissions to the folder::

    sudo chmod -R 777 $WRF_OUTPUT

Use the "ls" command to list the files in the "ctl" or "dfw4x" folders::

    ls $WRF_OUTPUT/ctl
    ls $WRF_OUTPUT/dfw4x
