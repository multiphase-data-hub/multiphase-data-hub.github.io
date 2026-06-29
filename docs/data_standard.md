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

