
.. dropdown:: Run METplus

   .. dropdown:: Define Environment Variables for METplus

      Set environment variables to define paths and Docker image names::

          METPLUS_IMAGE=ncar/iwrf-metplus:latest
          OBS_DATA_VOL=lulc-input-obs-d03
          OBS_DATA_IMAGE=ncar/iwrf-data:${OBS_DATA_VOL}.docker
          METPLUS_OUTPUT=~/metplus_out
          METPLUS_CONFIG_DIR=~/i-wrf/use_cases/Land_Use_Land_Cover/METplus
          PLOT_SCRIPT_DIR=~/i-wrf/use_cases/Land_Use_Land_Cover/Visualization

      The path to the WRF data to be read into METplus depends on how WRF was
      run in the previous steps.
      Set the **WRF_TOP_DIR** environment variable using one of the following approaches:

      If the Control simulation was run, set::

         WRF_TOP_DIR=${WRF_OUTPUT}/ctl

      If the DFW 4x simulation was run, set::

         WRF_TOP_DIR=${WRF_OUTPUT}/dfw4x

      If the WRF simulation was not run and the output was obtained via Ceph, set::

         WRF_TOP_DIR=~/lulc_full_output


   .. dropdown:: Get METplus Docker Images

      The METplus software and observation data are both available on DockerHub.
      Run commands to pull the images and create the Docker data volume::

          sudo docker pull ${METPLUS_IMAGE}
          sudo docker pull ${OBS_DATA_IMAGE}
          sudo docker create --name ${OBS_DATA_VOL} ${OBS_DATA_IMAGE}

  .. dropdown:: Run METplus

    The LULC use case includes verification for two meteorological variables:
    accumulated precipitation and radar reflectivity.
    Each verification is run separately using its own METplus configuration file.
    Run the accumulated precipitation verification::

        docker run --rm -it \
          --volumes-from ${OBS_DATA_VOL} \
          -v ${METPLUS_CONFIG_DIR}:/config \
          -v ${PLOT_SCRIPT_DIR}:/plot_scripts \
          -v ${WRF_TOP_DIR}:/data/input/wrf \
          -v ${METPLUS_OUTPUT}:/data/output ${METPLUS_IMAGE} \
          /metplus/METplus/ush/run_metplus.py /config/GridStat_apcp_lulc.conf

    Run the reflectivity verification::

        docker run --rm -it \
          --volumes-from ${OBS_DATA_VOL} \
          -v ${METPLUS_CONFIG_DIR}:/config \
          -v ${PLOT_SCRIPT_DIR}:/plot_scripts \
          -v ${WRF_TOP_DIR}:/data/input/wrf \
          -v ${METPLUS_OUTPUT}:/data/output ${METPLUS_IMAGE} \
          /metplus/METplus/ush/run_metplus.py /config/GridStat_refc_lulc.conf

  .. dropdown:: View the Plotted Simulation Results

     The METplus container plots the results of the simulation, outputting them as PNG images.
