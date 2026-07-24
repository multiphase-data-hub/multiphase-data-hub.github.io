# Multiphase Data Hub

Multiphase Data Hub is a proposed open catalogue for multiphase-flow datasets,
inspired by BlastNet but adapted to CFD, experimental diagnostics, and AI-ready
benchmarks for multiphase flows.

The repository is designed to host:

- a static website for dataset discovery;
- metadata records for externally hosted datasets;
- contribution and review guidelines;
- data-format recommendations for reproducible AI use.

Large data files should live outside this website repository. Recommended hosts
are ModelScope for China-accessible distribution, Kaggle for international
distribution, Zenodo for DOI-backed archival releases, or institutional object
storage for very large datasets. This repository stores persistent links,
metadata, checksums, documentation, and example loaders.

For simulation datasets, the data package itself should include a
`multiphase_info.json` file. This follows the BlastNet-style separation between
dataset-level metadata and snapshot/case-level file records, but uses variables
and parameters appropriate for multiphase-flow simulations.

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
    datasets.html
    dataset-random-vof-patches.html
    dataset-hit-droplet-breakup.html
    standard.html
    contribute.html
    hosting.html
    governance.html
    about.html
    styles.css
    datasets.js
    assets/
  datasets/
    random_interfaces_n256_to_n64_interface_patches_v2.json
  docs/
    contribution_guide.md
    data_standard.md
    governance.md
    kaggle_dataset_package_standard.md
    kaggle_dataset_package_standard_zh.md
    launch_checklist.md
    roadmap.md
    v0.1_release_notes.md
  templates/
    dataset_info.schema.json
    dataset_info.template.json
    multiphase_info.schema.json
    multiphase_info.template.json
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
4. Upload large datasets to ModelScope, Kaggle, Zenodo, or institutional
   storage and paste the resulting landing-page URL into the dataset metadata
   record.

For the v0.1 site, the recommended hosting policy is:

- ModelScope for China-accessible dataset distribution.
- Kaggle for international dataset mirrors and AI-community access.
- Zenodo when a standalone DOI-backed archival release is needed.

## Tools Needed

The first version deliberately uses the smallest possible toolchain:

- GitHub: hosts the website repository and accepts pull requests.
- GitHub Pages: publishes the static website for free.
- ModelScope, Kaggle, Zenodo, or institutional storage: hosts large data
  archives.
- JSON metadata files: describe datasets in a machine-readable way.
- Optional Python scripts: provide minimal data loaders and validation helpers.
- GitHub Actions: runs automated intake checks and optionally emails reviewers
  when SMTP secrets are configured.

No backend server, database, login system, or paid cloud service is required for
the initial release.


## Dataset Intake and Review

The contribution flow follows a BLASTNet-style split between automated intake
and human review:

1. Contributors host large files outside this repository.
2. Contributors open a dataset submission issue or pull request.
3. GitHub Actions labels dataset issues, validates `datasets/*.json` in pull
   requests, and runs the reviewer notification script.
4. If repository SMTP secrets are configured, reviewers listed in
   `.github/reviewers.yml` receive an email reminder.
5. Maintainers make the final decision after checking metadata completeness,
   access, license, citation, physical description, and file readability.

To enable email reminders, configure these repository secrets:

```text
SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
MAIL_FROM
```

Then replace the placeholder reviewer emails in `.github/reviewers.yml`.

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

## v0.1 Status

The first public structure includes:

- one seed dataset record for droplet breakup in homogeneous isotropic
  turbulence;
- an English website with Home, Datasets, Data Standard, Contribute, Hosting,
  Governance, and About pages;
- metadata templates for catalogue records and multiphase-flow simulation data;
- a contribution workflow based on externally hosted data and reviewed
  metadata.
