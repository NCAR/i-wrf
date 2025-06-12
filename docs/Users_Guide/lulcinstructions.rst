
Set Input, Output, and Configs Paths
====================================

Copy and paste the following lines to set up paths of the input, output, and configuration files::

    mkdir -p ~/lulc_output
    WRF_INPUT=~/lulc_input
    WRF_OUTPUT=~/lulc_output
    WRF_CONFIGS=~/lulc_configs



Run WPS and WRF Manually
========================

The instructions below will run WPS and WRF manually. It runs WPS and WRF and simulate the weather between 12:00, July 3 2017 to 15:00, July 3 2017, just a window of three hours over the Dallas-Fort Worth area. This simulation will take about 7 hours to run. If you would like to try the full simulation (between 12:00, July 3 2017 to 00:00, July 5 2017), read "Start WPS and WRF with a Script (Full Simulation)" Below.

You are ready to run the Docker container that will perform the simulation. First, make sure you are in a screen session. The command below starts the container and provides a shell prompt. From there, we will run each command one by one::

    sudo docker run --shm-size 100G -it \
    -v $WRF_INPUT:/home/wrfuser/lulc_input \
    -v $WRF_OUTPUT:/home/wrfuser/lulc_output \
    -v $WRF_CONFIGS:/home/wrfuser/lulc_configs \
    ncar/iwrf:lulc-2024-10-04 bash

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 100 -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:lulc-2024-10-04`` is the Docker image to use when creating the container.


Setting Up
----------
Set the container environment, ensure all required executables are in ``$PATH``, and address memory limits. First, source ``/etc/bashrc`` to load the environment, then allow unlimited stack size::

    source /etc/bashrc
    ulimit -s unlimited

And define some environment variables for input and output paths::

    WPS_DIR=/home/wrfuser/WPS
    WRF_DIR=/home/wrfuser/WRF
    WPS_INPUT=/home/wrfuser/lulc_input/WPS_input
    WRF_INPUT=/home/wrfuser/lulc_input/WRF_input
    CONFIGS=/home/wrfuser/lulc_configs
    OUTPUT=/home/wrfuser/lulc_output


Run WPS
-------

The first half of the instruction is to run **WRF Preprocessing Systems (WPS)** on geographic data and meteorological data. The WPS software is located at ``/home/wrfuser/WPS`` and the geographic data and meteorological data are in ``/home/wrfuser/lulc_input/WPS_input``, as ``WPS_GEOG`` and ``HRRR_0703``, respectively.

In WPS, the program ``geogrid.exe`` creates terrestrial data from static geographic data and defines the simulation domains. The section ``&geogrid`` in the ``namelist.wps`` directs ``geogrid.exe`` to read domain configuration parameters from ``WPS_GEOG``::

    cd $WPS_DIR
    cp ${CONFIGS}/WPS/namelist/namelist_geogrid.wps ${WPS_DIR}/namelist.wps
    ln -fs ${WPS_INPUT}/WPS_GEOG $WPS_DIR
    ./geogrid.exe

Next, the program ``ungrib.exe`` unpacks the meteorological data into WRF intermediate format. ``Vtable`` is used to specify which fields to unpack, by linking the Vtable file to ``${WPS_DIR}/Vtable``. The meteorological data consists of two formats, ``wrfprs`` and ``wrfnat``, which are linked and unpacked separately. The ``&ungrib`` section in ``namelist.wps`` specifies which files to use. Link the files and run ``ungrib.exe`` on ``wrfprs`` files to generate files with "HRRR_PRS" headers::

    cd $WPS_DIR
    cp ${CONFIGS}/WPS/namelist/namelist_ungrib_prs.wps ${WPS_DIR}/namelist.wps
    cp ${CONFIGS}/WPS/Vtable/Vtable.hrrr.modified ${WPS_DIR}/ungrib/Variable_Tables/
    ln -sf ${WPS_DIR}/ungrib/Variable_Tables/Vtable.hrrr.modified ${WPS_DIR}/Vtable
    ./link_grib.csh ${WPS_INPUT}/HRRR_0703/hrrr.*.wrfprs
    ./ungrib.exe

Link the files and run ``ungrib.exe`` on ``wrfnat`` files to generate files with "HRRR_NAT" headers using a new namelist containing a different ``&ungrib`` section::

    cd $WPS_DIR
    cp ${CONFIGS}/WPS/namelist/namelist_ungrib_nat.wps ${WPS_DIR}/namelist.wps
    ./link_grib.csh ${WPS_INPUT}/HRRR_0703/hrrr.*.wrfnat
    ./ungrib.exe

The last step is to call ``metgrid.exe`` to interpolate the meteorological data onto the simulation domain, and the outputs of ``metgrid.exe`` are used as inputs to ``WRF``. This process is guided by the ``&metgrid`` section of ``namelist.wps``::

    cd $WPS_DIR
    cp ${CONFIGS}/WPS/namelist/namelist_metgrid.wps ${WPS_DIR}/namelist.wps
    ./metgrid.exe


Run WRF
-------

