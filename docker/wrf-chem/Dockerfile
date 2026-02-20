# WRF-Chem 4.7.1 + WPS 4.6.0 + Preprocessing Tools on AlmaLinux 9
#
# Docker equivalent of wrf-chem_full_almalinux9.def (single-layer Apptainer build).
# Uses multi-stage build to reduce final image size.
#
# Build:
#   docker build -t wrf-chem:4.7.1 .
#
# Run interactively:
#   docker run --rm -it wrf-chem:4.7.1
#
# Run WRF with MPI:
#   docker run --rm -it wrf-chem:4.7.1 mpirun -np 4 --allow-run-as-root wrf.exe

# ==============================================================================
# Stage 1: Build everything
# ==============================================================================
FROM almalinux:9 AS build

LABEL maintainer="V. Weeks"
LABEL description="WRF-Chem 4.7.1 with WPS 4.6.0, preprocessing tools, on AlmaLinux 9"
LABEL version="1.0"

# ---------- System packages ----------
RUN dnf -y update && \
    dnf -y install epel-release && \
    dnf config-manager --set-enabled crb && \
    dnf -y groupinstall "Development Tools" && \
    dnf -y install \
        gcc gcc-gfortran gcc-c++ \
        make cmake m4 perl csh tcsh git wget file which hostname rsync && \
    dnf -y install --allowerasing curl libcurl libcurl-devel time && \
    dnf -y install \
        openmpi openmpi-devel \
        jasper jasper-libs jasper-devel \
        libpng libpng-devel \
        zlib zlib-devel zlib-static \
        libxml2 libxml2-devel \
        flex libfl-static bison bison-devel bison-runtime byacc && \
    dnf -y install python3 python3-pip python3-devel && \
    pip3 install --upgrade pip && \
    pip3 install numpy pyyaml && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

# ---------- Environment for building ----------
ENV PATH="/usr/lib64/openmpi/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/lib64/openmpi/lib" \
    CC=gcc \
    FC=gfortran \
    F77=gfortran \
    F90=gfortran \
    CXX=g++ \
    MPICC=mpicc \
    MPIF90=mpif90

# ---------- Build HDF5 1.14.5 ----------
ARG HDF5_VERSION=1.14.5
ARG PREFIX=/opt/wrf-deps

RUN mkdir -p /tmp/build ${PREFIX} && \
    cd /tmp/build && \
    wget -q https://github.com/HDFGroup/hdf5/releases/download/hdf5_${HDF5_VERSION}/hdf5-${HDF5_VERSION}.tar.gz && \
    tar xzf hdf5-${HDF5_VERSION}.tar.gz && \
    cd hdf5-${HDF5_VERSION} && \
    ./configure \
        --prefix=${PREFIX} \
        --enable-fortran \
        --enable-shared \
        --enable-static \
        --enable-hl \
        --with-zlib && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/build

# ---------- Build NetCDF-C 4.9.3 ----------
ARG NETCDF_C_VERSION=4.9.3

ENV PATH="${PREFIX}/bin:${PATH}" \
    LD_LIBRARY_PATH="${PREFIX}/lib:${LD_LIBRARY_PATH}" \
    CPPFLAGS="-I${PREFIX}/include" \
    LDFLAGS="-L${PREFIX}/lib"

RUN mkdir -p /tmp/build && \
    cd /tmp/build && \
    wget -q https://downloads.unidata.ucar.edu/netcdf-c/${NETCDF_C_VERSION}/netcdf-c-${NETCDF_C_VERSION}.tar.gz && \
    tar xzf netcdf-c-${NETCDF_C_VERSION}.tar.gz && \
    cd netcdf-c-${NETCDF_C_VERSION} && \
    ./configure \
        --prefix=${PREFIX} \
        --enable-shared \
        --enable-static \
        --enable-netcdf-4 \
        --disable-dap && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/build

# ---------- Build NetCDF-Fortran 4.6.2 ----------
ARG NETCDF_FORTRAN_VERSION=4.6.2

RUN mkdir -p /tmp/build && \
    cd /tmp/build && \
    wget -q https://downloads.unidata.ucar.edu/netcdf-fortran/${NETCDF_FORTRAN_VERSION}/netcdf-fortran-${NETCDF_FORTRAN_VERSION}.tar.gz && \
    tar xzf netcdf-fortran-${NETCDF_FORTRAN_VERSION}.tar.gz && \
    cd netcdf-fortran-${NETCDF_FORTRAN_VERSION} && \
    ./configure \
        --prefix=${PREFIX} \
        --enable-shared \
        --enable-static && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/build

