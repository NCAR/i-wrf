#!/usr/bin/env python3

"""
download_hrrr_from_aws_or_gc.py

Created by: Jared A. Lee (jaredlee@ucar.edu)
Created on: 6 Feb 2025

This script downloads HRRR output files for the requested cycle(s) and lead times from either AWS or Google Cloud.
"""

import os
import sys
import argparse
import pathlib
import datetime as dt
from urllib.error import HTTPError
import numpy as np
import pandas as pd
import wget
import logging
# from proc_util import exec_command

this_file = os.path.basename(__file__)
logging.basicConfig(format=f'{this_file}: %(asctime)s - %(message)s',
                    level=logging.DEBUG, datefmt='%Y-%m-%dT%H:%M:%S')
log = logging.getLogger(__name__)

long_time = 5
long_long_time = 15
short_time = 3
curr_dir=os.path.dirname(os.path.abspath(__file__))

def parse_args():
    ## Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--cycle_dt', default='20220801_00',
                        help='GFS cycle date/time to download [YYYYMMDD_HH] (default: 20220801_00)')
    parser.add_argument('-s', '--sim_hrs', default=48, type=int,
                        help='integer number of forecast hours to download (default: 48)')
    parser.add_argument('-o', '--out_dir_parent', default=None,
                        help='string or pathlib.Path object of the local directory where all downloaded HRRR data should be stored')
    parser.add_argument('-f', '--icbc_fc_dt', default=0, type=int,
                        help='integer number of hours prior to WRF cycle time for IC/LBC model cycle (default: 0)')
    parser.add_argument('-i', '--int_h', default=3, type=int,
                        help='integer number of hours between GEFS files to download (default: 3)')
    parser.add_argument('-n', '--native_grid', action='store_true',
                        help='If flag present, then download HRRR native-grid data for atmospheric variables, otherwise only download HRRR pressure-level data.')
    parser.add_argument('-c', '--icbc_source', default='AWS',
                        help='Repository from which to download HRRR data files (AWS|Google Cloud) (default: AWS)')
    parser.add_argument('-a', '--icbc_analysis', action='store_true',
                        help='If flag present, then download HRRR analysis [f00] data instead of forecast files)')

    args = parser.parse_args()
    cycle_dt = args.cycle_dt
    sim_hrs = args.sim_hrs
    out_dir_parent = args.out_dir_parent
    icbc_fc_dt = args.icbc_fc_dt
    int_h = args.int_h
    native_grid = args.native_grid
    icbc_source = args.icbc_source
    icbc_analysis = args.icbc_analysis

    if len(cycle_dt) != 11:
        log.error('ERROR! Incorrect length for positional argument cycle_dt. Exiting!')
        parser.print_help()
        sys.exit(1)
    elif cycle_dt[8] != '_':
        log.error('ERROR! Incorrect format for positional argument cycle_dt. Exiting!')
        parser.print_help()
        sys.exit(1)

    if out_dir_parent is None:
        log.error('ERROR: out_dir_parent not specified. Exiting!')
        sys.exit(1)
    else:
        out_dir_parent = pathlib.Path(out_dir_parent)

    return cycle_dt, sim_hrs, out_dir_parent, icbc_fc_dt, int_h, native_grid, icbc_source, icbc_analysis

def wget_error(error_msg, now_time_beg):
    log.error('ERROR: '+error_msg)
    log.error('Check if an earlier cycle has the required files and adjust icbc_fc_dt if necessary. Exiting!')
    now_time_end = dt.datetime.now(dt.UTC)
    run_time_tot = now_time_end - now_time_beg
    now_time_beg_str = now_time_beg.strftime('%Y-%m-%d %H:%M:%S')
    now_time_end_str = now_time_end.strftime('%Y-%m-%d %H:%M:%S')
    log.error('\nScript completed with an error.')
    log.error('   Beg time: '+now_time_beg_str)
    log.error('   End time: '+now_time_end_str)
    log.error('   Run time: '+str(run_time_tot)+'\n')
    sys.exit(1)

