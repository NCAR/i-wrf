.. _compute-platform-nsf-ncar:

NSF NCAR
--------

The `NSF NCAR computing resources <https://www.cisl.ucar.edu/capabilities/supercomputing>`_
are available for projects large or small; for researchers, instructors,
and students at U.S. academic institutions; and for modeling, machine learning,
and analysis activities.

.. dropdown:: Instructions

  .. dropdown:: Get Access to NCAR HPC

    To get started with running I-WRF on NCAR HPC systems, you will need access to one of the supported platforms
    (Derecho, Casper, or other NCAR computing resources).
    If you do not already have access, you will need to request an account through the NCAR
    Computing and Information Systems Laboratory (CISL).

    NCAR HPC access is typically provided to researchers affiliated with NCAR, university collaborators, or
    those with approved allocations.
    If you need to request access:

      * Visit the `Getting Started with NSF NCAR HPC Resources <https://ncar-hpc-docs-arc-iframe.readthedocs.io/getting-started/#getting-started-with-nsf-ncar-hpc-resources>`_ page to create an account
      * Provide information about your research project and institutional affiliation
      * Wait for account approval, which typically takes 1-2 business days
      * Once approved, you can log in to the HPC systems using SSH

    Most NCAR HPC systems use a batch job scheduling system for computational work.
    While the I-WRF exercises can be run interactively for demonstration purposes,
    production runs should be submitted through the job scheduler.
    Refer to the `NCAR HPC documentation <https://arc.ucar.edu/docs>`_ for specific guidance on your target system.
    Once you have access to an NCAR HPC system, you can log in using SSH from your local machine or through
    NCAR's web-based interfaces where available.

  .. dropdown:: Log in to NCAR HPC

    To log in, start your terminal or Secure Shell client and run an ssh command::

        ssh -X username@derecho.hpc.ucar.edu

    The ``-X`` is optional and requests simple X11 graphics forwarding to your client.
    You can omit username in the command above if your Derecho username is the same as your username on your local computer.

    With your successful login to Derecho through SSH,
    you can now create the run folders, install Docker software and download the data to run the simulation and verification.
