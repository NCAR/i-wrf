Running I-WRF On Jetstream2 with Hurricane Matthew Data
*******************************************************

Overview
========

The following instructions can be used to run
the `I-WRF weather simulation program <https://i-wrf.org>`_
from the `National Center for Atmospheric Research (NCAR) <https://ncar.ucar.edu/>`_
with data from `Hurricane Matthew <https://en.wikipedia.org/wiki/Hurricane_Matthew>`_
on the `Jetstream2 cloud computing platform <https://jetstream-cloud.org/>`_.
This exercise provides an introduction to using cloud computing platforms,
running computationally complex simulations and using containerized applications.

Simulations like I-WRF often require greater computing resources
than you may have on your personal computer,
but a cloud computing platform can provided the needed computational power.
Jetstream2 is a national cyberinfrastructure resource that is easy to use
and is available to researchers and educators.
This exercise runs the I-WRF program as a Docker "container",
which simplifyies the set-up work needed to run the simulation.

It is recommended that you follow the instructions in each section in the order presented
to avoid encountering issues during the process.
Most sections refer to external documentation to provide details about the necessary steps
and to offer additional background information.

Prepare to Use Jetstream2
=========================

To `get started with Jetstream2 <https://jetstream-cloud.org/get-started>`_,
you will need to:

* Create an account with the `National Science Foundation (NSF) <https://www.nsf.gov/>`_'s `ACCESS program <https://access-ci.org/>`_.
* Request a computational "allocation" from ACCESS.
* Log in to Jetstream2's web portal.

The sections below will guide you through this process.

Create an ACCESS Account
------------------------

If you do not already have one, `register for an ACCESS account <https://operations.access-ci.org/identity/new-user>`_.
Note that you can either choose to associate your existing University/Organizational account or
create an entirely new ACCESS account when registering. 

Get an Allocation
-----------------

With your ACCESS account set up, you may `request an allocation <https://allocations.access-ci.org/get-your-first-project>`_
that will allow you to use an ACCESS-affiliated cyberinfrastructure resource.
Be sure to read all of the information on that page so that you make a suitable request.
An "Explore" project will be sufficient to work with this exercise,
and you will want to work with the resource "Indiana Jetstream2 CPU" (*not* GPU).
The typical turnaround time for allocation requests is one business day.

Log in to the Exosphere Web Site
--------------------------------

Once you have an ACCESS account and allocation,
you can log in to their `Exosphere web dashboard <https://jetstream2.exosphere.app>`_.
The process of identifying your allocation and ACCESS ID to use Jetstream2
is described on `this page <https://cvw.cac.cornell.edu/jetstream/intro/jetstream-login>`_ of the
`Introduction to Jetstream2 <https://cvw.cac.cornell.edu/jetstream>`_ Cornell Virtual Workshop,
and on `this page <https://docs.jetstream-cloud.org/ui/exo/login>`_
of the `Jetstream2 documentation <https://docs.jetstream-cloud.org>`_.

While adding an allocation to your account, it is recommended that you choose
the "Indiana University" region of Jetstream2 for completing this exercise.

Create a Cloud Instance and Log In
==================================

After you have logged in to Jetstream2 and added your allocation to your account,
you are ready to create the cloud instance where you will run the I-WRF simulation.
If you are not familiar with the cloud computing terms "image" and "instance",
it is recommended that you `read about them <https://cvw.cac.cornell.edu/jetstream/intro/imagesandinstances>`_
before proceeding.

Create an SSH Key
-----------------

You must upload a public SSH key to Jetstream2 before creating your instance.
Jetstream2 injects that public key into the instance's default user account,
and you will need to provide the matching private SSH key to log in to the instance.
If you are not familiar with "SSH key pairs", you should
`read about them <https://cvw.cac.cornell.edu/jetstream/keys/about-keys>`_ before continuing.

* First, `create an SSH Key on your computer <https://cvw.cac.cornell.edu/jetstream/keys/ssh-create>`_ using the "ssh-keygen" command.  That command allows you to specify the name and location of the private key file it creates, with the default being "id_rsa".  The matching public key file is saved to the same location and name with ".pub" appended to the filename.  Later instructions will assume that your private key file is named "id_rsa", but you may choose a different name now and use that name in those later instructions.
* Then, `upload the public key to Jetstream2 <https://cvw.cac.cornell.edu/jetstream/keys/ssh-upload>`_ through the Exosphere web interface.

Create an Instance
------------------

The Cornell Virtual Workshop topic `Creating an Instance <https://cvw.cac.cornell.edu/jetstream/create-instance>`_
provides detailed information about creating a Jetstream2 instance.
While following those steps, be sure to make the following choices for this instance:

* When choosing an image as the instance source, if viewing "By Type", select the "Ubuntu 22.04 (latest)" image.  If viewing "By Image", choose the "Featured-Ubuntu22" image.
* Choose the "Flavor" m3.quad (4 CPUs) to provide a faster simulation run-time.
* Select a custom disk size of 100 GB - larege enough to hold this exercise's data and results.
* Select the SSH public key that you uploaded previously.
* You do not need to set any of the Advanced Options.

After clicking the "Create" button, wait for the instance to enter the "Ready" state (it takes several minutes).
Note that the instance will not only be created, but will be running so that you can log in right away.

Log in to the Instance
----------------------

The Exosphere web dashboard provides the easy-to-use Web Shell for accessing your Jetstream2 instances,
but after encountering some issues with this exercise when using Web Shell,
we are recommending that you use the SSH command to access your instance from a shell on your computer.
The instructions for `connecting to Jetstream2 using SSH <https://cvw.cac.cornell.edu/jetstream/instance-login/sshshell>`_
can executed in the Command Prompt on Windows (from the Start menu, type "cmd" and select Command Prompt)
or from the Terminal application on a Mac.