def main(cycle_dt_str, sim_hrs, out_dir_parent, icbc_fc_dt, now_time_beg, interval, native_grid, icbc_source, icbc_analysis):

    # Be very forgiving for variants of specifying GoogleCloud for the repository
    variants_aws = ['AWS', 'aws']
    variants_gc = ['GoogleCloud', 'googlecloud', 'Google_Cloud', 'google_cloud', 'GC', 'gc', 'GCloud', 'gcloud']
    if icbc_source not in variants_aws and icbc_source not in variants_gc:
        log.error('ERROR: Unknown icbc_source for downloading HRRR data: ' + icbc_source)
        log.error('Expected AWS or GoogleCloud (or some other variants thereof).')
        log.error('Exiting!')
        sys.exit(1)

    ## Calculate the desired lead hours for this cycle, accounting for the possible icbc_fc_dt offset.
    ## Build array of forecast lead times to download. GFS output on AWS is 1-hourly.
    leads = np.arange(icbc_fc_dt, sim_hrs+icbc_fc_dt+1, interval)
    n_leads = len(leads)

    fmt_hh = '%H'
    fmt_yyyymmdd = '%Y%m%d'
    fmt_yyyymmdd_hh = '%Y%m%d_%H'

    cycle_dt = pd.to_datetime(cycle_dt_str, format=fmt_yyyymmdd_hh)
    cycle_date = cycle_dt.strftime(fmt_yyyymmdd)
    cycle_hour = cycle_dt.strftime(fmt_hh)

    # Build the array of valid times for this simulation (most needed for icbc_analysis=True)
    valid_dt_beg = cycle_dt
    valid_dt_end = cycle_dt + dt.timedelta(hours=sim_hrs)
    valid_dt_all = pd.date_range(start=valid_dt_beg, end=valid_dt_end, freq=str(interval) + 'h')
    n_valid = len(valid_dt_all)

    # Both AWS and Google Cloud archive HRRR data back to the 20140730_18 cycle
    if cycle_dt < pd.to_datetime('20140730_18', format=fmt_yyyymmdd_hh):
        log.error('ERROR! HRRR data prior to the 20140730_18 cycle is not available on Google Cloud or AWS.')
        log.error('You chose ' + cycle_dt_str + ' for a cycle start date/time.')
        log.error('Please choose a later date or choose a different model than HRRR for ICs/LBCs.')
        log.error('Exiting!')
        sys.exit(1)

    # Directory structure for HRRR data on AWS and Google Cloud
    # All dates have conus directory. Some later dates have other domain directories (e.g., alaska).
    # TODO: Someday, allow users to request HRRR domains other than conus
    aws_dir_base = 'https://noaa-hrrr-bdp-pds.s3.amazonaws.com'
    gc_dir_base = 'https://storage.googleapis.com/high-resolution-rapid-refresh'

    # Loop over lead times
    if not icbc_analysis:
        if icbc_source in variants_aws:
            host_dir = aws_dir_base + '/hrrr.' + cycle_date + '/conus'
        elif icbc_source in variants_gc:
            host_dir = gc_dir_base + '/hrrr.' + cycle_date + '/conus'
        else:
            raise ValueError(f'Invalid IC/BC source value: {icbc_source}')

        # Create the local download directory for this HRRR cycle's files to match the AWS structure
        out_dir = out_dir_parent.joinpath('hrrr.' + cycle_date, 'conus')
        out_dir.mkdir(parents=True, exist_ok=True)
        os.chdir(out_dir)

        for ll in range(n_leads):
            this_lead = str(leads[ll]).zfill(2)

            # Download HRRR native-grid files if specified (atmosphere-only, no soil data)
            if native_grid:
                fname = 'hrrr.t' + cycle_hour + 'z.wrfnatf' + this_lead + '.grib2'
                url = host_dir+'/'+fname

                if not out_dir.joinpath(fname).is_file():
                    log.info('Downloading '+url)
                    try:
                        wget.download(url)
                        log.info('')
                    except HTTPError:
                        err_msg = 'HTTP Error 404: Not Found: ' + url
                        wget_error(str(err_msg), now_time_beg)
                else:
                    log.info('   File '+fname+' already exists locally. Not downloading again from server.')

            # Download HRRR pressure-level files no matter what (atmosphere + soil)
            fname = 'hrrr.t' + cycle_hour + 'z.wrfprsf' + this_lead + '.grib2'
            url = host_dir+'/'+fname

            if not out_dir.joinpath(fname).is_file():
                log.info('Downloading '+url)
                try:
                    wget.download(url)
                    log.info('')
                except HTTPError:
                    err_msg = 'HTTP Error 404: Not Found: ' + url
                    wget_error(str(err_msg), now_time_beg)
            else:
                log.info('   File '+fname+' already exists locally. Not downloading again from server.')
    else:
        # icbc_analysis = True, so loop through valid times of the simulation for f00 files
        for vv in range(n_valid):
            this_valid_dt = valid_dt_all[vv]
            valid_date = this_valid_dt.strftime(fmt_yyyymmdd)
            valid_hour = this_valid_dt.strftime(fmt_hh)

            if icbc_source in variants_aws:
                host_dir = aws_dir_base + '/hrrr.' + valid_date + '/conus'
            elif icbc_source in variants_gc:
                host_dir = gc_dir_base + '/hrrr.' + valid_date + '/conus'
            else:
                raise ValueError(f'Invalid IC/BC source value: {icbc_source}')

            # Create the local download directory for this HRRR cycle's files to match the AWS structure
            out_dir = out_dir_parent.joinpath('hrrr.' + valid_date, 'conus')
            out_dir.mkdir(parents=True, exist_ok=True)
            os.chdir(out_dir)

            # Download HRRR native-grid files if specified (atmosphere-only, no soil data)
            if native_grid:
                fname = 'hrrr.t' + valid_hour + 'z.wrfnatf00.grib2'
                url = host_dir + '/' + fname

                if not out_dir.joinpath(fname).is_file():
                    log.info('Downloading ' + url)
                    try:
                        wget.download(url)
                        log.info('')
                    except HTTPError:
                        err_msg = 'HTTP Error 404: Not Found: ' + url
                        wget_error(str(err_msg), now_time_beg)
                else:
                    log.info('   File ' + fname + ' already exists locally. Not downloading again from server.')

            # Download HRRR pressure-level files no matter what (atmosphere + soil)
            fname = 'hrrr.t' + valid_hour + 'z.wrfprsf00.grib2'
            url = host_dir + '/' + fname

            if not out_dir.joinpath(fname).is_file():
                log.info('Downloading ' + url)
                try:
                    wget.download(url)
                    log.info('')
                except HTTPError:
                    err_msg = 'HTTP Error 404: Not Found: ' + url
                    wget_error(str(err_msg), now_time_beg)
            else:
                log.info('   File ' + fname + ' already exists locally. Not downloading again from server.')


def run():
    now_time_beg = dt.datetime.now(dt.UTC)
    cycle_dt, sim_hrs, out_dir_parent, icbc_fc_dt, int_h, native_grid, icbc_source, icbc_analysis = parse_args()
    main(cycle_dt, sim_hrs, out_dir_parent, icbc_fc_dt, now_time_beg, int_h, native_grid, icbc_source, icbc_analysis)
    now_time_end = dt.datetime.now(dt.UTC)
    run_time_tot = now_time_end - now_time_beg
    now_time_beg_str = now_time_beg.strftime('%Y-%m-%d %H:%M:%S')
    now_time_end_str = now_time_end.strftime('%Y-%m-%d %H:%M:%S')
    log.info('')
    log.info(this_file + ' completed successfully.')
    log.info('   Beg time: '+now_time_beg_str)
    log.info('   End time: '+now_time_end_str)
    log.info('   Run time: '+str(run_time_tot)+'\n')


if __name__ == '__main__':
    run()
