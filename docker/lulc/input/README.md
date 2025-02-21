# How to create input data volumes

Input will need to be uploaded to DockerHub following both sets of instructions because data volumes are mounted to Docker and Apptainer differently.

## Stage the data

* Create a working directory
* Under the working directory, create directories stage/wrf and stage/obs to stage WRF and observation data respectively
* Add data files to the appropriate staging directories

## Docker

* Copy the Dockerfiles into the working directory

```
cp i-wrf/docker/lulc/input/Dockerfile* /path/to/working_dir/
```

* Run Docker commands to build the images and push them to DockerHub

### WRF input data
```
docker build -t ncar/iwrf:data-lulc-input-wrf-d03.docker -f Dockerfile.wrf .
docker push ncar/iwrf:data-lulc-input-wrf-d03.docker
```

### Observation input data
```
docker build -t ncar/iwrf:data-lulc-input-obs-d03.docker -f Dockerfile.obs .
docker push ncar/iwrf:data-lulc-input-obs-d03.docker
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

apptainer remote login --username MY_USERNAME oras://registry-1.docker.io
apptainer push -U input_wrf.sif oras://registry-1.docker.io/ncar/iwrf:data-lulc-input-wrf-d03.apptainer
```

### Observation input data
```
mksquashfs obs/ input_obs.squashfs
apptainer sif new input_obs.sif
apptainer sif add --datatype 4 --partarch 2 --partfs 1 --parttype 3 input_obs.sif input_obs.squashfs

apptainer remote login --username MY_USERNAME oras://registry-1.docker.io
apptainer push -U input_obs.sif oras://registry-1.docker.io/ncar/iwrf:data-lulc-input-obs-d03.apptainer
```

