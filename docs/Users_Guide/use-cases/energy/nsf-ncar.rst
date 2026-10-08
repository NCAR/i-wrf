.. _energy-nsf-ncar:

On NSF NCAR HPC
^^^^^^^^^^^^^^^

Follow the compute platform instructions for :ref:`compute-platform-nsf-ncar`
to secure access to and log in to NSF NCAR HPC.

These instructions are for running the Renewable Energy use case on NSF NCAR
HPC systems (Derecho, Casper). The Renewable Energy use case demonstrates
WRF simulations with HRRR initial and boundary conditions, specifically
configured for renewable energy forecasting applications including solar
and wind energy research.

.. dropdown:: Instructions

  .. dropdown:: Log into Derecho

    From a terminal window, log into Derecho HPC using your login credentials,
    passing the ``-Y`` argument to enable X window forwarding for viewing images::

        ssh -Y {username}@derecho.hpc.ucar.edu

  .. dropdown:: Start a Bash Shell

    The commands in these instructions use bash syntax.
    If your default shell on Derecho is tcsh, start a bash shell first::

        bash

  .. dropdown:: Load Required Modules

    NCAR HPC systems use environment modules to manage software.
    Load the Apptainer module which provides the containerization software
    needed to run WRF::

        module load apptainer

  .. dropdown:: Define Working Directory

    Set an environment variable called **WORKING_DIR** to a directory to
    store all input and output files for the simulation.
    Change this path to your preference::

        WORKING_DIR=${SCRATCH}/iwrf_re_demo

  .. include:: energy/common/set-env-vars.rst

  .. dropdown:: Set Apptainer Temp Directory

    Set the **$APPTAINER_TMPDIR** environment variable to **$TMPDIR** to ensure
    that the correct temp directory is used by Apptainer. **$TMPDIR** is set
    automatically upon login to NCAR HPC systems::

        export APPTAINER_TMPDIR=${TMPDIR}

  .. dropdown:: Create Working Directories

    Create the main working directory in your scratch space::

        mkdir -p ${WORKING_DIR}

    Create a directory to store the WRF inputs and outputs::

        mkdir -p ${WRF_DATE_DIR}

    Create a directory to store the HRRR data::

        mkdir -p ${HRRR_DATA_DIR}

    Create a directory for temporary Apptainer files.
    The $TMPDIR variable is automatically set on NCAR HPC systems::

        mkdir -p ${APPTAINER_TMPDIR}

  .. dropdown:: Create Environment File

    The environment variables set above will not be available inside the compute node,
    so create an environment file that can be sourced when running on compute nodes::

        echo export WORKING_DIR=${WORKING_DIR} > ${WORKING_DIR}/env_re_demo.sh
        echo export HPC_ACCOUNT=${HPC_ACCOUNT} >> ${WORKING_DIR}/env_re_demo.sh
        echo export WRF_IMAGE=${WRF_IMAGE} >> ${WORKING_DIR}/env_re_demo.sh
        echo export WRF_TOP_DIR=${WRF_TOP_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export WRF_DATE_DIR=${WRF_DATE_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export METPLUS_DIR=${METPLUS_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export WRF_CONFIG_DIR=${WRF_CONFIG_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export METPLUS_CONFIG_DIR=${METPLUS_CONFIG_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export PLOT_SCRIPT_DIR=${PLOT_SCRIPT_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export HRRR_DATA_DIR=${HRRR_DATA_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export GEOG_DATA_DIR=${GEOG_DATA_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export WPS_FILES_DIR=${WPS_FILES_DIR} >> ${WORKING_DIR}/env_re_demo.sh
        echo export APPTAINER_TMPDIR=${APPTAINER_TMPDIR} >> ${WORKING_DIR}/env_re_demo.sh

  .. include:: energy/common/download-config-files.rst

  .. dropdown:: Pull the WRF Container Image

    Pull the WRF software container from the container registry to your HPC system::

        apptainer pull ${WORKING_DIR}/iwrf_latest.sif docker://${WRF_IMAGE}

    .. note::

      If an error is displayed when attempting to pull the images,
      you may need to authenticate with DockerHub::

          apptainer remote login --username {USERNAME} docker://docker.io

      where **{USERNAME}** is your DockerHub username.

    Check that the image was pulled successfully::

        ls -lh ${WORKING_DIR}/iwrf_latest.sif

  .. include:: energy/common/download-wrf-data.rst

  .. dropdown:: Gain Interactive Access To A Compute Node

    Tasks that are resource intensive should not be run on the login nodes.
    Submit an interactive job in the ``develop`` queue before starting WRF::

        cd ${WORKING_DIR}
        qsub -l select=2:ncpus=128:mpiprocs=128 -A ${HPC_ACCOUNT} -l walltime=02:00:00 -I -q main

    .. note::

      The account ``NERP0002`` is the default for this demo, set via the
      ``HPC_ACCOUNT`` variable above.  Replace it with your own allocation
      if needed.

    This requests 2 nodes (256 MPI ranks total), which is needed for WRF to
    complete within the 2-hour walltime.  WPS steps (geogrid, ungrib, metgrid)
    will also run in this allocation.  The ``main`` queue is required because
    WRF exceeds the 30-minute walltime limit of the ``develop`` queue.

    When the interactive job starts, your prompt will change to something like
    ``user@decNNNN``. Once you see this new prompt, your interactive job is active.

  .. dropdown:: Source Environment File

    Source the environment file that was created earlier::

        source ${WORKING_DIR}/env_re_demo.sh

  .. dropdown:: Configure Container Data Bindings for WRF

    Set environment variable to bind directories to the container
    (this can also be accomplished by passing the value using ``--bind`` argument)::

        export APPTAINER_BIND="${GEOG_DATA_DIR}:/home/wrfuser/terrestrial_data/geog,${WPS_FILES_DIR}:/home/wrfuser/terrestrial_data/wps_files,${HRRR_DATA_DIR}:/tmp/hrrr_data,${WRF_DATE_DIR}:/tmp/renewable_energy,/var/spool/pbs:/var/spool/pbs,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"

    The bindings provide:

    * Geographic data (WPS_GEOG) for geogrid:
      ``${GEOG_DATA_DIR}`` -> ``/home/wrfuser/terrestrial_data/geog``

    * Auxiliary WPS files (QNWFA/QNIFA aerosol climatology):
      ``${WPS_FILES_DIR}`` -> ``/home/wrfuser/terrestrial_data/wps_files``

    * Downloaded HRRR GRIB2 input data:
      ``${HRRR_DATA_DIR}`` -> ``/tmp/hrrr_data``

    * WRF configuration files, intermediate files, and output:
      ``${WRF_DATE_DIR}`` -> ``/tmp/renewable_energy``

    * Job queue information (required for mpirun):
      ``/var/spool/pbs`` -> ``/var/spool/pbs``

    * Apptainer temp directory:
      ``${APPTAINER_TMPDIR}`` -> ``${APPTAINER_TMPDIR}``

  .. dropdown:: Running WRF In The Container

    Once the interactive job has started, run WRF inside the container::

        module load apptainer
        apptainer exec ${WORKING_DIR}/iwrf_latest.sif /tmp/renewable_energy/run.sh

    The ``run.sh`` script will execute WPS (geogrid, ungrib, metgrid) and WRF (real, wrf).

    Once WRF begins to execute, there will not be any log updates for several
    minutes until WRF completes and a new terminal prompt appears.

    After the script finishes, check that WRF output was created::

        ls ${WRF_DATE_DIR}/wrfout_d01*

    If these files exist, the WRF run was successful. If not, check the
    ``${WRF_DATE_DIR}/rsl.error.*`` files for errors.

  .. dropdown:: Source Environment File for METplus

    After WRF completes, configure the environment for METplus verification.
    Set up the environment file::

        echo export WORKING_DIR=${WORKING_DIR} > ${WORKING_DIR}/env_re_metplus.sh
        echo export WRF_TOP_DIR=${WRF_TOP_DIR} >> ${WORKING_DIR}/env_re_metplus.sh
        echo export WRF_DATE_DIR=${WRF_DATE_DIR} >> ${WORKING_DIR}/env_re_metplus.sh
        echo export METPLUS_DIR=${METPLUS_DIR} >> ${WORKING_DIR}/env_re_metplus.sh
        echo export METPLUS_CONFIG_DIR=${METPLUS_CONFIG_DIR} >> ${WORKING_DIR}/env_re_metplus.sh
        echo export PLOT_SCRIPT_DIR=${PLOT_SCRIPT_DIR} >> ${WORKING_DIR}/env_re_metplus.sh
        echo export HRRR_DATA_DIR=${HRRR_DATA_DIR} >> ${WORKING_DIR}/env_re_metplus.sh
        echo export APPTAINER_TMPDIR=${APPTAINER_TMPDIR} >> ${WORKING_DIR}/env_re_metplus.sh

  .. dropdown:: Configure Container Data Bindings for METplus

    Set up the Apptainer bind mounts for METplus::

        export APPTAINER_BIND="${METPLUS_CONFIG_DIR}:/config,${WRF_TOP_DIR}:/data/input/wrf,${METPLUS_DIR}:/data/output,${PLOT_SCRIPT_DIR}:/plot_scripts,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"

  .. dropdown:: Run METplus

    Execute METplus verification::

        apptainer exec ${WORKING_DIR}/iwrf-metplus.sif /metplus/METplus/ush/run_metplus.py /config/GridStat_re_demo.conf

    METplus will generate statistical verification metrics and visualization plots.

  .. dropdown:: Exit the Interactive Compute Node

    Be sure to run ``exit`` when you are done to stop the compute node::

        exit

  .. dropdown:: Examine the Plots

    The images generated by METplus can be viewed using the ``display`` command
    if X-window forwarding has been enabled::

        display ${WORKING_DIR}/metplus_out/met_plot/line_T2_RMSE_BCMSE.png