# ---------- WRF-Chem build environment ----------
ENV WRF_DEPS=/opt/wrf-deps \
    NETCDF=/opt/wrf-deps \
    NETCDF_DIR=/opt/wrf-deps \
    HDF5=/opt/wrf-deps \
    HDF5_DIR=/opt/wrf-deps \
    MPI_ROOT=/usr/lib64/openmpi \
    JASPERLIB=/usr/lib64 \
    JASPERINC=/usr/include/jasper \
    YACC="yacc -d" \
    FLEX_LIB_DIR=/usr/lib64 \
    WRF_CHEM=1 \
    WRF_KPP=1 \
    EM_CORE=1 \
    WRF_EM_CORE=1 \
    WRF_NMM_CORE=0 \
    WRFIO_NCD_LARGE_FILE_SUPPORT=1 \
    FCFLAGS="-fallow-argument-mismatch" \
    FFLAGS="-fallow-argument-mismatch" \
    F90FLAGS="-fallow-argument-mismatch"

# ---------- Build WRF-Chem Preprocessing Tools ----------
ARG WRF_CHEM_PREPROC=/opt/WRF-Chem-Preprocessing-Tools
ARG PREPROC_BIN=${WRF_CHEM_PREPROC}/bin

RUN cd /opt && \
    git clone https://github.com/NCAR/WRF-Chem-Preprocessing-Tools.git ${WRF_CHEM_PREPROC} && \
    mkdir -p ${PREPROC_BIN} && \
    GCC10_FLAG="-fallow-argument-mismatch" && \
    # Patch all Makefiles for GCC 10+ compatibility
    find "${WRF_CHEM_PREPROC}" -name "Makefile" -type f | while read makefile; do \
        sed -i "s/-ffree-line-length-none/-ffree-line-length-none $GCC10_FLAG/g" "$makefile" 2>/dev/null || true; \
        sed -i "s/FFLAGS = -g/FFLAGS = -g $GCC10_FLAG/g" "$makefile" 2>/dev/null || true; \
        sed -i "s/FFLAGS= -g/FFLAGS= -g $GCC10_FLAG/g" "$makefile" 2>/dev/null || true; \
        sed -i "s/F90FLAGS = /F90FLAGS = $GCC10_FLAG /g" "$makefile" 2>/dev/null || true; \
    done && \
    find "${WRF_CHEM_PREPROC}" -name "make_*" -type f | while read makescript; do \
        sed -i "s/-ffree-line-length-none/-ffree-line-length-none $GCC10_FLAG/g" "$makescript" 2>/dev/null || true; \
        sed -i "s/gfortran -g/gfortran -g $GCC10_FLAG/g" "$makescript" 2>/dev/null || true; \
        sed -i "s/gfortran -c/gfortran $GCC10_FLAG -c/g" "$makescript" 2>/dev/null || true; \
    done && \
    # Build mozbc
    cd ${WRF_CHEM_PREPROC}/mozbc && \
    rm -f *.o mozbc 2>/dev/null || true && \
    if [ -f make_mozbc ]; then csh ./make_mozbc && cp mozbc ${PREPROC_BIN}/; fi && \
    # Build anthro_emis
    cd ${WRF_CHEM_PREPROC}/anthro_emiss/src && \
    rm -f *.o anthro_emis 2>/dev/null || true && \
    if [ -f make_anthro ]; then csh ./make_anthro && cp anthro_emis ${PREPROC_BIN}/; fi && \
    # Build fire_emis
    cd ${WRF_CHEM_PREPROC}/fire_emiss/src && \
    rm -f *.o fire_emis 2>/dev/null || true && \
    if [ -f make_fire_emis ]; then csh ./make_fire_emis && cp fire_emis ${PREPROC_BIN}/; fi && \
    # Build megan_bio_emiss
    cd ${WRF_CHEM_PREPROC}/megan_bio_emiss && \
    rm -f *.o megan_bio_emiss 2>/dev/null || true && \
    if [ -f make_util ]; then csh ./make_util megan_bio_emiss && cp megan_bio_emiss ${PREPROC_BIN}/; fi && \
    # Build wesely
    cd ${WRF_CHEM_PREPROC}/wes_coldens && \
    rm -f *.o wesely 2>/dev/null || true && \
    if [ -f make_util ]; then csh ./make_util wesely && cp wesely ${PREPROC_BIN}/; fi && \
    # Build exo_coldens
    cd ${WRF_CHEM_PREPROC}/wes_coldens && \
    rm -f *.o exo_coldens 2>/dev/null || true && \
    if [ -f make_util ]; then csh ./make_util exo_coldens && cp exo_coldens ${PREPROC_BIN}/; fi

