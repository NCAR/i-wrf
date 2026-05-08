# How to create input data volumes

Input will need to be uploaded to DockerHub following both sets of instructions because data volumes are mounted to Docker and Apptainer differently.

## Stage the data

* Create a working directory
* Under the working directory, create stage/obs directory to stage observation data
* Add data files to the staging directory

## Docker

* Copy the Dockerfiles into the working directory

```
cp i-wrf/docker/matthew/input/Dockerfile /path/to/working_dir/
```

* Run Docker commands to build the image and push it to DockerHub

### Observation input data
```
docker build -t ncar/iwrf-data:matthew-input-obs.docker .
docker push ncar/iwrf-data:matthew-input-obs.docker
```

## Apptainer

The following instructions were run on casper from the stage directory.

Load the apptainer module:
```
module load apptainer
```

### Observation input data
```
mksquashfs obs/ input_obs.squashfs
apptainer sif new input_obs.sif
apptainer sif add --datatype 4 --partarch 2 --partfs 1 --parttype 3 input_obs.sif input_obs.squashfs

apptainer registry login --username MY_USERNAME oras://registry-1.docker.io
apptainer push -U input_obs.sif oras://registry-1.docker.io/ncar/iwrf-data:matthew-input-obs.apptainer
```
