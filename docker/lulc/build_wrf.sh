#! /bin/bash

# Make sure we have a value for a username. This should already be set
# in the /etc/bashrc, but use this default just in case it is not found.
if [[ -z "${WRFUSER}" ]]; then
  WRFUSER="wrfuser"
fi

# Build zlib
source /etc/bashrc
cd /opt/src
tar -xzf zlib-1.2.11.tar.gz
cd /opt/src/zlib-1.2.11
./configure --prefix=/opt/zlib 2>&1 | tee configure.log
make -j 4 install 2>&1 | tee build.log
echo 'export ZLIB=/opt/zlib' >> /etc/bashrc
echo 'export LD_LIBRARY_PATH=${ZLIB}/lib:${LD_LIBRARY_PATH}' >> /etc/bashrc

# Build szip
source /etc/bashrc
cd /opt/src
tar -xzf szip-2.1.1.tar.gz
cd /opt/src/szip-2.1.1
./configure --prefix=/opt/szip 2>&1 | tee configure.log
make -j 4 install 2>&1 | tee build.log
echo 'export SZIP=/opt/szip' >> /etc/bashrc
echo 'export LD_LIBRARY_PATH=${SZIP}/lib:${LD_LIBRARY_PATH}' >> /etc/bashrc

# Build HDF5
source /etc/bashrc
cd /opt/src
tar -xzf hdf5-1.10.10.tar.gz
cd /opt/src/hdf5-1.10.10
./configure --prefix=/opt/hdf5 --enable-parallel --enable-fortran --with-zlib=${ZLIB} --with-szlib=${SZIP} 2>&1 | tee configure.log
make -j 4 install 2>&1 | tee build.log
echo 'export HDF5=/opt/hdf5' | tee -a /etc/bashrc
echo 'export PATH=${HDF5}/bin:${PATH}' | tee -a /etc/bashrc
echo 'export LD_LIBRARY_PATH=${HDF5}/lib:${LD_LIBRARY_PATH}' | tee -a /etc/bashrc

# Build NetCDF
source /etc/bashrc
cd /opt/src
tar -xzf netcdf-4.7.3.tar.gz
cd netcdf-c-4.7.3
export CPPFLAGS="-I${HDF5}/include -I${SZIP}/include -I${ZLIB}/include"
export LDFLAGS="-L${HDF5}/lib -L${SZIP}/lib -L${ZLIB}/lib"
./configure --prefix=/opt/netcdf --disable-dap-remote-tests --enable-mmap --enable-netcdf4 2>&1 | tee configure.log
make -j 4 install 2>&1 | tee build.log
echo 'export NETCDF=/opt/netcdf' | tee -a /etc/bashrc
echo 'export PATH=${NETCDF}/bin:${PATH}' | tee -a /etc/bashrc
echo 'export LD_LIBRARY_PATH=${NETCDF}/lib:${LD_LIBRARY_PATH}' | tee -a /etc/bashrc

# Build NetCDF Fortran libraries
source /etc/bashrc
cd /opt/src
tar -xzf netcdf-fortran-4.5.2.tar.gz
cd netcdf-fortran-4.5.2
export CPPFLAGS="-I${HDF5}/include -I${SZIP}/include -I${NETCDF}/include"
export LDFLAGS="-L${HDF5}/lib -L${SZIP}/lib -L${NETCDF}/lib"
./configure --prefix=/opt/netcdf 2>&1 | tee configure.log
make install 2>&1 | tee build.log

# Build NetCDF C++ libraries
source /etc/bashrc
cd /opt/src
tar -xzf netcdf-cxx-4.3.1.tar.gz
cd netcdf-cxx4-4.3.1
export CPPFLAGS="-I${HDF5}/include -I${SZIP}/include -I${NETCDF}/include"
export LDFLAGS="-L${HDF5}/lib -L${SZIP}/lib -L${NETCDF}/lib"
./configure --prefix=/opt/netcdf 2>&1 | tee configure.log
make install 2>&1 | tee build.log

