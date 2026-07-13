# Kaggle Dataset Package Standard for Multiphase-Flow Data

This document defines the recommended file structure and metadata requirements
for publishing multiphase-flow datasets on Kaggle and indexing them in
Multiphase Data Hub.

The primary goal is practical reuse: a downloader should be able to read the
field data with Python, reconstruct the grid and variables, and build their own
task-specific training dataset.

## Core Principle

The raw data format is not forced. Contributors may upload solver-native CFD
outputs or preprocessed machine-learning arrays. However, the metadata must be
complete enough for a third-party user to read and interpret the data without
private knowledge from the authors.

## Dataset Format Classes

### Class A: Preprocessed Array Datasets

Use this class when the data have already been converted into machine-learning
friendly arrays.

Typical formats:

```text
.npy
.npz
.h5 / .hdf5
.zarr
.nc / NetCDF
```

Examples:

```text
data/train.npz
data/val.npz
data/test.npz
data/fields.h5
```

Required metadata:

- array names;
- array shapes;
- dtype;
- units;
- normalization or nondimensionalization;
- train/validation/test split, if present;
- relation between arrays, for example input/output pairs, HR/LR pairs, or
  fields/labels;
- coordinate order, for example `[z, y, x]` or `[x, y, z]`;
- whether arrays are cell-centered or node-centered.

Recommended files:

```text
load_example.py
```

The loader should show how to load at least one sample and print its shape.

### Class B: Standard CFD Field Files

Use this class when data are stored in common CFD or visualization formats.

Typical formats:

```text
.dat
.vtk / .vti / .vtu / .vtr
.xdmf + .h5
EnSight Gold case/geometry/variable files
OpenFOAM time directories
Basilisk outputs
```

Required metadata:

- file format;
- variable names and physical meanings;
- units;
- grid type;
- grid dimensions;
- coordinate source, for example analytic uniform grid, coordinate files, or
  mesh file;
- field location, for example cell-centered, node-centered, face-centered;
- snapshot/time-step mapping;
- file path pattern;
- whether the files can be opened directly by common readers such as PyVista,
  meshio, h5py, xarray, or custom code.

Required additional files:

- mesh, geometry, or coordinate files when the grid cannot be reconstructed from
  metadata alone;
- a case/index file when needed to associate variables and time steps.

For uniform Cartesian grids, coordinate files are not required if `info.json`
fully specifies the domain bounds, dimensions, spacing, and axis convention.

Recommended files:

```text
load_example.py
```

This is strongly recommended even when the format is common, because solver
output conventions vary.

### Class C: Solver-Specific Binary Files Without Extension

Use this class when the data are raw or semi-raw CFD binary files with no
standard extension or no self-describing structure.

Examples:

```text
Gvol.000001
V.000001
P.000001
VOF.000001
field000120
```

This class is acceptable, but only if the package includes explicit reading
instructions.

Required metadata:

- binary format description;
- header size in bytes;
- dtype;
- endianness;
- payload shape;
- vector component layout, if applicable;
- reshape order;
- file path pattern;
- units;
- grid dimensions and coordinate convention;
- example code that reads at least one field correctly.

Required additional file:

```text
load_example.py
```

For this class, `load_example.py` is mandatory. Without it, most external users
cannot reliably decode the data.

## Required Package Files

Every Kaggle dataset package must include:

```text
dataset-metadata.json
info.json
data/
```

### `dataset-metadata.json`

This is required by Kaggle.

Minimum content:

```json
{
  "title": "Dataset title",
  "id": "kaggle-user/dataset-slug",
  "licenses": [
    {
      "name": "CC-BY-4.0"
    }
  ]
}
```

The owner in `id` must match the Kaggle username in `~/.kaggle/kaggle.json`.

### `info.json`

This is the authoritative metadata file for Multiphase Data Hub. It should not
be treated as optional documentation.

Required `global` fields:

