#!/usr/bin/env bash


source /etc/bashrc
ulimit -s unlimited


WPS_DIR=/home/wrfuser/WPS
WRF_DIR=/home/wrfuser/WRF
WPS_INPUT=/home/wrfuser/lulc_input/WPS_input
WRF_INPUT=/home/wrfuser/lulc_input/WRF_input
CONFIGS=/home/wrfuser/lulc_configs
OUTPUT=/home/wrfuser/lulc_output


cd $WPS_DIR
cp ${CONFIGS}/WPS/namelist/namelist_geogrid_full.wps ${WPS_DIR}/namelist.wps
ln -fs ${WPS_INPUT}/WPS_GEOG $WPS_DIR
./geogrid.exe


cd $WPS_DIR
cp ${CONFIGS}/WPS/namelist/namelist_ungrib_prs_full.wps ${WPS_DIR}/namelist.wps
cp ${CONFIGS}/WPS/Vtable/Vtable.hrrr.modified ${WPS_DIR}/ungrib/Variable_Tables/
ln -sf ${WPS_DIR}/ungrib/Variable_Tables/Vtable.hrrr.modified ${WPS_DIR}/Vtable
./link_grib.csh ${WPS_INPUT}/HRRR_0703_full/hrrr.*.wrfprs
./ungrib.exe


cd $WPS_DIR
cp ${CONFIGS}/WPS/namelist/namelist_ungrib_nat_full.wps ${WPS_DIR}/namelist.wps
./link_grib.csh ${WPS_INPUT}/HRRR_0703_full/hrrr.*.wrfnat
./ungrib.exe


cd $WPS_DIR
cp ${CONFIGS}/WPS/namelist/namelist_metgrid_full.wps ${WPS_DIR}/namelist.wps
./metgrid.exe


cd $WRF_DIR
ln -sf ${WRF_DIR}/run/* $WRF_DIR
cp ${CONFIGS}/WRF/namelist/namelist_full.input ${WRF_DIR}/namelist.input
cp ${CONFIGS}/WRF/ctl/wrfvar_lulc_*.txt $WRF_DIR
ln -sf ${WPS_DIR}/met_em* $WRF_DIR


cd $WRF_DIR
./main/real.exe


cd $WRF_DIR
mkdir -p ${WRF_DIR}/wrfdata
mpiexec -n 60 -ppn 60 ./main/wrf.exe


mv ${WRF_DIR}/wrfdata ${OUTPUT}/ctl


cd $WRF_DIR
rm met_em*
rm wrfbdy_d01
rm wrfinput*


ln -sf ${WRF_DIR}/run/* $WRF_DIR
ln -sf ${WRF_INPUT}/dfw4x_full/wrfbdy_d01 $WRF_DIR
ln -sf ${WRF_INPUT}/dfw4x_full/wrfinput* $WRF_DIR
ln -sf ${WRF_INPUT}/dfw4x_full/met_em* $WRF_DIR


cd $WRF_DIR
mkdir -p ${WRF_DIR}/wrfdata
mpiexec -n 60 -ppn 60 ./main/wrf.exe


mv ${WRF_DIR}/wrfdata ${OUTPUT}/dfw4x
