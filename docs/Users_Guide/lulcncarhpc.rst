:orphan:

.. _lulcncarhpc:

***************************************************************
Running I-WRF on NCAR HPCs with Land Use/Land Cover Change Data
***************************************************************

Overview
========

The following instructions can be used to run METplus verification for the Land Use/Land Cover Change (LULC) use case of the I-WRF weather simulation framework from the National Center for Atmospheric Research (NCAR) on NCAR High Performance Computing (HPC) platforms. The steps below configure and execute the METplus verification framework using containerized applications with Apptainer (formerly Singularity) to analyze I-WRF LULC simulation output.

The LULC use case examines how changes in land surface characteristics impact weather patterns and atmospheric dynamics through idealized modeling scenarios. METplus provides statistical analysis and evaluation tools to quantify these meteorological impacts, making this verification workflow valuable for studies in urban meteorology, land-atmosphere interactions, and climate change impact assessment.

NCAR HPC systems provide the computational resources needed for efficient METplus processing of large I-WRF datasets. This exercise uses containerized METplus applications, which simplifies the setup work needed to run the verification and ensures consistency across different HPC environments.

It is recommended that you follow the instructions in each section in the order presented to avoid encountering issues during the process. This guide assumes that I-WRF LULC simulations have already been completed and focuses specifically on the METplus verification workflow.


Prepare to Use NCAR HPCs
========================

To get started with running METplus verification on NCAR HPC systems, you will need access to one of the supported platforms (Derecho, Casper, or other NCAR computing resources). If you do not already have access, you will need to request an account through the NCAR Computing and Information Systems Laboratory (CISL).

NCAR HPC access is typically provided to researchers affiliated with NCAR, university collaborators, or those with approved allocations. If you need to request access:

* Visit the NCAR CISL user registration page to create an account
* Provide information about your research project and institutional affiliation
* Wait for account approval, which typically takes 1-2 business days
* Once approved, you can log in to the HPC systems using SSH

Most NCAR HPC systems use a batch job scheduling system for computational work. While this exercise can be run interactively for demonstration purposes, production runs should be submitted through the job scheduler. Refer to the NCAR HPC documentation for specific guidance on your target system.
Once you have access to an NCAR HPC system, you can log in using SSH from your local machine or through NCAR's web-based interfaces where available.

Preparing the Environment
=========================

With your NCAR HPC account active and you logged in to the system, you can now set up the environment and create the necessary directories to run METplus verification. You will only need to perform these steps once per system, as the directory structure and configuration will remain available for future use.

The following sections instruct you to issue numerous Linux commands in your shell. The commands in each section can be copied and pasted into your shell terminal.

Load Required Modules
---------------------

NCAR HPC systems use environment modules to manage software. Load the Apptainer module which provides the containerization software needed to run METplus::

   module load apptainer

Define Environment Variables
----------------------------

We will be using environment variables throughout this exercise to ensure consistent file paths and resource names. Copy and paste the definitions below into your shell before proceeding::

    IWRF_WORK_DIR=${SCRATCH}/iwrf_work
    LOCAL_OUTPUT_DIR=${IWRF_WORK_DIR}/metplus_out
    export APPTAINER_TMPDIR=${TMPDIR}

Any time you open a new shell session on the HPC system, you will need to reload the apptainer module and redefine these variables before executing the commands that follow.

Create Working Directories
--------------------------

The METplus verification process requires specific directory structures to organize input data, configuration files, and output results. Create the main working directory in your scratch space::

    mkdir -p ${IWRF_WORK_DIR}

Create a directory to store the METplus verification output::

    mkdir -p ${LOCAL_OUTPUT_DIR}

Create a directory for temporary Apptainer files. The $TMPDIR variable is automatically set on NCAR HPC systems to an appropriate temporary storage location::

    mkdir -p ${APPTAINER_TMPDIR}

Download Configuration Files
----------------------------

METplus requires configuration files to direct its verification behavior. These are available in the I-WRF GitHub repository. Clone the repository to access the LULC use case configuration::

   git clone https://github.com/NCAR/i-wrf ${IWRF_WORK_DIR}/i-wrf

This creates a local copy of all I-WRF configuration files, including the METplus settings needed for the LULC verification workflow.

Pull Apptainer Objects
======================

As mentioned above, the METplus software is provided as a containerized image that will run using Apptainer on your NCAR HPC system. Apptainer (formerly Singularity) is the preferred containerization technology on HPC systems, as it provides secure container execution without requiring root privileges. Unlike cloud environments that use Docker directly, NCAR HPC systems use Apptainer to run containerized applications.

