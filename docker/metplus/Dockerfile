ARG METPLUS_TAG=6.0.0

FROM dtcenter/metplus-analysis:${METPLUS_TAG}

# NCAR/wrf-python commit: 69fd6a458ab60b417f1696d163ac7e9ab8363a69
RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install git+https://github.com/NCAR/wrf-python.git@develop \
  && python3 -m pip install cartopy
