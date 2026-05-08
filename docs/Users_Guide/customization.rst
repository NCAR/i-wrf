.. _customization:

*************
Customization
*************

WRF
===

This section contains WRF customization options for users to modify existing use cases. Locate the use case you are interested in for additional options that explore some of the WRF settings. 

Hurricane Matthew
-----------------

#. Change the physics suite

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

Visualization
=============