The METplus image contains all the necessary software and dependencies to perform verification of I-WRF LULC simulation output. You can "pull" (download) the METplus image from the container registry to your HPC system's storage.

Get the METplus and Data Container Images
-----------------------------------------

You must pull the METplus software container and the input data containers that contain the observational and WRF simulation data for the LULC use case::

   apptainer pull ${IWRF_WORK_DIR}/iwrf-metplus.sif docker://ncar/iwrf-metplus:latest
   apptainer pull ${IWRF_WORK_DIR}/data-lulc-input-obs.sif docker://ncar/iwrf-data:lulc-input-obs-d03.apptainer
   apptainer pull ${IWRF_WORK_DIR}/data-lulc-input-wrf.sif docker://ncar/iwrf-data:lulc-input-wrf-d03.apptainer

These commands download three container images: the METplus software, the observational data, and the WRF simulation data. The process may take several minutes depending on your network connection.

Run METplus
===========

After the container images have been downloaded, you can run the METplus verification to compare the I-WRF LULC simulation results against observational data and generate statistical verification results and visualization plots. This process involves configuring the data bindings and executing the verification workflow for two meteorological variables.

Configure Container Data Bindings
---------------------------------

METplus requires access to input data, configuration files, and output directories. Apptainer uses bind mounts to make local directories and container images available inside the running container. Set up the environment variables that define these data bindings.

First, define the local directory paths for configuration and visualization scripts::

    LOCAL_METPLUS_CONFIG_DIR=${IWRF_WORK_DIR}/i-wrf/use_cases/Land_Use_Land_Cover/METplus
    LOCAL_PLOT_SCRIPT_DIR=${IWRF_WORK_DIR}/i-wrf/use_cases/Land_Use_Land_Cover/Visualization

Next, configure the Apptainer bind mounts. This environment variable tells Apptainer how to map local directories and container images to paths inside the running container::

   export APPTAINER_BIND="${IWRF_WORK_DIR}/data-lulc-input-obs.sif:/data/input/obs:image-src=/,${LOCAL_METPLUS_CONFIG_DIR}:/config,${IWRF_WORK_DIR}/data-lulc-input-wrf.sif:/data/input/wrf:image-src=/,${LOCAL_OUTPUT_DIR}:/data/output,${LOCAL_PLOT_SCRIPT_DIR}:/plot_scripts,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"

This configuration provides the container with access to:

* Observational data from the ``data-lulc-input-obs.sif`` container image at ``/data/input/obs``
* WRF simulation data from the ``data-lulc-input-wrf.sif`` container image at ``/data/input/wrf``
* METplus configuration files from the I-WRF repository at ``/config``
* Visualization script files for generating plots at ``/plot_scripts``
* Output directory for writing verification results at ``/data/output``
* Temporary directory for Apptainer operations

Execute METplus Verification
----------------------------

The LULC use case includes verification for two meteorological variables: accumulated precipitation and radar reflectivity. Each verification is run separately using its own METplus configuration file.

Run the accumulated precipitation verification::

   apptainer exec ${IWRF_WORK_DIR}/iwrf-metplus.sif /metplus/METplus/ush/run_metplus.py /config/GridStat_apcp_lulc.conf

This process compares simulated precipitation accumulation against observational data and generates statistical metrics. Progress information is displayed while the verification is performed.

Run the reflectivity verification::

   apptainer exec ${IWRF_WORK_DIR}/iwrf-metplus.sif /metplus/METplus/ush/run_metplus.py /config/GridStat_refc_lulc.conf

This process evaluates the model's ability to simulate radar reflectivity patterns compared to observed radar data.

Both verification processes use GridStat, which computes grid-to-grid verification statistics. The tools generate comprehensive statistical output including bias, correlation, and skill scores that quantify the model's performance.

Verify Output Generation
------------------------

After both METplus runs complete successfully, you can verify that the output files were created properly.

Check that the GridStat verification output was generated::

   ls ${LOCAL_OUTPUT_DIR}/grid_stat/* -1

This should show directories containing statistical output files in text format that can be viewed and analyzed.

Check that the METplotpy visualization plots were created locally::

   ls ${LOCAL_OUTPUT_DIR}/met_plot/*/*.png -1

This should display a list of PNG image files containing plots and graphics that visualize the verification results. These plots provide graphical representations of the statistical comparisons between the I-WRF LULC simulations and observational data.

Visualize the Results
=====================

In the near future, this exercise will be extended to include instructions to visualize the results.
