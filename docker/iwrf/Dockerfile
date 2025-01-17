# Cornell uses ubuntu 22.04
FROM ubuntu:22.04 as wrfbuild

# Update the OS
RUN apt -y update
RUN apt -y upgrade

# Install compilers
RUN apt -y install cmake pkg-config build-essential wget libcurl4-openssl-dev m4
RUN wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor > /usr/share/keyrings/oneapi-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" > /etc/apt/sources.list.d/oneAPI.list
RUN apt -y update
RUN apt -y install intel-oneapi-compiler-fortran-2023.1.0 intel-oneapi-dpcpp-cpp-2023.1.0 intel-oneapi-mpi-2021.9.0 intel-oneapi-mpi-devel-2021.9.0
RUN apt -y --fix-broken install
RUN apt -y update

# Install other required packages
RUN apt -y install libexpat1 libexpat1-dev expat git csh file

# Install packages used for debugging
RUN apt -y install vim

# Add system user
RUN useradd -u 5000 wrfuser

# Configure bash
RUN echo 'source /etc/bash.bashrc' >> /etc/bashrc
RUN echo 'export MPI="/opt/intel/oneapi/mpi/latest"' >> /etc/bashrc
RUN echo 'export OPENMPI="${MPI}"' >> /etc/bashrc
RUN echo 'export INTEL="/opt/intel/oneapi/compiler/latest/linux"' >> /etc/bashrc
RUN echo 'export PATH="${INTEL}/bin/intel64:${MPI}/bin:${PATH}"' >> /etc/bashrc
RUN echo 'export SCC="icx"' >> /etc/bashrc
RUN echo 'export SFC="ifx"' >> /etc/bashrc
RUN echo 'export I_MPI_CC="icx"' >> /etc/bashrc
RUN echo 'export I_MPI_CXX="icpx"' >> /etc/bashrc
RUN echo 'export I_MPI_FC="ifx"' >> /etc/bashrc
RUN echo 'export I_MPI_F90="ifx"' >> /etc/bashrc
RUN echo 'export FC="mpifc"' >> /etc/bashrc
RUN echo 'export F90="mpifc"' >> /etc/bashrc
RUN echo 'export F77="mpifc"' >> /etc/bashrc
RUN echo 'export CC="mpicc"' >> /etc/bashrc
RUN echo 'export CXX="mpicxx"' >> /etc/bashrc
RUN echo 'export CPP="${CC} -E"' >> /etc/bashrc
RUN echo 'export CC_FOR_BUILD="${CC}"' >> /etc/bashrc
RUN echo 'export CPP_FOR_BUILD="${CPP}"' >> /etc/bashrc
RUN echo 'export CXXCPP="${CXX} -E"' >> /etc/bashrc
RUN echo 'export ABI="64"' >> /etc/bashrc
RUN echo 'export FCFLAGS="-I${MPI}/include"' >> /etc/bashrc
RUN echo 'export CFLAGS="-I${MPI}/include"' >> /etc/bashrc
RUN echo 'export LDFLAGS="-L${MPI}/lib -L${MPI}/lib/release"' >> /etc/bashrc
RUN echo 'export LD_LIBRARY_PATH="${MPI}/lib/release:${MPI}/lib"' >> /etc/bashrc
RUN echo 'source /opt/intel/oneapi/setvars.sh --force > /dev/null' >> /etc/bashrc
RUN echo 'export PATH="/opt/intel/oneapi/mpi/latest/bin:${PATH}"' >> /etc/bashrc
RUN echo 'export WRFUSER="wrfuser"' >> /etc/bashrc
# TODO: This is not taking effect for the stack, we had to manually run: 'ulimit -s unlimited'
RUN echo '*    hard    stack    unlimited' >> /etc/security/limits.conf
RUN echo '*    soft    stack    unlimited' >> /etc/security/limits.conf

# Download source
RUN mkdir -p /opt/src
WORKDIR /opt/src
RUN wget https://www.wrfcloud.com/libs/cmake-3.25.0-rc3.tar.gz
RUN wget https://www.wrfcloud.com/libs/eccodes-2.27.0.tar.gz
RUN wget https://www.wrfcloud.com/libs/g2clib-1.6.0-patch.tar.gz
RUN wget https://www.wrfcloud.com/libs/jasper-1.900.1.tar.gz
RUN wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.10/src/hdf5-1.10.10.tar.gz
RUN wget https://www.wrfcloud.com/libs/libaec-v1.0.6.tar.gz
RUN wget https://www.wrfcloud.com/libs/libpng-1.2.50.tar.gz
RUN wget https://www.wrfcloud.com/libs/ncview-2.1.7.tar.gz
RUN wget https://www.wrfcloud.com/libs/netcdf-4.7.3.tar.gz
RUN wget https://www.wrfcloud.com/libs/netcdf-cxx-4.3.1.tar.gz
RUN wget https://www.wrfcloud.com/libs/netcdf-fortran-4.5.2.tar.gz
RUN wget https://www.wrfcloud.com/libs/szip-2.1.1.tar.gz
RUN wget https://www.wrfcloud.com/libs/zlib-1.2.11.tar.gz
RUN wget https://downloads.unidata.ucar.edu/udunits/2.2.28/udunits-2.2.28.tar.gz

#COPY WPS.patch /tmp/WPS.patch
COPY build_wrf.sh /tmp/build_wrf.sh
RUN bash /tmp/build_wrf.sh


FROM ubuntu:22.04

# Update the OS
RUN apt -y update
RUN apt -y upgrade

COPY --from=wrfbuild /home/wrfuser /home/wrfuser
COPY --from=wrfbuild /opt/hdf5 /opt/hdf5
COPY --from=wrfbuild /opt/jasper /opt/jasper
COPY --from=wrfbuild /opt/libpng /opt/libpng
COPY --from=wrfbuild /opt/netcdf /opt/netcdf
COPY --from=wrfbuild /opt/szip /opt/szip
COPY --from=wrfbuild /opt/udunits /opt/udunits
COPY --from=wrfbuild /opt/zlib /opt/zlib
COPY --from=wrfbuild /etc/bashrc /etc/bashrc

# Install required runtime packages
# Note: To get a list of Intel OneAPI runtime packages, run the following:
#     apt-cache pkgnames intel | grep intel-oneapi-runtime
RUN apt -y install cmake pkg-config build-essential wget libcurl4-openssl-dev m4 csh
RUN wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor > /usr/share/keyrings/oneapi-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" > /etc/apt/sources.list.d/oneAPI.list
RUN apt -y update
RUN apt -y install intel-oneapi-runtime-mpi-2021 intel-oneapi-common-vars intel-oneapi-compiler-shared-runtime-2023.1.0 intel-oneapi-compiler-fortran-runtime-2023.1.0

WORKDIR /home/wrfuser
