#! /bin/bash

# script adapted from instructions at https://www2.mmm.ucar.edu/wrf/OnLineTutorial/CASES/SingleDomain/ungrib.php
# docker run -it -v /home/hahn/git:/home/wrfuser/git -v /mnt/storage/terrestrial_data:/home/wrfuser/terrestrial_data iwrf:latest /bin/bash

source /etc/bashrc

CYCLE_DIR="/tmp/hurricane_matthew"
WPS_DIR="/home/wrfuser/WPS"
WRF_DIR="/home/wrfuser/WRF"

function main
{
  mkdir -p "${CYCLE_DIR}"
  download_case_study_data
  link_gfs_vtable
  modify_namelist_wps
  run_ungrib
  download_sst_data
  run_geogrid
  run_metgrid
  modify_namelist_wrf
  run_real
  run_wrf
}


function download_case_study_data
{
  cd "${CYCLE_DIR}"
  wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_1deg.tar.gz
  tar -xvzf matthew_1deg.tar.gz
  rm -f matthew_1deg.tar.gz
}


function link_gfs_vtable
{
  cd "${CYCLE_DIR}"
  ln -sf "${WPS_DIR}/ungrib/Variable_Tables/Vtable.GFS" Vtable
  ${WPS_DIR}/link_grib.csh "${CYCLE_DIR}/matthew/*.grib2"
}


function modify_namelist_wps
{
  cd "${CYCLE_DIR}"
  cp "${WPS_DIR}/namelist.wps" .

  _snr namelist.wps "max_dom.*," "max_dom = 1,"
  _snr namelist.wps "start_date = .*," "start_date = '2016-10-06_00:00:00',"
  _snr namelist.wps "end_date .*= .*," "end_date = '2016-10-08_00:00:00',"
  _snr namelist.wps "interval_seconds = .*" "interval_seconds = 21600"
  _snr namelist.wps "prefix = .*," "prefix = 'FILE',"
}


function run_ungrib
{
  cd "${CYCLE_DIR}"
  ln -s "${WPS_DIR}/ungrib.exe" .
  ./ungrib.exe
}


function download_sst_data
{
  cd "${CYCLE_DIR}"
  wget https://www2.mmm.ucar.edu/wrf/TUTORIAL_DATA/matthew_sst.tar.gz
  tar -xzvf matthew_sst.tar.gz
  rm -f matthew_sst.tar.gz
}


function run_geogrid
{
  cd "${CYCLE_DIR}"

  _snr namelist.wps "parent_id.*," "parent_id = 1,"
  _snr namelist.wps "parent_grid_ratio.*," "parent_grid_ratio = 1,"
  _snr namelist.wps "i_parent_start.*," "i_parent_start = 1,"
  _snr namelist.wps "i_parent_end.*," "i_parent_end = 1,"
  _snr namelist.wps "e_we.*," "e_we = 91,"
  _snr namelist.wps "e_sn.*," "e_sn = 100,"
  _snr namelist.wps "geog_data_res.*," "geog_data_res = 'default',"
  _snr namelist.wps "dx.*," "dx = 27000,"
  _snr namelist.wps "dy.*," "dy = 27000,"
  _snr namelist.wps "map_proj.*," "map_proj = 'mercator',"
  _snr namelist.wps "ref_lat.*," "ref_lat = 28.00,"
  _snr namelist.wps "ref_lon.*," "ref_lon = -75.00,"
  _snr namelist.wps "truelat1.*," "truelat1 = 30.0,"
  _snr namelist.wps "truelat2.*," "truelat2 = 60.0,"
  _snr namelist.wps "stand_lon.*," "stand_lon = -75.0,"
  _snr namelist.wps "geog_data_path.*" "geog_data_path = '\/home\/wrfuser\/terrestrial_data\/WPS_GEOG'"

  ln -s "${WPS_DIR}"/* .
  ./geogrid.exe
}


function run_metgrid
{
  cd "${CYCLE_DIR}"
  ./metgrid.exe
}


function modify_namelist_wrf
{
  cd "${CYCLE_DIR}"
  cp "${WRF_DIR}/test/em_real/namelist.input" .

  _snr namelist.input "run_days .*," "run_days = 0,"
  _snr namelist.input "run_hours .*," "run_hours = 48,"
  _snr namelist.input "run_minutes .*," "run_minutes = 0,"
  _snr namelist.input "run_seconds .*," "run_seconds = 0,"
  _snr namelist.input "start_year .*," "start_year = 2016,"
  _snr namelist.input "start_month .*," "start_month = 10,"
  _snr namelist.input "start_day .*," "start_day = 06,"
  _snr namelist.input "start_hour .*," "start_hour = 00,"
  _snr namelist.input "end_year .*," "end_year = 2016,"
  _snr namelist.input "end_month .*," "end_month = 10,"
  _snr namelist.input "end_day .*," "end_day = 08,"
  _snr namelist.input "end_hour .*," "end_hour = 00,"
  _snr namelist.input "interval_seconds .*" "interval_seconds = 21600"
  _snr namelist.input "input_from_file .*," "input_from_file = .true.,"
  _snr namelist.input "history_interval .*," "history_interval = 180,"
  _snr namelist.input "frames_per_outfile .*," "frames_per_outfile = 1,"
  _snr namelist.input "restart .*," "restart = .false.,"
  _snr namelist.input "restart_interval .*," "restart_interval = 1440,"
  _snr namelist.input "time_step .*," "time_step = 150,"
  _snr namelist.input "max_dom .*," "max_dom = 1,"
  _snr namelist.input "e_we .*," "e_we = 91,"
  _snr namelist.input "e_sn .*," "e_sn = 100,"
  _snr namelist.input "e_vert .*," "e_vert = 45,"
  _snr namelist.input "num_metgrid_levels .*" "num_metgrid_levels = 32"
  _snr namelist.input "dx .*," "dx = 27000,"
  _snr namelist.input "dy .*," "dy = 27000,"
}


function run_real
{
  cd "${CYCLE_DIR}"
  ln -s "${WRF_DIR}"/test/em_real/* .
  ./real.exe
}


function run_wrf
{
  ulimit -s unlimited
  cd "${CYCLE_DIR}"
  ln -s "${WRF_DIR}"/test/em_real/* .
  ./wrf.exe
}


function _snr
{
  file="${1}"
  search="${2}"
  replace="${3}"
  temp_file="$(mktemp)"

  cat "${file}" | sed "s/${search}/${replace}/g" > "${temp_file}"
  mv -f "${temp_file}" "${file}"
  rm -f "${temp_file}"
}


main
