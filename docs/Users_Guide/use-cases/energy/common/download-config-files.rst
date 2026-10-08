.. dropdown:: Download Configuration Files

  Both WRF and METplus require configuration files to direct their behavior.
  The commands below clone the I-WRF repository and copy the Renewable Energy
  use case configuration files into the WRF run folder.

  Clone the I-WRF repository::

      git clone https://github.com/NCAR/i-wrf ${WORKING_DIR}/i-wrf

  Copy the WRF configuration files and run script::

      cp ${WRF_CONFIG_DIR}/namelist.wps.hrrr ${WRF_DATE_DIR}/namelist.wps
      cp ${WRF_CONFIG_DIR}/namelist.input.hrrr ${WRF_DATE_DIR}/namelist.input
      cp ${WRF_CONFIG_DIR}/iofields.txt ${WRF_DATE_DIR}/iofields.txt
      cp ${WORKING_DIR}/i-wrf/use_cases/Renewable_Energy/WRF/run.sh ${WRF_DATE_DIR}/run.sh
      chmod +x ${WRF_DATE_DIR}/run.sh

  .. note::

    The template namelists have a ``.hrrr`` suffix indicating they are configured
    for HRRR initial and boundary conditions.  They are copied without the suffix
    because that is the filename WPS and WRF expect.
