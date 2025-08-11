*************
Configuration
*************

Default Datasets and Namelists
==============================
---------------------------
Hurricane Matthew Test Case
---------------------------
^^^^^^^^^^^^
WPS Namelist
^^^^^^^^^^^^
Use this in the namelist.wps file when running WPS for the Hurricane Matthew case, from the Github repository:

https://github.com/NCAR/i-wrf/blob/main/use_cases/Hurricane_Matthew/WRF/namelist.wps

Note that you will need to update geog_data_path, opt_geogrid_tbl_path, and opt_metgrid_tbl_path for your machine/environment to point to locations of the WPS_GEOG dataset, GEOGRID.TBL, and METGRID.TBL files, respectively. WPS_GEOG is a large static dataset of geographic data that is required for geogrid.exe to run (see: https://www2.mmm.ucar.edu/wrf/OnLineTutorial/Basics/GEOGRID/ter_data.php). GEOGRID.TBL and METGRID.TBL are typically found in the geogrid/ and metgrid/ directories inside the WPS installation directory.::

  &share
   wrf_core = 'ARW',
   max_dom = 1,
   start_date = '2016-10-06_00:00:00','2019-09-04_12:00:00',
   end_date   = '2016-10-08_00:00:00','2019-09-04_12:00:00',
   interval_seconds = 21600,
  /

  &geogrid
   parent_id         =   1,   1,
   parent_grid_ratio =   1,   3,
   i_parent_start    =   1,  53,
   j_parent_start    =   1,  25,
   e_we              =  91, 220,
   e_sn              = 100, 214,
   geog_data_res = 'default','default',
   dx = 27000,
   dy = 27000,
   map_proj = 'mercator',
   ref_lat   =  28.00,
   ref_lon   = -75.00,
   truelat1  =  30.0,
   truelat2  =  60.0,
   stand_lon = -75.0,
   geog_data_path = '/glade/work/wrfhelp/WPS_GEOG/'
   opt_geogrid_tbl_path = '/glade/u/home/jaredlee/programs/WPS-4.5-serial-intel/geogrid/',
  /

  &ungrib
   out_format = 'WPS',
   prefix = 'FILE',
  /

  &metgrid
   fg_name = 'FILE'
   opt_metgrid_tbl_path = '/glade/u/home/jaredlee/programs/WPS-4.5-serial-intel/metgrid/',
  /

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
WRF Namelist and Other Config Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use this namelist.input file when running WRF for the Hurricane Matthew case, from the Github repository:

https://github.com/NCAR/i-wrf/blob/main/use_cases/Hurricane_Matthew/WRF/namelist.input

Note that the iofields_filename variable points to a file called vars_io.txt. This file adds or removes WRF variables from various output (history) streams (stream 0 is the default history stream). Note also that the auxhist22* and auxhist23* variables are specified for the height-level and pressure-level diagnostics, respectively. The levels at which to write out those height-level and pressure-level diagnostics are specified in the &diags namelist, and vars_io.txt also changes which variables are written to these files from the default settings for streams 22 and 23. METplus expects to find the wrfout_plev* files in order to do upper-air verification against radiosonde observations at mandatory pressure levels.

Use this for the vars_io.txt file for the Hurricane Matthew case, from the Github repository:

https://github.com/NCAR/i-wrf/blob/main/use_cases/Hurricane_Matthew/WRF/vars_io.txt

^^^^^^^^^^^^^^^^^^^
METplus Config File
^^^^^^^^^^^^^^^^^^^
For the METplus configuration file for the Hurricane Matthew case, please use this file on the Github repository:
https://github.com/NCAR/i-wrf/blob/main/use_cases/Hurricane_Matthew/METplus/PointStat_matthew.conf


---------------------------------
Land Usage/Land Cover Change Case
---------------------------------

The WPS namelist, WRF namelist, METplus configurations, and other configurations can all be found here:

https://github.com/NCAR/i-wrf/tree/main/use_cases/Land_Use_Land_Cover
