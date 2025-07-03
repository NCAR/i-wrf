
Download Configuration Files
============================

Both WPS and WRF require some configuration files to direct their behavior, and those are downloaded from the I-WRF GitHub repository. Those configuration files are then copied into a folder. These commands perform the necessary operations::

    git clone https://github.com/NCAR/i-wrf ~/i-wrf
    cp -r ~/i-wrf/use_cases/Land_Use_Land_Cover ~/lulc_configs
    chmod 777 ~/lulc_configs/run_full.sh
    