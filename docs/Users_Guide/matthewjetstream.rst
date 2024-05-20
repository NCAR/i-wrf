Running I-WRF On Jetstream2 with Hurricane Matthew Data
****************************************************************

Overview
=================

The following instructions can be used to run
the `I-WRF weather simulation program <https://i-wrf.org>`_
with data from `Hurricane Matthew <https://en.wikipedia.org/wiki/Hurricane_Matthew>`_
on the `Jetstream2 cloud computing platform <https://jetstream-cloud.org/>`_.
This exercise provides an introduction to using cloud computing platforms,
running computationally complex simulations and using containerized applications.

Simulations like I-WRF often require greater computing resources
than you may have on your personal computer,
but a cloud computing platform can provided the needed computational power.
Jetstream2 is a national cyberinfrastructure resource that is easy to use
and is available to researchers and educators.
This example delivers the I-WRF program as a Docker "image",
simplifying the set-up for running the simulation.

Prepare to Use Jetstream2
===============================

To `get started with Jetstream2<https://jetstream-cloud.org/get-started>`_,
you will need to:

* Create an account with the `National Science Foundation (NSF)<https://www.nsf.gov/>`_'s `ACCESS program<https://access-ci.org/>`_.
* Request a computational "allocation" from ACCESS.
* Log in to Jetstream2's web portal.

The sections below will guide you through this process

Create an ACCESS Account
--------------------------------

If you do not already have one, `register for an ACCESS account<https://operations.access-ci.org/identity/new-user>`_.
Note that you can either choose to use an existing University/Organizational account or
create an entirely new ACCESS account when registering. 

Get an Allocation
-------------------

With your ACCESS account set up, you may `request an allocation<https://allocations.access-ci.org/get-your-first-project>`_
that will allow you to use an ACCESS-affiliated cyberinfrastructure resource.
Be sure to read all of the information on that page so that you make a suitable request.
An "Explore" project will be sufficient to work with this example,
and you will want to work with the resource "Indiana Jetstream2 CPU" (*not* GPU).
The typical turnaround time for allocation requests is one business day.

Log in to the Exosphere Web Site
------------------------------------

Once you have an ACCESS account and allocation,
you can log in to their `Exosphere web dashboard<https://jetstream2.exosphere.app/)>`_.
The process of identifying your allocation and ACCESS ID to use Jetstream2
is described on `this page<https://cvw.cac.cornell.edu/jetstream/intro/jetstream-login>`_ of the
`Introduction to Jetstream2<https://cvw.cac.cornell.edu/jetstream>`_ Cornell Virtual Workshop,
and on `this page<https://docs.jetstream-cloud.org/ui/exo/login/)>`_
of the `Jetstream2 documentation<https://docs.jetstream-cloud.org/)>`_.

While adding an allocation to your account, it is recommended that you choose
the "Indiana University" region of Jetstream2 for completing this example.

Create a Cloud Instance and Log In
====================================

After you have logged in to Jetstream2 and added your allocation to your account,
you are ready to create the cloud instance where you will run the I-WRF simulation.
If you are not familiar with the cloud computing terms "image" and "instance",
it is recommended that you `read about them<https://cvw.cac.cornell.edu/jetstream/intro/imagesandinstances)>`_
before proceeding.

Create an SSH Key
-------------------

If you are not familiar with "SSH key pairs", you should
`read about them<https://cvw.cac.cornell.edu/jetstream/keys/about-keys)>`_ before continuing.
A key pair is needed when creating your instance so that you can log in to it,
as password-based log-ins are disabled on Jetstream2.

* First, `create an SSH Key on your computer<https://cvw.cac.cornell.edu/jetstream/keys/ssh-create>`_ using the "ssh-keygen" command.
* Then `upload the key to Jetstream2<https://cvw.cac.cornell.edu/jetstream/keys/ssh-upload)>`_ through the Exosphere web interface. 

Create an Instance
---------------------

The Cornell Virtual Workshop topic `Creating an Instance<https://cvw.cac.cornell.edu/jetstream/create-instance>`_
provides detailed information about creating a Jetstream2 instance.
While following those steps, be sure to make the following choices for this instance:

* Choose the Featured-Ubuntu22 image as the instance source.
* Choose the "Flavor" m3.quad (4 CPUs) to provide faster a simulation run-time.
* Select a custom disk size of 100 GB to hold this example's data and results.
* Select "Yes" for Enable web desktop.
* Select the SSH public key that you uploaded previously.
* You do not need to set any of the Advanced Options.

After clicking the "Create" button, wait for the instance to enter the "Ready" state (it takes several minutes).
Note that the instance will not only be created, but will be running so that you can log in right away.

