#!/bin/bash

source /etc/bashrc
ulimit -s unlimited


cd /home/wrfuser/WPS
cp /home/wrfuser/input/namelist/WPS/namelist1.wps /home/wrfuser/WPS/namelist.wps
./geogrid.exe


cp /home/wrfuser/input/namelist/WPS/Vtable.hrrr.modified /home/wrfuser/WPS/ungrib/Variable_Tables/
ln -sf ./ungrib/Variable_Tables/Vtable.hrrr.modified Vtable
./link_grib.csh /home/wrfuser/input/HRRR/0703/hrrr.*.wrfprs
./ungrib.exe


cp /home/wrfuser/input/namelist/WPS/namelist2.wps /home/wrfuser/WPS/namelist.wps
./link_grib.csh /home/wrfuser/input/HRRR/0703/hrrr.*.wrfnat
./ungrib.exe

./metgrid.exe


cd /home/wrfuser/WRF
ln -sf /home/wrfuser/WRF/run/* .
cp /home/wrfuser/input/namelist/WRF/namelist.input .
cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d01.txt .
cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d02.txt .
cp /home/wrfuser/input/namelist/WRF/wrfvar_lulc_d03.txt .
ln -sf /home/wrfuser/WPS/met_em* .

./main/real.exe

mkdir wrfdata
mpiexec -n 60 -ppn 60 ./main/wrf.exe

mv -r wrfdata/* /home/wrfuser/output