# ---------- Build WRF-Chem 4.7.1 ----------
ARG WRF_VERSION=4.7.1
ARG WRF_DIR=/opt/WRF
ARG WPS_DIR=/opt/WPS
ARG BIN_DIR=/wrf/bin

RUN mkdir -p ${WRF_DIR} ${WPS_DIR} ${BIN_DIR} /tmp/build && \
    echo "WRF_VERSION=${WRF_VERSION}" > ${WRF_DIR}/.version && \
    cd /tmp/build && \
    # IMPORTANT: Use release tarball, not "Source Code" (missing NoahMP submodule)
    wget -q https://github.com/wrf-model/WRF/releases/download/v${WRF_VERSION}/v${WRF_VERSION}.tar.gz && \
    tar xzf v${WRF_VERSION}.tar.gz && \
    ln -s WRFV${WRF_VERSION} WRF && \
    cd WRF && \
    ./clean -a 2>/dev/null || true && \
    # Configure WRF: option 34 = GNU dmpar, option 1 = basic nesting
    echo -e "34\n1" | ./configure 2>&1 | tee ${WRF_DIR}/configure_wrf.log && \
    # Patch configure.wrf for GCC 10+
    sed -i 's/FCOPTIM.*=.*/& -fallow-argument-mismatch/' configure.wrf && \
    sed -i 's/FCBASEOPTS_NO_G.*=.*/& -fallow-argument-mismatch/' configure.wrf && \
    # Fix WRF 4.7.1 KPP bugs
    sed -i 's|tuv_kpp FIRST ../../inc/|tuv_kpp FIRST ../../../../inc/|g' chem/KPP/compile_wkc && \
    sed -i 's|char openMode\[1\] = "a"|char openMode[2] = "a"|' chem/KPP/util/wkc/tuv_kpp.c && \
    # Compile WRF-Chem (J=1 or omit J for serial - REQUIRED for chem)
    ./compile em_real 2>&1 | tee ${WRF_DIR}/compile_wrf.log && \
    # Verify
    test -f main/wrf.exe && test -f main/real.exe && \
    # Install executables
    cp main/*.exe ${BIN_DIR}/ && \
    # Copy runtime files
    cp configure.wrf ${WRF_DIR} && \
    cp README* ${WRF_DIR} && \
    cp LICENSE.txt ${WRF_DIR} && \
    rsync -avL run ${WRF_DIR} --exclude "*.exe" && \
    rsync -av doc ${WRF_DIR} && \
    rsync -av Registry ${WRF_DIR}

# ---------- Build WPS 4.6.0 ----------
ARG WPS_VERSION=4.6.0

RUN cd /tmp/build && \
    echo "WPS_VERSION=${WPS_VERSION}" > ${WPS_DIR}/.version && \
    wget -q https://github.com/wrf-model/WPS/archive/refs/tags/v${WPS_VERSION}.tar.gz -O wps-v${WPS_VERSION}.tar.gz && \
    tar xzf wps-v${WPS_VERSION}.tar.gz && \
    cd WPS-${WPS_VERSION} && \
    # Configure WPS: option 3 = GNU dmpar
    echo "3" | ./configure 2>&1 | tee ${WPS_DIR}/configure_wps.log && \
    sed -i 's/FFLAGS.*=.*/& -fallow-argument-mismatch/' configure.wps && \
    ./compile 2>&1 | tee compile_wps.log && \
    # Verify
    test -f geogrid/src/geogrid.exe && \
    test -f ungrib/src/ungrib.exe && \
    test -f metgrid/src/metgrid.exe && \
    # Install executables
    cp geogrid/src/geogrid.exe ${BIN_DIR}/ && \
    cp ungrib/src/ungrib.exe ${BIN_DIR}/ && \
    cp metgrid/src/metgrid.exe ${BIN_DIR}/ && \
    cp link_grib.csh ${BIN_DIR}/ && \
    rsync -avL util ${BIN_DIR}/ --exclude "src" --exclude "CMakeLists.txt" --exclude "Makefile" --exclude ".gitignore" && \
    # Copy runtime files
    cp configure.wps ${WPS_DIR} && \
    cp namelist* ${WPS_DIR} && \
    cp README ${WPS_DIR} && \
    rsync -av geogrid ${WPS_DIR} --exclude "*.exe" --exclude "src" --exclude "util" --exclude "CMakeLists.txt" --exclude "Makefile" && \
    rsync -av metgrid ${WPS_DIR} --exclude "*.exe" --exclude "src" --exclude "CMakeLists.txt" --exclude "Makefile" && \
    rsync -av ungrib  ${WPS_DIR} --exclude "*.exe" --exclude "src" --exclude "CMakeLists.txt" --exclude "Makefile" --exclude ".gitignore" && \
    # Cleanup build artifacts
    cd / && \
    rm -rf /tmp/build

