.. dropdown:: Define Environment Variables

  We will be using some environment variables throughout this exercise to
  make sure that we refer to the same resource names and file paths wherever they are used.
  Copy and paste the definitions below into your shell to define the variables before proceeding::

      WRF_IMAGE=ncar/iwrf:latest
      METPLUS_IMAGE=ncar/iwrf-metplus:latest
      WRF_TOP_DIR=${WORKING_DIR}/wrf
      WRF_DATE_DIR=${WRF_TOP_DIR}/20161006_00
      METPLUS_DIR=${WORKING_DIR}/metplus_out
      WRF_CONFIG_DIR=${WORKING_DIR}/i-wrf/use_cases/Hurricane_Matthew/WRF
      METPLUS_CONFIG_DIR=${WORKING_DIR}/i-wrf/use_cases/Hurricane_Matthew/METplus
      PLOT_SCRIPT_DIR=${WORKING_DIR}/i-wrf/use_cases/Hurricane_Matthew/Visualization
      OBS_DATA_VOL=matthew-input-obs

  Any time you open a new shell on your instance, you will need to perform this action
  to redefine the variables before executing the commands that follow.