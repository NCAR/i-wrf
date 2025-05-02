:orphan:

.. _lulcredcloud:

Running I-WRF On Red Cloud with Land Use/Land Cover (LULC) Data
***************************************************************


Overview
========

The following instructions can be used to run elements of
the `I-WRF weather simulation framework <https://i-wrf.org>`_
from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_
and the `Cornell Center for Advanced Computing <https://cac.cornell.edu/>`_.
The steps below run the `Weather Research & Forecasting (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ and `WRF Pre-Processing System (WPS) <https://github.com/wrf-model/WPS>`_
models with data from `The High-Resolution Rapid Refresh (HRRR) <https://rapidrefresh.noaa.gov/hrrr/>`_ 
and modified meteorological data on the `Red Cloud cloud computing platform <https://www.cac.cornell.edu/services/cloudservices.aspx/>`_ 
provided by Cornell Center for Advanced Computing (CAC).
This science use case focuses on a deep convection system that passed over the Dallas-Fort Worth (DFW) metropolitan region on July 4th, 2017, and the simulations follow Zhou et al. 2024. This exercise provides an introduction to using cloud computing platforms, running computationally complex simulations and analyses, and using containerized applications.

Simulations like WRF often require greater computing resources
than you may have on your personal computer,
but a cloud computing platform can provide the needed computational power.
Red Cloud is a subscription-based Infrastructure as a Service cloud that provides 
root access to virtual servers and on-demand storage to Cornell researchers.
This exercise runs the I-WRF programs as Docker "containers",
which simplifies the setup work needed to run the simulation.

It is recommended that you follow the instructions in each section in the order presented
to avoid encountering issues during the process.
Most sections refer to external documentation to provide details about the necessary steps
and to offer additional background information.

Reference
---------
Zhou, X., Letson, F., Crippa, P. and Pryor, S.C., 2024. Urban effect on precipitation and deep convective systems over Dallas-Fort Worth. Journal of Geophysical Research: Atmospheres, 129(10), p.e2023JD039972. 

Prepare to Use Red Cloud
========================

To `get started with Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud2/#getting-started-on-red-cloud-v2>`_,
you will need to:

* Go to the `CAC portal <https://portal.cac.cornell.edu/>`_ and log in. The instructions to log in are on the `CAC TechDocs page: Portal Login <https://portal.cac.cornell.edu/techdocs/general/CACportal/#portal-login>`_.

* Get access to Red Cloud by doing one of the following options on the CAC portal:

  * Start a new project by making a project request. The instructions are on the `CAC TechDocs page: As a Cornell Faculty or Staff, How Do I Start a New Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#as-a-cornell-faculty-or-staff-how-do-i-start-a-new-project>`__ (Only available for Cornell Faculty and Staff)

  * Join an existing project. The instructions are on the `CAC TechDocs page: How Do I Join an Existing Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-join-an-existing-project>`__
  
  * Request an exploratory account. The instructions are on the `CAC TechDocs page: How Do I Request an Exploratory Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-request-an-exploratory-project>`__ Note that an exploratory project does not have enough compute hours to complete this set of instructions.

* For new projects and the existing projects, make sure that the project has Red Cloud subscriptions. 

* Log in to Red Cloud's `Red Cloud Horizon web interface <https://redcloud2.cac.cornell.edu/>`_.

The section below will guide you through this process. 
For an overview of Red Cloud, read Cornell `CAC TechDocs Red Cloud documentation <https://portal.cac.cornell.edu/techdocs/redcloud2/#red-cloud-v2>`_.


Start a Project
---------------

One way to get a CAC account is to request a project. 
Note that you must be a Cornell faculty member or staff to view the pages below and start a project. 
You may submit a project request at the CAC portal.
Thoroughly review the `rates <https://portal.cac.cornell.edu/rates>`_ (login required) page to understand the Red Cloud subscription service.
Once your project is approved, you can manage your project on the CAC portal. Read the `Portal Overview <https://portal.cac.cornell.edu/techdocs/general/CACportal/#portal-overview>`_ to learn how to manage a project. Detailed instructions to start a project are available at the `CAC TechDocs page: As a Cornell Faculty or Staff, How Do I Start a New Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#as-a-cornell-faculty-or-staff-how-do-i-start-a-new-project>`__


Join a Project
--------------

To join an existing project, submit a request to join on the CAC portal. You should only do this if your PI has requested you to submit the request. Once the project PI approves the request, an email is sent to you with the login information. For the full instructions, read the `CAC TechDocs page: How Do I Join an Existing Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-join-an-existing-project>`__



