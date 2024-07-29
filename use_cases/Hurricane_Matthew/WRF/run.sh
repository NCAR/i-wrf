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
  cd "${CYCLE_DIR}"
  link_gfs_vtable
  run_ungrib
  run_geogrid
  run_metgrid
  run_real
  run_wrf
}

function link_gfs_vtable
{
  ln -sf "${WPS_DIR}/ungrib/Variable_Tables/Vtable.GFS" Vtable
  ${WPS_DIR}/link_grib.csh "${CYCLE_DIR}/matthew/*.grib2"
}

function run_ungrib
{
  ln -s "${WPS_DIR}/ungrib.exe" . 2>/dev/null
  ./ungrib.exe
}

function run_geogrid
{
  ln -s "${WPS_DIR}"/* . 2>/dev/null
  ./geogrid.exe
}

function run_metgrid
{
  ./metgrid.exe
}

function run_real
{
  ln -s "${WRF_DIR}"/test/em_real/* . 2>/dev/null
  ./real.exe
}

function run_wrf
{
  ulimit -s unlimited
  ln -s "${WRF_DIR}"/test/em_real/* . 2>/dev/null
  mpirun ./wrf.exe
}

main
