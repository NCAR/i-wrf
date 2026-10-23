#PBS -N iwrf_re_demo
#PBS -l select=2:ncpus=128:mpiprocs=128
#PBS -l walltime=02:00:00
#PBS -q main
#PBS -j oe

WORKING_DIR=${WORKING_DIR:-${SCRATCH}/iwrf_re_demo}
source ${WORKING_DIR}/env_re_demo.sh
module load apptainer

export APPTAINER_BIND="${GEOG_DATA_DIR}:/home/wrfuser/terrestrial_data/geog,${WPS_FILES_DIR}:/home/wrfuser/terrestrial_data/wps_files,${HRRR_DATA_DIR}:/tmp/hrrr_data,${WRF_DATE_DIR}:/tmp/renewable_energy,${WORKING_DIR}/i-wrf/use_cases/Renewable_Energy/WRF/config:/tmp/renewable_energy/config,/var/spool/pbs:/var/spool/pbs,${APPTAINER_TMPDIR}:${APPTAINER_TMPDIR}"

apptainer exec ${WORKING_DIR}/iwrf_latest.sif /tmp/renewable_energy/run.sh
