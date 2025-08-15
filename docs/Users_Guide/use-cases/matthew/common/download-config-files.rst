.. dropdown:: Download Configuration Files

  Both WRF and METplus require some configuration files to direct their behavior,
  and those are downloaded from the I-WRF GitHub repository.
  Some of those configuration files are then copied into the run folders.
  These commands perform the necessary operations::

      git clone https://github.com/NCAR/i-wrf ${WORKING_DIR}/i-wrf
      cp ${WRF_CONFIG_DIR}/namelist.* ${WRF_DATE_DIR}
      cp ${WRF_CONFIG_DIR}/vars_io.txt ${WRF_DATE_DIR}
      cp ${WRF_CONFIG_DIR}/run.sh ${WRF_DATE_DIR}
