.. dropdown:: Define Environment Variables

  We will be using environment variables throughout this exercise to
  ensure consistent file paths and resource names across all commands.

  Define the following environment variables before proceeding::

      # HPC account key for job submissions — change to your own allocation if needed
      HPC_ACCOUNT=NERP0002

      # Container images
      WRF_IMAGE=ncar/iwrf:latest
      METPLUS_IMAGE=ncar/iwrf-metplus:latest

      # Working directories
      WRF_TOP_DIR=${WORKING_DIR}/wrf
      WRF_DATE_DIR=${WRF_TOP_DIR}/20250407_06
      METPLUS_DIR=${WORKING_DIR}/metplus_out

      # Renewable Energy use case configuration
      WRF_CONFIG_DIR=${WORKING_DIR}/i-wrf/use_cases/Renewable_Energy/WRF/config
      METPLUS_CONFIG_DIR=${WORKING_DIR}/i-wrf/use_cases/Renewable_Energy/METplus
      PLOT_SCRIPT_DIR=${WORKING_DIR}/i-wrf/use_cases/Renewable_Energy/Visualization

      # HRRR input data
      HRRR_DATA_DIR=${WORKING_DIR}/hrrr_data

      # Geographic data (WPS_GEOG) and auxiliary WPS files
      # On NSF NCAR HPC these are available on shared storage
      GEOG_DATA_DIR=/glade/work/wrfhelp/WPS_GEOG
      WPS_FILES_DIR=/glade/work/wrfhelp/WPS_files

  Any time you open a new shell on your HPC system, you will need to redefine
  these variables before executing the commands that follow.

  .. note::

    ``NERP0002`` is the NSF NCAR project account used for this demo.
    Replace it with your own account ID if you are running on a different
    allocation on Derecho/Casper.