In either case you will need to know the location and name of the private SSH key created on your computer (see above),
the IP address of your instance (found in the Exosphere web dashboard)
and the default username on your instance, which is "exouser".

Once you are logged in to the web shell you can proceed to the
"Install Software and Download Data" section below.
You will know that your login has been successful when the prompt has the form ``exouser@instance-name:~$``,
which indicates your username, the instance name, and your current working directory, followed by "$"

Managing a Jetstream2 Instance
------------------------------

In order to use cloud computing resources efficiently, you must know how to
`manage your instances <https://cvw.cac.cornell.edu/jetstream/manage-instance/states-actions>`_.
Instances incur costs whenever they are running (on Jetstream2, this is when they are "Ready").
"Shelving" an instance stops it from using the cloud's CPUs and memory,
and therefore stops it from incurring any charges against your allocation.

When you are through working on this exercise,
be sure to use the instance's "Actions" menu in the web dashboard to
"Shelve" the instance so that it is no longer spending your credits.
If you later return to the dashboard and want to use the instance again,
Use the Action menu's "Unshelve" option to start the instance up again.
Note that any programs that were running when you shelve the instance will be lost,
but the contents of the disk are preserved when shelving.

You may also want to try the "Resize" action to change the number of CPUs of the instance.
Increasing the number of CPUs (say, to flavor "m3.8") can make your computations finish more quickly.
But of course, doubling the number of CPUs doubles the cost per hour to run the instance,
so Shelving as soon as you are done becomes even more important!

Install Software and Download Data
==================================

With your instance created and running and you logged in to it through a Web Shell,
you can now install the necessary software and download the data to run the simulation.
You will only need to perform these steps once,
as they essentially change the contents of the instance's disk
and those changes will remain even after the instance is shelved and unshelved.

The following sections instruct you to issue numerous Linux commands in your web shell.
If you are not familiar with Linux, you may want to want to refer to
`An Introduction to Linux <https://cvw.cac.cornell.edu/Linux>`_ when working through these steps.
The commands in each section can be copied using the button in the upper right corner
and then pasted into your web shell by right-clicking.

If your web shell ever becomes unresponsive or disconnected from the instance,
you can recover from that situation by rebooting the instance.
In the Exosphere dashboard page for your instance, in the Actions menu, select "Reboot".
The process takes several minutes, after which the instance status will return to "Ready".

Install Docker and Get the I-WRF Image
--------------------------------------

As mentioned above, the I-WRF simulation application is provided as a Docker image that will run as a
`"container" <https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/>`_
on your cloud instance.
To run a Docker container, you must first install the Docker Engine on your instance.
You can then "pull" (download) the I-WRF image that will be run as a container.

The `instructions for installing Docker Engine on Ubuntu <https://docs.docker.com/engine/install/ubuntu/>`_
are very thorough and make a good reference, but we only need to perform a subset of those steps.
These commands run a script that sets up the Docker software repository on your instance,
then installs Docker::

    curl --location https://bit.ly/3R3lqMU > install-docker.sh
    source install-docker.sh

If a text dialog is displayed asking which services should be restarted, type ``Enter``.
When the installation is complete, you can verify that the Docker command line tool works by asking for its version::

    docker --version

Next, you must start the Docker daemon, which runs in the background and processes commands::

    sudo service docker start

If that command appeared to succeed, you can confirm its status with this command::

    sudo systemctl --no-pager status docker

Once all of that is in order, you must pull the latest version of the I-WRF image onto your instance::

    docker pull ncar/iwrf

Get the Geographic Data
-----------------------

To run I-WRF on the Hurricane Matthew data set, you need a copy of the
geographic data representing the terrain in the area of the simulation.
These commands download an archive file containing that data,
uncompress the archive into a folder named "WPS_GEOG", and delete the archive file.
They take several minutes to complete::

    wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
    tar -xzf geog_high_res_mandatory.tar.gz
    rm geog_high_res_mandatory.tar.gz

Create the Run Folder
---------------------

The simulation is performed using a script that must first be downloaded.
The script expects to run in a folder where it can download data files and create result files.
The instructions in this exercise create that folder in the user's home directory and name it "matthew".
The simulation script is called "run.sh".
The following commands create the empty folder and download the script into it,
then change its permissions so it can be run::

    mkdir matthew
    curl --location https://bit.ly/3KoBtRK > matthew/run.sh
    chmod 775 matthew/run.sh

Run I-WRF
=========

With everything in place, you are now ready to run the Docker container that will perform the simulation.
The downloaded script runs inside the container, prints lots of status information,
and creates output files in the run folder you created.
Execute this command to run the simulation in your web shell::

    time docker run --shm-size 14G -it -v ~/:/home/wrfuser/terrestrial_data -v ~/matthew:/tmp/hurricane_matthew ncar/iwrf:latest /tmp/hurricane_matthew/run.sh

The command has numerous arguments and options, which do the following:

* ``time docker run`` prints the runtime of the "docker run" command.
* ``--shm-size 14G -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the contianer.
* ``ncar/iwrf:latest`` is the Docker image to use when creating the container.
* ``/tmp/hurricane_matthew/run.sh`` is the location within the container of the script that it runs.

The simulation initially prints lots of information while initializing things, then settles in to the computation.
The provided configuration simulates 12 hours of weather and takes under three minutes to finish on an m3.quad Jetstream2 instance.
Once completed, you can view the end of any of the output files to confirm that it succeeded::

    tail matthew/rsl.out.0000

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

