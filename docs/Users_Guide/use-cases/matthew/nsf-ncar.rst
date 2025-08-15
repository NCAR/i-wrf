.. _matthew-nsf-ncar:
  
On NSF NCAR HPC 
^^^^^^^^^^^^^^^
  
Follow the compute platform instructions for :ref:`compute-platform-nsf-ncar`
to secure access to and log in to NSF NCAR HPC.

These instructions are currently limited to running the METplus verification
software and assume that WRF output is already available in a local directory.

.. dropdown:: Instructions

  .. dropdown:: Pull The Docker Image As A Singularity Image File (.sif)

    Derecho uses the ``modules`` command to make it easy to load various software libraries.  We
    need to load a few modules to make basic commands available to the environment and then
    the container image can be pulled from Docker Hub::

        module load charliecloud apptainer gcc cuda ncarcompilers
        mkdir ${HOME}/iwrf ; cd ${HOME}/iwrf
        singularity pull docker://ncar/iwrf:latest

    Check that there is a file named ``iwrf_latest.sif`` if the current directory to confirm
    that the image was pulled successfully.

  .. dropdown:: Gain Interactive Access To A Compute Node

    Tasks that are resource intensive should not be run on the login nodes, so a compute node
    should be accessed through Derecho's job queue before starting the container.  The following
    command will submit an interactive job in the `develop` queue.::

        qsub -l select=1:ncpus=8:mpiprocs=8 -A <account_id> -l walltime=01:00:00 -I -q develop

    The above command should be modified with your specific account ID for charging computing time.
    The number of processors needed can also be specified here.  The full documentation for the `qsub`
    command can be found on `Adaptive Computing's <http://docs.adaptivecomputing.com/torque/4-0-2/Content/topics/commands/qsub.htm>`_ website.

  .. dropdown:: Running WRF In The Container

    Once the interactive job has started, the container can be started and WRF can run.

    To simplify the WRF execution process, there is a script that will download case study data for Hurricane Matthew (2016),
    run Ungrib, Geogrid, Metgrid, REAL, and WRF processes.  Use the following command to download the script.::

        wget https://raw.githubusercontent.com/NCAR/i-wrf/feature/hurricane-matthew-script/run_hurricane_matthew_case.sh

    Now the singularity container can be started.::

        module load charliecloud apptainer gcc cuda ncarcompilers
        singularity run --bind /glade/work/wrfhelp/WPS_GEOG:/terrestrial_data --bind /var/spool/pbs:/var/spool/pbs iwrf_latest.sif /bin/bash

    The ``--bind /glade/work/wrfhelp/WPS_GEOG:/terrestrial_data`` option will make the terrestrial data available to the container,
    which is pre-installed on Derecho.  This data set is required by the Geogrid step that will be running.
    The ``--bind /var/spool/pbs:/var/spool/pbs`` option will make the job queue information available to the container, which provides
    the available hosts and number of compute cores.  This information is required by the ``mpirun`` command in the script.

    Now that we are running inside the container, we can execute the ``run_hurricane_matthew_case.sh`` script to run the model.::

        bash ./run_hurricane_matthew_case.sh

    After the script finishes running the WRF output data will be in ``/tmp/hurricane_matthew/wrfout_d01*``.  If these files exist,
    it indicates that the WRF run was successful.  If these files do not appear, you can check ``/tmp/hurricane_matthew/rsl.error.*``
    files for errors.


  .. dropdown:: Load Required Modules

    NCAR HPC systems use environment modules to manage software. Load the Apptainer module which provides the containerization software needed to run METplus::

        module load apptainer

  .. dropdown:: Define Environment Variables

    We will be using environment variables throughout this exercise to ensure consistent file paths and resource names. Copy and paste the definitions below into your shell before proceeding::

        IWRF_WORK_DIR=${SCRATCH}/iwrf_work
        LOCAL_OUTPUT_DIR=${IWRF_WORK_DIR}/metplus_out
        export APPTAINER_TMPDIR=${TMPDIR}

    Any time you open a new shell session on the HPC system, you will need to reload the apptainer module, switch shells, if needed, and redefine these variables before executing the commands that follow.

  .. dropdown:: Create Working Directories

    The METplus verification process requires specific directory structures to organize input data, configuration files, and output results. Create the main working directory in your scratch space::

        mkdir -p ${IWRF_WORK_DIR}

    Create a directory to store the METplus verification output::

        mkdir -p ${LOCAL_OUTPUT_DIR}

    Create a directory for temporary Apptainer files. The $TMPDIR variable is automatically set on NCAR HPC systems to an appropriate temporary storage location::

        mkdir -p ${APPTAINER_TMPDIR}
  
  .. dropdown:: Download Configuration Files
  
    METplus requires configuration files to direct its verification behavior. These are available in the I-WRF GitHub repository. Clone the repository to access the Hurricane Matthew use case configuration::

        git clone https://github.com/NCAR/i-wrf ${IWRF_WORK_DIR}/i-wrf

    This creates a local copy of all I-WRF configuration files, including the METplus settings needed for the Hurricane Matthew verification workflow.
  
  .. dropdown:: Get the METplus and Data Container Images

    Change to the working directory and pull the METplus software image and
    observation data from the container registry to your HPC system's storage.
    This will create a files ending in :code:`.sif` in the current directory::

       apptainer pull ${IWRF_WORK_DIR}/iwrf-metplus.sif docker://ncar/iwrf-metplus:latest
       apptainer pull ${IWRF_WORK_DIR}/data-matthew-input-obs.sif oras://registry-1.docker.io/ncar/iwrf-data:matthew-input-obs.apptainer

    .. note::

      If an error is displayed when attempting to pull the METplus image,
      creating a DockerHub account and authenticating through apptainer may be
      necessary::

          apptainer remote login --username {USERNAME} docker://docker.io

      where **{USERNAME}** is your DockerHub username.

  .. dropdown:: Configure Container Data Bindings

    Set environment variable to bind directories to the containers
    (note: this can also be accomplished by passing the value on the command line
    using the --bind argument)

    * Input data directories for WRF, raob, and metar input data

      * WRF:

        * Local: /glade/derecho/scratch/jaredlee/nsf_i-wrf/matthew
        * Container: /data/input/wrf

      * RAOB:

        * Local: From data-matthew-input-obs.sif
        * Container: /data/input/obs/raob

      * METAR:

        * Local: From data-matthew-input-obs.sif
        * Container: /data/input/obs/metar

      * Config directory containing METplus use case configuration file

        * Local: ${IWRF_WORK_DIR}/i-wrf/use_cases/Hurricane_Matthew/METplus
        * Container: /config

      * Plot script directory containing WRF plotting scripts

        * Local: ${IWRF_WORK_DIR}/i-wrf/use_cases/Hurricane_Matthew/Visualization
        * Container: /plot_scripts

      * Output directory to write output

        * Local: ${IWRF_WORK_DIR}/metplus_out

      * Container: /data/output

    * Apptainer temp directory

      * Local: ${APPTAINER_TMPDIR}
      * Container: ${APPTAINER_TMPDIR}

   ::

       LOCAL_METPLUS_CONFIG_DIR=${IWRF_WORK_DIR}/i-wrf/use_cases/Hurricane_Matthew/METplus
       LOCAL_PLOT_SCRIPT_DIR=${IWRF_WORK_DIR}/i-wrf/use_cases/Hurricane_Matthew/Visualization
       LOCAL_FCST_INPUT_DIR=/glade/derecho/scratch/jaredlee/nsf_i-wrf/matthew

       export APPTAINER_BIND="${IWRF_WORK_DIR}/data-matthew-input-obs.sif:/data/input/obs:image-src=/,${LOCAL_METPLUS_CONFIG_DIR}:/config,${LOCAL_FCST_INPUT_DIR}:/data/input/wrf,${LOCAL_OUTPUT_DIR}:/data/output,${LOCAL_PLOT_SCRIPT_DIR}:/plot_scripts,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"

  .. dropdown:: Run METplus

    Execute the run_metplus.py command inside the container to run the use case::

        apptainer exec ${IWRF_WORK_DIR}/iwrf-metplus.sif /metplus/METplus/ush/run_metplus.py /config/PointStat_matthew.conf

    Check that the output data was created locally::

        ls -1  ${IWRF_WORK_DIR}/metplus_out/point_stat
