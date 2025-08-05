.. _compute-platform-windows:

Windows (Intel CPU)
-------------------

Simulations like WRF often require significant computing resources,
so it is recommended that the computer you use have at least four cores, 32 GB of RAM, and 50 Gb of available disk space.
This exercise runs the I-WRF programs as Docker "containers",
which simplifies the set-up work needed to run the simulation and verification.
However, the code used to build those Docker containers was compiled expressly for use on
`Intel CPUs <https://www.intel.com/content/www/us/en/products/details/processors.html>`_,
so the Windows 10 or 11 computer you use must contain an Intel processor
(note that these instructions are not intended for use on a system running Windows Server).
Your Windows account will also need to have administrative privileges in order to perform all necessary steps.

During the I-WRF exercises, you will create the run folders, install the software and download the data
that are needed to run the simulation and verification.
You will only need to perform these steps once.
The following sections instruct you to issue numerous DOS commands in a Windows "Command Prompt" shell.
To open such a shell:

  * Click the Start icon and then type :code:`cmd` to display matching commands.
  * Right click on the "Command Prompt" option that is shown and select "Run as administrator".
  * A black shell window should open.
