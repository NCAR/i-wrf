"""
map_funcs.py

Created by: Jared A. Lee (jaredlee@ucar.edu)
Created on: 28 May 2024

This file contains common functions and procedures useful for plotting maps with Cartopy,
typically from WRF model output.
"""

import sys
import numpy as np
import datetime as dt
import wrf
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.geoaxes import GeoAxes

def calc_bearing(lon1, lat1, lon2, lat2):
    """
    Function to calculate the bearing angle between two points (lon1, lat1) and (lon2, lat2).
    -- Inputs:
        - lon1, lat1: floats, longitude and latitude of point 1
        - lon2, lat2: floats, longitude and latitude of point 2
    -- Outputs:
        - bearing_geog: float, geographical bearing (0 deg = north, 90 deg = east, etc.)
        - bearing_math: float, mathematical bearing (0 deg = east, 90 deg = north, etc.)
    -- Reference:
        - https://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/
    """
    DEG2RAD = np.pi / 180.0
    RAD2DEG = 180.0 / np.pi
    x = np.cos(lat2 * DEG2RAD) * np.sin((lon2 - lon1) * DEG2RAD)
    y = ((np.cos(lat1 * DEG2RAD) * np.sin(lat2 * DEG2RAD)) -
         (np.sin(lat1 * DEG2RAD) * np.cos(lat2 * DEG2RAD) * np.cos((lon2-lon1)*DEG2RAD)))
    bearing_geog = np.arctan2(x, y) * RAD2DEG
    bearing_math = 90.0 - bearing_geog
    # Perhaps unnecessary, but keeps it in the range (-180, 180]
    if bearing_math <= -180.0:
        bearing_math += 360.0

    return bearing_geog, bearing_math

def get_cartopy_features():
    """
    Function to get some commonly used Cartopy features (borders, states, oceans, lakes, rivers, land)
    for use in Matplotlib/Cartopy plots.
    -- Inputs: None.
    -- Outputs:
      - borders, states, oceans, lakes, rivers, land
    """

    borders = cartopy.feature.BORDERS
    states  = cartopy.feature.NaturalEarthFeature(category='cultural', scale='10m', facecolor='none',
                                                  name='admin_1_states_provinces_lakes')
    oceans  = cartopy.feature.OCEAN
    lakes   = cartopy.feature.LAKES
    rivers  = cartopy.feature.RIVERS
    land    = cartopy.feature.LAND

    return borders, states, oceans, lakes, rivers, land

def truncate_cmap(cmap, minval=0.0, maxval=1.0, n=100):
    """
    Function to truncate a matplotlib colormap. Particularly useful when plotting terrain.
    -- Required Positional Inputs:
        - cmap: Original Matplotlib colormap
    -- Optional Inputs:
        - minval: Fraction into the original colormap to start the new colormap (default: 0.0)
        - maxval: Fraction into the original colormap to end the new colormap (default: 1.0)
        - n: Number of colors to create in the new colormap (default: 100)
    -- Output:
        - new_cmap: New, truncated colormap
    """
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval), cmap(np.linspace(minval, maxval, n)))
    return new_cmap

