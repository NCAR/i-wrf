ARG METPLUS_TAG=6.0.0

FROM dtcenter/metplus-analysis:${METPLUS_TAG}

# install wrf python package from branch in PR NCAR/wrf-python#242
# because wrf will not install from pip
RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install git+https://github.com/DWesl/wrf-python.git@cmake-build \
  && python3 -m pip install cartopy