Create a Cloud Instance and Log In
==================================

After you have logged in to the Red Cloud Horizon web interface,
you are ready to create the cloud instance where you will run the I-WRF simulation.
If you are not familiar with the cloud computing terms "image" and "instance",
it is recommended that you read about them here before proceeding: `Red Cloud: Images <https://portal.cac.cornell.edu/techdocs/redcloud2/compute/#images>`__ 
and `Red Cloud: Run Linux Instance <https://portal.cac.cornell.edu/techdocs/redcloud2/run_linux_instances/>`__


Create an SSH Key
-----------------

You can either upload a public SSH key to Red Cloud or generate an SSH key pair on Red Cloud before creating your instance.
Red Cloud injects the uploaded public key or generated public key into the instance's default user account,
and you will need to provide the matching private SSH key to log in to the instance.
If you are not familiar with "SSH key pairs", you should
`read about them <https://portal.cac.cornell.edu/techdocs/redcloud2/compute/#keypairs>`__ before continuing.

* `Create an SSH Key on your computer <https://portal.cac.cornell.edu/techdocs/openstack/keypairs/#creating-a-passphrase-protected-key-pair-recommended>`_ using the "ssh-keygen" command.  That command allows you to specify the name of the private key file it creates, with the default being "id_rsa".  The matching public key file is saved and named with ".pub" appended to the filename. 
* `Import the public key to Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud2/horizon_ssh_keys/#import-a-public-key>`_ through the Red Cloud web interface.

Alternatively, you can `create a key pair on Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud2/horizon_ssh_keys/#create-a-new-ssh-key-pair>`_. Be sure to follow the steps and save the private key it generated with the correct format and permission before proceeding. 


Create a Security Group
-----------------------

Security groups are firewalls that control inbound and outbound network traffic to your instances. For an instance to be accessible, its security group must have port 22 (SSH) enabled. You can read more about them at `Red Cloud: Security Groups <https://portal.cac.cornell.edu/techdocs/redcloud2/network/#security>`__. 

If you will access the instance from a Cornell Network (eduroam Wi-Fi, Ethernet, Cornell VPN, etc.), it's sufficient to use the security group that already exists on your project: "campus-only-ssh". This security group is already configured to enable SSH traffic from anywhere in the Cornell Network.

If you cannot use any of the options above, you will need to create a security group and add an SSH rule for an IP address you frequently use. Follow the steps below to create a security group:

* `Create a security group <https://portal.cac.cornell.edu/techdocs/redcloud2/horizon_security_groups/#create-a-security-group>`__

* `Add an SSH rule to the security group to allow SSH <https://portal.cac.cornell.edu/techdocs/redcloud2/horizon_security_groups/#manage-your-security-group>`__

 * In the Rule dropdown, select "SSH"
 * In the CIDR field, put your IP address followed by "/32", e.g., "128.84.0.0/32"

Note that once you put your IP address in the CIDR field, you may connect to the instance from that IP address. If your IP address changes for any reason, you will need to remove and update the rule.


Create an Instance
------------------

The Cornell TechDocs `Creating a New Linux Instance <https://portal.cac.cornell.edu/techdocs/redcloud2/run_linux_instances/#creating-a-new-linux-instance>`_
provides detailed instructions about creating a Linux instance on Red Cloud.
While following those steps, be sure to make the following choices for this instance:

* When choosing an image as the instance source:
  
  * Select Boot from Source is "Image"
  * Volume Size (GB) is 1500
  * Delete Volume on Instance Delete is "Yes"
  * Select the "ubuntu-24.04-LTS" image

* In Flavor, choose the "Flavor" c64.m120 (64 Virtual CPUs) to provide a faster simulation run-time. Note that this will consume Red Cloud subscriptions very fast.
* In Network, select "public".
* In Security Groups, select "campus_only_ssh" or the security group you created.
* In Key Pair, select the SSH public key that you created or uploaded previously.

When all the required options are selected, click on the "Launch Instance" button, and wait for the instance to enter the "Active" state. Note that the instance will not only be created, but also running so that you can log in after a couple of minutes.


Log in to the Instance
----------------------

The instructions for `connecting to Red Cloud Linux instances using SSH <https://portal.cac.cornell.edu/techdocs/redcloud2/run_linux_instances/#accessing-instances>`_
can be executed in the Command Prompt or PowerShell on Windows (from the Start menu, type "cmd" and select Command Prompt or search for PowerShell) or from the Terminal application on a Mac.

