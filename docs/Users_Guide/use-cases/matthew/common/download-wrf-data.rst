.. dropdown:: Download Data for WRF

  To run WRF on the Hurricane Matthew data set, you need to have
  several data sets to support the computation.
  The commands in these sections download archive files containing that data,
  then uncompress the archives into folders.
  The geographic data is large and takes several minutes to acquire,
  while the other two data sets are smaller and are downloaded directly into the WRF run folder,
  rather than the user's home directory.

  Get the geographic data representing the terrain in the area of the simulation::

      cd ${WORKING_DIR}
      wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
      tar -xzf geog_high_res_mandatory.tar.gz
      rm geog_high_res_mandatory.tar.gz

  Get the case study data (GRIB2 files)::

      cd ${WRF_DIR}
      wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_1deg.tar.gz
      tar -xvzf matthew_1deg.tar.gz
      rm -f matthew_1deg.tar.gz

  Get the SST (Sea Surface Temperature) data::

      cd ${WRF_DIR}
      wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_sst.tar.gz
      tar -xzvf matthew_sst.tar.gz
      rm -f matthew_sst.tar.gz
