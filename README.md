# Multiphase Data Hub

Multiphase Data Hub is a proposed open catalogue for multiphase-flow datasets,
inspired by BlastNet but adapted to CFD, experimental diagnostics, and AI-ready
benchmarks for multiphase flows.

The repository is designed to host:

- a static website for dataset discovery;
- metadata records for externally hosted datasets;
- contribution and review guidelines;
- data-format recommendations for reproducible AI use.

Large data files should live outside this website repository, for example on
Zenodo, Figshare, Kaggle, Hugging Face Datasets, institutional object storage,
or a project server. This repository stores persistent links, metadata,
checksums, documentation, and example loaders.

## First Milestone

The first public version should contain at least one seed dataset from the
current two-phase-flow + AI work, even if it is small. A working first release is
more useful than an empty portal because it establishes:

- the naming convention;
- the metadata standard;
- the expected citation and license fields;
- the minimum quality bar for external contributors.

## Repository Layout

```text
multiphase-data-hub/
  README.md
  website/
    index.html
    dataset-random-vof-patches.html
    standard.html
    contribute.html
    styles.css
    datasets.js
    assets/
  datasets/
    random_interfaces_n256_to_n64_interface_patches_v2.json
  docs/
    contribution_guide.md
    data_standard.md
    governance.md
    launch_checklist.md
    roadmap.md
  templates/
    dataset_info.schema.json
    dataset_info.template.json
  examples/
    load_random_vof_patches.py
```

## Publish Model

Recommended deployment:

1. Create a GitHub organization, for example `MultiphaseDataHub`.
2. Push this folder as a repository named `multiphase-data-hub` or
   `multiphase-data-hub.github.io`.
3. Enable GitHub Pages from the repository root and use `website/index.html` as
   the public entry point, or move website files to the repository root before
   publishing.
4. Upload large datasets to Zenodo or Hugging Face Datasets and paste the
   resulting DOI/URL into the dataset metadata record.

## Tools Needed

The first version deliberately uses the smallest possible toolchain:

- GitHub: hosts the website repository and accepts pull requests.
- GitHub Pages: publishes the static website for free.
- Zenodo, Hugging Face Datasets, Kaggle, Figshare, or institutional storage:
  hosts large data archives.
- JSON metadata files: describe datasets in a machine-readable way.
- Optional Python scripts: provide minimal data loaders and validation helpers.

No backend server, database, login system, or paid cloud service is required for
the initial release.

## Local Preview

From this repository folder, run:

```powershell
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/website/index.html
```

## Scope

The portal should accept datasets from:

- direct numerical simulation, LES, RANS, and interface-resolved CFD;
- VOF, level-set, front-tracking, phase-field, SPH, LBM, and hybrid methods;
- gas-liquid, liquid-liquid, solid-liquid, droplets, bubbles, sprays, films,
  breakup, coalescence, and atomization;
- experimental measurements such as PIV, PLIF, X-ray, shadowgraphy, and
  high-speed imaging;
- AI-ready derived products such as patches, closures, super-resolution pairs,
  segmentation labels, reduced-order snapshots, and benchmark splits.
