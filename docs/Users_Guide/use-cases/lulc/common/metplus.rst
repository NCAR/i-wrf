
.. dropdown:: Run METplus

  .. dropdown:: Define Environment Variables for METplus

     Set environment variables to define paths and Docker image names::

         METPLUS_IMAGE=ncar/iwrf-metplus:latest
         OBS_DATA_VOL=lulc-input-obs-d03
         OBS_DATA_IMAGE=ncar/iwrf-data:${OBS_DATA_VOL}.docker
         WRF_CTL_DATA_VOL=lulc-input-wrf-ctl-d03
         WRF_CTL_DATA_IMAGE=ncar/iwrf-data:${WRF_CTL_DATA_VOL}.docker
         WRF_DFW4X_DATA_VOL=lulc-input-wrf-dfw4x-d03
         WRF_DFW4X_DATA_IMAGE=ncar/iwrf-data:${WRF_DFW4X_DATA_VOL}.docker
         METPLUS_OUTPUT=~/metplus_out
         METPLUS_CONFIG_DIR=~/i-wrf/use_cases/Land_Use_Land_Cover/METplus
         PLOT_SCRIPT_DIR=~/i-wrf/use_cases/Land_Use_Land_Cover/Visualization

  .. dropdown:: Get METplus Docker Images

     The METplus software and observation data are both available on DockerHub.
     Run commands to pull the images and create the Docker data volume::

         sudo docker pull ${METPLUS_IMAGE}
         sudo docker pull ${OBS_DATA_IMAGE}
         sudo docker create --name ${OBS_DATA_VOL} ${OBS_DATA_IMAGE}

  .. dropdown:: Choose the WRF Data

     The WRF plotting script reads the output of both the Control and DFW 4x simulations,
     and the METplus verification reads the output of the DFW 4x simulation.
     Output of each simulation is available on DockerHub,
     so any simulation that was not run in the previous steps can be obtained from there.
     Set the **WRF_INPUT_ARGS** environment variable using the approach
     that matches the simulations that were run.

     If both simulations were run, use the output in the ``ctl`` and ``dfw4x``
     directories of the output directory::

         WRF_INPUT_ARGS="-v ${WRF_OUTPUT}:/data/input/wrf"

     If only the Control simulation was run, pull the DFW 4x image
     and create a Docker data volume from it::

         sudo docker pull ${WRF_DFW4X_DATA_IMAGE}
         sudo docker create --name ${WRF_DFW4X_DATA_VOL} ${WRF_DFW4X_DATA_IMAGE}

     Then use the Control output from the output directory
     and the DFW 4x output from the data volume::

         WRF_INPUT_ARGS="-v ${WRF_OUTPUT}/ctl:/data/input/wrf/ctl --volumes-from ${WRF_DFW4X_DATA_VOL}"

     If only the DFW 4x simulation was run, pull the Control image
     and create a Docker data volume from it::

         sudo docker pull ${WRF_CTL_DATA_IMAGE}
         sudo docker create --name ${WRF_CTL_DATA_VOL} ${WRF_CTL_DATA_IMAGE}

     Then use the DFW 4x output from the output directory
     and the Control output from the data volume::

         WRF_INPUT_ARGS="-v ${WRF_OUTPUT}/dfw4x:/data/input/wrf/dfw4x --volumes-from ${WRF_CTL_DATA_VOL}"

     If neither simulation was run, pull both images
     and create a Docker data volume from each::

         sudo docker pull ${WRF_CTL_DATA_IMAGE}
         sudo docker create --name ${WRF_CTL_DATA_VOL} ${WRF_CTL_DATA_IMAGE}
         sudo docker pull ${WRF_DFW4X_DATA_IMAGE}
         sudo docker create --name ${WRF_DFW4X_DATA_VOL} ${WRF_DFW4X_DATA_IMAGE}

     Then use the output of both simulations from the data volumes::

         WRF_INPUT_ARGS="--volumes-from ${WRF_CTL_DATA_VOL} --volumes-from ${WRF_DFW4X_DATA_VOL}"

     .. note::

        The output on the full output Ceph share in ``~/lulc_full_output``
        (see **View Full WRF Output**) can also be used as input
        in place of one of the data volumes.
        To do so, mount it with ``-v`` at ``/data/input/wrf/ctl`` or
        ``/data/input/wrf/dfw4x``, depending on the simulation it contains.

  .. dropdown:: Run METplus Verification

    The LULC use case includes verification for two meteorological variables:
    accumulated precipitation and radar reflectivity.
    Each verification is run separately using its own METplus configuration file.
    Run the accumulated precipitation verification::

        docker run --rm -it \
          --volumes-from ${OBS_DATA_VOL} \
          ${WRF_INPUT_ARGS} \
          -v ${METPLUS_CONFIG_DIR}:/config \
          -v ${PLOT_SCRIPT_DIR}:/plot_scripts \
          -v ${METPLUS_OUTPUT}:/data/output ${METPLUS_IMAGE} \
          /metplus/METplus/ush/run_metplus.py /config/GridStat_apcp_lulc.conf

    Run the reflectivity verification::

        docker run --rm -it \
          --volumes-from ${OBS_DATA_VOL} \
          ${WRF_INPUT_ARGS} \
          -v ${METPLUS_CONFIG_DIR}:/config \
          -v ${PLOT_SCRIPT_DIR}:/plot_scripts \
          -v ${METPLUS_OUTPUT}:/data/output ${METPLUS_IMAGE} \
          /metplus/METplus/ush/run_metplus.py /config/GridStat_refc_lulc.conf

    Both verification processes use GridStat, which computes grid-to-grid verification statistics.
    The METplus configuration files verify the DFW 4x simulation.

  .. dropdown:: Plot the WRF Output

    The WRF plotting script creates maps that compare the Control and DFW 4x simulations
    side by side with the NEXRAD observations.
    Run the WRF plotting script::

        docker run --rm -it \
          --volumes-from ${OBS_DATA_VOL} \
          ${WRF_INPUT_ARGS} \
          -v ${PLOT_SCRIPT_DIR}:/plot_scripts \
          -v ${METPLUS_OUTPUT}:/data/output ${METPLUS_IMAGE} \
          python3 /plot_scripts/plot_wrf_lulc.py \
          --wrf_dir_parent /data/input/wrf \
          --out_dir_parent /data/output/wrf_plot \
          --nexrad_dir /data/input/obs

    By default, the script plots each hour from 00:00 on July 4 to 00:00 on July 5,
    which requires output from the full simulation.
    If WRF was run manually and the output ends at 15:00 on July 3,
    add the following arguments to the end of the command
    to plot each hour from 13:00 to 15:00 on July 3 instead::

        --beg_lead_time 01:00 --end_lead_time 03:00
