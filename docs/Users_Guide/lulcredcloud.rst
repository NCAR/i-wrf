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

To `get started with Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud/#getting-started-on-red-cloud>`_,
you will need to:

* Go to the `CAC portal <https://portal.cac.cornell.edu/>`_ and log in. The instructions to log in are on the `CAC TechDocs page: Portal Login <https://portal.cac.cornell.edu/techdocs/general/CACportal/#portal-login>`_.

* Get access to Red Cloud by doing one of the following options on the CAC portal:

  * Start a new project by making a project request. The instructions are on the `CAC TechDocs page: As a Cornell Faculty or Staff, How Do I Start a New Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#as-a-cornell-faculty-or-staff-how-do-i-start-a-new-project>`__ (Only available for Cornell Faculty and Staff)

  * Join an existing project. The instructions are on the `CAC TechDocs page: How Do I Join an Existing Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-join-an-existing-project>`__
  
  * Request an exploratory account. The instructions are on the `CAC TechDocs page: How Do I Request an Exploratory Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-request-an-exploratory-project>`__ Note that an exploratory project does not have enough compute hours to complete this set of instructions.

* For new projects and existing projects, make sure that the project has Red Cloud subscriptions. 

* Log in to Red Cloud's `Red Cloud Horizon web interface <https://redcloud2.cac.cornell.edu/>`_.

The section below will guide you through this process. 
For an overview of Red Cloud, read Cornell `CAC TechDocs Red Cloud documentation <https://portal.cac.cornell.edu/techdocs/redcloud/#red-cloud>`_.


Start a Project
---------------

One way to get a CAC account is to request a project. 
Note that you must be a Cornell faculty member or staff member to view the pages below and start a project. 
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
it is recommended that you read about them here before proceeding: `Red Cloud: Images <https://portal.cac.cornell.edu/techdocs/redcloud/compute/#images>`__ 
and `Red Cloud: Run Linux Instance <https://portal.cac.cornell.edu/techdocs/redcloud/run_linux_instances/>`__


Create an SSH Key
-----------------

You can either upload a public SSH key to Red Cloud or generate an SSH key pair on Red Cloud before creating your instance.
Red Cloud injects the uploaded public key or generated public key into the instance's default user account,
and you will need to provide the matching private SSH key to log in to the instance.
If you are not familiar with "SSH key pairs", you should
`read about them <https://portal.cac.cornell.edu/techdocs/redcloud/compute/#keypairs>`__ before continuing.

* It's highly recommended that you `create a key pair on Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud/horizon_ssh_keys/#create-a-new-ssh-key-pair>`_. Be sure to follow the steps and save the private key it generated with the correct format and permission before proceeding. This is the easiest way to generate a key pair for this exercise. 

* Alternatively, `create an SSH Key on your computer <https://portal.cac.cornell.edu/techdocs/clusterinfo/linuxconnect/#public-key-authentication>`_ using the "ssh-keygen" command. That command allows you to specify the name of the private key file it creates, with the default being "id_rsa".  The matching public key file is saved and named with ".pub" appended to the filename. Then, `import the public key to Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud/horizon_ssh_keys/#import-a-public-key>`_ through the Red Cloud web interface.

Create a Security Group
-----------------------

Security groups are firewalls that control inbound and outbound network traffic to your instances. For an instance to be accessible, its security group must have port 22 (SSH) enabled. You can read more about them at `Red Cloud: Security Groups <https://portal.cac.cornell.edu/techdocs/redcloud/network/#security>`__. 

If you will access the instance from a Cornell Network (eduroam Wi-Fi, Ethernet, Cornell VPN, etc.), it's sufficient to use the security group that already exists on your project: "campus-only-ssh". This security group is already configured to enable SSH traffic from anywhere in the Cornell Network.

If you cannot use any of the options above, you will need to create a security group and add an SSH rule for an IP address you frequently use. Follow the steps below to create a security group:

* `Create a security group <https://portal.cac.cornell.edu/techdocs/redcloud/horizon_security_groups/#create-a-security-group>`__

* `Add an SSH rule to the security group to allow SSH <https://portal.cac.cornell.edu/techdocs/redcloud/horizon_security_groups/#manage-your-security-group>`__

 * In the Rule dropdown, select "SSH"
 * In the CIDR field, put your IP address followed by "/32", e.g., "128.84.0.0/32"

Note that once you put your IP address in the CIDR field, you may connect to the instance from that IP address. If your IP address changes for any reason, you will need to remove and update the rule.


Create an Instance
------------------

The Cornell TechDocs `Creating a New Linux Instance <https://portal.cac.cornell.edu/techdocs/redcloud/run_linux_instances/#creating-a-new-linux-instance>`_
provides detailed instructions about creating a Linux instance on Red Cloud.
While following those steps, be sure to make the following choices for this instance:

* When choosing an image as the instance source:
  
  * Select Boot from Source is "Image"
  * Volume Size (GB) is 1000
  * Delete Volume on Instance Delete is "Yes"
  * Select the "ubuntu-24.04-LTS" image

* In Flavor, choose the "Flavor" c64.m120 (64 Virtual CPUs) to provide a faster simulation run-time. Note that this will consume Red Cloud subscriptions very fast.
* In Network, select "public".
* In Security Groups, select "campus-only-ssh" or the security group you created.
* In Key Pair, select the SSH public key that you created or uploaded previously.