# ==============================================================================
# Stage 2: Runtime image (no build tools, smaller image)
# ==============================================================================
FROM almalinux:9

LABEL maintainer="V. Weeks"
LABEL description="WRF-Chem 4.7.1 with WPS 4.6.0, preprocessing tools, on AlmaLinux 9"
LABEL version="1.0"

# Install only runtime dependencies
RUN dnf -y update && \
    dnf -y install epel-release && \
    dnf config-manager --set-enabled crb && \
    dnf -y install \
        openmpi openmpi-devel \
        jasper-libs \
        libpng \
        zlib \
        libxml2 \
        libcurl \
        csh tcsh \
        file which hostname rsync time && \
    dnf -y install python3 python3-pip && \
    pip3 install numpy pyyaml && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

# Copy built artifacts from build stage
COPY --from=build /opt/wrf-deps /opt/wrf-deps
COPY --from=build /opt/WRF /opt/WRF
COPY --from=build /opt/WPS /opt/WPS
COPY --from=build /opt/WRF-Chem-Preprocessing-Tools /opt/WRF-Chem-Preprocessing-Tools
COPY --from=build /wrf/bin /wrf/bin

# Runtime environment
ENV LC_ALL=C \
    LANG=C \
    WRF_DEPS=/opt/wrf-deps \
    HDF5=/opt/wrf-deps \
    HDF5_DIR=/opt/wrf-deps \
    NETCDF=/opt/wrf-deps \
    NETCDF_DIR=/opt/wrf-deps \
    MPI_ROOT=/usr/lib64/openmpi \
    JASPERLIB=/usr/lib64 \
    JASPERINC=/usr/include/jasper \
    YACC="yacc -d" \
    FLEX_LIB_DIR=/usr/lib64 \
    WRF_DIR=/opt/WRF \
    WPS_DIR=/opt/WPS \
    WRF_CHEM_PREPROC=/opt/WRF-Chem-Preprocessing-Tools \
    WRF_CHEM=1 \
    WRF_KPP=1 \
    EM_CORE=1 \
    WRFIO_NCD_LARGE_FILE_SUPPORT=1

ENV PATH="/wrf/bin:/opt/WRF-Chem-Preprocessing-Tools/bin:/opt/wrf-deps/bin:/usr/lib64/openmpi/bin:${PATH}" \
    LD_LIBRARY_PATH="/opt/wrf-deps/lib:/usr/lib64/openmpi/lib"

WORKDIR /wrf

CMD ["/bin/bash", "-c", \
    "echo '========================================' && \
     echo 'WRF-Chem Container - AlmaLinux 9' && \
     echo '========================================' && \
     echo '' && \
     echo 'Versions:' && \
     echo '  WRF-Chem: 4.7.1' && \
     echo '  WPS: 4.6.0' && \
     echo '  HDF5: 1.14.5' && \
     echo '  NetCDF-C: 4.9.3' && \
     echo '  NetCDF-Fortran: 4.6.2' && \
     echo '' && \
     echo 'WRF Executables: wrf.exe, real.exe, ndown.exe, tc.exe' && \
     echo 'WPS Executables: geogrid.exe, ungrib.exe, metgrid.exe' && \
     echo 'Preprocessing: mozbc, anthro_emis, fire_emis, megan_bio_emiss, wesely, exo_coldens' && \
     echo '' && \
     echo 'Key directories:' && \
     echo '  WRF: /opt/WRF' && \
     echo '  WPS: /opt/WPS' && \
     echo '  Preprocessing: /opt/WRF-Chem-Preprocessing-Tools' && \
     echo '  Executables: /wrf/bin' && \
     exec /bin/bash"]