def map_plot(opts):
    """
    Procedure to make a map plot with filled contours using matplotlib and Cartopy.
    Optionally overlays the map with wind barbs, markers, text labels, a polygon, or cross-section path.
    -- Input:
        - opts: Dictionary containing plotting options
            Required keys:
            - fname: string or pathlib object specifying the output file name
            - fill_var: 2D variable array to be plotted with filled contours
            - suptitle: string for overall plot title (usually one line)
            - cbar_lab: string for colorbar label (e.g., 'Wind Speed [m/s]')
            - cart_proj: Cartopy object, map projection
            - lons: 1D or 2D array of longitude values
            - lats: 1D or 2D array of latitude values
            - cmap: Matplotlib colormap
            - bounds: Matplotlib colormap bounds
            - norm: matplotlib colormap norm
            Optional keys:
            - cart_xlim: Cartopy object, x-axis limits
            - cart_ylim: Cartopy object, y-axis limits
            - extend: string for colorbar caps ('max', 'min', 'both' [default])
            - fontsize: integer, base fontsize (default: 14)
            - figsize: 2D tuple, defining the figure size (default: (10, 8))
            - cbar_loc: string, identifier for positioning of the colorbar ('bottom' [default], 'top', 'right', 'left')
            - borders, states, oceans, lakes, rivers, land: Cartopy feature objects for the map
            - border_width: numerical line thickness for national borders & coastlines (default: 1.5)
            - water_color: string defining water color for the map (default: 'none' [transparent])
            - lat_labels: array of latitude values to label explicitly on the map
            - lon_labels: array of longitude values to label explicitly on the map
            - suptitle_y: float, y-axis position of the suptitle (default: 0.95)
            - title_l: string, plot subtitle (1 or 2 lines) that gets placed above the top-left corner of the plot axes
            - title_r: string, plot subtitle (1 or 2 lines) that gets placed above the top-right corner of the plot axes
            - title_c: string, plot subtitle (1 or 2 lines) that gets placed above the center of the plot axes
            - map_x_thin: integer, thin wind barb location overlays in x-direction (every Nth grid point) (default: 25)
            - map_y_thin: integer, thin wind barb location overlays in y-direction (every Nth grid point) (default: 25)
            - barb_width: float, linewidth of wind barbs (default: 0.25)
            - u: array-like, define the barb directions
            - v: array-like, define the barb directions
            - markN_lon: array of longitude values for set N of markers
            - markN_lat: array of latitude values for set N of markers
            - markN_size: integer specifying marker size for set N of markers (default: 100)
            - markN_style: string specifying marker style for set N of markers (default: 'o')
            - markN_color: string specifying the marker color for set N of markers
            - markN_edgecolor: string specifying the marker edge color for set N of markers (default: 'black')
            - markN_width: float specifying linewidth for set N of markers
            - markN_val_fill: boolean flag to fill set N of markers from data value, cmap, and norm (default: False)
            - markN_var: variable containing data to fill in set N of markers (e.g., plot obs station data)
            - markN_zorder: integer indicator of the Matplotlib draw order for set N of markers (default: 9+N)
            - textN_lat: array of floats for latitudes for set N of text
            - textN_lon: array of floats for longitudes for set N of text
            - textN_lab: array of strings for labels for set N of text
            - textN_lab_wt: numeric or string indicating font weight for set N of text (default: 'normal')
            - textN_color: string specifying text color (default: 'black')
            - lg_text: array of legend labels
            - lg_loc: string, defining legend placement
            - lg_fontsize: integer fontsize for legend labels
            - polygonN_verts: vertices of polygon N to plot
            - polygonN_color: string specifying the line color for polygon N
            - n_sets: integer, max number of sets of markers, text labels, & polygons that can be plotted (def: 10)
            - cont_var: array with a variable/quantity to use in drawing unfilled contours overlay (default: None)
            - cont_levs: array specifying which values to use in drawing unfilled contours overlay (default: None)
            - cont_color: string, defining the color of the unfilled contours overlay (default: black)
            - cont_linewidth: numeric, defining the point value of the thickness of unfilled contours (default: 0.75)
    -- Output:
        - generates a plot saved to fname
    """
    # Set default values for optional dictionary entries
    opts.setdefault('cart_xlim', None)
    opts.setdefault('cart_ylim', None)
    opts.setdefault('extend', 'both')
    opts.setdefault('fontsize', 14)
    opts.setdefault('figsize', (10,8))
    opts.setdefault('cbar_loc', 'bottom')
    opts.setdefault('borders', None)
    opts.setdefault('states', None)
    opts.setdefault('oceans', None)
    opts.setdefault('lakes', None)
    opts.setdefault('rivers', None)
    opts.setdefault('land', None)
    opts.setdefault('water_color', 'none')
    opts.setdefault('border_width', 1.5)
    opts.setdefault('lat_labels', None)
    opts.setdefault('lon_labels', None)
    opts.setdefault('suptitle_y', 0.95)
    opts.setdefault('title_l', None)
    opts.setdefault('title_r', None)
    opts.setdefault('title_c', None)
    opts.setdefault('map_x_thin', 25)
    opts.setdefault('map_y_thin', 25)
    opts.setdefault('barb_width', 0.25)
    opts.setdefault('u', None)
    opts.setdefault('v', None)
    opts.setdefault('lg_text', None)
    opts.setdefault('lg_loc', 'lower left')
    opts.setdefault('lg_fontsize', 14)
    opts.setdefault('n_sets', 10)
    n_sets = opts['n_sets']
    for nn in range(1, n_sets):
        opts.setdefault('mark' + str(nn) + '_lat', None)
        opts.setdefault('mark' + str(nn) + '_lon', None)
        opts.setdefault('mark' + str(nn) + '_var', None)
        opts.setdefault('mark' + str(nn) + '_size', 100)
        opts.setdefault('mark' + str(nn) + '_style', 'o')
        opts.setdefault('mark' + str(nn) + '_width', 1.5)
        opts.setdefault('mark' + str(nn) + '_color', None)
        opts.setdefault('mark' + str(nn) + '_edgecolor', 'black')
        opts.setdefault('mark' + str(nn) + '_zorder', 9 + nn)
        opts.setdefault('mark' + str(nn) + '_val_fill', False)
        opts.setdefault('text' + str(nn) + '_lat', None)
        opts.setdefault('text' + str(nn) + '_lon', None)
        opts.setdefault('text' + str(nn) + '_lab', None)
        opts.setdefault('text' + str(nn) + '_lab_wt', 'normal')
        opts.setdefault('text' + str(nn) + '_color', 'black')
        opts.setdefault('polygon' + str(nn) + '_verts', None)
        opts.setdefault('polygon' + str(nn) + '_color', 'black')
    opts.setdefault('cont_var', None)
    opts.setdefault('cont_levs', None)
    opts.setdefault('cont_color', 'black')
    opts.setdefault('cont_width', 0.75)

    # Pull most things out of the opts dict into variables for cleaner code later on
    fname = opts['fname']
    fill_var = opts['fill_var']
    suptitle = opts['suptitle']
    cbar_lab = opts['cbar_lab']
    cart_proj = opts['cart_proj']
    cart_xlim = opts['cart_xlim']
    cart_ylim = opts['cart_ylim']
    lons = opts['lons']
    lats = opts['lats']
    cmap = opts['cmap']
    bounds = opts['bounds']
    norm = opts['norm']
    extend = opts['extend']
    fontsize = opts['fontsize']
    figsize = opts['figsize']
    cbar_loc = opts['cbar_loc']
    borders = opts['borders']
    states = opts['states']
    oceans = opts['oceans']
    lakes = opts['lakes']
    rivers = opts['rivers']
    land = opts['land']
    water_color = opts['water_color']
    border_width = opts['border_width']
    lat_labels = opts['lat_labels']
    lon_labels = opts['lon_labels']
    suptitle_y = opts['suptitle_y']
    title_l = opts['title_l']
    title_r = opts['title_r']
    title_c = opts['title_c']
    map_x_thin = opts['map_x_thin']
    map_y_thin = opts['map_y_thin']
    barb_width = opts['barb_width']
    u = opts['u']
    v = opts['v']
    lg_text = opts['lg_text']
    lg_loc = opts['lg_loc']
    lg_fontsize = opts['lg_fontsize']
    cont_var = opts['cont_var']
    cont_levs = opts['cont_levs']
    cont_color = opts['cont_color']
    cont_width = opts['cont_width']

    # Set some Matplotlib resources
    mpl.rcParams['figure.figsize'] = figsize
    mpl.rcParams['grid.color'] = 'gray'
    mpl.rcParams['grid.linestyle'] = ':'
    mpl.rcParams['font.size'] = fontsize + 2
    mpl.rcParams['figure.titlesize'] = fontsize + 2
    mpl.rcParams['savefig.bbox'] = 'tight'
    ll_size = fontsize - 2
    data_crs = ccrs.PlateCarree()

    print('-- Plotting ' + str(fname))

    # Define the figure and axes
    fig = plt.figure()
    ax = plt.subplot(projection=cart_proj)
    # fig, ax = plt.subplots(nrows=1, ncols=1,
    #                        subplot_kw={'projection': cart_proj},)

    # If cart_xlim and cart_ylim tuples are not provided, then set plot limits from lat/lon data directly
    if cart_xlim is not None and cart_ylim is not None:
        ax.set_xlim(cart_xlim)
        ax.set_ylim(cart_ylim)
    else:
        ax.set_extent([np.min(lons), np.max(lons), np.min(lats), np.max(lats)], crs=cart_proj)

    # If lons & lats are 1D, make them into 2D arrays
    if lons.ndim == 1 and lats.ndim == 1:
        ll2d = np.meshgrid(lons, lats)
        lons = ll2d[0]
        lats = ll2d[1]

    # Optional: Add various cartopy features
    if borders != None:
        ax.add_feature(borders, linewidth=border_width, linestyle='-', zorder=3)
    if states != None:
        ax.add_feature(states, linewidth=border_width/3.0, edgecolor='black', zorder=4)
    if oceans != None:
        # Drawing the oceans can be VERY slow with Cartopy 0.20+ for some domains, so may want to skip it
        # Can set the facecolor for the axes to water_color instead (usually we want this 'none' except for terrain)
        ax.add_feature(oceans, facecolor=water_color, zorder=2)
        # ax.add_feature(oceans, facecolor='none', zorder=2)
        # ax.set_facecolor(opts['water_color'])
    if lakes != None:
        # Unless facecolor='none', lakes w/ facecolor will appear above filled contour plot, which is undesirable
        ax.add_feature(lakes, facecolor=water_color, linewidth=0.25, edgecolor='black', zorder=5)
    ax.coastlines(zorder=6, linewidth=border_width)

    # Sometimes longitude labels show up on y-axis, and latitude labels on x-axis in older versions of Cartopy
    # Print lat/lon labels only for a specified set (determined by trial & error) to avoid this problem for now
    gl = ax.gridlines(draw_labels=True, x_inline=False, y_inline=False)
    gl.rotate_labels = False
    # If specific lat/lon labels are not specified, then just label the default gridlines
    if lon_labels is not None:
        gl.xlocator = mticker.FixedLocator(lon_labels)
    if lat_labels is not None:
        gl.ylocator = mticker.FixedLocator(lat_labels)
    gl.top_labels = True
    gl.bottom_labels = True
    gl.left_labels = True
    gl.right_labels = True
    gl.xlabel_style = {'size': ll_size}
    gl.ylabel_style = {'size': ll_size}

    # Optional: Draw unfilled contours of another variable
    if cont_var is not None:
        ax.contour(wrf.to_np(lons), wrf.to_np(lats), wrf.to_np(cont_var), cont_levs,
                    colors=cont_color, linewidths=cont_width, transform=data_crs, transform_first=(ax, True))

    # Draw the actual filled contour plot
    # NOTE: Sometimes a cartopy contourf plot may fail with a Shapely TopologicalError.
    #       It appears to happen sometimes when projecting a dataset onto a different projection.
    #       This error occurs more often if nans are present.
    #       Replacing nans with scipy.interpolate.griddata solves some of these errors, but not all.
    #       Interestingly, plt.contour still seems to work in these situations as a (suboptimal) workaround.
    #       This bug occurs with Shapely 1.8.0, Cartopy 0.20.1.
    #       This issue was resolved with Cartopy 0.20.2 (https://github.com/SciTools/cartopy/issues/1936).
    # Using the transform_first argument results in a noticeable speed-up:
    #    https://scitools.org.uk/cartopy/docs/latest/gallery/scalar_data/contour_transforms.html
    #  - This also requires the X and Y variables to be 2-D arrays.
    #  - This also resolves TopologyException: side location conflict errors that can occur when NaNs are present.

    # If the variable has the same shape as lats, then plot the filled contour field
    if fill_var.shape == lats.shape:
        contourf = True
        plt.contourf(wrf.to_np(lons), wrf.to_np(lats), wrf.to_np(fill_var), bounds,
                     cmap=cmap, norm=norm, extend=extend, transform=data_crs, transform_first=(ax, True))
    # Otherwise, we presumably need to plot an empty map and then plot markers
    else:
        contourf = False
        if opts['mark1_lon'] is None or opts['mark1_lat'] is None:
            print('ERROR: map_plot in map_funcs.py:')
            print('   var does not match the shape of lons or lats.')
            print('   If plotting a contour map, fix the mismatch in shape between fill_var and lons/lats.')
            print('   Otherwise, this could imply a need for a blank map with markers.')
            print('   However, mark1_lon and/or mark1_lat are not provided either.')
            print('   If a filled contour map is desired, ensure fill_var is the same shape as lons and lats.')
            print('   If a blank map with markers is desired instead, provide mark1_lon and mark1_lat.')
            print('   If the markers should be filled according to a data value, then set mark1_val_fill=True.')
            print('   Or if a future use case is identified that requires a blank map & no markers, then modify code.')
            print('   Exiting!')
            sys.exit()

    # Optional: Add up to n_sets of markers to the plot
    for nn in range(1, n_sets):
        mark_num = 'mark' + str(nn)
        mark_lon = opts[mark_num + '_lon']
        mark_lat = opts[mark_num + '_lat']
        mark_var = opts[mark_num + '_var']
        mark_size = opts[mark_num + '_size']
        mark_style = opts[mark_num + '_style']
        mark_width = opts[mark_num + '_width']
        mark_color = opts[mark_num + '_color']
        mark_zorder = opts[mark_num + '_zorder']
        mark_val_fill = opts[mark_num + '_val_fill']
        mark_edgecolor = opts[mark_num + '_edgecolor']

        if mark_lat is None or mark_lon is None:
            continue

        if mark_lat.shape != mark_lon.shape:
            print('ERROR: map_plot in map_funcs.py:')
            print('       ' + mark_num + '_lat and ' + mark_num + '_lon do not have the same shape.')
            print('       Exiting!')
            sys.exit(1)
        if lg_text is None:
            lg_lab = None
        else:
            lg_lab = lg_text[nn-1]
        if mark_val_fill:
            # Fill markers according to their data value, cmap, and norm
            # NOTE: If plotting markers over a blank map, must use plt.scatter, not ax.scatter,
            #       to avoid an error about the lack of a mappable when drawing the colorbar below.
            if mark_var.shape == mark_lat.shape:
                if contourf:
                    ax.scatter(mark_lon, mark_lat, c=mark_var, marker=mark_style, s=mark_size,
                               edgecolors=mark_edgecolor, label=lg_lab, linewidths=mark_width,
                               cmap=cmap, norm=norm, transform=data_crs, zorder=mark_zorder)
                else:
                    plt.scatter(mark_lon, mark_lat, c=mark_var, marker=mark_style, s=mark_size,
                                edgecolors=mark_edgecolor, label=lg_lab, linewidths=mark_width,
                                cmap=cmap, norm=norm, transform=data_crs, zorder=mark_zorder)
            else:
                print('ERROR: map_plot in map_funcs.py:')
                print('       ' + mark_num + '_var, ' + mark_num + '_lat, and ' + mark_num + '_lon are not all the same shape.')
                print('       Exiting!')
                sys.exit(1)
        # Marker set not filled by any data values
        else:
            ax.scatter(mark_lon, mark_lat, marker=mark_style, s=mark_size, color=mark_color,
                       edgecolors=mark_edgecolor, label=lg_lab, linewidths=mark_width,
                       transform=data_crs, zorder=mark_zorder)

    # Draw the colorbar
    # Credit: https://stackoverflow.com/questions/30030328/correct-placement-of-colorbar-relative-to-geo-axes-cartopy
    # Create colorbar axes (temporarily) anywhere
    cax = fig.add_axes([0, 0, 0.1, 0.1])
    # Find the location of the main plot axes
    posn = ax.get_position()
    # Adjust the positioning and orientation of the colorbar, and then draw it
    # The colorbar will inherit the norm/extend attributes from the plt.contourf or plt.scatter call above
    if cbar_loc == 'bottom':
        cax.set_position([posn.x0, posn.y0-0.09, posn.width, 0.05])
        plt.colorbar(cax=cax, orientation='horizontal', label=cbar_lab)
    elif cbar_loc == 'right':
        cax.set_position([posn.x0+posn.width+0.05, posn.y0, 0.04, posn.height])
        plt.colorbar(cax=cax, orientation='vertical', label=cbar_lab)
    elif cbar_loc == 'top' or cbar_loc == 'left':
        print('WARNING: cbar_loc=' + cbar_loc + ' requested. Unsupported option. Colorbar will not be drawn.')
        print('   Add directives in map_funcs.map_plot to handle that option and draw the colorbar.')

    # Add the overall plot title
    plt.suptitle(suptitle, y=suptitle_y)

    # Optional: Add titles to the subplot
    if title_l is not None:
        ax.set_title(title_l, fontsize=fontsize, loc='left')
    if title_r is not None:
        ax.set_title(title_r, fontsize=fontsize, loc='right')
    if title_c is not None:
        ax.set_title(title_c, fontsize=fontsize, loc='center')

    # Optional: Add up to n_sets polygons to the plot
    for nn in range(1, n_sets):
        poly_verts = opts['polygon' + str(nn) + '_verts']
        poly_color = opts['polygon' + str(nn) + '_color']
        if poly_verts is not None:
            n_vertices = poly_verts.shape[0]
            # Draw a line between each vertex of the polygon
            for vv in range(n_vertices):
                lon_beg = poly_verts[vv][0]
                lat_beg = poly_verts[vv][1]
                if vv < n_vertices - 1:
                    lon_end = poly_verts[vv + 1][0]
                    lat_end = poly_verts[vv + 1][1]
                else:   # loop back around to the first vertex
                    lon_end = poly_verts[0][0]
                    lat_end = poly_verts[0][1]
                # Plot each side of the polygon (could optionally add a marker at each vertex if desired)
                ax.plot([lon_beg, lon_end], [lat_beg, lat_end], color=poly_color, linewidth=2, transform=data_crs)

    # Optional: Add up to n_sets of text labels to the plot
    for nn in range(1, n_sets):
        text_num = 'text' + str(nn)
        text_lab = opts[text_num + '_lab']
        text_lat = opts[text_num + '_lat']
        text_lon = opts[text_num + '_lon']
        text_lab_wt = opts[text_num + '_lab_wt']
        text_color = opts[text_num + '_color']
        if text_lab is not None and text_lat is not None and text_lon is not None:
            # print(nn)
            # print(text_lab)
            # print(text_lat)
            # print(text_lon)
            if len(text_lab) != len(text_lat) or len(text_lab) != len(text_lon):
                print('ERROR: map_plot in map_funcs.py:')
                print('       ' + text_num + '_lab, ' + text_num + '_lat, and ' + text_num + '_lon do not all have the same length.')
                print('       Exiting!')
                sys.exit(1)
            n_text = len(text_lab)
            # print('text_color = ' + text_color)
            for xx in range(n_text):
                ax.text(text_lon[xx], text_lat[xx], text_lab[xx], horizontalalignment='center',
                        transform=data_crs, size=fontsize, zorder=13, weight=text_lab_wt, color=text_color)

    # Optional: Draw wind barbs
    if u is not None and v is not None:
        if isinstance(lons, np.ndarray):
            x_thin = lons[::map_y_thin, ::map_x_thin]
        else:
            x_thin = lons[::map_y_thin, ::map_x_thin].values
        if isinstance(lats, np.ndarray):
            y_thin = lats[::map_y_thin, ::map_x_thin]
        else:
            y_thin = lats[::map_y_thin, ::map_x_thin].values
        u_thin = u[::map_y_thin, ::map_x_thin]
        v_thin = v[::map_y_thin, ::map_x_thin]
        # Assume winds input to here are in m/s instead of kts, so reduce the barb_increments from 5/10/50 to 2.5/5/25
        ax.barbs(x_thin, y_thin, u_thin, v_thin, length=5, transform=data_crs, linewidth=barb_width,
                 barb_increments={'half': 2.5, 'full': 5, 'flag': 25})

    # Optional: Add a legend (most useful if 2+ sets of markers)
    if lg_text is not None:
        ax.legend(loc=lg_loc, fontsize=lg_fontsize).set_zorder(15)

    # Save and close the figure
    plt.savefig(fname)
    plt.close()


