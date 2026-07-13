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

## Multiphase Simulation Variables

The primary catalogue target is multiphase-flow simulation data. The standard
therefore defines required flow-field variables and keeps fixed case parameters
separate from stored field variables.

### Required Stored Fields

A complete multiphase-flow simulation dataset should include:

- phase indicator or interface representation: `alpha`, `phi`, interface mesh,
  or equivalent;
- velocity components: `u`, `v`, and `w` for 3D, or `u` and `v` for 2D;
- pressure: `p`;
- grid or coordinates;
- time or snapshot id.

For VOF datasets, the preferred phase-indicator variable is:

```text
alpha
```

with:

```text
alpha = 1: liquid phase
alpha = 0: gas phase
0 < alpha < 1: interfacial cell
```

For level-set datasets, the preferred interface variable is:

```text
phi
```

with the sign convention explicitly documented.

### Required Case Parameters

The following quantities are usually fixed settings of a simulation case and
should be stored as metadata, not as default field variables:

- phase densities, for example `rho_liquid`, `rho_gas`;
- phase dynamic viscosities, for example `mu_liquid`, `mu_gas`;
- surface tension coefficient `sigma`;
- gravity or body-force vector `g`;
- contact angle or wall-wetting model parameters;
- Reynolds, Weber, Capillary, Froude, Bond, Ohnesorge, or Atwood numbers when
  relevant;
- boundary conditions and initial conditions.

Only store `rho`, `mu`, `sigma`, or `g` as variables when they genuinely vary in
space/time or are part of the solver output being released. In that case their
variable role should be `material_property_field` or `derived_diagnostic`.

### Optional Derived Fields

Datasets may additionally include derived fields when they are available and
useful:

- interface normal: `nx`, `ny`, `nz`;
- curvature: `kappa`;
- interface area density;
- vorticity;
- strain-rate or dissipation diagnostics;
- cell volume, face area, and grid spacing if not obvious from the grid;
- temperature or species fields for thermally coupled or reacting multiphase
  simulations.

Derived fields should never replace the required primitive flow fields unless
the dataset is explicitly documented as a reduced derived product.

### Benchmark Metadata

If the dataset is intended for model development or benchmarking, it should also
provide:

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
units, shapes, locations, and conventions. Fixed physical settings belong in
`global.physics.physical_parameters` or `local.case_parameters`, while the
`local` section maps each case or snapshot to actual field files.

For Kaggle packages, see `docs/kaggle_dataset_package_standard.md` for the
required package files and accepted data-format classes.

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

## Benchmark Requirements

Datasets intended for machine-learning or numerical-method benchmarks should
additionally provide:

- train/validation/test split policy;
- leakage prevention rule, for example split by case, geometry, or Reynolds
  number rather than random patches only;
- baseline model or baseline numerical operator;
- evaluation metrics;
- preprocessing scripts;
- a minimal data loader.
