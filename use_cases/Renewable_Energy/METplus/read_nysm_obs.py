import sys
import argparse
from argparse import Namespace
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np
import xarray as xr

VALID_DATA_TYPES = (
    'profiler',
    'standard',
)

STATION_TABLE_COLUMN_RENAME = {
    'stid': 'station',
    'lat [degrees]': 'latitude',
    'lon [degrees]': 'longitude',
    'elevation [m]': 'elevation',
}

LOCATION_VARS = ["latitude", "longitude", "elevation"]

# MET 11-column format
# (1) typ  - string:  Message_Type ('ADPSFC')
# (2) sid  - string:  Station_ID (AIRPORT)
# (3) vld  - string:  Valid_Time(YYYYMMDD_HHMMSS)
# (4) lat  - numeric: Lat(Deg North)
# (5) lon  - numeric: Lon(Deg East)
# (6) elv  - numeric: Elevation(msl)
# (7) var  - string:  Var_Name(or GRIB_Code)
# (8) lvl  - numeric: Level
# (9) hgt  - numeric: Height(msl or agl)
# (10) qc  - string:  QC_String
# (11) obs - numeric: Observation_Value

MET_COLUMN_ORDER = ['typ', 'sid', 'vld', 'lat', 'lon', 'elv', 'var', 'lvl', 'hgt', 'qc', 'obs']

def main():
    args = read_args()
    ds = xr.open_dataset(args.data_file)

    # check if requested field is in the dataset
    if args.field_name not in ds.variables:
        print(f'ERROR: Field {args.field_name} not found in dataset')
        xr.close_dataset(ds)
        sys.exit(1)

    # set message type to surface for standard or upper air for profiler
    message_type = 'ADPSFC' if 'range' not in ds.variables else 'ADPUPA'

    # check if dataset has location information included in the file
    has_location_info = all(var in ds.variables for var in LOCATION_VARS)
    if not has_location_info:
        if not args.station_file:
            print('ERROR: Dataset does not have location information and no station file was provided')
            sys.exit(1)

        ds = add_location_from_station_file(args, ds)

    # set location variables as coordinates
    ds = ds.set_coords(LOCATION_VARS)
    df = ds[args.field_name].to_dataframe().reset_index()

    return dataframe_to_met_format(args, df, message_type)

def dataframe_to_met_format(args: Namespace, df, message_type: str) -> Any:
    print_debug(args.debug, df)
    print_debug(args.debug, "Removing rows with NaN values")
    df.dropna(inplace=True)
    print_debug(args.debug, df)

    print_debug(args.debug, "Reformat and add columns to match MET format")
    df['typ'] = message_type
    df['lvl'] = 0
    df['hgt'] = 0
    df['qc'] = 'NYSM'
    df.rename(columns={
        'station': 'sid',
        'time': 'vld',
        args.field_name: 'obs',
        'latitude': 'lat',
        'longitude': 'lon',
        'elevation': 'elv'
    }, inplace=True)
    df['vld'] = df['vld'].dt.strftime('%Y%m%d_%H%M%S')
    df['var'] = args.field_name

    # reorder to match expected MET format
    df = df[MET_COLUMN_ORDER]
    print(df)

    return df.values.tolist()

def print_debug(debug, content):
    if debug:
        print(content)

def add_location_from_station_file(args: Namespace, ds) -> Any:
    station_df = read_station_file(args.station_file)
    latitudes = []
    longitudes = []

    # remove PROF_ from the profiler station names and set the location info from the station file
    for station_name in ds.station.values:
        if station_name in station_df.index:
            latitudes.append(station_df.loc[station_name, "latitude"])
            longitudes.append(station_df.loc[station_name, "longitude"])
        else:
            # warn and add NaN values if station not found in station file
            print(f'WARNING: Station {station_name} not found in station lookup file.')
            latitudes.append(np.nan)
            longitudes.append(np.nan)

    ds["latitude"] = ("station", latitudes)
    ds["longitude"] = ("station", longitudes)

    # rename range to elevation for consistency
    ds = ds.rename({"range": "elevation"})
    return ds


def read_args():
    # read arguments: station CSV file, data file, [profiler/standard]
    argparser = argparse.ArgumentParser()
    argparser.add_argument('data_file', help='Data file to read')
    argparser.add_argument('field_name', help='Field name to read')
    argparser.add_argument('--station_file', required=False, help='Station CSV file to get lat/lon if needed')
    argparser.add_argument('--debug', action="store_true", help='Print debug messages')
    args = argparser.parse_args()

    # check that arguments are correct

    if not Path(args.data_file).exists():
        print(f'ERROR: Data file does not exist: {args.data_file}')
        sys.exit(1)

    if args.station_file and not Path(args.station_file).exists():
        print(f'ERROR: Station file does not exist: {args.station_file}')
        sys.exit(1)

    return args

def read_station_file(station_file: str):
    df = pd.read_csv(station_file, index_col='stid', usecols=list(STATION_TABLE_COLUMN_RENAME.keys()))
    df = df.rename(columns=STATION_TABLE_COLUMN_RENAME)
    return df

point_data = main()