In either case, you will need to know the location and name of the private SSH key created on your computer or downloaded from Red Cloud (see above),
the IP address of your instance (found in the Red Cloud OpenStack interface)
and the default username on your instance, which is "ubuntu".

You will know that your login has been successful when the prompt has the form ``ubuntu@instance-name:~$``,
which indicates your username, the instance name, and your current working directory, followed by "$"


Managing a Red Cloud Instance
-----------------------------

In order to use cloud computing resources efficiently, you must know how to
`manage your instances <https://portal.cac.cornell.edu/techdocs/redcloud2/compute/#instance-states>`_.
Instances incur costs whenever they are running (on Red Cloud, this is when they are "Active").
"Shelving" an instance stops it from using the cloud's CPUs and memory,
and therefore stops it from incurring any charges against your project.

When you are finished with this exercise,
be sure to use the instance's dropdown menu in the web interface to
"Shelve" the instance so that it is no longer consuming your computing hours.
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
If you are not familiar with Linux, you may want to refer to
`An Introduction to Linux <https://cvw.cac.cornell.edu/Linux>`_ when working through these steps.
The commands in each section can be copied using the button in the upper right corner
and then pasted into your shell by right-clicking.


Access Data for WPS and WRF
===========================

Install and Enable CephFS
-------------------------

You need to access the data used in this exercise. In total, the data are close to 90 GB in size. Usually, such large datasets cannot be shared easily. However, Red Cloud now has a Ceph cluster, a distributed file system that stores the data locally at Cornell CAC. Any Linux machine on the Cornell network can access this data using the following steps. 

First, update the package list::

    sudo apt update

Install CephFS client::

    sudo apt install ceph-common

The CephFS mounting steps are slightly more complicated. When a CephFS share is created, access rules must be set for writing or reading the data. This credential is called a keyring, which consists of an entity name (accessTo) and a key (accessKey). For this exercise, copy and paste the credentials for read-only access::

    accessTo="globus-public"
    accessKey="AQCewqNnk5WcOBAAngE0Ktm1SfPV1711Q82uVw==" 

The following commands set up the keyring::

    mkdir -p /etc/ceph
    echo -e "[client.${accessTo}]\n    key = ${accessKey}" | sudo tee /etc/ceph/ceph.client.${accessTo}.keyring

The keyring file must be only readable to root::

    sudo chown root:root /etc/ceph/ceph.client.${accessTo}.keyring
    sudo chmod 600 /etc/ceph/ceph.client.${accessTo}.keyring

Choose the mount point for the CephFS share, which will be in the home directory::

    cephfsPath="128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/a33ce441-0ebd-4fab-b850-c0124bc46b70/89b3c9d9-b31c-4d64-9251-38b86a874c7d"
    mountPoint="/home/ubuntu/lulc_input"

Mount to the location::

    echo "${cephfsPath} ${mountPoint} ceph name=${accessTo},x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw 0 2" | sudo tee -a /etc/fstab
    sudo systemctl daemon-reload
    mkdir -p ${mountPoint}
    sudo mount ${mountPoint}

Run the following command to test if mount is successful::

    df -h ${mountPoint}

If the CephFS share is mounted correctly, the following output is shown:

..

    Filesystem                                                                                                                                                                             Size  Used Avail Use% Mounted on
    128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/a33ce441-0ebd-4fab-b850-c0124bc46b70/89b3c9d9-b31c-4d64-9251-38b86a874c7d  100G   85G   16G  85% /home/ubuntu/lulc_input


Install Docker and Pull Docker Objects
======================================

Install Docker
--------------

As mentioned above, the WRF and WPS software are provided in a Docker image that will run as a
`"container" <https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/>`_
on your cloud instance.
To run a Docker container, you must first install the Docker Engine on your instance.
You can then "pull" (download) the image that will be run as a container.

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


Get the Docker Image
--------------------

Once Docker is running, you must pull the correct versions of the image that will be used in this exercise onto your instance::

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
==========================

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

You are now ready to run the Docker container that will perform the simulation. First, make sure you are in a screen session. If you would like to run the entire process in one command, you just have to run the script. If you had used a different flavor than c64.m120 on this instance, adjust the CPU core count to a suitable number in the script (e.g. ``mpiexec -n 60 -ppn 60 ./main/wrf.exe`` to ``mpiexec -n 28 -ppn 28 ./main/wrf.exe`` for the c28.m224 flavor).

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
