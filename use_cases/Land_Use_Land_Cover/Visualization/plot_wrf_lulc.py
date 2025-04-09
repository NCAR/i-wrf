"""
plot_wrf_lulc.py

Created by: Jared A. Lee (jaredlee@ucar.edu)
Created on: 26 Mar 2025

This script plots various WRF output fields from two WRF experiments demonstrating land use/land cover (LULC) change.
One experiment is a control run, and the other is an experiment where the urban area of Dallas/Fort Worth has been
expanded 4x. The script generates side-by-side two-panel map figures to compare the two WRF experiments at a given time.
"""

import sys
import argparse
import pathlib
import warnings
import datetime as dt
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import wrf
import matplotlib as mpl

# Import functions from a local file
import map_funcs

def main(opts):
    # ==============
    # USER SETTINGS:
    # ==============

    # Default plot type selection
    plot_type = 'png'
    plot_stations = True     # Plot station markers & labels on the map (e.g., cities of interest)
    plot_single = False     # Plot single figures for each variable/experiment
    plot_panels = True      # Plot multi-panel figures for each variable containing both experiments (+ obs if avail.)
    plot_nexrad = True   # Plot NEXRAD radar/rain panel alongside the WRF experiment panels

    # Which variables should be plotted?
    plot_TERRAIN = False  # terrain height [m]
    plot_LU_INDEX = True  # land use index (13=urban)
    plot_T2 = True  # 2-m temperature [C]
    plot_RH2 = True  # 2-m relative humidity [%]
    plot_WS10 = True  # 10-m wind speed [m s-1]
    plot_REFL = True  # simulated radar reflectivity [dBZ]
    plot_RAIN = True  # total accumulated rainfall during the simulation [mm]

    # Plot any overlays, like wind barbs?
    plot_wind_barbs_sfc = True  # overlay 10-m wind barbs for selected plots
    plot_wind_barbs_upr = True  # overlay upper-air wind barbs for selected plots

    # Default water color (generally use only in terrain plots)
    water_color = 'lightblue'

    # Set some other plot options
    suptitle_y_single = 1.00
    suptitle_y_panel = 0.82
    plot_fontsize = 13
    barb_thin = 10
    barb_width = 0.5
    figsize = (8, 10)
    figsize_2panels = (16, 12)
    figsize_3panels = (24, 12)

    # Set some text labels for demonstration
    if plot_stations:
        text1_lab = ['Dallas', 'Fort Worth', 'DFW', 'Waco', 'Wichita Falls', 'Tyler']
        mark1_lat = np.asarray([32.7854, 32.7468, 32.8965, 31.5547, 33.9050, 32.3539])
        mark1_lon = np.asarray([-96.8011, -97.3231, -97.0337, -97.1304, -98.4874, -95.3008])
        text1_lat = np.asarray(mark1_lat) + np.asarray([-0.20, -0.20, 0.10, -0.20, -0.20, -0.20])
        text1_lon = np.asarray(mark1_lon) + np.asarray([0.12, -0.12, 0, 0, 0, 0])
        mark1_size = 36
        mark1_color = 'black'

    # Domain plotting ranges in (i,j) space (whole domain by default)
    i_beg, i_end = 0, -1
    j_beg, j_end = 0, -1

    # If labels are set to None, they'll be chosen automatically, which usually works fine
    lat_labels = None
    lon_labels = None
    # lat_labels = [31, 32, 33, 34, 35]
    # lon_labels = [-94, -95, -96, -97, -98, -99]

    # Some variables useful for the plots
    en_dash = '\u2013'
    em_dash = '\u2014'
    deg_uni = '\u00B0'
    dom_id = opts['domain']
    wrf_dom = 'd0' + str(dom_id)
    title1 = 'Control'
    title2 = 'DFW 4x'
    title3 = 'NEXRAD'
    suptitle_suffix = ' (Domain ' + str(dom_id) + ')'
    suptitle_panel = 'WRF Domain ' + str(dom_id)
    suptitle_panel_lu = suptitle_panel + ' ' + em_dash + ' Urban Land Use (outlined)'

    # Set map contour plot limits
    min_terrain = 0.0
    max_terrain = 1000.1
    int_terrain = 50.0

    min_t2 = 10.0
    max_t2 = 40.1
    int_t2 = 1.0

    min_rh2 = 0.0
    max_rh2 = 100.1
    int_rh2 = 5.0

    min_ws10 = 0.0
    max_ws10 = 20.0
    int_ws10 = 1.0

    min_rain = 0.0
    max_rain = 100.1
    int_rain = 5.0

    # =================
    # END USER SETTINGS
    # =================

    fmt_yyyymmdd = '%Y%m%d'
    fmt_yyyymmdd_hh = '%Y%m%d_%H'
    fmt_yyyymmdd_hhmm = '%Y%m%d_%H%M'
    fmt_wrf_date = '%Y-%m-%d'
    fmt_hhmm = '%H%M'
    fmt_time_file = fmt_yyyymmdd_hhmm
    fmt_time_plot = '%d %b %Y/%H%M UTC'

    mpl_ms1 = 'm $\mathregular{s^{-1}}$'

    # Define a custom colormap for radar reflectivity plots
    # Modified to add gray for 0–5 dBZ and lightpurple for 75+ dBZ
    cmap_radar = np.array([
        [200, 200, 200], [4, 233, 231], [1, 159, 244], [3, 0, 244],
        [2, 253, 2], [1, 197, 1], [0, 142, 0],
        [253, 248, 2], [229, 188, 0], [253, 149, 0],
        [253, 0, 0], [212, 0, 0], [188, 0, 0],
        [248, 0, 253], [152, 84, 198], [228, 199, 243]], np.float32) / 255.0
    bounds_radar = np.arange(0., 75.01, 5.0)
    # Color names are approximate and only intended for assistance deciphering the RGB table above
    colors_radar = np.array([
        'gray', 'cyan', 'lightblue', 'darkblue',
        'lightgreen', 'green', 'darkgreen',
        'yellow', 'lightorange', 'orange',
        'red', 'darkred', 'brickred',
        'fuschia', 'violet', 'lavender'])

    # Retrieve the experiment names
    exp_names = opts['exp_names']
    n_exps = len(exp_names)

    # Set WRF directories
    wrf_dir_parent = opts['wrf_dir_parent']
    wrf_dir1 = wrf_dir_parent.joinpath(exp_names[0])
    wrf_dir2 = wrf_dir_parent.joinpath(exp_names[1])

    # Set output directories
    out_dir_parent = opts['out_dir_parent']
    out_dir1 = out_dir_parent.joinpath(exp_names[0])
    out_dir2 = out_dir_parent.joinpath(exp_names[1])

    # NEXRAD directory
    nexrad_dir = opts['nexrad_dir']

    # Build array of valid times from start time and requested lead times
    init_dt_str = opts['init_dt']
    beg_lead_time = opts['beg_lead_time']
    end_lead_time = opts['end_lead_time']
    str_lead_time = opts['str_lead_time']
    beg_lead_hr = int(beg_lead_time.split(sep=':')[0])
    beg_lead_mn = int(beg_lead_time.split(sep=':')[1])
    end_lead_hr = int(end_lead_time.split(sep=':')[0])
    end_lead_mn = int(end_lead_time.split(sep=':')[1])
    init_dt = pd.to_datetime(init_dt_str, format=fmt_yyyymmdd_hh)
    valid_dt_beg = init_dt + dt.timedelta(hours=beg_lead_hr, minutes=beg_lead_mn)
    valid_dt_end = init_dt + dt.timedelta(hours=end_lead_hr, minutes=end_lead_mn)
    valid_dt_all = pd.date_range(start=valid_dt_beg, end=valid_dt_end, freq=str(str_lead_time) + 'min')
    n_valid = len(valid_dt_all)

    start_time_plot = 'Start: ' + init_dt.strftime(fmt_time_plot)

    # Build array of times in the NEXRAD files, as its time variable is unhelpful
    nexrad_dt = pd.date_range(start=init_dt, end=init_dt + dt.timedelta(hours=36), freq='10min')
    n_nexrad_times = len(nexrad_dt)

    # Loop over valid times
    for vv in range(n_valid):
        valid_dt = valid_dt_all[vv]
        valid_dt_wrf = valid_dt.strftime(fmt_wrf_date + '_' + fmt_hhmm)
        valid_dt_plot = valid_dt.strftime(fmt_time_plot)
        valid_dt_file = valid_dt.strftime(fmt_time_file)
        valid_time_plot = 'Valid: ' + valid_dt_plot

        # Time index in NEXRAD files
        ind_nexrad = np.where(nexrad_dt == valid_dt)[0][0]

        map_prefix = 'map_wrf_' + wrf_dom + '_'
        map_prefix1 = 'map_wrf_' + wrf_dom + '_' + exp_names[0] + '_'
        map_prefix2 = 'map_wrf_' + wrf_dom + '_' + exp_names[1] + '_'
        panel_map_prefix = 'panel_' + map_prefix
        map_suffix = '_' + valid_dt_file + '.' + plot_type
        title_r = start_time_plot + '\n' + valid_time_plot
        title_r_no_start = valid_time_plot
        title_r_no_valid = start_time_plot
        title_r_blank = ''

        # Read in both WRF files
        # TODO: Double-check WRF directory/file naming convention when from inside container
        wrf_fname1 = 'wrfout_' + wrf_dom + '_' + valid_dt_wrf + '.morr300.nc'
        wrf_fname2 = 'wrfout_' + wrf_dom + '_' + valid_dt_wrf + '.morr300.' + exp_names[1] + '.nc'
        wrf_file1 = wrf_dir1.joinpath(wrf_fname1)
        wrf_file2 = wrf_dir2.joinpath(wrf_fname2)

        try:
            wrf_file1.is_file()
        except FileNotFoundError:
            print('WARNING: File ' + str(wrf_file1) + ' not found. Continuing to the next valid time.')
            continue
        print('Reading ' + str(wrf_file1))
        # Use NetCDF4-python to open a Dataset, as wrf-python doesn't yet take an xarray Dataset
        # wrf.getvar will return an xarray Dataset by default, though
        ds_wrf_nc1 = netCDF4.Dataset(wrf_file1, mode='r')

        try:
            wrf_file2.is_file()
        except FileNotFoundError:
            print('WARNING: File ' + str(wrf_file2) + ' not found. Continuing to the next valid time.')
            continue
        print('Reading ' + str(wrf_file2))
        # Use NetCDF4-python to open a Dataset, as wrf-python doesn't yet take an xarray Dataset
        # wrf.getvar will return an xarray Dataset by default, though
        ds_wrf_nc2 = netCDF4.Dataset(wrf_file2, mode='r')

        # Read NEXRAD file(s) if requested, but only need to read them once because they have all the times
        if plot_nexrad and vv == 0:
            if plot_REFL:
                nexrad_fname = 'RADAR_DFW22_NCR_20170703_' + wrf_dom + '_2017Jul03_2017Jul05.nc'
                nexrad_refl_file = nexrad_dir.joinpath(nexrad_fname)
                print('Reading ' + str(nexrad_refl_file))
                ds_nexrad_refl_xr = xr.open_dataset(nexrad_refl_file)
                da_nexrad_refl = ds_nexrad_refl_xr['NX_data']
                # Dimensions (time, lon, lat). Time is every 10 min from 20170703_1200 to 20170705_0000.
                # Lon & Lat are the same as the WRF grid.
                nexrad_refl = da_nexrad_refl.values

            if plot_RAIN:
                nexrad_fname = 'RADAR_DFW22_N1P_20170703_' + wrf_dom + '_2017Jul03_2017Jul05.nc'
                nexrad_rain_file = nexrad_dir.joinpath(nexrad_fname)
                print('Reading ' + str(nexrad_rain_file))
                ds_nexrad_rain_xr = xr.open_dataset(nexrad_rain_file)
                da_nexrad_rain = ds_nexrad_rain_xr['NX_accum']
                nexrad_rain = da_nexrad_rain.values

        # Static fields only need to be read in once from one of the wrfout files
        if vv == 0:
            # Latitude, Longitude
            da_lat = wrf.getvar(ds_wrf_nc1, 'lat', squeeze=False)
            da_lon = wrf.getvar(ds_wrf_nc1, 'lon', squeeze=False)
            wrf_lat = da_lat.values[0, :, :]
            wrf_lon = da_lon.values[0, :, :]
            n_wrf_lat = wrf_lat.shape[0]
            n_wrf_lon = wrf_lon.shape[1]
            n_wrf_lev = int(getattr(ds_wrf_nc1, 'BOTTOM-TOP_GRID_DIMENSION'))
            wrf_lats, wrf_lons = wrf.latlon_coords(da_lat)

            print('Getting cartopy mapping objects')
            cart_proj = wrf.get_cartopy(wrfin=ds_wrf_nc1)
            cart_bounds = wrf.geo_bounds(var=da_lat[0, j_beg:j_end, i_beg:i_end])
            cart_xlim = wrf.cartopy_xlim(wrfin=ds_wrf_nc1, geobounds=cart_bounds)
            cart_ylim = wrf.cartopy_ylim(wrfin=ds_wrf_nc1, geobounds=cart_bounds)
            borders, states, oceans, lakes, rivers, land = map_funcs.get_cartopy_features()

            # Start populating dictionary for map plotting options. Update later with other options.
            map_opts = {
                'cart_proj': cart_proj, 'cart_xlim': cart_xlim, 'cart_ylim': cart_ylim,
                'borders': borders, 'states': states, 'oceans': oceans, 'lakes': lakes,
                'lons': wrf_lons, 'lats': wrf_lats,
                'lat_labels': lat_labels, 'lon_labels': lon_labels, 'fontsize': plot_fontsize,
                'map_x_thin': barb_thin, 'map_y_thin': barb_thin, 'barb_width': barb_width,
            }

            if plot_stations:
                map_opts['text1_lab'] = text1_lab
                map_opts['text1_lat'] = text1_lat
                map_opts['text1_lon'] = text1_lon
                map_opts['mark1_lat'] = mark1_lat
                map_opts['mark1_lon'] = mark1_lon
                map_opts['mark1_size'] = mark1_size
                map_opts['mark1_color'] = mark1_color

            # Land use (want available for all plots as a contour)
            if plot_LU_INDEX:
                print('   Reading land use index')
                da1_lu = wrf.getvar(ds_wrf_nc1, 'LU_INDEX', squeeze=False)
                da2_lu = wrf.getvar(ds_wrf_nc2, 'LU_INDEX', squeeze=False)
                wrf1_lu = da1_lu.values[0, :, :]
                wrf2_lu = da2_lu.values[0, :, :]
                wrf1_lu_urb = np.where(wrf1_lu==13, wrf1_lu, 0)
                wrf2_lu_urb = np.where(wrf2_lu==13, wrf2_lu, 0)
                urb_lu_suffix = '; Urban LU (outline)'
                map_opts['cont_levs'] = 13  # urban value for LU_INDEX
                map_opts['cont_color'] = 'red'
                map_opts['cont_width'] = 0.05

            # Terrain
            if plot_TERRAIN:
                print('   Reading terrain')
                da_terrain = wrf.getvar(ds_wrf_nc1, 'ter', squeeze=False)
                wrf_terrain = da_terrain.values[0, :, :]

                var_file = 'TERRAIN'
                var_name = 'Terrain Height'
                var_unit = 'm'
                wrf_var = wrf_terrain
                min_val = np.nanmin(wrf_var)
                max_val = np.nanmax(wrf_var)
                extend = 'both'
                cmap = map_funcs.truncate_cmap(mpl.cm.terrain, minval=0.20, maxval=0.95)
                bounds = np.arange(min_terrain, max_terrain, int_terrain)
                norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend=extend)
                title_l = var_name + f'\nMin: {min_val:.1f} ' + var_unit + f', Max: {max_val:.1f} ' + var_unit
                map_opts['figsize'] = figsize
                map_opts['suptitle'] = title1 + suptitle_suffix
                map_opts['fill_var'] = wrf_var
                map_opts['water_color'] = water_color
                map_opts['extend'] = extend
                map_opts['cmap'] = cmap
                map_opts['bounds'] = bounds
                map_opts['norm'] = norm
                map_opts['cbar_lab'] = 'Model ' + var_name + ' [' + var_unit + ']'
                map_opts['fname'] = out_dir_parent.joinpath(map_prefix + var_file + '.' + plot_type)
                map_opts['title_l'] = title_l
                map_opts['title_r'] = title_r_blank
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf1_lu_urb

                if plot_single:
                    map_funcs.map_plot(map_opts)

                if plot_panels:
                    n_rows, n_cols = 1, 2
                    n_panels = n_rows * n_cols
                    map_opts['fname'] = out_dir_parent.joinpath(panel_map_prefix + var_file + '.' + plot_type)
                    map_opts['n_rows'] = n_rows
                    map_opts['n_cols'] = n_cols
                    map_opts['single_cbar'] = True
                    map_opts['figsize'] = figsize_2panels
                    map_opts['title_l1'] = title_l
                    map_opts['title_l2'] = title_l
                    map_opts['title_c1'] = title1 + '\n\n'
                    map_opts['title_c2'] = title2 + '\n\n'
                    map_opts['suptitle'] = suptitle_panel
                    map_opts['suptitle_y'] = suptitle_y_panel
                    if plot_LU_INDEX:
                        map_opts['cont1_var'] = wrf1_lu_urb
                        map_opts['cont2_var'] = wrf2_lu_urb
                        map_opts['suptitle'] = suptitle_panel_lu
                    for pp in range(1, n_panels+1):
                        # Set options that are common across all panels
                        map_opts['fill_var' + str(pp)] = wrf_var
                        map_opts['extend' + str(pp)] = extend
                        map_opts['bounds' + str(pp)] = bounds
                        map_opts['cmap' + str(pp)] = cmap
                        map_opts['norm' + str(pp)] = norm
                        map_opts['cont' + str(pp) + '_levs'] = 13
                        map_opts['cont' + str(pp) + '_color'] = 'red'
                        map_opts['cont' + str(pp) + '_width'] = 0.05
                    map_funcs.map_plot_panels(map_opts)

        # For non-terrain plots, water color should be 'none' (not None)
        map_opts['water_color'] = 'none'

        # Maximum reflectivity
        if plot_REFL:
            print('   Reading maximum reflectivity')
            da1_max_refl = wrf.getvar(ds_wrf_nc1, 'mdbz', squeeze=False)
            da2_max_refl = wrf.getvar(ds_wrf_nc2, 'mdbz', squeeze=False)
            #da1_max_refl = wrf.getvar(ds_wrf_nc1, 'REFD_MAX', squeeze=False)
            #da2_max_refl = wrf.getvar(ds_wrf_nc2, 'REFD_MAX', squeeze=False)
            wrf1_max_refl = da1_max_refl.values[0, :, :]
            wrf2_max_refl = da2_max_refl.values[0, :, :]

            var_file = 'MAX_REFL'
            var_name = 'Maximum Reflectivity'
            var_unit = 'dBZ'
            wrf_var1 = wrf1_max_refl[:, :]
            wrf_var2 = wrf2_max_refl[:, :]
            min_val1 = np.nanmin(wrf_var1)
            max_val1 = np.nanmax(wrf_var1)
            min_val2 = np.nanmin(wrf_var2)
            max_val2 = np.nanmax(wrf_var2)
            #wrf_var1 = np.where(wrf_var1 == 0.0, -0.1, wrf_var1)
            #wrf_var2 = np.where(wrf_var2 == 0.0, -0.1, wrf_var2)
            extend = 'max'
            refl_rgb = cmap_radar
            bounds = bounds_radar
            cmap, norm = mpl.colors.from_levels_and_colors(bounds, refl_rgb, extend=extend)
            title_l1 = var_name + f'\nMin: {min_val1:.1f} ' + var_unit + f', Max: {max_val1:.1f} ' + var_unit
            title_l2 = var_name + f'\nMin: {min_val2:.1f} ' + var_unit + f', Max: {max_val2:.1f} ' + var_unit
            map_opts['figsize'] = figsize
            map_opts['extend'] = extend
            map_opts['cmap'] = cmap
            map_opts['bounds'] = bounds
            map_opts['norm'] = norm
            map_opts['cbar_lab'] = var_name + ' [' + var_unit + ']'
            map_opts['title_r'] = title_r

            if plot_nexrad:
                nexrad_var = nexrad_refl[ind_nexrad, :, :]
                min_val3 = np.nanmin(nexrad_var)
                max_val3 = np.nanmax(nexrad_var)
                title_l3 = var_name + f'\nMin: {min_val3:.1f} ' + var_unit + f', Max: {max_val3:.1f} ' + var_unit

            if plot_single:
                map_opts['fname'] = out_dir_parent.joinpath(map_prefix1 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var1
                map_opts['title_l'] = title_l1
                map_opts['suptitle'] = title1 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf1_lu_urb
                map_funcs.map_plot(map_opts)

                map_opts['fname'] = out_dir_parent.joinpath(map_prefix2 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var2
                map_opts['title_l'] = title_l2
                map_opts['suptitle'] = title2 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf2_lu_urb
                map_funcs.map_plot(map_opts)

                map_opts['fill_var'] = nexrad_var
                map_opts['title_l'] = title_l3
                map_opts['title_r'] = title_r_no_start
                map_opts['suptitle'] = title3 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf1_lu_urb
                map_funcs.map_plot(map_opts)

            if plot_panels:
                if plot_nexrad:
                    n_rows, n_cols = 1, 3
                    map_opts['figsize'] = figsize_3panels
                else:
                    n_rows, n_cols = 1, 2
                    map_opts['figsize'] = figsize_2panels
                n_panels = n_rows * n_cols
                map_opts['fname'] = out_dir_parent.joinpath(panel_map_prefix + var_file + '_' + valid_dt_file + '.' + plot_type)
                map_opts['n_rows'] = n_rows
                map_opts['n_cols'] = n_cols
                map_opts['single_cbar'] = True
                map_opts['fill_var1'] = wrf_var1
                map_opts['fill_var2'] = wrf_var2
                map_opts['title_l1'] = title_l1
                map_opts['title_l2'] = title_l2
                map_opts['title_c1'] = title1 + '\n\n'
                map_opts['title_c2'] = title2 + '\n\n'
                map_opts['suptitle'] = suptitle_panel
                map_opts['suptitle_y'] = suptitle_y_panel
                if plot_LU_INDEX:
                    map_opts['cont1_var'] = wrf1_lu_urb
                    map_opts['cont2_var'] = wrf2_lu_urb
                    map_opts['suptitle'] = suptitle_panel_lu
                for pp in range(1, n_panels + 1):
                    # Set options that are common across all panels
                    map_opts['title_r' + str(pp)] = title_r
                    map_opts['extend' + str(pp)] = extend
                    map_opts['bounds' + str(pp)] = bounds
                    map_opts['cmap' + str(pp)] = cmap
                    map_opts['norm' + str(pp)] = norm
                    map_opts['cont' + str(pp) + '_levs'] = 13
                    map_opts['cont' + str(pp) + '_color'] = 'brown'
                    map_opts['cont' + str(pp) + '_width'] = 0.05
                if plot_nexrad:
                    map_opts['figsize'] = figsize_3panels
                    map_opts['title_l3'] = title_l3
                    map_opts['title_c3'] = title3 + '\n\n'
                    map_opts['fill_var3'] = nexrad_var
                    map_opts['cont3_var'] = wrf1_lu_urb
                    map_opts['title_r3'] = title_r_no_start
                map_funcs.map_plot_panels(map_opts)


        # Accumulated precipitation
        if plot_RAIN:
            print('   Reading accumulated precipitation')
            da1_rainc = wrf.getvar(ds_wrf_nc1, 'RAINC', squeeze=False)
            da1_rainnc = wrf.getvar(ds_wrf_nc1, 'RAINNC', squeeze=False)
            da2_rainc = wrf.getvar(ds_wrf_nc2, 'RAINC', squeeze=False)
            da2_rainnc = wrf.getvar(ds_wrf_nc2, 'RAINNC', squeeze=False)
            wrf1_rain = da1_rainc.values[0, :, :] + da1_rainnc.values[0, :, :]
            wrf2_rain = da2_rainc.values[0, :, :] + da2_rainnc.values[0, :, :]
            # For plotting purposes, make anything less than 0.1 mm accumulation be zero
            wrf1_rain = np.where(wrf1_rain < 0.0, 0.0, wrf1_rain)
            wrf2_rain = np.where(wrf2_rain < 0.0, 0.0, wrf2_rain)
            wrf1_rain_plot = np.where(wrf1_rain < 0.1, -0.1, wrf1_rain)
            wrf2_rain_plot = np.where(wrf2_rain < 0.1, -0.1, wrf2_rain)

            var_file = 'RAIN'
            var_name = 'Accumulated Precipitation'
            var_unit = 'mm'
            wrf_var1 = wrf1_rain[:, :]
            wrf_var2 = wrf2_rain[:, :]
            min_val1 = np.nanmin(wrf_var1)
            max_val1 = np.nanmax(wrf_var1)
            min_val2 = np.nanmin(wrf_var2)
            max_val2 = np.nanmax(wrf_var2)
            wrf_var1_plot = wrf1_rain_plot
            wrf_var2_plot = wrf2_rain_plot
            extend = 'max'
            cmap = mpl.cm.GnBu
            bounds = np.arange(min_rain, max_rain, int_rain)
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend=extend)
            title_l1 = var_name + f'\nMin: {min_val1:.1f} ' + var_unit + f', Max: {max_val1:.1f} ' + var_unit
            title_l2 = var_name + f'\nMin: {min_val2:.1f} ' + var_unit + f', Max: {max_val2:.1f} ' + var_unit
            map_opts['figsize'] = figsize
            map_opts['extend'] = extend
            map_opts['cmap'] = cmap
            map_opts['bounds'] = bounds
            map_opts['norm'] = norm
            map_opts['cbar_lab'] = var_name + ' [' + var_unit + ']'
            map_opts['title_r'] = title_r

            if plot_nexrad:
                nexrad_var = nexrad_rain[ind_nexrad, :, :]
                nexrad_var_plot = np.where(nexrad_var < 0.1, -0.1, nexrad_var)
                min_val3 = np.nanmin(nexrad_var)
                max_val3 = np.nanmax(nexrad_var)
                title_l3 = var_name + f'\nMin: {min_val3:.1f} ' + var_unit + f', Max: {max_val3:.1f} ' + var_unit

            if plot_single:
                map_opts['fname'] = out_dir_parent.joinpath(map_prefix1 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var1_plot
                map_opts['title_l'] = title_l1
                map_opts['suptitle'] = title1 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf1_lu_urb
                map_funcs.map_plot(map_opts)

                map_opts['fname'] = out_dir_parent.joinpath(map_prefix2 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var2_plot
                map_opts['title_l'] = title_l2
                map_opts['suptitle'] = title2 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf2_lu_urb
                map_funcs.map_plot(map_opts)

                map_opts['fill_var'] = nexrad_var_plot
                map_opts['title_l'] = title_l3
                map_opts['title_r'] = title_r_no_start
                map_opts['suptitle'] = title3 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf1_lu_urb
                map_funcs.map_plot(map_opts)

            if plot_panels:
                if plot_nexrad:
                    n_rows, n_cols = 1, 3
                    map_opts['figsize'] = figsize_3panels
                else:
                    n_rows, n_cols = 1, 2
                    map_opts['figsize'] = figsize_2panels
                n_panels = n_rows * n_cols
                map_opts['fname'] = out_dir_parent.joinpath(panel_map_prefix + var_file + '_' + valid_dt_file + '.' + plot_type)
                map_opts['n_rows'] = n_rows
                map_opts['n_cols'] = n_cols
                map_opts['single_cbar'] = True

#                map_opts['fill_var1'] = wrf_var1
#                map_opts['fill_var2'] = wrf_var2
                map_opts['fill_var1'] = wrf_var1_plot
                map_opts['fill_var2'] = wrf_var2_plot
                map_opts['title_l1'] = title_l1
                map_opts['title_l2'] = title_l2
                map_opts['title_c1'] = title1 + '\n\n'
                map_opts['title_c2'] = title2 + '\n\n'
                map_opts['suptitle'] = suptitle_panel
                map_opts['suptitle_y'] = suptitle_y_panel
                if plot_LU_INDEX:
                    map_opts['cont1_var'] = wrf1_lu_urb
                    map_opts['cont2_var'] = wrf2_lu_urb
                    map_opts['suptitle'] = suptitle_panel_lu
                for pp in range(1, n_panels + 1):
                    # Set options that are common across all panels
                    map_opts['title_r' + str(pp)] = title_r
                    map_opts['extend' + str(pp)] = extend
                    map_opts['bounds' + str(pp)] = bounds
                    map_opts['cmap' + str(pp)] = cmap
                    map_opts['norm' + str(pp)] = norm
                    map_opts['cont' + str(pp) + '_levs'] = 13
                    map_opts['cont' + str(pp) + '_color'] = 'brown'
                    map_opts['cont' + str(pp) + '_width'] = 0.05
                if plot_nexrad:
                    map_opts['figsize'] = figsize_3panels
                    map_opts['title_l3'] = title_l3
                    map_opts['title_c3'] = title3 + '\n\n'
#                    map_opts['fill_var3'] = nexrad_var
                    map_opts['fill_var3'] = nexrad_var_plot
                    map_opts['cont3_var'] = wrf1_lu_urb
                    map_opts['title_r3'] = title_r_no_start
                map_funcs.map_plot_panels(map_opts)

        # 10-m wind speed
        if plot_WS10 or plot_wind_barbs_sfc:
            print('   Reading 10-m wind components (rotated to Earth coordinates)')
            da1_uvmet = wrf.getvar(ds_wrf_nc1, 'uvmet10', squeeze=False)
            da2_uvmet = wrf.getvar(ds_wrf_nc2, 'uvmet10', squeeze=False)
            wrf1_u10 = da1_uvmet.values[0, 0, :, :]
            wrf1_v10 = da1_uvmet.values[1, 0, :, :]
            wrf2_u10 = da2_uvmet.values[0, 0, :, :]
            wrf2_v10 = da2_uvmet.values[1, 0, :, :]
            wrf1_ws10 = np.sqrt(np.square(wrf1_u10) + np.square(wrf1_v10))
            wrf2_ws10 = np.sqrt(np.square(wrf2_u10) + np.square(wrf2_v10))

            var_file = 'WS10'
            var_name = '10-m Wind Speed'
            var_unit = mpl_ms1
            wrf_var1 = wrf1_ws10[:, :]
            wrf_var2 = wrf2_ws10[:, :]
            min_val1 = np.nanmin(wrf_var1)
            max_val1 = np.nanmax(wrf_var1)
            min_val2 = np.nanmin(wrf_var2)
            max_val2 = np.nanmax(wrf_var2)
            extend = 'max'
            cmap = mpl.cm.GnBu
            bounds = np.arange(min_ws10, max_ws10, int_ws10)
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend=extend)
            title_l1 = var_name + f'\nMin: {min_val1:.1f} ' + var_unit + f', Max: {max_val1:.1f} ' + var_unit
            title_l2 = var_name + f'\nMin: {min_val2:.1f} ' + var_unit + f', Max: {max_val2:.1f} ' + var_unit
            map_opts['figsize'] = figsize
            map_opts['extend'] = extend
            map_opts['cmap'] = cmap
            map_opts['bounds'] = bounds
            map_opts['norm'] = norm
            map_opts['cbar_lab'] = var_name + ' [' + var_unit + ']'
            map_opts['title_r'] = title_r

            if plot_single and plot_WS10:
                map_opts['fname'] = out_dir_parent.joinpath(map_prefix1 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var1_plot
                map_opts['title_l'] = title_l1
                map_opts['suptitle'] = title1 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf1_lu_urb
                if plot_wind_barbs_sfc:
                    map_opts['u'] = wrf1_u10
                    map_opts['v'] = wrf1_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot(map_opts)

                map_opts['fname'] = out_dir_parent.joinpath(map_prefix2 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var2_plot
                map_opts['title_l'] = title_l2
                map_opts['suptitle'] = title2 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf2_lu_urb
                if plot_wind_barbs_sfc:
                    map_opts['u'] = wrf2_u10
                    map_opts['v'] = wrf2_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot(map_opts)

            if plot_panels and plot_WS10:
                n_rows, n_cols = 1, 2
                map_opts['figsize'] = figsize_2panels
                n_panels = n_rows * n_cols
                map_opts['fname'] = out_dir_parent.joinpath(panel_map_prefix + var_file + '_' + valid_dt_file + '.' + plot_type)
                map_opts['n_rows'] = n_rows
                map_opts['n_cols'] = n_cols
                map_opts['single_cbar'] = True

                map_opts['fill_var1'] = wrf_var1
                map_opts['fill_var2'] = wrf_var2
                map_opts['title_l1'] = title_l1
                map_opts['title_l2'] = title_l2
                map_opts['title_c1'] = title1 + '\n\n'
                map_opts['title_c2'] = title2 + '\n\n'
                map_opts['suptitle'] = suptitle_panel
                map_opts['suptitle_y'] = suptitle_y_panel
                if plot_LU_INDEX:
                    map_opts['cont1_var'] = wrf1_lu_urb
                    map_opts['cont2_var'] = wrf2_lu_urb
                    map_opts['suptitle'] = suptitle_panel_lu
                for pp in range(1, n_panels + 1):
                    # Set options that are common across all panels
                    map_opts['title_r' + str(pp)] = title_r
                    map_opts['extend' + str(pp)] = extend
                    map_opts['bounds' + str(pp)] = bounds
                    map_opts['cmap' + str(pp)] = cmap
                    map_opts['norm' + str(pp)] = norm
                    map_opts['cont' + str(pp) + '_levs'] = 13
                    map_opts['cont' + str(pp) + '_color'] = 'brown'
                    map_opts['cont' + str(pp) + '_width'] = 0.05
                if plot_wind_barbs_sfc:
                    map_opts['u1'] = wrf1_u10
                    map_opts['v1'] = wrf1_v10
                    map_opts['u2'] = wrf2_u10
                    map_opts['v2'] = wrf2_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot_panels(map_opts)

        # 2-m temperature
        if plot_T2:
            print('   Reading 2-m temperature')
            da1_t2 = wrf.getvar(ds_wrf_nc1, 'T2', squeeze=False)
            da2_t2 = wrf.getvar(ds_wrf_nc2, 'T2', squeeze=False)
            wrf1_t2 = da1_t2.values[0, :, :] - 273.15
            wrf2_t2 = da2_t2.values[0, :, :] - 273.15

            var_file = 'T2'
            var_name = '2-m Temperature'
            var_unit = deg_uni + 'C'
            wrf_var1 = wrf1_t2[:, :]
            wrf_var2 = wrf2_t2[:, :]
            min_val1 = np.nanmin(wrf_var1)
            max_val1 = np.nanmax(wrf_var1)
            min_val2 = np.nanmin(wrf_var2)
            max_val2 = np.nanmax(wrf_var2)
            extend = 'both'
            cmap = mpl.cm.rainbow
            bounds = np.arange(min_t2, max_t2, int_t2)
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend=extend)
            title_l1 = var_name + f'\nMin: {min_val1:.1f} ' + var_unit + f', Max: {max_val1:.1f} ' + var_unit
            title_l2 = var_name + f'\nMin: {min_val2:.1f} ' + var_unit + f', Max: {max_val2:.1f} ' + var_unit
            map_opts['figsize'] = figsize
            map_opts['extend'] = extend
            map_opts['cmap'] = cmap
            map_opts['bounds'] = bounds
            map_opts['norm'] = norm
            map_opts['cbar_lab'] = var_name + ' [' + var_unit + ']'
            map_opts['title_r'] = title_r

            if plot_single:
                map_opts['fname'] = out_dir_parent.joinpath(map_prefix1 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var1_plot
                map_opts['title_l'] = title_l1
                map_opts['suptitle'] = title1 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf1_lu_urb
                if plot_wind_barbs_sfc:
                    map_opts['u'] = wrf1_u10
                    map_opts['v'] = wrf1_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot(map_opts)

                map_opts['fname'] = out_dir_parent.joinpath(map_prefix2 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var2_plot
                map_opts['title_l'] = title_l2
                map_opts['suptitle'] = title2 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf2_lu_urb
                if plot_wind_barbs_sfc:
                    map_opts['u'] = wrf2_u10
                    map_opts['v'] = wrf2_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot(map_opts)

            if plot_panels:
                n_rows, n_cols = 1, 2
                map_opts['figsize'] = figsize_2panels
                n_panels = n_rows * n_cols
                map_opts['fname'] = out_dir_parent.joinpath(panel_map_prefix + var_file + '_' + valid_dt_file + '.' + plot_type)
                map_opts['n_rows'] = n_rows
                map_opts['n_cols'] = n_cols
                map_opts['single_cbar'] = True

                map_opts['fill_var1'] = wrf_var1
                map_opts['fill_var2'] = wrf_var2
                map_opts['title_l1'] = title_l1
                map_opts['title_l2'] = title_l2
                map_opts['title_c1'] = title1 + '\n\n'
                map_opts['title_c2'] = title2 + '\n\n'
                map_opts['suptitle'] = suptitle_panel
                map_opts['suptitle_y'] = suptitle_y_panel
                if plot_LU_INDEX:
                    map_opts['cont1_var'] = wrf1_lu_urb
                    map_opts['cont2_var'] = wrf2_lu_urb
                    map_opts['suptitle'] = suptitle_panel_lu
                for pp in range(1, n_panels + 1):
                    # Set options that are common across all panels
                    map_opts['title_r' + str(pp)] = title_r
                    map_opts['extend' + str(pp)] = extend
                    map_opts['bounds' + str(pp)] = bounds
                    map_opts['cmap' + str(pp)] = cmap
                    map_opts['norm' + str(pp)] = norm
                    map_opts['cont' + str(pp) + '_levs'] = 13
                    map_opts['cont' + str(pp) + '_color'] = 'brown'
                    map_opts['cont' + str(pp) + '_width'] = 0.05
                if plot_wind_barbs_sfc:
                    map_opts['u1'] = wrf1_u10
                    map_opts['v1'] = wrf1_v10
                    map_opts['u2'] = wrf2_u10
                    map_opts['v2'] = wrf2_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot_panels(map_opts)

        # 2-m relative humidity
        if plot_RH2:
            print('   Reading 2-m relative humidity')
            da1_rh2 = wrf.getvar(ds_wrf_nc1, 'rh2', squeeze=False)
            da2_rh2 = wrf.getvar(ds_wrf_nc2, 'rh2', squeeze=False)
            wrf1_rh2 = da1_rh2.values[0, :, :]
            wrf2_rh2 = da2_rh2.values[0, :, :]

            var_file = 'RH2'
            var_name = '2-m Relative Humidity'
            var_unit = '%'
            wrf_var1 = wrf1_rh2[:, :]
            wrf_var2 = wrf2_rh2[:, :]
            min_val1 = np.nanmin(wrf_var1)
            max_val1 = np.nanmax(wrf_var1)
            min_val2 = np.nanmin(wrf_var2)
            max_val2 = np.nanmax(wrf_var2)
            extend = 'max'
            cmap = mpl.cm.YlGnBu
            bounds = np.arange(min_rh2, max_rh2, int_rh2)
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend=extend)
            title_l1 = var_name + f'\nMin: {min_val1:.1f} ' + var_unit + f', Max: {max_val1:.1f} ' + var_unit
            title_l2 = var_name + f'\nMin: {min_val2:.1f} ' + var_unit + f', Max: {max_val2:.1f} ' + var_unit
            map_opts['figsize'] = figsize
            map_opts['extend'] = extend
            map_opts['cmap'] = cmap
            map_opts['bounds'] = bounds
            map_opts['norm'] = norm
            map_opts['cbar_lab'] = var_name + ' [' + var_unit + ']'
            map_opts['title_r'] = title_r

            if plot_single:
                map_opts['fname'] = out_dir_parent.joinpath(map_prefix1 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var1_plot
                map_opts['title_l'] = title_l1
                map_opts['suptitle'] = title1 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf1_lu_urb
                if plot_wind_barbs_sfc:
                    map_opts['u'] = wrf1_u10
                    map_opts['v'] = wrf1_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot(map_opts)

                map_opts['fname'] = out_dir_parent.joinpath(map_prefix2 + var_file + '_' + map_suffix + '.' + plot_type)
                map_opts['fill_var'] = wrf_var2_plot
                map_opts['title_l'] = title_l2
                map_opts['suptitle'] = title2 + suptitle_suffix
                map_opts['suptitle_y'] = suptitle_y_single
                if plot_LU_INDEX:
                    map_opts['cont_var'] = wrf2_lu_urb
                if plot_wind_barbs_sfc:
                    map_opts['u'] = wrf2_u10
                    map_opts['v'] = wrf2_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot(map_opts)

            if plot_panels:
                n_rows, n_cols = 1, 2
                map_opts['figsize'] = figsize_2panels
                n_panels = n_rows * n_cols
                map_opts['fname'] = out_dir_parent.joinpath(panel_map_prefix + var_file + '_' + valid_dt_file + '.' + plot_type)
                map_opts['n_rows'] = n_rows
                map_opts['n_cols'] = n_cols
                map_opts['single_cbar'] = True

                map_opts['fill_var1'] = wrf_var1
                map_opts['fill_var2'] = wrf_var2
                map_opts['title_l1'] = title_l1
                map_opts['title_l2'] = title_l2
                map_opts['title_c1'] = title1 + '\n\n'
                map_opts['title_c2'] = title2 + '\n\n'
                map_opts['suptitle'] = suptitle_panel
                map_opts['suptitle_y'] = suptitle_y_panel
                if plot_LU_INDEX:
                    map_opts['cont1_var'] = wrf1_lu_urb
                    map_opts['cont2_var'] = wrf2_lu_urb
                    map_opts['suptitle'] = suptitle_panel_lu
                for pp in range(1, n_panels + 1):
                    # Set options that are common across all panels
                    map_opts['title_r' + str(pp)] = title_r
                    map_opts['extend' + str(pp)] = extend
                    map_opts['bounds' + str(pp)] = bounds
                    map_opts['cmap' + str(pp)] = cmap
                    map_opts['norm' + str(pp)] = norm
                    map_opts['cont' + str(pp) + '_levs'] = 13
                    map_opts['cont' + str(pp) + '_color'] = 'brown'
                    map_opts['cont' + str(pp) + '_width'] = 0.05
                if plot_wind_barbs_sfc:
                    map_opts['u1'] = wrf1_u10
                    map_opts['v1'] = wrf1_v10
                    map_opts['u2'] = wrf2_u10
                    map_opts['v2'] = wrf2_v10
                    map_opts['map_x_thin'] = 40
                    map_opts['map_y_thin'] = 40
                map_funcs.map_plot_panels(map_opts)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wrf_dir_parent',
                        default='/glade/campaign/ral/wsap/i-wrf/science_case2_LULC_modification/wrfout/0703dfw/morr_nc300',
                        help='string specifying the directory path to the parent WRF output directories, '
                             'above any experiment or cycle datetime subdirectories (default: '
                             '/glade/campaign/ral/wsap/i-wrf/science_case2_LULC_modification/wrfout/0703dfw/morr_nc300)')
    parser.add_argument('-o', '--out_dir_parent', default='/glade/derecho/scratch/jaredlee/nsf_i-wrf/lulc',
                        help='string specifying the directory path to the parent plot directories (default: '
                             '/glade/derecho/scratch/jaredlee/nsf_i-wrf/lulc)')
    parser.add_argument('-n', '--nexrad_dir',
                        default='/glade/campaign/ral/wsap/i-wrf/science_case2_LULC_modification/nexrad',
                        help='string specifying the directory path to the NEXRAD observation files '
                             '(default: /glade/campaign/ral/wsap/i-wrf/science_case2_LULC_modification/nexrad)')
    parser.add_argument('-i', '--init_dt', default='20170703_12',
                        help='string specifying the model start date/time [YYYYMMDD_HH] for the WRF simulations '
                             '(default: 20170703_12)')
    parser.add_argument('-b', '--beg_lead_time', default='12:00',
                        help='beginning lead time for plotting WRF simulations [HH:MM] (default: 12:00)')
    parser.add_argument('-e', '--end_lead_time', default='36:00',
                        help='ending lead time for plotting WRF simulations [HH:MM] (default: 36:00)')
    parser.add_argument('-s', '--str_lead_time', default=60, type=int,
                        help='stride to create plots every N minutes (default: 60)')
    parser.add_argument('-d', '--domain', default='3', help='WRF domain number to be plotted (default: 3)')
    parser.add_argument('-x', '--exp_name', default='ctl,dfw4x',
                        help='WRF experiment name(s), if applicable. If requesting plots for multiple experiments, '
                             'separate them by commas (e.g., exp01,exp02). (default: ctl,dfw4x)')

    args = parser.parse_args()
    wrf_dir_parent = args.wrf_dir_parent
    out_dir_parent = args.out_dir_parent
    nexrad_dir = args.nexrad_dir
    init_dt = args.init_dt
    beg_lead_time = args.beg_lead_time
    end_lead_time = args.end_lead_time
    str_lead_time = args.str_lead_time
    domain = args.domain
    exp_names = args.exp_name.split(',')

    if out_dir_parent is None:
        out_dir_parent = wrf_dir_parent

    # Make path strings into pathlib objects
    wrf_dir_parent = pathlib.Path(wrf_dir_parent)
    out_dir_parent = pathlib.Path(out_dir_parent)
    nexrad_dir = pathlib.Path(nexrad_dir)

    if len(init_dt) != 11:
        print('ERROR! Incorrect length for positional argument init_dt. Exiting!')
        parser.print_help()
        sys.exit()
    elif init_dt[8] != '_':
        print('ERROR! Incorrect format for positional argument init_dt. Exiting!')
        parser.print_help()
        sys.exit()

    if len(beg_lead_time) != 5:
        print('ERROR! Incorrect length for optional argument -b (beg_lead_time). Exiting!')
        parser.print_help()
        sys.exit()
    elif beg_lead_time[2] != ':':
        print('ERROR! Incorrect format for optional argument -b (beg_lead_time). Exiting!')
        parser.print_help()
        sys.exit()

    if len(end_lead_time) != 5:
        print('ERROR! Incorrect length for optional argument -e (end_lead_time). Exiting!')
        parser.print_help()
        sys.exit()
    elif end_lead_time[2] != ':':
        print('ERROR! Incorrect format for optional argument -e (end_lead_time). Exiting!')
        parser.print_help()
        sys.exit()

    # Put all these configuration options into a dictionary, to make further development or customization easier
    script_config_opts = {
        'wrf_dir_parent': wrf_dir_parent,
        'out_dir_parent': out_dir_parent,
        'nexrad_dir': nexrad_dir,
        'init_dt': init_dt,
        'beg_lead_time': beg_lead_time,
        'end_lead_time': end_lead_time,
        'str_lead_time': str_lead_time,
        'domain': domain,
        'exp_names': exp_names,
    }

    return script_config_opts

if __name__ == '__main__':
    now_time_beg = dt.datetime.utcnow()
    script_config_opts = parse_args()
    main(script_config_opts)
    now_time_end = dt.datetime.utcnow()
    run_time_tot = now_time_end - now_time_beg
    now_time_beg_str = now_time_beg.strftime('%Y-%m-%d %H:%M:%S')
    now_time_end_str = now_time_end.strftime('%Y-%m-%d %H:%M:%S')
    print('\nScript completed successfully.')
    print('   Beg time: '+now_time_beg_str)
    print('   End time: '+now_time_end_str)
    print('   Run time: '+str(run_time_tot)+'\n')