When all the required options are selected, click on the "Launch Instance" button, and wait for the instance to enter the "Active" state. Note that the instance will not only be created, but also running so that you can log in after a couple of minutes.


Log in to the Instance
----------------------

The instructions for `connecting to Red Cloud Linux instances using SSH <https://portal.cac.cornell.edu/techdocs/redcloud/run_linux_instances/#accessing-instances>`_
can be executed in the Command Prompt or PowerShell on Windows (from the Start menu, type "cmd" and select Command Prompt or search for PowerShell) or from the Terminal application on a Mac.

In either case, you will need to know the location and name of the private SSH key created on your computer or downloaded from Red Cloud (see above),
the IP address of your instance (found in the Red Cloud OpenStack interface)
and the default username on your instance, which is "ubuntu".

You will know that your login has been successful when the prompt has the form ``ubuntu@instance-name:~$``,
which indicates your username, the instance name, and your current working directory, followed by "$"


Managing a Red Cloud Instance
-----------------------------

In order to use cloud computing resources efficiently, you must know how to
`manage your instances <https://portal.cac.cornell.edu/techdocs/redcloud/compute/#instance-states>`_.
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
Decreasing the number of CPUs (say, to flavor "c8.m64") may slow down your computations, but it will also reduce the cost per hour to run the instance. Or, you may increase the number of CPUs to c128.m240 to speed up the computations. Nonetheless, it's important to shelve the instance as soon as you are done. 



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



Access Data for WPS and WRF
===========================


Install and Enable CephFS
-------------------------

You need to access the data used in this exercise. In total, the full data are close to 90 GB in size. Usually, such large datasets cannot be shared easily. However, Red Cloud now has a Ceph cluster, a distributed file system that stores the data locally at Cornell CAC. Any Linux machine on the Cornell network can access this data using the following steps. 

First, update the package list::

    sudo apt update

Install CephFS client::

    sudo apt install ceph-common

The CephFS mounting steps are slightly more complicated. When a CephFS share is created, access rules must be set for writing or reading the data. This credential is called a keyring, which consists of an entity name (accessTo) and a key (accessKey). For this exercise, copy and paste the credentials for read-only access::

    accessTo="iwrf-lulc-read-only"
    accessKey="AQBsg0lozVQiDxAAZYNFvpyD9lqdzYD1ouv/Wg==" 

The following commands set up the keyring::

    mkdir -p /etc/ceph
    echo -e "[client.${accessTo}]\n    key = ${accessKey}" | sudo tee /etc/ceph/ceph.client.${accessTo}.keyring

The keyring file must be only readable to root::

    sudo chown root:root /etc/ceph/ceph.client.${accessTo}.keyring
    sudo chmod 600 /etc/ceph/ceph.client.${accessTo}.keyring

Choose the mount point for the CephFS share, which will be in the home directory::

    cephfsPath="128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/e91d7ccd-9845-4d2a-acc6-d40e572ee796/937df611-6035-47bc-92ed-ad09fb225715"
    mountPoint="/home/ubuntu/lulc_input"

Mount to the location::

    echo "${cephfsPath} ${mountPoint} ceph name=${accessTo},x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw 0 2" | sudo tee -a /etc/fstab
    sudo systemctl daemon-reload
    mkdir -p ${mountPoint}
    sudo mount ${mountPoint}

You might encounter some errors during the mount step. Disregard these errors, and run the following command to test if mount is successful::

    df -h ${mountPoint}

If the CephFS share is mounted correctly, the following output is shown:

.. raw:: html

    <style>
        .no-copybutton .copybtn {
            display: none !important;
        }
    </style>

.. code-block:: console
    :class: no-copybutton

    Filesystem                                                                                                                                                                             Size  Used Avail Use% Mounted on
    128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/e91d7ccd-9845-4d2a-acc6-d40e572ee796/937df611-6035-47bc-92ed-ad09fb225715  100G   85G   16G  85% /home/ubuntu/lulc_input

    
.. include:: lulcconfigfiles.rst

.. include:: lulcscreen.rst

.. include:: lulcinstructions.rst


View Full WRF Output
--------------------

If you do not have the resource to run the entire simulation but would like to see the results, paste the following commands to access the full output Ceph share::

    accessTo="iwrf-lulc-output-read-only"
    accessKey="AQCe60lo0kUiJBAAkf9bYacxnfjVM4zcku67Xw==" 
    cephfsPath="128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/4686628e-540f-4e99-8cd1-9e53dcb9f97d/686fafb3-94a2-4547-b33a-178f1f59ff8f"
    mountPoint="/home/ubuntu/lulc_full_output"

::

    mkdir -p /etc/ceph
    echo -e "[client.${accessTo}]\n    key = ${accessKey}" | sudo tee /etc/ceph/ceph.client.${accessTo}.keyring

::

    sudo chown root:root /etc/ceph/ceph.client.${accessTo}.keyring
    sudo chmod 600 /etc/ceph/ceph.client.${accessTo}.keyring

::

    echo "${cephfsPath} ${mountPoint} ceph name=${accessTo},x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw 0 2" | sudo tee -a /etc/fstab

::

    sudo systemctl daemon-reload

::

    mkdir -p ${mountPoint}
    sudo mount ${mountPoint}

::
      
    df -h ${mountPoint}

The full output should be in ``/home/ubuntu/lulc_full_output``.
