.. dropdown:: Download HRRR Data for WRF

  WRF is initialized and forced at the boundaries using HRRR GRIB2 files
  downloaded from the NOAA AWS archive.  Run the download script from the
  login node before requesting a compute node, since downloading does not
  require compute resources.

  .. note::

    The download script requires Python with the ``wget``, ``numpy``, and
    ``pandas`` packages.  On NSF NCAR HPC systems, load the ``npl`` conda
    environment::

        module load conda
        conda activate npl

  Download 49 hourly HRRR pressure-level files (f00 through f48) for the
  simulation period::

      python ${WORKING_DIR}/i-wrf/download_hrrr_from_aws_or_gc.py \
        -b 20250407_06 \
        -s 48 \
        -i 1 \
        -o ${HRRR_DATA_DIR} \
        -c AWS

  Files will be placed under ``${HRRR_DATA_DIR}/hrrr.20250407/conus/`` with
  names like ``hrrr.t06z.wrfprsf00.grib2``, ``hrrr.t06z.wrfprsf01.grib2``, etc.

  .. note::

    The ``-i 1`` flag downloads one file per hour to match the
    ``interval_seconds = 3600`` setting in ``namelist.wps``.
    Omitting it uses the default of 3-hourly files, which will cause
    WPS to fail.

  .. note::

    To download from Google Cloud instead of AWS, replace ``-c AWS``
    with ``-c GoogleCloud``.