- `dataset_id`;
- `title`;
- `description`;
- `format`;
- `snapshots` or number of samples;
- `variables`;
- `grid`;
- `physics`;
- `contributors`;
- `license`;
- `doi` or citation note;
- `known_limitations`, if any.

Required `local` records:

- snapshot/sample id;
- time value if available;
- file paths for each variable included in that snapshot/sample.

The `info.json` must match the actual uploaded files. If only `Gvol` is
uploaded, `info.json` must not list missing variables such as velocity or
pressure as available files.

### `data/`

The `data/` directory contains the actual field data. Subdirectories are
recommended:

```text
data/Gvol/
data/V/
data/P/
data/train/
data/test/
```

The layout may differ by dataset, but it must be described in `info.json`.

## Strongly Recommended Files

### `load_example.py`

Recommended for all datasets and mandatory for solver-specific binary files.

The script should:

- run from the dataset root directory;
- read at least one sample/snapshot;
- print variable names, shapes, dtype, min, and max;
- avoid requiring private code;
- use common Python packages where possible.

For large datasets, the loader may read only one file or one slice.

### `README.md`

Recommended but should remain short. It does not need to repeat all metadata in
`info.json`.

Suggested content:

```text
Dataset name
One-paragraph description
List of included variables
Instruction: see info.json for full metadata
Instruction: use load_example.py for Python reading
Kaggle/DOI citation note
```

### `checksums.sha256`

Recommended for integrity verification, especially for large binary datasets.

Generate with:

```bash
find . -type f ! -name checksums.sha256 -print0 | sort -z | xargs -0 sha256sum > checksums.sha256
```

## Optional Files

Include these only when useful:

```text
figures/
scripts/
grid/
metadata/
case files
mesh files
```

Examples:

- preview images;
- conversion scripts;
- preprocessing scripts;
- train/validation/test split files;
- solver input files;
- mesh or coordinate files;
- original case file for ParaView/EnSight/OpenFOAM.

## Minimum `info.json` Template

```json
{
  "schema_version": "0.1.0",
  "dataset_type": "multiphase_flow_simulation",
  "global": {
    "dataset_id": "kaggle-user/dataset-slug",
    "title": "Dataset title",
    "description": "Short dataset description.",
    "format": "NPZ / HDF5 / VTK / EnSight binary / custom binary",
    "snapshots": 1,
    "variables": ["Gvol", "V", "P"],
    "grid": {
      "type": "uniform_cartesian",
      "cell_dims": [256, 256, 256],
      "domain_bounds_xyz": [[-3.14159, 3.14159], [-3.14159, 3.14159], [-3.14159, 3.14159]],
      "field_location": "cell_centered",
      "coordinate_order": "x,y,z"
    },
    "physics": {
      "flow_type": "two_phase_flow",
      "configuration": "droplet breakup in homogeneous isotropic turbulence",
      "physical_parameters": {
        "density_liquid": "TBD",
        "density_gas": "TBD",
        "viscosity_liquid": "TBD",
        "viscosity_gas": "TBD",
        "surface_tension": "TBD"
      },
      "boundary_conditions": "TBD",
      "initial_conditions": "TBD"
    },
    "contributors": ["TBD"],
    "license": "TBD",
    "doi": "TBD",
    "known_limitations": []
  },
  "local": [
    {
      "id": 0,
      "snapshot_id": "000001",
      "time": {
        "value": null,
        "units": "TBD"
      },
      "files": {
        "Gvol": "./data/Gvol/Gvol.000001"
      }
    }
  ]
}
```

## Acceptance Checklist

Before submitting a dataset link to Multiphase Data Hub, verify:

- `dataset-metadata.json` exists and has the correct Kaggle owner id;
- `info.json` exists and matches actual uploaded files;
- all listed file paths exist;
- variable units and shapes are documented;
- grid reconstruction is possible;
- phase convention is documented, for example whether `Gvol=1` denotes liquid;
- at least one sample can be read with Python;
- custom binary data include `load_example.py`;
- license and citation information are clear.

