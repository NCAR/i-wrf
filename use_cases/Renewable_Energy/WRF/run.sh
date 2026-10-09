#! /bin/bash

source /etc/bashrc

CYCLE_DIR="/tmp/renewable_energy"
WPS_DIR="/home/wrfuser/WPS"
WRF_DIR="/home/wrfuser/WRF"

function main
{
  mkdir -p "${CYCLE_DIR}"
  cd "${CYCLE_DIR}"
  run_geogrid
  link_hrrr_grib
  run_ungrib
  run_avg_tsfc
  run_metgrid
  run_real
  run_wrf
}

function run_geogrid
{
  ln -s "${WPS_DIR}"/* . 2>/dev/null
  ./geogrid.exe
}

function link_hrrr_grib
{
  ln -sf "/tmp/renewable_energy/config/Vtable.raphrrr.pres" Vtable
  ${WPS_DIR}/link_grib.csh /tmp/hrrr_data/hrrr.*/conus/*.grib2
}

function run_ungrib
{
  ln -s "${WPS_DIR}/ungrib.exe" . 2>/dev/null
  ./ungrib.exe
}

function run_avg_tsfc
{
  ln -s "${WPS_DIR}/util/avg_tsfc.exe" . 2>/dev/null
  ./avg_tsfc.exe
}

function run_metgrid
{
  ln -s "${WPS_DIR}/metgrid.exe" . 2>/dev/null
  ./metgrid.exe
}

function run_real
{
  ln -s "${WRF_DIR}"/test/em_real/* . 2>/dev/null
  cp "${CYCLE_DIR}/config/namelist.input.hrrr" namelist.input
  local nprocs=$(( ${PBS_NP:-4} < 4 ? ${PBS_NP:-4} : 4 ))
  mpirun -n ${nprocs} ./real.exe
}

function run_wrf
{
  ulimit -s unlimited
  ln -s "${WRF_DIR}"/test/em_real/* . 2>/dev/null
  mpirun ./wrf.exe
}

main
