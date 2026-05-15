.. _customization:

*************
Customization
*************

WRF
===

This section contains WRF customization options for users to modify existing use cases. Locate the use case you are interested in for additional options that explore some of the WRF settings. 

Hurricane Matthew
-----------------

#. Change The Physics Suite

For this customized change, updating the physics suite will have a noticable impact on the final output of the use case. This is due to each physics suite having its own physics packages associated with it, and how those packages will ultimately influence the entire life cycle of the hurricane.

In the "namelist.input" file, update 

  physics_suite = 'CONUS'

to the following

  physics_suite = 'tropical'

After this adjustment, run the use case as described. You should find that the WRF plots and METplus statistical output has changed.

METplus
=======

This section contains METplus configuration customization options for users to modify existing use cases. Locate the use case you are interested in for additional options that explore some of the METplus confiugration settings. 

Hurricane Matthew
-----------------

#. Create A Mask For Regional Focus Using GenVxMask

Currently, this use case utilizes the entire forecast domain area for verification. This can be seen in the setting

  POINT_STAT_MASK_GRID = FULL

Sometimes meaningful details in large-scale events like a hurricane can be lost when the domain is left to FULL. By creating a mask in the GenVxMask tool, the use case verification area will be limited to the mask, allowing better visualization of the end results.

Begin by adding an instance of GenVxMask to the PROCESS_LIST, ensuring that it is added before any PointStat instances are run. It should look like the following:

  PROCESS_LIST = MADIS2NC(metar), MADIS2NC(raob), **GenVxMask**, PointStat(surface), PointStat(upper_air), UserScript(wrf_plot), UserScript(metplotpy)

Now, set the input template for the input file, as well as the template for the mask file. Be sure to also create an output template for the resulting mask file. Since the mask will be created from latitude and longitude points, the mask file template is ignored by METplus (but must still exist!). The additions should look like this:

  **GEN_VX_MASK_INPUT_TEMPLATE = /data/input/wrf/{init?fmt=%Y%m%d_%H}/wrfout_d01_{valid?fmt=%Y-%m-%d_%H:%M:%S}**

  **GEN_VX_MASK_INPUT_MASK_TEMPLATE = /data/input/wrf/{init?fmt=%Y%m%d_%H}/wrfout_d01_{valid?fmt=%Y-%m-%d_%H:%M:%S}**

  **GEN_VX_MASK_OUTPUT_TEMPLATE = {OUTPUT_BASE}/genvxmask/LatLonMask.nc**

To avoid having this mask be overwritten each time the initialization time is incremented, add the **GEN_VX_MASK_SKIP_IF_OUTPUT_EXISTS** setting to the configuration file. This will allow GenVxMask to skip file creation if it detects that the mask file already exists. It should be set as follows:

  **GEN_VX_MASK_SKIP_IF_OUTPUT_EXISTS = True**

Now, add the latitude and longitude values of focus, as well as a proper **-type** flag so the GenVxMask tool knows what type of mask to create. This is completed through the **GEN_VX_MASK_OPTIONS** setting. The latitude and longitude bounds can be set as desired; for the purposes of this exercise, they are set to the following:

  **GEN_VX_MASK_OPTIONS = -type lat,lon -thresh ge12&&le36, le-57&&ge-81**

This example restricts the masking region between latitude values of 12 and 36 degrees North, and longitude values of -57 and -81 degrees West. 

Now run the use case as described. You should find that the WRF plots and METplus statistical output has changed. Changing the latitude and longitude bounds will result in different output; take some time to adjust the values to see the end result.

#. Create Thresholds For TMP Variable For Categorical Statistics 

Currently this use case generates continuous statistics, as well as wind field statistics. By adding thresholds to any of the variable fields, categorical statistics can be requested. These statistics can provide new and insightful information on how the chosen category of forecast values performed against observational data, allowing fine-tuning of model runs.

Visualization
=============
