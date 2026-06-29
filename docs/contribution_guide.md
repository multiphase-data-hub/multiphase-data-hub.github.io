# Contribution Guide

The goal is to make dataset submission easy while keeping the catalogue useful
for reproducible research.

## Submission Workflow

1. Host the dataset on a stable external platform.
2. Add a metadata JSON file under `datasets/`.
3. Add preview figures when available.
4. Open a pull request.
5. Maintainers review metadata completeness, link stability, license clarity,
   and basic scientific provenance.

## Hosting Recommendations

Recommended public hosts:

- Zenodo for DOI-backed archival releases;
- Figshare or institutional repositories for citable data packages;
- Hugging Face Datasets for ML-friendly public access;
- Kaggle for competition-style datasets;
- project object storage for very large datasets, with clear persistence notes.

The website repository should not store large data archives.

## Minimum Acceptance Criteria

A submitted dataset should have:

- explicit license;
- clear citation;
- working download link;
- documented variable names, units, and shapes;
- provenance information;
- at least one contact person;
- enough documentation for an external user to load a sample.

## Review Categories

Dataset records can be marked as:

- `draft`: metadata exists but the data is not ready for public reuse;
- `seed`: internally contributed dataset used to establish the standard;
- `community`: external community contribution;
- `benchmark`: curated dataset with fixed splits and metrics;
- `archived`: retained for citation but not actively maintained.

