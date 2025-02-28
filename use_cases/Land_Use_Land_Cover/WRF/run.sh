#!/usr/bin/env bash


source /etc/bashrc
ulimit -s unlimited


WPS=/home/wrfuser/WPS
WRF=/home/wrfuser/WRF
LULC_OUTPUT=/home/wrfuser/lulc_output
LULC_WPS_INPUT=/home/wrfuser/lulc_input/WPS_input
LULC_WRF_INPUT=/home/wrfuser/lulc_input/WRF_input


cd $WPS
cp $LULC_WPS_INPUT/namelist/namelist_PRS.wps $WPS/namelist.wps
ln -fs $LULC_WPS_INPUT/WPS_GEOG $WPS
./geogrid.exe


cd $WPS
cp $LULC_WPS_INPUT/namelist/Vtable.hrrr.modified $WPS/ungrib/Variable_Tables/
ln -sf $WPS/ungrib/Variable_Tables/Vtable.hrrr.modified $WPS/Vtable
./link_grib.csh $LULC_WPS_INPUT/HRRR_0703/hrrr.*.wrfprs
./ungrib.exe


cd $WPS
cp $LULC_WPS_INPUT/namelist/namelist_NAT.wps $WPS/namelist.wps
./link_grib.csh $LULC_WPS_INPUT/HRRR_0703/hrrr.*.wrfnat
./ungrib.exe


cd $WPS
./metgrid.exe



cd $WRF
ln -sf $WRF/run/* $WRF
cp $LULC_WRF_INPUT/namelist/namelist.input $WRF
cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d01.txt $WRF
cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d02.txt $WRF
cp $LULC_WRF_INPUT/ctl/wrfvar_lulc_d03.txt $WRF
ln -sf $WPS/met_em* $WRF


cd $WRF
./main/real.exe


cd $WRF
mkdir $WRF/wrfdata
mpiexec -n 60 -ppn 60 ./main/wrf.exe


mv $WRF/wrfdata $LULC_OUTPUT/ctl


cd $WRF
rm met_em*
rm wrfbdy_d01
rm wrfinput*


ln -sf $WRF/run/* $WRF
ln -sf $LULC_WRF_INPUT/dfw4x/wrfbdy_d01 $WRF
ln -sf $LULC_WRF_INPUT/dfw4x/wrfinput* $WRF
ln -sf $LULC_WRF_INPUT/dfw4x/met_em* $WRF


cd $WRF
mkdir $WRF/wrfdata
mpiexec -n 60 -ppn 60 ./main/wrf.exe


mv $WRF/wrfdata $LULC_OUTPUT/dfw4x
