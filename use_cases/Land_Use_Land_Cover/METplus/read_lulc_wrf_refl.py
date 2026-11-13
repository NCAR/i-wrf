import sys
import os
import glob
from datetime import datetime

import numpy as np
import netCDF4 as nc

"""
Read composite radar reflectivity from WRF output for MET Python embedding.

MET cannot compute the maximum over the vertical levels of a 3D field, so
this script reads REFL_10CM from a wrfout file and returns the maximum value
in each column. This matches the NEXRAD composite reflectivity used as the
observations. It works on full, unmodified WRF output, so no pre-processing
of the WRF files is needed.

The grid definition is read from the WRF global attributes and the
initialization time from SIMULATION_START_DATE, matching how MET defines
them when it reads a wrfout file directly.
"""

VAR_NAME = 'REFL_10CM'
LEVEL = 'COLMAX'
WRF_TIME_FMT = '%Y-%m-%d_%H:%M:%S'


def usage():
    print(f"Usage: {os.path.basename(__file__)} wrf_dir domain valid_time")
    print('     wrf_dir = directory containing wrfout files')
    print('      domain = WRF domain, e.g. d03')
    print('  valid_time = time to read in YYYYMMDD_HHMM format')
    print(f'Example: {os.path.basename(__file__)} /data/input/wrf/dfw4x d03 20170704_0000')
    sys.exit(1)


def main():
    wrf_dir, domain, valid_time = read_inputs()

    try:
        valid_dt = datetime.strptime(valid_time, '%Y%m%d_%H%M')
    except ValueError:
        print(f'ERROR: Invalid valid time specified: {valid_time}')
        sys.exit(1)

    wrf_file = find_wrf_file(wrf_dir, domain, valid_dt)
    ds = nc.Dataset(wrf_file, 'r')

    init_dt = datetime.strptime(ds.getncattr('SIMULATION_START_DATE'), WRF_TIME_FMT)
    lead_seconds = int((valid_dt - init_dt).total_seconds())
    if lead_seconds < 0:
        print(f'ERROR: Valid time {valid_dt} is before simulation start {init_dt}')
        sys.exit(1)

    # REFL_10CM dimensions are (Time, bottom_top, south_north, west_east)
    refl = np.ma.filled(ds[VAR_NAME][0, :, :, :].astype(np.float64), np.nan)
    data = np.nanmax(refl, axis=0)

    # WRF row 0 is the southern edge, MET expects row 0 to be the northern edge
    met_data = data[::-1].copy()

    attrs = {
        'valid': valid_dt.strftime('%Y%m%d_%H%M%S'),
        'init':  init_dt.strftime('%Y%m%d_%H%M%S'),
        'lead':  sec_to_hhmmss(lead_seconds),
        'accum': '00',

        'name':      VAR_NAME,
        'long_name': 'composite radar reflectivity (column maximum of REFL_10CM)',
        'level':     LEVEL,
        'units':     ds[VAR_NAME].units,

        'grid': get_grid(ds, domain),
    }

    ds.close()
    return met_data, attrs


def find_wrf_file(wrf_dir, domain, valid_dt):
    pattern = os.path.join(wrf_dir, f"wrfout_{domain}_{valid_dt.strftime('%Y-%m-%d_%H:%M')}*")
    matches = sorted(glob.glob(pattern))
    if not matches:
        print(f'ERROR: No WRF file found matching {pattern}')
        sys.exit(1)
    if len(matches) > 1:
        print(f'WARNING: Multiple WRF files match {pattern}, using {matches[0]}')
    return matches[0]


def get_grid(ds, domain):
    """Build a MET Lambert Conformal grid from WRF global attributes."""
    map_proj = ds.getncattr('MAP_PROJ')
    if map_proj != 1:
        print(f'ERROR: Only Lambert Conformal (MAP_PROJ=1) is supported, found {map_proj}')
        sys.exit(1)

    nx = len(ds.dimensions['west_east'])
    ny = len(ds.dimensions['south_north'])
    truelat1 = float(ds.getncattr('TRUELAT1'))

    return {
        'name': f'WRF {domain}',
        'type': 'Lambert Conformal',
        'hemisphere': 'S' if truelat1 < 0 else 'N',
        'scale_lat_1': truelat1,
        'scale_lat_2': float(ds.getncattr('TRUELAT2')),
        'lat_pin': float(ds.getncattr('CEN_LAT')),
        'lon_pin': float(ds.getncattr('CEN_LON')),
        'x_pin': 0.5 * (nx - 1),
        'y_pin': 0.5 * (ny - 1),
        'lon_orient': float(ds.getncattr('STAND_LON')),
        'd_km': float(ds.getncattr('DX')) / 1000.0,
        'r_km': 6371.2,
        'nx': nx,
        'ny': ny,
    }


def sec_to_hhmmss(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f'{hours:02d}{minutes:02d}{secs:02d}'


def read_inputs():
    if len(sys.argv) != 4:
        print('ERROR: Invalid arguments')
        print(sys.argv)
        usage()
    return sys.argv[1], sys.argv[2], sys.argv[3]


met_data, attrs = main()
print(attrs)
print(met_data)
