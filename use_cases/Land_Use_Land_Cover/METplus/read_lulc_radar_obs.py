import sys
import os
import re
from datetime import datetime, timedelta

import netCDF4 as nc

"""
The NEXRAD products were processed by Dr. Fred Letson (fl368@cornell.edu):
  1) Precipitation rate, accumulated precipitation, and composite radar
     reflectivity are regridded onto WRF d02 and d03 domains.
  2) The time period and data frequency matches the WRF simulations that
     covers 36 hours start from the 12:00Z with a 10min frequency.
  3) Fields are stored in two files:
     RADAR_DFW22_N1P*: precipitation related fields
        NX_data  -> precipitation rate in the unit of {mm/h}
        NX_accum -> accumulated precipitation in the unit of {mm}
     RADAR_DFW22_NCR*: composite radar reflectivity
        NX_data  -> composite radar reflectivity (e.g., max radar ref in
                    a vertical column) in the unit of {dBZ}
"""

# 10 minute time interval in radar files
TIME_INTERVAL = timedelta(minutes=10)

def usage():
    print(f"Usage: {os.path.basename(__file__)} netcdf_file field valid_time")
    print('  netcdf_file = path to RADAR_DFW22_NCR/N1P input file')
    print('        field = name to read, e.g. rate, accum, or refl')
    print('   valid_time = time to read in YYYYMMDD_HHMM format')
    print('Note: refl is found in NCR file and rate/accum are found in N1P file')
    print(f'Example: {os.path.basename(__file__)} RADAR_DFW22_N1P_20170703_d03_2017Jul03_2017Jul05.nc rate 20170704_0000')
    print(f'Example: {os.path.basename(__file__)} RADAR_DFW22_N1P_20170703_d03_2017Jul03_2017Jul05.nc accum 20170704_0000')
    print(f'Example: {os.path.basename(__file__)} RADAR_DFW22_NCR_20170703_d03_2017Jul03_2017Jul05.nc refl 20170704_0000')
    sys.exit(1)

def main():
    nc_filename, field, valid_time = read_inputs()
    var_name, long_name, units = get_field_info(field, nc_filename)
    ds = nc.Dataset(nc_filename, 'r')

    try:
        valid_dt = datetime.strptime(valid_time, '%Y%m%d_%H%M')
    except ValueError:
        print(f'ERROR: Invalid valid time specified: {valid_time}')
        sys.exit(1)

    time_index = get_time_index(nc_filename, ds, valid_dt)
    if time_index is None:
        sys.exit(1)

    # get lat/lon info
    lat = ds['LAT'][:]
    lon = ds['LON'][:]

    # get data from field at time
    data = ds[var_name][time_index,:,:]

    # flip data vertically
    met_data = data[::-1].copy()

    nx = len(lon)
    ny = len(lat)

    # see https://dtcenter.org/sites/default/files/community-code/met/python-scripts/read_PostProcessed_WRF.py.txt

    attrs = {
       'valid': valid_dt.strftime("%Y%m%d_%H%M%S"),
       'init':  valid_dt.strftime("%Y%m%d_%H%M%S"),
       'lead':  '00',
       'accum': '00',

       'name':      field,
       'long_name': long_name,
       'level':     'Surface',
       'units':     units,

       'grid': {
           'name': 'WRF d03',
           'type': 'Lambert Conformal',
           'hemisphere': 'N',
           'scale_lat_1': 29.0,
           'scale_lat_2': 39.0,
           'lat_pin': 32.82182,
           'lon_pin': -96.96198,
           'x_pin': float(nx/2),
           'y_pin': float(ny/2),
           'lon_orient': -96.9781,
           'd_km': 1.0,
           'r_km': 6371.2,
           'nx': nx,
           'ny': ny,
       }
    }

    return met_data, attrs

def get_time_index(filename, ds, valid_dt):
    match = re.match(r'.*_(\d{8})_.*', os.path.basename(filename))
    if not match:
        print(f'ERROR: Could not parse YYYYMMDD from filename: {filename}')
        return None

    num_times = len(ds.variables['time'])
    start_dt = datetime.strptime(f"{match.group(1)}12", '%Y%m%d%H')
    time_index = int((valid_dt - start_dt) / TIME_INTERVAL)
    # check if valid time is out of range
    if time_index < 0 or time_index > num_times:
        print(f"ERROR: Could not compute time index. Must be between 0 and {num_times}."
              " Requested valid time is not in file.")
        return None

    return time_index

def read_inputs():
    if len(sys.argv) != 4:
        print('ERROR: Invalid arguments')
        print(sys.argv)
        usage()
    return sys.argv[1], sys.argv[2], sys.argv[3]

def get_field_info(field, nc_filename):
    if field == 'rate':
        var_name = 'NX_data'
        long_name = 'precipitation rate'
        units = 'mm/h'
    elif field == 'accum':
        var_name = 'NX_accum'
        long_name = 'accumulated precipitation'
        units = 'mm'
    elif field == 'refl':
        var_name = 'NX_data'
        long_name = 'composite radar reflectivity'
        units = 'dBZ'
    else:
        print(f'ERROR: Invalid field provided ({field}). Options are rate, accum, or refl')
        usage()

    # ensure NCR file is provided if requesting reflectivity
    if field == 'refl' and 'NCR' not in os.path.basename(nc_filename):
        print('ERROR: Reflectivity field requested from file without NCR in name')
        usage()

    return var_name, long_name, units


met_data, attrs = main()
print(attrs)
print(met_data)
