# WRF-Chem Container (AlmaLinux 9)

Apptainer container definition for WRF-Chem 4.7.1 with WPS 4.6.0 and all preprocessing tools, built on AlmaLinux 9.

## Software Versions

| Component | Version |
|-----------|---------|
| WRF-Chem | 4.7.1 |
| WPS | 4.6.0 |
| HDF5 | 1.14.5 |
| NetCDF-C | 4.9.3 |
| NetCDF-Fortran | 4.6.2 |
| OpenMPI | System (AlmaLinux 9) |
| OS | AlmaLinux 9 |

### Preprocessing Tools (from [NCAR/WRF-Chem-Preprocessing-Tools](https://github.com/NCAR/WRF-Chem-Preprocessing-Tools))

- **mozbc** - Boundary/initial conditions from global models (WACCM/MOZART)
- **anthro_emis** - Anthropogenic emissions processing
- **fire_emis** - Fire emissions (FINN) processing
- **megan_bio_emiss** - Biogenic emissions (MEGAN) processing
- **wesely** - Dry deposition calculations
- **exo_coldens** - Photolysis column densities

## Building

### Single-layer build (recommended for distribution)

```bash
apptainer build --fakeroot wrf-chem_full_almalinux9.sif wrf-chem_full_almalinux9.def
```

Build takes approximately 1.5-2 hours and requires internet access to download source code from GitHub and Unidata.

### Multi-layer build (recommended for development)

Building in layers allows you to rebuild only the layer that changed (e.g., rebuild WRF without recompiling HDF5/NetCDF).

```bash
# Layer 1: OS base + HDF5 + NetCDF (~20 min)
apptainer build --fakeroot wrf-chem_deps_almalinux9.sif wrf-chem_deps_almalinux9.def

# Layer 2: Preprocessing tools (~5 min)
apptainer build --fakeroot wrf-chem_preproc_almalinux9.sif wrf-chem_preproc_almalinux9.def

# Layer 3: WRF-Chem 4.7.1 + WPS 4.6.0 (~60 min)
apptainer build --fakeroot wrf-chem_almalinux9.sif wrf-chem_almalinux9.def
```

### Build on an HPC cluster (e.g., Derecho)

When building on a cluster, use a compute node to avoid head-node resource limits. Set `APPTAINER_TMPDIR` to a filesystem with sufficient space (the default `/tmp` is often too small).

```bash
export APPTAINER_TMPDIR=/glade/derecho/scratch/$USER/apptainer_tmp
export APPTAINER_CACHEDIR=$HOME/.apptainer/cache
mkdir -p $APPTAINER_TMPDIR $APPTAINER_CACHEDIR

apptainer build --fakeroot wrf-chem_full_almalinux9.sif wrf-chem_full_almalinux9.def
```

### Build troubleshooting

If the build fails at the WRF compile step, check the compile log inside the container (sandbox mode is helpful for debugging):

```bash
# Build as a writable sandbox instead of SIF
apptainer build --fakeroot --sandbox wrf-chem_sandbox wrf-chem_full_almalinux9.def

# Shell into the sandbox to inspect
apptainer shell --fakeroot --writable wrf-chem_sandbox
```

## Running

### Interactive shell

```bash
apptainer shell wrf-chem_full_almalinux9.sif
```

### Execute a command

```bash
# Run WRF with 4 MPI processes
apptainer exec wrf-chem_full_almalinux9.sif mpirun -np 4 wrf.exe

# Run real.exe
apptainer exec wrf-chem_full_almalinux9.sif mpirun -np 4 real.exe

# Run mozbc (stdin redirection for input file)
apptainer exec wrf-chem_full_almalinux9.sif mpirun -np 1 mozbc < mozcart_icbc.inp
```

### Running on Derecho (PBS)

Bind-mount your working directories so the container can access data on GLADE. The `--pwd` flag sets the container's working directory, and `--env TMPDIR=` provides a writable location for OpenMPI session files.

```bash
module load apptainer

# Configuration
CONTAINER=/glade/work/$USER/containers/wrf-chem_full_almalinux9.sif
WORK_DIR=/glade/work/$USER/forecast/20250115
WRF_WORK_DIR=$WORK_DIR/wrf
TMPDIR=$WORK_DIR/tmp
mkdir -p $TMPDIR

# Bind mounts: make GLADE paths visible inside the container
BIND_OPTS="-B $WORK_DIR --env TMPDIR=$TMPDIR"

# Define reusable apptainer exec command
APPTAINER_EXEC="apptainer exec $BIND_OPTS --pwd $WRF_WORK_DIR $CONTAINER"

# Run real.exe (preprocessing)
$APPTAINER_EXEC mpirun -np 36 real.exe

# Run mozbc (boundary conditions from WACCM - reads input file via stdin)
$APPTAINER_EXEC mpirun -np 1 mozbc < mozcart_icbc.inp

# Run WRF-Chem (main forecast)
$APPTAINER_EXEC mpirun -np 256 wrf.exe
```

Key notes for Derecho:
- Load the apptainer module first: `module load apptainer`
- Use `--pwd` to set the working directory inside the container
- Bind-mount all filesystem paths the job needs (GLADE paths are not visible inside the container by default)
- Set `TMPDIR` via `--env` so OpenMPI can create session directories inside a writable location
- The operational scripts (`submit_aq_fcst.bash`, `submit_daily_wrf_jobs.bash`) handle all of this automatically via PBS job submission with dependency chains

## Container Internal Layout

```
/opt/
├── wrf-deps/              # HDF5 + NetCDF libraries
│   ├── bin/               # nc-config, nf-config, h5dump, etc.
│   ├── include/           # Header files
│   └── lib/               # Shared/static libraries
├── WRF/                   # WRF source tree (run/ directory with runtime files)
│   ├── run/               # Runtime data files (tables, coefficients)
│   ├── Registry/
│   └── doc/
├── WPS/                   # WPS configuration and support files
│   ├── geogrid/
│   ├── metgrid/
│   └── ungrib/
└── WRF-Chem-Preprocessing-Tools/
    ├── bin/               # Compiled preprocessing executables
    ├── mozbc/
    ├── anthro_emiss/
    ├── fire_emiss/
    ├── megan_bio_emiss/
    └── wes_coldens/

/wrf/bin/                  # All executables (in PATH)
    wrf.exe, real.exe, ndown.exe, tc.exe,
    geogrid.exe, ungrib.exe, metgrid.exe,
    link_grib.csh, util/
```

## Known Issues

### WRF 4.7.1 KPP compile bugs (patched in this def)

WRF 4.7.1 has two bugs in its KPP (Kinetic PreProcessor) integration that cause the compile to fail. Both are patched automatically in the def file:

1. **`compile_wkc` wrong relative path**: The `FIRST` call uses `../../inc/` but is invoked from `chem/KPP/mechanisms/$model`, requiring `../../../../inc/`.
2. **`tuv_kpp.c` buffer overflow**: `char openMode[1] = "a"` needs `[2]` to accommodate the null terminator.

### OpenMPI temporary directory

OpenMPI needs a writable temporary directory for session files. When running inside the container on a cluster, the default `/tmp` may not be writable or may be shared. Always set `TMPDIR` to a writable location via `--env TMPDIR=/path/to/writable/dir`.
