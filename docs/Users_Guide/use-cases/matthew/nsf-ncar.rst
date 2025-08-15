.. _matthew-nsf-ncar:

On NSF NCAR HPC 
^^^^^^^^^^^^^^^
  
Follow the compute platform instructions for :ref:`compute-platform-nsf-ncar`
to secure access to and log in to NSF NCAR HPC.

These instructions are currently limited to running the METplus verification
software and assume that WRF output is already available in a local directory.

.. dropdown:: Instructions

  .. dropdown:: Load Required Modules

    NCAR HPC systems use environment modules to manage software.
    Load the Apptainer module which provides the containerization software needed to run WRF and METplus::

        module load charliecloud apptainer gcc cuda ncarcompilers

  .. dropdown:: Define Working Directory

    Set an environment variable called **WORKING_DIR** to a directory to
    store all of the input and output files for the use case.
    Change this path to your preference::

      WORKING_DIR=${SCRATCH}/iwrf_work

  .. include:: matthew/common/set-env-vars.rst

  .. dropdown:: Set Apptainer Temp Directory

    Set the **$APPTAINER_TMPDIR** environment variable to **$TMPDIR** to ensure
    that the correct temp directory is used by Apptainer. **$TMPDIR** is set
    automatically upon log in to the NCAR HPC::

        export APPTAINER_TMPDIR=${TMPDIR}

  .. dropdown:: Create Environment File

    The environment variables set in the above instructions will not be
    available inside the compute node, so create an environment file that can
    be sourced.
    ::

        echo export WORKING_DIR=${WORKING_DIR} > ${WORKING_DIR}/env_matthew.sh
        echo export WRF_TOP_DIR=${WRF_TOP_DIR} >> ${WORKING_DIR}/env_matthew.sh
        echo export WRF_DATE_DIR=${WRF_DATE_DIR} >> ${WORKING_DIR}/env_matthew.sh
        echo export METPLUS_CONFIG_DIR=${METPLUS_CONFIG_DIR} >> ${WORKING_DIR}/env_matthew.sh
        echo export PLOT_SCRIPT_DIR=${PLOT_SCRIPT_DIR} >> ${WORKING_DIR}/env_matthew.sh
        echo export METPLUS_DIR=${METPLUS_DIR} >> ${WORKING_DIR}/env_matthew.sh
        echo export OBS_DATA_VOL=${OBS_DATA_VOL} >> ${WORKING_DIR}/env_matthew.sh
        echo export APPTAINER_TMPDIR=${APPTAINER_TMPDIR} >> ${WORKING_DIR}/env_matthew.sh


  .. dropdown:: Create Working Directories

    The METplus verification process requires specific directory structures to organize input data, configuration files, and output results.
    Create the main working directory in your scratch space::

        mkdir -p ${WORKING_DIR}

    Create a directory to store the METplus verification output::

        mkdir -p ${METPLUS_DIR}

    Create a directory to store the WRF inputs and outputs::

        mkdir -p ${WRF_DATE_DIR}

    Create a directory for temporary Apptainer files.
    The $TMPDIR variable is automatically set on NCAR HPC systems to an appropriate temporary storage location::

        mkdir -p ${APPTAINER_TMPDIR}

  .. include:: matthew/common/download-config-files.rst

  .. dropdown:: Pull The Docker Image As A Singularity Image Files (.sif)

    Pull the WRF software, METplus software image and
    observation data from the container registry to your HPC system's storage.
    This will create a files ending in :code:`.sif` in the **${WORKING_DIR}** directory::

       apptainer pull ${WORKING_DIR}/iwrf_latest.sif docker://${WRF_IMAGE}
       apptainer pull ${WORKING_DIR}/iwrf-metplus.sif docker://${METPLUS_IMAGE}
       apptainer pull ${WORKING_DIR}/data-${OBS_DATA_VOL}.sif oras://registry-1.docker.io/ncar/iwrf-data:${OBS_DATA_VOL}.apptainer

    .. note::

      If an error is displayed when attempting to pull the images,
      creating a DockerHub account and authenticating through apptainer may be
      necessary::

          apptainer remote login --username {USERNAME} docker://docker.io

      where **{USERNAME}** is your DockerHub username.

    Check that there are files named ``iwrf_latest.sif``, ``iwrf-metplus.sif``,
    and ``data-matthew-input-obs.sif`` in the **${WORKING_DIR}** directory
    to confirm that the images were pulled successfully::

        ls ${WORKING_DIR}


  .. include:: matthew/common/download-wrf-data.rst

  .. dropdown:: Gain Interactive Access To A Compute Node

    Tasks that are resource intensive should not be run on the login nodes, so a compute node
    should be accessed through Derecho's job queue before starting the container.
    Change directory to the $WORKING_DIR, then
    run the following command to submit an interactive job in the `develop` queue.::

        cd ${WORKING_DIR}
        qsub -l select=1:ncpus=8:mpiprocs=8 -A <account_id> -l walltime=01:00:00 -I -q develop

    The above command should be modified with your specific account ID for charging computing time.
    The number of processors needed can also be specified here. The full documentation for the `qsub`
    command can be found on `Adaptive Computing's <http://docs.adaptivecomputing.com/torque/4-0-2/Content/topics/commands/qsub.htm>`_ website.

    This will take a few minutes. When it completes, the terminal prompt will change to something like user@decNNNN.

  .. dropdown:: Source Environment File

    Source the environment file that was created earlier::

        source env_matthew.sh


  .. dropdown:: Configure Container Data Bindings for WRF

    Set environment variable to bind directories to the containers
    (note: this can also be accomplished by passing the value on the command line
    using the --bind argument)

    * Terrestrial Data:

      Data required by Geogrid

      * Local: ${WORKING_DIR}
      * Container: /home/wrfuser/terrestrial_data

    * WRF:

      WRF configuration files and run script

      * Local: ${WRF_DATE_DIR}
      * Container: /tmp/hurricane_matthew

    * Job Queue Information:

      Make the job queue information available to the container, which provides
      the available hosts and number of compute cores.
      This information is required by the ``mpirun`` command in the script.

      * Local: /var/spool/pbs
      * Container: /var/spool/pbs

    * Apptainer temp directory

      * Local: ${APPTAINER_TMPDIR}
      * Container: ${APPTAINER_TMPDIR}

   ::

       export APPTAINER_BIND="${WORKING_DIR}:/home/wrfuser/terrestrial_data,${WRF_DATE_DIR}:/tmp/hurricane_matthew,/var/spool/pbs:/var/spool/pbs,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"


  .. dropdown:: Running WRF In The Container

    Once the interactive job has started,
    the run script can be called inside the container to run WRF::

        module load charliecloud apptainer gcc cuda ncarcompilers
        apptainer exec ${WORKING_DIR}/iwrf_latest.sif /tmp/hurricane_matthew/run.sh


    After the script finishes running the WRF output data will be in ``${WRF_DATE_DIR}/wrfout_d01*``.
    If these files exist, it indicates that the WRF run was successful.
    If these files do not appear, you can check the ``${WRF_DATE_DIR}/rsl.error.*``
    files for errors.

  .. dropdown:: Configure Container Data Bindings for METplus

    Set environment variable to bind directories to the containers
    (note: this can also be accomplished by passing the value on the command line
    using the --bind argument)

    * Input data directories for WRF, raob, and metar input data

      * WRF:

        * Local: ${WRF_TOP_DIR}
        * Container: /data/input/wrf

      * RAOB:

        * Local: From data-matthew-input-obs.sif
        * Container: /data/input/obs/raob

      * METAR:

        * Local: From data-matthew-input-obs.sif
        * Container: /data/input/obs/metar

      * Config directory containing METplus use case configuration file

        * Local: ${METPLUS_CONFIG_DIR}
        * Container: /config

      * Plot script directory containing WRF plotting scripts

        * Local: ${PLOT_SCRIPT_DIR}
        * Container: /plot_scripts

      * Output directory to write output

        * Local: ${METPLUS_DIR}
        * Container: /data/output

    * Apptainer temp directory

      * Local: ${APPTAINER_TMPDIR}
      * Container: ${APPTAINER_TMPDIR}

   ::

       export APPTAINER_BIND="${WORKING_DIR}/data-matthew-input-obs.sif:/data/input/obs:image-src=/,${METPLUS_CONFIG_DIR}:/config,${WRF_TOP_DIR}:/data/input/wrf,${METPLUS_DIR}:/data/output,${PLOT_SCRIPT_DIR}:/plot_scripts,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"

  .. dropdown:: Run METplus

    Execute the run_metplus.py command inside the container to run the use case::

        apptainer exec ${WORKING_DIR}/iwrf-metplus.sif /metplus/METplus/ush/run_metplus.py /config/PointStat_matthew.conf

    Check that the output data was created locally::

        ls -1  ${WORKING_DIR}/metplus_out/point_stat

