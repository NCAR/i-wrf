.. dropdown:: Download Data for WRF

  To run WRF on the Hurricane Matthew data set, you need to have
  several data sets to support the computation.
  The commands in these sections download archive files containing that data,
  then uncompress the archives into folders.
  The geographic data is large and takes several minutes to acquire,
  while the other two data sets are smaller and are downloaded directly into the WRF run folder,
  rather than the user's home directory.

  Get the geographic data representing the terrain in the area of the simulation::

      wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz -O ${WORKING_DIR}/geog_high_res_mandatory.tar.gz
      tar -xvzf ${WORKING_DIR}/geog_high_res_mandatory.tar.gz -C ${WORKING_DIR}
      rm -f ${WORKING_DIR}/geog_high_res_mandatory.tar.gz

  Get the case study data (GRIB2 files)::

      wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_1deg.tar.gz -O ${WRF_DATE_DIR}/matthew_1deg.tar.gz
      tar -xvzf ${WRF_DATE_DIR}/matthew_1deg.tar.gz -C ${WRF_DATE_DIR}
      rm -f ${WRF_DATE_DIR}/matthew_1deg.tar.gz

  Get the SST (Sea Surface Temperature) data::

      wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_sst.tar.gz -O ${WRF_DATE_DIR}/matthew_sst.tar.gz
      tar -xzvf ${WRF_DATE_DIR}/matthew_sst.tar.gz -C ${WRF_DATE_DIR}
      rm -f ${WRF_DATE_DIR}/matthew_sst.tar.gz
