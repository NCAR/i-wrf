.. _matthew-jetstream2:

On Jetstream2
^^^^^^^^^^^^^
  
Follow the compute platform instructions for :ref:`compute-platform-jetstream2`
to secure access to and log in to a Jetstream2 instance.
  
The following sections instruct you to issue numerous Linux commands in your shell.
If you are not familiar with Linux, you may want to want to refer to
`An Introduction to Linux <https://cvw.cac.cornell.edu/Linux>`_ when working through these steps.
The commands in each section can be copied using the button in the upper right corner
and then pasted into your web shell by right-clicking.

.. dropdown:: Instructions
  
  .. dropdown:: Instance Configuration
    
    .. _jetstream2_instance_configuration:

    Make the following choices when creating your instance:
      
      * When choosing an image as the instance source, if viewing "By Type", select the "Ubuntu 22.04" image.  If viewing "By Image", choose the "Featured-Ubuntu22" image.
      * Choose the "Flavor" m3.quad (4 CPUs) to provide a faster simulation run-time.
      * Select a custom disk size of 100 GB, which is large enough to hold this exercise's data and results.
      * For "Enable web desktop?", select Yes.
      * For "Choose an SSH public key", select None unless you want to use your own SSH key that you uploaded previously.
      * You do not need to set any of the Advanced Options.

  .. dropdown:: Define Working Directory

    Set an environment variable called **WORKING_DIR** to a directory to
    store all of the input and output files for the use case::

      WORKING_DIR=/home/exouser

  .. include:: matthew/common/set-env-vars.rst

  .. dropdown:: Create the WRF and METplus Run Folders
  
    The simulation is performed using a script that expects to run in a folder where it can create result files.
    The first command below creates a folder (named "wrf") under the user's home directory,
    and a sub-folder within "wrf" to hold the output of this simulation.
    The subfolder is named "20161006_00", which is the beginning date and time of the simulation.
    Similarly, a run folder named "metplus_out" must be created for the METplus process to use::
  
        mkdir -p ${WRF_DATE_DIR}
        mkdir -p ${METPLUS_DIR}

  .. include:: matthew/common/download-config-files.rst
  
  .. dropdown:: Pull Docker Objects
  
    As mentioned above, the WRF and METplus software are provided as Docker images that will run as a
    `"container" <https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/>`_
    on your cloud instance.
    To run a Docker container, the Docker Engine must be installed on your instance.
    You can then "pull" (download) the WRF and METplus images that will be run as containers.
    The Ubuntu instance you created already has the Docker Engine installed and running.
  
    To get the WRF and METplus Docker Images and the observed weather data,
    you must pull the correct versions of the WRF and METplus images onto your instance::
  
        docker pull ${WRF_IMAGE}
        docker pull ${METPLUS_IMAGE}
  
    METplus is run to perform verification of the results of the WRF simulation
    against observations gathered during Hurricane Matthew.
    We download that observation data by pulling a Docker volume that holds it,
    and then referencing that volume when we run the METplus Docker container.
    The commands to pull and create the volume are::
  
        docker pull ncar/iwrf-data:${OBS_DATA_VOL}.docker
        docker create --name ${OBS_DATA_VOL} ncar/iwrf-data:${OBS_DATA_VOL}.docker

  .. include:: matthew/common/download-wrf-data.rst

  .. dropdown:: Run WRF
  
    With everything in place, you are now ready to run the Docker container that will perform the simulation.
    The downloaded script runs inside the container, prints lots of status information,
    and creates output files in the run folder you created.
    Execute this command to run the simulation in your shell::
  
        docker run --shm-size 14G -it \
          -v ${WORKING_DIR}:/home/wrfuser/terrestrial_data \
          -v ${WRF_DATE_DIR}:/tmp/hurricane_matthew \
          ${WRF_IMAGE} /tmp/hurricane_matthew/run.sh
  
    The command has numerous arguments and options, which do the following:
  
    * ``docker run`` creates the container if needed and then runs it.
    * ``--shm-size 14G -it`` tells the command how much shared memory to use, and to run interactively in the shell.
    * The ``-v`` options map folders in your cloud instance to paths within the container.
    * ``ncar/iwrf:latest`` is the Docker image to use when creating the container.
    * ``/tmp/hurricane_matthew/run.sh`` is the location within the container of the script that it runs.
  
    The simulation initially prints lots of information while initializing things, then settles in to the computation.
    The provided configuration simulates 48 hours of weather and takes about 12 minutes to finish on an m3.quad Jetstream2 instance.
    Once completed, you can view the end of an output file to confirm that it succeeded::
  
        tail ${WRF_DATE_DIR}/rsl.out.0000
  
    The output should look something like this::
  
        Timing for main: time 2016-10-07_23:50:00 on domain 1: 0.25548 elapsed seconds
        Timing for main: time 2016-10-07_23:52:30 on domain 1: 0.25495 elapsed seconds
        Timing for main: time 2016-10-07_23:55:00 on domain 1: 0.25066 elapsed seconds
        Timing for main: time 2016-10-07_23:57:30 on domain 1: 0.25231 elapsed seconds
        Timing for main: time 2016-10-08_00:00:00 on domain 1: 0.25795 elapsed seconds
        Timing for Writing wrfout_d01_2016-10-08_00:00:00 for domain 1: 0.68666 elapsed seconds
        Timing for Writing wrfout_zlev_d01_2016-10-08_00:00:00 for domain 1: 0.47411 elapsed seconds
        Timing for Writing wrfout_plev_d01_2016-10-08_00:00:00 for domain 1: 0.47619 elapsed seconds
        Timing for Writing restart for domain 1: 1.54598 elapsed seconds
        d01 2016-10-08_00:00:00 wrf: SUCCESS COMPLETE WRF
  
  .. dropdown:: Run METplus
  
    After the WRF simulation has finished, you can run the METplus verification to compare the simulated results
    to the actual weather observations during the hurricane and generate plots of the simulation.
    This process takes about nine minutes to complete.
    We use command line options to tell the METplus container several things,
    including where the observed data is located,
    where the METplus configuration can be found,
    where the plotting scripts can be found,
    where the WRF output data is located,
    and where it should create its output files::
  
        docker run --rm -it \
          --volumes-from ${OBS_DATA_VOL} \
          -v ${METPLUS_CONFIG_DIR}:/config \
          -v ${PLOT_SCRIPT_DIR}:/plot_scripts \
          -v ${WRF_TOP_DIR}:/data/input/wrf \
          -v ${METPLUS_DIR}:/data/output ${METPLUS_IMAGE} \
          /metplus/METplus/ush/run_metplus.py /config/PointStat_matthew.conf
  
    Progress information is displayed while the verification is performed.
    **WARNING** log messages are expected because observations files are not available for every valid time and METplus is
    configured to allow some missing inputs. An **ERROR** log message indicates that something went wrong.
    METplus first converts the observation data files to a format that the MET tools can read using the MADIS2NC wrapper.
    Point-Stat is run to generate statistics comparing METAR observations to surface-level model fields and
    RAOB observations to "upper air" fields.
    METplus will print its completion status when the processing finishes.
  
    The results of the METplus verification can be found in ``${WORKING_DIR}/metplus_out/point_stat``.
    These files contain tabular output that can be viewed in a text editor. Turn off word wrapping for better viewing.
    Refer to the MET User's Guide for more information about the
    `Point-Stat output <https://met.readthedocs.io/en/latest/Users_Guide/point-stat.html#point-stat-output>`_.
  
  .. dropdown:: View the Plotted Simulation Results
  
    The METplus container also plots the results of the simulation, outputting them as PNG images.
    To view these images:
  
    * Find the desktop shortcut "Files" on the left side of the desktop and click it to open a file browser.
    * Double-click on the following folders in order: metplus_out, wrf, 20161006_00, then plots.
    * Double-click on the first image in the folder, which opens an image viewing application.
    * Click the Maximize button in the upper right to increase the viewer to full size.
    * Click the button in the middle of the right side of the image to advance to the next image.
    * Image legends are shown at the bottom and timeframes are shown in the upper right.
    * Each of the six plot sequences contains 16 or 17 images.
  
  When you are finished running simulations and viewing their results,
  you can close the web browser tab containing your Web Desktop.
  Then, return to the Exosphere dashboard to manage your instance so it does not incur further charges.
  
Refer back to the **Managing a Jetstream2 Instance** section of the :ref:`compute-platform-jetstream2`
instructions to avoid unneccessary computing costs.