def map_plot_panels(opts):
    """
    Procedure to make a multi-paneled map plot with filled contours using matplotlib and Cartopy.
    Based off map_plot, but some axes handling with a single plot/panel vs. multiple panels is fundamentally different,
    which necessitates a separate function to handle multi-panel plotting.

    NOTE: This function requires each panel to have the same GeoAxes (projection and mapped area).
    """
    # Set default values for optional dictionary entries
    opts.setdefault('n_rows', 1)
    opts.setdefault('n_cols', 1)
    opts.setdefault('single_cbar', True)
    opts.setdefault('cart_xlim', None)
    opts.setdefault('cart_ylim', None)
    opts.setdefault('extend', 'both')
    opts.setdefault('fontsize', 14)
    opts.setdefault('figsize', (12, 12))
    opts.setdefault('cbar_loc', 'bottom')
    opts.setdefault('borders', None)
    opts.setdefault('states', None)
    opts.setdefault('oceans', None)
    opts.setdefault('lakes', None)
    opts.setdefault('rivers', None)
    opts.setdefault('land', None)
    opts.setdefault('water_color', 'none')
    opts.setdefault('border_width', 1.5)
    opts.setdefault('lat_labels', None)
    opts.setdefault('lon_labels', None)
    opts.setdefault('suptitle_y', 0.95)
    opts.setdefault('title_l', None)
    opts.setdefault('title_r', None)
    opts.setdefault('title_c', None)
    opts.setdefault('map_x_thin', 25)
    opts.setdefault('map_y_thin', 25)
    opts.setdefault('barb_width', 0.25)
    opts.setdefault('u', None)
    opts.setdefault('v', None)
    opts.setdefault('lg_text', None)
    opts.setdefault('lg_loc', 'lower left')
    opts.setdefault('lg_fontsize', 14)
    opts.setdefault('n_sets', 10)
    n_sets = opts['n_sets']
    for nn in range(1, n_sets + 1):
        opts.setdefault('mark' + str(nn) + '_lat', None)
        opts.setdefault('mark' + str(nn) + '_lon', None)
        opts.setdefault('mark' + str(nn) + '_var', None)
        opts.setdefault('mark' + str(nn) + '_size', 100)
        opts.setdefault('mark' + str(nn) + '_style', 'o')
        opts.setdefault('mark' + str(nn) + '_width', 1.5)
        opts.setdefault('mark' + str(nn) + '_color', None)
        opts.setdefault('mark' + str(nn) + '_edgecolor', 'black')
        opts.setdefault('mark' + str(nn) + '_zorder', 9 + nn)
        opts.setdefault('mark' + str(nn) + '_val_fill', False)
        opts.setdefault('text' + str(nn) + '_lat', None)
        opts.setdefault('text' + str(nn) + '_lon', None)
        opts.setdefault('text' + str(nn) + '_lab', None)
        opts.setdefault('text' + str(nn) + '_lab_wt', 'normal')
        opts.setdefault('text' + str(nn) + '_color', 'black')
        opts.setdefault('polygon' + str(nn) + '_verts', None)
        opts.setdefault('polygon' + str(nn) + '_color', 'black')
    n_rows = opts['n_rows']
    n_cols = opts['n_cols']
    n_panels = n_rows * n_cols
    for pp in range(1, n_panels + 1):
        opts.setdefault('cont' + str(pp) + '_var', None)
        opts.setdefault('cont' + str(pp) + '_levs', None)
        opts.setdefault('cont' + str(pp) + '_color', 'black')
        opts.setdefault('cont' + str(pp) + '_width', 0.75)
        opts.setdefault('fill_var' + str(pp), None)
        opts.setdefault('title_l' + str(pp), None)
        opts.setdefault('title_r' + str(pp), None)
        opts.setdefault('title_c' + str(pp), None)
        opts.setdefault('cmap' + str(pp), None)
        opts.setdefault('bounds' + str(pp), None)
        opts.setdefault('norm' + str(pp), None)
        opts.setdefault('extend' + str(pp), 'both')
        opts.setdefault('cbar' + str(pp) + '_loc', 'bottom')
        opts.setdefault('cbar' + str(pp) + '_lab', None)
        opts.setdefault('u' + str(pp), None)
        opts.setdefault('v' + str(pp), None)

    # Pull most things out of the opts dict into variables for cleaner code later on

    fname = opts['fname']
    suptitle = opts['suptitle']
    cbar_lab = opts['cbar_lab']
    cart_proj = opts['cart_proj']
    cart_xlim = opts['cart_xlim']
    cart_ylim = opts['cart_ylim']
    lons = opts['lons']
    lats = opts['lats']
    cmap = opts['cmap']
    bounds = opts['bounds']
    norm = opts['norm']
    extend = opts['extend']
    fontsize = opts['fontsize']
    figsize = opts['figsize']
    cbar_loc = opts['cbar_loc']
    borders = opts['borders']
    states = opts['states']
    oceans = opts['oceans']
    lakes = opts['lakes']
    rivers = opts['rivers']
    land = opts['land']
    water_color = opts['water_color']
    border_width = opts['border_width']
    lat_labels = opts['lat_labels']
    lon_labels = opts['lon_labels']
    suptitle_y = opts['suptitle_y']
    title_l = opts['title_l']
    title_r = opts['title_r']
    title_c = opts['title_c']
    map_x_thin = opts['map_x_thin']
    map_y_thin = opts['map_y_thin']
    barb_width = opts['barb_width']
    u = opts['u']
    v = opts['v']
    lg_text = opts['lg_text']
    lg_loc = opts['lg_loc']
    lg_fontsize = opts['lg_fontsize']
    single_cbar = opts['single_cbar']

    # Set some Matplotlib resources
    mpl.rcParams['figure.figsize'] = figsize
    mpl.rcParams['grid.color'] = 'gray'
    mpl.rcParams['grid.linestyle'] = ':'
    mpl.rcParams['font.size'] = fontsize + 2
    mpl.rcParams['figure.titlesize'] = fontsize + 2
    mpl.rcParams['savefig.bbox'] = 'tight'
    ll_size = fontsize - 2
    data_crs = ccrs.PlateCarree()

    print('-- Plotting ' + str(fname))

    # Define the figure and axes
    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols,
                           subplot_kw={'projection': cart_proj},)

    # If there's only one panel, axs can't be iterable or flattened below
    if n_panels == 1:
        print('ERROR: n_rows = 1 and n_cols = 1, so n_panels = 1.')
        print('       Function map_plot_panels requires more than just a single panel.')
        print('       If only a single-panel plot is desired, use function map_plot instead.\nExiting!')
        sys.exit(1)

    # axs is a 2D array of GeoAxes. Flatten it to a 1D array.
    axs = axs.flatten()

    # Iterate over the axes/panels
    for pp in range(n_panels):
        # Define some local variables for this loop
        # For naming the dictionary options, index from 1 instead of 0
        cont_var_pp = opts['cont' + str(pp + 1) + '_var']
        cont_levs_pp = opts['cont' + str(pp + 1) + '_levs']
        cont_color_pp = opts['cont' + str(pp + 1) + '_color']
        cont_width_pp = opts['cont' + str(pp + 1) + '_width']
        fill_var_pp = opts['fill_var' + str(pp + 1)]
        title_l_pp = opts['title_l' + str(pp + 1)]
        title_r_pp = opts['title_r' + str(pp + 1)]
        title_c_pp = opts['title_c' + str(pp + 1)]
        cmap_pp = opts['cmap' + str(pp + 1)]
        bounds_pp = opts['bounds' + str(pp + 1)]
        norm_pp = opts['norm' + str(pp + 1)]
        extend_pp = opts['extend' + str(pp + 1)]
        cbar_loc_pp = opts['cbar' + str(pp + 1) + '_loc']
        cbar_lab_pp = opts['cbar' + str(pp + 1) + '_lab']
        u_pp = opts['u' + str(pp + 1)]
        v_pp = opts['v' + str(pp + 1)]

        # If cart_xlim and cart_ylim tuples are not provided, then set plot limits from lat/lon data directly
        if cart_xlim is not None and cart_ylim is not None:
            axs[pp].set_xlim(cart_xlim)
            axs[pp].set_ylim(cart_ylim)
        else:
            axs[pp].set_extent([np.min(lons), np.max(lons), np.min(lats), np.max(lats)], crs=cart_proj)

        # If lons & lats are 1D, make them into 2D arrays
        if lons.ndim == 1 and lats.ndim == 1:
            ll2d = np.meshgrid(lons, lats)
            lons = ll2d[0]
            lats = ll2d[1]

        # Optional: Add various cartopy features
        if borders != None:
            axs[pp].add_feature(borders, linewidth=border_width, linestyle='-', zorder=3)
        if states != None:
            axs[pp].add_feature(states, linewidth=border_width / 3.0, edgecolor='black', zorder=4)
        if oceans != None:
            # Drawing the oceans can be VERY slow with Cartopy 0.20+ for some domains, so may want to skip it
            # Can set the facecolor for the axes to water_color instead (usually we want this 'none' except for terrain)
            axs[pp].add_feature(oceans, facecolor=water_color, zorder=2)
            # ax.add_feature(oceans, facecolor='none', zorder=2)
            # ax.set_facecolor(opts['water_color'])
        if lakes != None:
            # Unless facecolor='none', lakes w/ facecolor will appear above filled contour plot, which is undesirable
            axs[pp].add_feature(lakes, facecolor=water_color, linewidth=0.25, edgecolor='black', zorder=5)
        axs[pp].coastlines(zorder=6, linewidth=border_width)

        # Sometimes longitude labels show up on y-axis, and latitude labels on x-axis in older versions of Cartopy
        # Print lat/lon labels only for a specified set (determined by trial & error) to avoid this problem for now
        gl = axs[pp].gridlines(draw_labels=True, x_inline=False, y_inline=False)
        gl.rotate_labels = False
        # If specific lat/lon labels are not specified, then just label the default gridlines
        if lon_labels is not None:
            gl.xlocator = mticker.FixedLocator(lon_labels)
        if lat_labels is not None:
            gl.ylocator = mticker.FixedLocator(lat_labels)
        gl.top_labels = True
        gl.bottom_labels = True
        gl.left_labels = True
        gl.right_labels = True
        gl.xlabel_style = {'size': ll_size}
        gl.ylabel_style = {'size': ll_size}

        # Optional: Draw unfilled contours of another variable
        if cont_var_pp is not None:
            axs[pp].contour(wrf.to_np(lons), wrf.to_np(lats), wrf.to_np(cont_var_pp), cont_levs_pp,
                            colors=cont_color_pp, linewidths=cont_width_pp, transform=data_crs,
                            transform_first=(axs[pp], True))

        # Draw the actual filled contour plot
        # If the variable has the same shape as lats, then plot the filled contour field
        if fill_var_pp is None:
            print('ERROR: fill_var' + str(pp) + ' is None. Please provide an array for this fill variable. Exiting!')
            sys.exit(1)
        if fill_var_pp.shape == lats.shape:
            contourf = True
            cs = axs[pp].contourf(wrf.to_np(lons), wrf.to_np(lats), wrf.to_np(fill_var_pp), bounds,
                                  cmap=cmap_pp, norm=norm_pp, extend=extend_pp, transform=data_crs,
                                  transform_first=(axs[pp], True))
        # Otherwise, we presumably need to plot an empty map and then plot markers
        else:
            contourf = False
            if opts['mark1_lon'] is None or opts['mark1_lat'] is None:
                print('ERROR: map_plot_panels in map_funcs.py:')
                print('   var does not match the shape of lons or lats.')
                print('   If plotting a contour map, fix the mismatch in shape between fill_var and lons/lats.')
                print('   Otherwise, this could imply a need for a blank map with markers.')
                print('   However, mark1_lon and/or mark1_lat are not provided either.')
                print('   If a filled contour map is desired, ensure fill_var is the same shape as lons and lats.')
                print('   If a blank map with markers is desired instead, provide mark1_lon and mark1_lat.')
                print('   If the markers should be filled according to a data value, then set mark1_val_fill=True.')
                print(
                    '   Or if a future use case is identified that requires a blank map & no markers, then modify code.')
                print('   Exiting!')
                sys.exit()

        # Optional: Add up to n_sets of markers to the plot
        for nn in range(1, n_sets):
            mark_num = 'mark' + str(nn)
            mark_lon = opts[mark_num + '_lon']
            mark_lat = opts[mark_num + '_lat']
            mark_var = opts[mark_num + '_var']
            mark_size = opts[mark_num + '_size']
            mark_style = opts[mark_num + '_style']
            mark_width = opts[mark_num + '_width']
            mark_color = opts[mark_num + '_color']
            mark_zorder = opts[mark_num + '_zorder']
            mark_val_fill = opts[mark_num + '_val_fill']
            mark_edgecolor = opts[mark_num + '_edgecolor']

            if mark_lat is None or mark_lon is None:
                continue

            if mark_lat.shape != mark_lon.shape:
                print('ERROR: map_plot_panels in map_funcs.py:')
                print('       ' + mark_num + '_lat and ' + mark_num + '_lon do not have the same shape.')
                print('       Exiting!')
                sys.exit(1)
            if lg_text is None:
                lg_lab = None
            else:
                lg_lab = lg_text[nn - 1]
            if mark_val_fill:
                # Fill markers according to their data value, cmap, and norm
                # NOTE: If plotting markers over a blank map, must use plt.scatter, not ax.scatter,
                #       to avoid an error about the lack of a mappable when drawing the colorbar below.
                if mark_var.shape == mark_lat.shape:
                    if contourf:
                        axs[pp].scatter(mark_lon, mark_lat, c=mark_var, marker=mark_style, s=mark_size,
                                        edgecolors=mark_edgecolor, label=lg_lab, linewidths=mark_width,
                                        cmap=cmap_pp, norm=norm_pp, transform=data_crs, zorder=mark_zorder)
                    else:
                        # TODO: Determine if this causes a problem (it probably will, but can be dealt with then...)
                        plt.scatter(mark_lon, mark_lat, c=mark_var, marker=mark_style, s=mark_size,
                                    edgecolors=mark_edgecolor, label=lg_lab, linewidths=mark_width,
                                    cmap=cmap_pp, norm=norm_pp, transform=data_crs, zorder=mark_zorder)
                else:
                    print('ERROR: map_plot_panels in map_funcs.py:')
                    print('       ' + mark_num + '_var, ' + mark_num + '_lat, and ' + mark_num +
                          '_lon are not all the same shape.')
                    print('       Exiting!')
                    sys.exit(1)
            # Marker set not filled by any data values
            else:
                axs[pp].scatter(mark_lon, mark_lat, marker=mark_style, s=mark_size, color=mark_color,
                                edgecolors=mark_edgecolor, label=lg_lab, linewidths=mark_width,
                                transform=data_crs, zorder=mark_zorder)

        # Optional: Add up to n_sets of text labels to the plot
        for nn in range(1, n_sets):
            text_num = 'text' + str(nn)
            text_lab = opts[text_num + '_lab']
            text_lat = opts[text_num + '_lat']
            text_lon = opts[text_num + '_lon']
            text_lab_wt = opts[text_num + '_lab_wt']
            text_color = opts[text_num + '_color']
            if text_lab is not None and text_lat is not None and text_lon is not None:
                if len(text_lab) != len(text_lat) or len(text_lab) != len(text_lon):
                    print('ERROR: map_plot in map_funcs.py:')
                    print(
                        '       ' + text_num + '_lab, ' + text_num + '_lat, and ' + text_num + '_lon do not all have the same length.')
                    print('       Exiting!')
                    sys.exit(1)
                n_text = len(text_lab)
                # print('text_color = ' + text_color)
                for xx in range(n_text):
                    axs[pp].text(text_lon[xx], text_lat[xx], text_lab[xx], horizontalalignment='center',
                                 transform=data_crs, size=fontsize, zorder=13, weight=text_lab_wt, color=text_color)

        # Optional: Add up to n_sets polygons to the plot
        for nn in range(1, n_sets):
            poly_verts = opts['polygon' + str(nn) + '_verts']
            poly_color = opts['polygon' + str(nn) + '_color']
            if poly_verts is not None:
                n_vertices = poly_verts.shape[0]
                # Draw a line between each vertex of the polygon
                for vv in range(n_vertices):
                    lon_beg = poly_verts[vv][0]
                    lat_beg = poly_verts[vv][1]
                    if vv < n_vertices - 1:
                        lon_end = poly_verts[vv + 1][0]
                        lat_end = poly_verts[vv + 1][1]
                    else:  # loop back around to the first vertex
                        lon_end = poly_verts[0][0]
                        lat_end = poly_verts[0][1]
                    # Plot each side of the polygon (could optionally add a marker at each vertex if desired)
                    axs[pp].plot([lon_beg, lon_end], [lat_beg, lat_end], color=poly_color, linewidth=2,
                                 transform=data_crs)

        # Optional: Add titles to the subplot
        if title_l_pp is not None:
            axs[pp].set_title(title_l_pp, fontsize=fontsize, loc='left')
        if title_r_pp is not None:
            axs[pp].set_title(title_r_pp, fontsize=fontsize, loc='right')
        if title_c_pp is not None:
            axs[pp].set_title(title_c_pp, fontsize=fontsize, loc='center', fontweight='heavy')

        # Optional: Draw wind barbs
        if u_pp is not None and v_pp is not None:
            if isinstance(lons, np.ndarray):
                x_thin = lons[::map_y_thin, ::map_x_thin]
            else:
                x_thin = lons[::map_y_thin, ::map_x_thin].values
            if isinstance(lats, np.ndarray):
                y_thin = lats[::map_y_thin, ::map_x_thin]
            else:
                y_thin = lats[::map_y_thin, ::map_x_thin].values
            u_thin = u_pp[::map_y_thin, ::map_x_thin]
            v_thin = v_pp[::map_y_thin, ::map_x_thin]
            # Assume winds input to here are in m/s instead of kts, so reduce barb_increments from 5/10/50 to 2.5/5/25
            axs[pp].barbs(x_thin, y_thin, u_thin, v_thin, length=5, transform=data_crs, linewidth=barb_width,
                          barb_increments={'half': 2.5, 'full': 5, 'flag': 25})

        if not single_cbar:
            # Draw the colorbar
            # Credit: https://stackoverflow.com/questions/30030328/correct-placement-of-colorbar-relative-to-geo-axes-cartopy
            # Create colorbar axes (temporarily) anywhere
            cax = fig.add_axes([0, 0, 0.1, 0.1])
            # Find the location of the main plot axes
            posn = axs[pp].get_position()
            # Adjust the positioning and orientation of the colorbar, and then draw it
            # The colorbar will inherit the norm/extend attributes from the plt.contourf or plt.scatter call above
            if cbar_loc_pp == 'bottom':
                cax.set_position([posn.x0, posn.y0 - 0.09, posn.width, 0.03])
                fig.colorbar(cs, cax=cax, orientation='horizontal', label=cbar_lab_pp)
            elif cbar_loc_pp == 'right':
                cax.set_position([posn.x0 + posn.width + 0.05, posn.y0, 0.03, posn.height])
                fig.colorbar(cs, cax=cax, orientation='vertical', label=cbar_lab_pp)
            elif cbar_loc_pp == 'top' or cbar_loc_pp == 'left':
                print(
                    'WARNING: cbar_loc=' + cbar_loc_pp + ' requested. Unsupported option. Colorbar will not be drawn.')
                print('   Add directives in map_funcs.map_plot to handle that option and draw the colorbar.')

    # Draw a single colorbar for the whole plot
    if single_cbar:
        # Initially draw colobar axes somewhere (this is a good starting point for on the bottom)
        cax = fig.add_axes([0.2, 0.2, 0.6, 0.03])
        # Find the location of the last axis plotted (lower-right)
        posn = axs[-1].get_position()
        # Adjust the positioning and orientation of the colorbar, then draw it
        if cbar_loc == 'bottom':
            cax.set_position([0.2, posn.y0 - 0.06, 0.6, 0.03])
            fig.colorbar(cs, cax=cax, orientation='horizontal', label=cbar_lab)
        elif cbar_loc == 'right':
            cax.set_position([posn.x0 + posn.width + 0.05, posn.y0, 0.03, posn.height])
            fig.colorbar(cs, cax=cax, orientation='vertical', label=cbar_lab)

    # Add the overall plot title
    plt.suptitle(suptitle, y=suptitle_y)

    # Save and close the figure
    plt.savefig(fname)
    plt.close()
