# Data Standard

This standard defines the minimum information required for a multiphase-flow
dataset to be reusable by researchers who were not involved in producing it.

## Required Metadata

Every dataset record should include:

- stable dataset id;
- title and short description;
- version;
- authors and contact;
- license;
- persistent URL or DOI;
- recommended citation;
- checksum for each downloadable archive;
- flow configuration;
- phases and material properties;
- numerical or experimental method;
- variables, units, array shapes, and coordinate conventions;
- train/validation/test split if the dataset is intended for AI;
- preprocessing and normalization steps;
- known limitations.

## Multiphase Core Variables

Unlike combustion DNS datasets, multiphase-flow datasets cannot require one
single universal list of fields for every contribution. VOF, level-set,
front-tracking, phase-field, particle methods, and experiments expose different
native variables. The standard therefore uses three levels.

### Level 1: Required for Every Dataset

Every dataset must provide enough information to identify phases and interpret
space/time:

- phase indicator or interface representation, for example `alpha`, `phi`,
  interface mesh, mask, particle labels, or segmented image;
- grid or coordinates;
- time or snapshot id;
- phase convention, for example `alpha=1` means liquid and `alpha=0` means gas;
- boundary conditions and initial conditions;
- material properties or enough information to reconstruct them;
- units and coordinate order.

For VOF-style datasets, the preferred phase-indicator variable is:

```text
alpha
```

with:

```text
alpha = 1: liquid phase
alpha = 0: gas phase
0 < alpha < 1: interfacial cell
```

### Level 2: Required for Flow-Field Simulation Datasets

If the dataset claims to provide a flow field, it should include:

- velocity components: `u`, `v`, and `w` for 3D, or `u`, `v` for 2D;
- pressure: `p`;
- phase indicator: `alpha`, `phi`, mask, or interface geometry;
- density and viscosity, either as fields `rho`, `mu` or as phase constants plus
  a mixing rule;
- surface tension coefficient `sigma` when capillarity is active;
- gravity or body-force vector when relevant.

### Level 3: Recommended for Interface-Learning Datasets

For AI tasks such as super-resolution, interface reconstruction, curvature
closure, breakup prediction, or segmentation, contributors should include or
document how to compute:

- interface normal: `nx`, `ny`, `nz`;
- curvature: `kappa`;
- signed-distance or level-set field: `phi`;
- interface area density;
- cell volume, face area, and grid spacing;
- train/validation/test split;
- baseline numerical operator or model;
- evaluation metrics.

## `multiphase_info.json`

Each dataset should include a `multiphase_info.json` file following the
BlastNet-style split between global metadata and local sample metadata:

```text
multiphase_info.json
  global: dataset-level physics, method, grid, variables, license, citation
  local: case-level or snapshot-level file paths, times, and parameters
```

Templates are provided in:

```text
templates/multiphase_info.template.json
templates/multiphase_info.schema.json
```

The `global.variables` list is the authoritative declaration of variable names,
units, shapes, locations, and conventions. The `local` section maps each case or
snapshot to actual files.

## Recommended File Layout

```text
dataset_name/
  README.md
  dataset_info.json
  checksums.sha256
  data/
    train/
    val/
    test/
  metadata/
  scripts/
    load_example.py
    reproduce_preprocessing.py
  figures/
```

Large datasets may use a different storage layout, but `dataset_info.json` and
checksums should remain available at the top level.

## Preferred Formats

Use formats with stable readers in Python and common HPC environments:

- `HDF5` or `Zarr` for large multidimensional fields;
- `NetCDF` for geoscience-style gridded data;
- `NPZ` for compact AI-ready tensors;
- `VTK`, `XDMF/HDF5`, or `EnSight` for CFD visualization outputs;
- `CSV` or `Parquet` for scalar diagnostics and benchmark metrics.

Avoid undocumented binary dumps unless a tested loader is provided.

## Coordinate and Unit Conventions

Each dataset must specify:

- coordinate order, for example `[x, y, z]`, `[i, j, k]`, or `[z, y, x]`;
- cell-centered versus node-centered storage;
- physical units;
- nondimensionalization;
- domain size and grid spacing;
- boundary conditions;
- whether fields are instantaneous snapshots, time series, or derived patches.

## AI Benchmark Requirements

AI-ready datasets should additionally provide:

- train/validation/test split policy;
- leakage prevention rule, for example split by case, geometry, or Reynolds
  number rather than random patches only;
- baseline model or baseline numerical operator;
- evaluation metrics;
- preprocessing scripts;
- a minimal data loader.