# Build libpng
source /etc/bashrc
cd /opt/src
tar -xzf libpng-1.2.50.tar.gz
cd libpng-1.2.50
export CPPFLAGS="-I${ZLIB}/include"
export LDFLAGS="-L${ZLIB}/lib"
./configure --prefix=/opt/libpng 2>&1 | tee configure.log
make -j 4 install 2>&1 | tee build.log
echo 'export LIBPNG=/opt/libpng' | tee -a /etc/bashrc
echo 'export PATH=${LIBPNG}/bin:${PATH}' | tee -a /etc/bashrc
echo 'export LD_LIBRARY_PATH=${LIBPNG}/lib:${LD_LIBRARY_PATH}' | tee -a /etc/bashrc

# Build jasper
source /etc/bashrc
cd /opt/src
tar -xzf jasper-1.900.29-iwrf-mods.tar.gz
cd jasper-1.900.29-iwrf-mods
./configure --prefix=/opt/jasper 2>&1 | tee configure.log
make -j 4 install 2>&1 | tee build.log
echo 'export JASPER=/opt/jasper' | tee -a /etc/bashrc
echo 'export PATH=${JASPER}/bin:${PATH}' | tee -a /etc/bashrc
echo 'export LD_LIBRARY_PATH=${JASPER}/lib:${LD_LIBRARY_PATH}' | tee -a /etc/bashrc

# Build g2clib
source /etc/bashrc
mkdir -p /opt/src
cd /opt/src
tar -xzf g2clib-1.6.0-patch.tar.gz
cd g2clib-1.6.0-patch
cat makefile | sed "s/INC=.*/INC=-I\/opt\/jasper\/include -I\/opt\/libpng\/include -I\/opt\/zlib\/include/g" > makefile2
make -f makefile2 2>&1 | tee build.log
mkdir -p /opt/g2clib/lib
cp -f libgrib2c.a /opt/g2clib/lib
echo 'export G2C=/opt/g2clib' | tee -a /etc/bashrc
echo 'export LD_LIBRARY_PATH=${G2C}/lib:${LD_LIBRARY_PATH}' | tee -a /etc/bashrc

# Build udunits
source /etc/bashrc
mkdir -p /opt/src
cd /opt/src
tar -xzf udunits-2.2.28.tar.gz
cd udunits-2.2.28
./configure --prefix=/opt/udunits 2>&1 | tee configure.log
make -j 4 install 2>&1 | tee build.log
echo 'export UDUNITS=/opt/udunits' | tee -a /etc/bashrc
echo 'export PATH=${UDUNITS}/bin:${PATH}' | tee -a /etc/bashrc
echo 'export LD_LIBRARY_PATH=${UDUNITS}/lib:${LD_LIBRARY_PATH}' | tee -a /etc/bashrc

# Build WRF
source /etc/bashrc
mkdir -p /home/${WRFUSER}
cd /home/${WRFUSER}
git clone https://github.com/wrf-model/WRF
cd WRF
git checkout v4.3.3  # v4.5.2 is latest
# TODO: configure complains that NetCDF was built without --enable-netcdf4, however, that flag is set in the NetCDF build.  This was only a problem with WRF v4.5.  Solution: export NETCDF_classic=1
./clean
./configure << EOF
15
1
EOF
cat configure.wrf | sed "s/-lz/-lz -L\/opt\/zlib\/lib/g" > configure.wrf.zlib
mv -f configure.wrf.zlib configure.wrf
./compile em_real 2>&1 | tee build.log
cd /home/${WRFUSER}
chown -R ${WRFUSER}.${WRFUSER} WRF

# Build WPS
source /etc/bashrc
cd /home/${WRFUSER}
git clone https://github.com/wrf-model/WPS
cd WPS
git checkout v4.4
export JASPERLIB="-L${SZIP}/lib -L${LIBPNG}/lib -L${ZLIB}/lib -L${JASPER}/lib -L${G2C}/lib -ljasper -lpng -lz -lgrib2c"
export JASPERINC="-I${SZIP}/include -I${LIBPNG}/include -I${ZLIB}/include -I${JASPER}/include"
export FCFLAGS="${FCFLAGS} ${JASPERINC}"
./clean
./configure << EOF
19
EOF
cd ..
tar -xvzf /opt/src/WPS-v4.4-iwrf-patch.tar.gz
cd WPS
./compile 2>&1 | tee build.log
cd /home/${WRFUSER}
chown -R ${WRFUSER}.${WRFUSER} WPS