The latter half of the exercise involves running two WRF simulations to investigate the impact of land use and land cover (LULC) on simulated deep convection over different sizes of the Dallas-Fort Worth (DFW) area. The first simulation is a control simulation using data generated from the previous WPS steps. The second simulation is a perturbed simulation with modified data, where the DFW area is expanded to four times its original size.


Control Simulation
^^^^^^^^^^^^^^^^^^

The control simulation runs WRF with the outputs generated from the previous WPS steps. Copy the relevant namelist, define environment variabless, and link the ``met_em`` files from WPS::

    cd $WRF_DIR
    ln -sf ${WRF_DIR}/run/* ${WRF_DIR}
    cp ${CONFIGS}/WRF/namelist/namelist.input $WRF_DIR
    cp ${CONFIGS}/WRF/ctl/wrfvar_lulc_*.txt $WRF_DIR
    ln -sf ${WPS_DIR}/met_em* $WRF_DIR


The WRF software is located at ``/home/wrfuser/WRF``, which contains two programs, ``real.exe`` and ``wrf.exe``. ``real.exe`` vertically interpolates the outputs of ``metgrid.exe`` and generates boundary and initial conditions: ``wrfbdy_d01``, ``wrfinput_d01``, ``wrfinput_d02``, and ``wrfinput_d03``::

    cd $WRF_DIR
    ./main/real.exe


Create a directory named ``wrfdata`` in the WRF directory to store the output from WRF and run WRF simulation with 60 CPU cores. If you had used a different flavor on this instance, adjust the CPU core count to a suitable number::
    
    cd $WRF_DIR
    mkdir -p ${WRF_DIR}/wrfdata
    mpiexec -n 60 -ppn 60 ./main/wrf.exe

This step will take about 3 hours to run. When it's finished, move the outputs from ``wrfdata`` to the output directory::

    mv ${WRF_DIR}/wrfdata ${OUTPUT}/ctl


DFW4X Simulation
^^^^^^^^^^^^^^^^

The perturbed simulation will modify the inputs such that the DFW area is four times its original size. Instead of making modifications on our own, the modified data is provided. 

First, remove the files used for the control simulation::

    cd $WRF_DIR
    rm met_em*
    rm wrfbdy_d01
    rm wrfinput*

Link the appropriate files for DFW4X simulation::

    ln -sf ${WRF_DIR}/run/* $WRF_DIR
    ln -sf ${WRF_INPUT}/dfw4x/wrfbdy_d01 $WRF_DIR
    ln -sf ${WRF_INPUT}/dfw4x/wrfinput* $WRF_DIR
    ln -sf ${WRF_INPUT}/dfw4x/met_em* $WRF_DIR

Create a directory named ``wrfdata`` in the WRF directory to store the output from WRF and run WRF simulation with 60 CPU cores. If you had used a different flavor on this instance, adjust the CPU core count to a suitable number::
    
    cd $WRF_DIR
    mkdir -p ${WRF_DIR}/wrfdata
    mpiexec -n 60 -ppn 60 ./main/wrf.exe

When it's finished, move the outputs from ``wrfdata`` to the output directory::

    mv ${WRF_DIR}/wrfdata ${OUTPUT}/dfw4x

After moving the outputs, you may exit the container by entering ``exit``.



Start WPS and WRF with a Script (Full Simulation)
=================================================

If would like to run WPS and WPS for the entire duration, from 12:00, July 3 2017 to 00:00, July 5 2017, you can use the script ``run_full.sh`` provided in the ``~/lulc_configs`` directory. 

First, make sure you are in a screen session. If you would like to run the entire process in one command, you just have to run the script. If you had used a different flavor than c64.m120 on this instance, adjust the CPU core count to a suitable number in the script (e.g. ``mpiexec -n 60 -ppn 60 ./main/wrf.exe`` to ``mpiexec -n 28 -ppn 28 ./main/wrf.exe`` for the c28.m224 flavor).

The script runs inside the container, prints lots of status information, and creates output files in the output directory you created. Execute this command to start a container with the image we pulled::
 
    sudo docker run --shm-size 100G -it \
    -v $WRF_INPUT:/home/wrfuser/lulc_input \
    -v $WRF_OUTPUT:/home/wrfuser/lulc_output \
    -v $WRF_CONFIGS:/home/wrfuser/lulc_configs \
    ncar/iwrf:lulc-2024-10-04 /home/wrfuser/lulc_configs/run_full.sh

The command has numerous arguments and options, which do the following:

* ``docker run`` creates the container if needed and then runs it.
* ``--shm-size 100 -it`` tells the command how much shared memory to use, and to run interactively in the shell.
* The ``-v`` options map folders in your cloud instance to paths within the container.
* ``ncar/iwrf:lulc-2024-10-04`` is the Docker image to use when creating the container.

The simulation will take about 4 days to run, and when the results are ready, the terminal will become available again. The output files will be in the ``lulc_output`` directory in the home directory. See the section below for instructions on how to view the outputs.



View Outputs
============

To view the outputs in the ``lulc_output`` directory, you must get read permission::

    sudo chmod -R a+r $WRF_OUTPUT

Use the ``ls`` command to list the files in the ``ctl`` or ``dfw4x`` directory::

    ls $WRF_OUTPUT/ctl
    ls $WRF_OUTPUT/dfw4x
