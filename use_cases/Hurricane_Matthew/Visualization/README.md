# plot_wrf
Python scripts and functions to make nice plots of WRF model output using Cartopy.

plot_wrf.py can be called with a set of arguments (use option -h to get the current usage statement):

```
> python plot_wrf.py -h
usage: plot_wrf.py [-h] [-w WRF_DIR_PARENT] [-o OUT_DIR_PARENT] [-f CYCLE_DT_FIRST] [-l CYCLE_DT_LAST]
                   [-i CYCLE_STRIDE_H] [-b BEG_LEAD_TIME] [-e END_LEAD_TIME] [-s STR_LEAD_TIME] [-d DOMAIN]

options:
  -h, --help            show this help message and exit
  -w WRF_DIR_PARENT, --wrf_dir_parent WRF_DIR_PARENT
                        string specifying the directory path to the parent WRF output directories, above any
                        experiment or cycle datetime subdirectories (default:
                        /glade/derecho/scratch/jaredlee/nsf_i-wrf/matthew)
  -o OUT_DIR_PARENT, --out_dir_parent OUT_DIR_PARENT
                        string specifying the directory path to the parent plot directories (default: same as
                        --wrf_dir_parent)
  -f CYCLE_DT_FIRST, --cycle_dt_first CYCLE_DT_FIRST
                        beginning date/time of first WRF simulation [YYYYMMDD_HH] (default: 20161006_00)
  -l CYCLE_DT_LAST, --cycle_dt_last CYCLE_DT_LAST
                        beginning date/time of last WRF simulation [YYYYMMDD_HH]
  -i CYCLE_STRIDE_H, --cycle_stride_h CYCLE_STRIDE_H
                        stride in hours between cycles (default: 24)
  -b BEG_LEAD_TIME, --beg_lead_time BEG_LEAD_TIME
                        beginning lead time for plotting WRF simulations [HH:MM] (default: 00:00)
  -e END_LEAD_TIME, --end_lead_time END_LEAD_TIME
                        ending lead time for plotting WRF simulations [HH:MM] (default: 48:00)
  -s STR_LEAD_TIME, --str_lead_time STR_LEAD_TIME
                        stride to create plots every N minutes (default: 180)
  -d DOMAIN, --domain DOMAIN
                        WRF domain number to be plotted (default: 1)
```

The plot_wrf.parse_args function creates a dictionary of options that is then passed to the main routine. Doing this via a dictionary object should make it simpler to add even more customization/options in the future, requiring changes in fewer places than passing numerous positional arguments around.

The plot_wrf script opens specified wrfout files in sequence, reads in user-specified variables (currently set with options like plot_TERRAIN = True and plot_T2 = False in the main function), creates a dictionary of plotting options that is then passed to map_funcs.map_plot to create and save each plot to a file. Inside the main function there are also user-settable boolean flags to turn on/off plotting surface wind barb overlays, labeled stations/cities, etc.

Both these requested variables for plotting and other plot customization options could eventually be changed to be passed in on the command line to not require users to modify the script itself before running it, but that is left for future development.
