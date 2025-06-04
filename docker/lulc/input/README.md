# How to create input data volumes

Input will need to be uploaded to DockerHub following both sets of instructions because data volumes are mounted to Docker and Apptainer differently.

## Stage the data

* Create a working directory
* Under the working directory, create directories stage/wrf and stage/obs to stage WRF and observation data respectively
* Add the observation data files to the stage/obs staging directories
* Subset the WRF data to remove fields that are not used by the use cases.

### Subset WRF data

This assumes that the full WRF files are in a directory called full/wrf and the stage/wrf directory already exists.

### Subset hourly files to include RAINC, RAINNC, REFD_MAX, HAILNC, HAIL_MAX2D, and dimension variables

```
for f in full/wrf/wrfout_d03_2017-07-0*00.morr*
do
    echo ncks -v Times,XLAT,XLONG,RAINC,RAINNC,REFD_MAX,HAILNC,HAIL_MAX2D $f stage${f:4}
    ncks -v Times,XLAT,XLONG,RAINC,RAINNC,REFD_MAX,HAILNC,HAIL_MAX2D $f stage${f:4}
done
```

### Subset 10 minute files to include RAINC, RAINNC, HAILNC, and dimension variables

```
for minutes in 10 20 30 40 50
do
    for f in full/wrf/wrfout_d03_2017-07-0*${minutes}.morr*
    do
        echo ncks -v Times,XLAT,XLONG,RAINC,RAINNC,HAILNC $f stage${f:4}
        ncks -v Times,XLAT,XLONG,RAINC,RAINNC,HAILNC $f stage${f:4}
    done
done
```

## Docker

* Copy the Dockerfiles into the working directory

```
cp i-wrf/docker/lulc/input/Dockerfile* /path/to/working_dir/
```

* Run Docker commands to build the images and push them to DockerHub

### WRF input data
```
docker build -t ncar/iwrf-data:lulc-input-wrf-d03.docker -f Dockerfile.wrf .
docker push ncar/iwrf-data:lulc-input-wrf-d03.docker
```

### Observation input data
```
docker build -t ncar/iwrf-data:lulc-input-obs-d03.docker -f Dockerfile.obs .
docker push ncar/iwrf-data:lulc-input-obs-d03.docker
```

## Apptainer

The following instructions were run on casper from the stage directory.

Load the apptainer module:
```
module load apptainer
```

### WRF input data
```
mksquashfs wrf/ input_wrf.squashfs
apptainer sif new input_wrf.sif
apptainer sif add --datatype 4 --partarch 2 --partfs 1 --parttype 3 input_wrf.sif input_wrf.squashfs

apptainer registry login --username MY_USERNAME oras://registry-1.docker.io
apptainer push -U input_wrf.sif oras://registry-1.docker.io/ncar/iwrf-data:lulc-input-wrf-d03.apptainer
```

### Observation input data
```
mksquashfs obs/ input_obs.squashfs
apptainer sif new input_obs.sif
apptainer sif add --datatype 4 --partarch 2 --partfs 1 --parttype 3 input_obs.sif input_obs.squashfs

apptainer registry login --username MY_USERNAME oras://registry-1.docker.io
apptainer push -U input_obs.sif oras://registry-1.docker.io/ncar/iwrf-data:lulc-input-obs-d03.apptainer
```