Log in to the Instance
-----------------------------

The Exosphere web dashboard provides two easy ways to log in to Jetstream2 instances
Web Shell and Web Desktop.
For this example, you can use the `Web Shell<https://cvw.cac.cornell.edu/jetstream/instance-login/webshell>`_ option
to open a terminal tab in your web browser.
You may also want to read about the `features of Guacamole<https://cvw.cac.cornell.edu/jetstream/instance-login/guacamole>`_,
which is the platform that supports both Web Shell and Web Desktop.

Once you are logged in to the web shell you can proceed to the
"Install Software and Download Data" section below.

Managing a Jetstream2 Instance
------------------------------------

An appropriate aspect of efficient cloud computing is knowing how to
`manage your instances<https://cvw.cac.cornell.edu/jetstream/manage-instance/states-actions>`_.
Instances incur costs whenever they are running (on Jetstream, this is when they are "Ready").
"Shelving" an instance stops it from using the cloud's CPUs and memory,
and therefore stops it from incurring any charges on your allocation.

When you are through working on this example,
be sure to use the instance's "Actions" menu in the web dashboard to
"Shelve" the instance so that it is no longer spending your credits.
If you alter return to the dashboard and want to use the instance again,
Use the Action menu's "Unshelve" option to start the instance up again.
Note that any programs that were running when you shelve the instance will be lost,
but the contents of the disk are preserved when shelving.

You may also want to try the "Resize" action to change the number of CPUs of the instance.
Increasing the number of CPUs (say to flavor "m3.8") can make your computations finish more quickly.
But of course, doubling the number of CPUs doubles the cost per hour to run the instance,
so Shelving as soon as you are done becomes even more important.

Install Software and Download Data
=====================================

With your instance created and running and you logged in to it through a Web Shell,
you can now install the necessary software and download the data to run the simulation.
You will only need to perform these steps once,
as they essentially change the contents of the instance's disk
and those changes will remain even after the instance is shelved and unshelved.

Install Docker and Get the I-WRF Image
-----------------------------------------

As mentioned above, the I-WRF simulation application is available as an image that will run as a
`Docker "container"<https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/>`_
on your instance.
To do so, you must first install the Docker Engine on the instance
and then download, or "pull" the I-WRF image that will be run as a container in Docker.

The `instructions for installing Docker Engine on Ubuntu<https://docs.docker.com/engine/install/ubuntu/>`_
are very thorough and make a good reference, but we only need to perform a subset of those steps.
The following commands can be copied and pasted into your shell.
This first, complicated sequence sets up the Docker repository on your instance::

    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
      -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
      https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

Now you can simply install the Docker Engine::

    sudo apt-get install docker-ce docker-ce-cli

And finally, you pull the latest version of the I-WRF image onto your instance::

    docker pull ncar/iwrf

Get the Geographic Data
----------------------------

To run I-WRF on the Hurricane Matthew data set, you need a copy of the
geographic data representing the terrain in the area of the simulation.
These commands download an archive file containing that data,
uncompress the archive into a folder named "WPS_GEOG", and delete the archive file.::

    wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
    tar -xzf geog_high_res_mandatory.tar.gz
    rm geog_high_res_mandatory.tar.tz

Create the Run Folder
-------------------------

The simulation is started by a script that must first be downloaded.
The script expects to run in a folder where it can download data files and generate results.
In this example, we expect this folder to be named "matthew" and to be in the user's home directory.
The script is called "run.sh".
The following commands create the empty folder and download the script into it,
and they can be copied and pasted into your web shell.::

    mkdir matthew
    https://gist.githubusercontent.com/Trumbore/27cef8073048cde7a8142af9bfb0b264/raw/1115ce9de4a30ad665055ed323c40a4e7aa411b2/run.sh > matthew/run.sh

Run I-WRF
===========

With everything in place, you are now ready to run the Docker container that will perform the simulation.
The downloaded script runs inside the container, prints lots of status information,
and creates output files in the run folder you created.
Copy and paste this command into your web shell::

    time docker run --shm-size 14G -it -v ~/:/home/wrfuser/terrestrial_data \
      -v ~/matthew:/tmp/hurricane_matthew ncar/iwrf:latest /tmp/hurricane_matthew/run.sh

The command has numerous arguments and options, which do the following:

* ``time docker run`` prints the runtime of the "docker run" command.
* ``--shm-size 14G -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in the instance to paths within the contianer.
* ``ncar/iwrf:latest`` is the Docker image to use when creating the container.
* ``/tmp/hurricane_matthew/run.sh`` is the location within the container of the script that it runs.

It takes about 12 minutes for the simulation to finish on an m3.quad Jetstream instance.

