***************
Getting Started
***************

What to Expect
==============

This guide contains instructions to demonstrate how to use containers to
run WRF to generate model output and METplus to perform verification of the
WRF output using observations.

Future work will add instructions to easily generate plots of the WRF and
METplus output to visualize the results.

Container Software
==================

The `Docker <https://www.docker.com/>`_ or `Apptainer <https://apptainer.org>`_
containerization software is required to run I-WRF. Check if either of these
options is already installed on your system.

.. dropdown:: Instructions

  To check if Docker is already available, the following command should display
  the usage statement::

      docker --help

  To check if Apptainer is already available, the following command should display
  the usage statement::

      apptainer --help

Refer to the relevant section below for instructions to obtain this software
on various supported environments.

.. dropdown:: NSF NCAR Instructions

  On the NCAR supercomputers Casper and Derecho, Apptainer is available as a module.

  To load apptainer, run the following::

      module load apptainer

  Refer to `NCAR HPC User Documentation <https://ncar-hpc-docs-arc-iframe.readthedocs.io/>`_
  for additional details.

.. dropdown:: Jetstream2 Instructions

  If running on a `Jetstream2 <https://jetstream-cloud.org/index.html>`_ instance, Docker must be installed on the instance.

  The `instructions for installing Docker Engine on Ubuntu <https://docs.docker.com/engine/install/ubuntu/>`_
  are very thorough and serve as a good reference, but we only need to perform a subset of those steps.
  These commands run a script that sets up the Docker software repository on your instance,
  then installs Docker::

      curl --location https://bit.ly/3R3lqMU > install-docker.sh
      source install-docker.sh

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

.. dropdown:: User Workstation Instructions

  To install Docker or Apptainer on a personal workstation,
  please refer to the installation instructions to
  `Get Docker <https://docs.docker.com/get-docker>`_ or
  `Install Apptainer <https://apptainer.org/docs/admin/main/installation.html>`_.

Next Steps
==========

Once you have confirmed access to a platform on which you can run
`Docker <https://www.docker.com/>`_ or `Apptainer <https://apptainer.org>`_, the next
step is running an I-WRF use case. Instructions are provided for a handful of use
cases, but :ref:`use-case-matthew` is the simplest and serves as a great starting
place. Users are strongly encourged to run the :ref:`use-case-matthew` use case before
proceeding to more complex ones or making any changes to the default configuration
settings.
