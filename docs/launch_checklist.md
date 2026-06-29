# Launch Checklist

This checklist turns the local website into a public community dataset portal.

## Accounts

- GitHub account or GitHub organization.
- Zenodo, Hugging Face Datasets, Kaggle, Figshare, or institutional storage
  account for large dataset archives.
- Contact email for dataset submissions.

## Repository Setup

1. Create a GitHub repository, for example `multiphase-data-hub`.
2. Upload the contents of this folder.
3. In GitHub repository settings, open `Pages`.
4. Select the main branch as the source.
5. Use `/root` as the publish folder if website files remain under `website/`.
6. Public entry page:

```text
https://<owner>.github.io/<repository>/website/index.html
```

For a cleaner URL, move the contents of `website/` to the repository root after
the first version is stable.

## Dataset Release

1. Decide whether to publish raw CFD outputs, derived AI-ready arrays, or both.
2. Package the dataset with:
   - data archive;
   - README;
   - metadata JSON;
   - checksums;
   - loader script;
   - preview figures.
3. Upload the archive to Zenodo or another stable host.
4. Copy the DOI or public URL into `datasets/*.json`.
5. Replace all `TBD` fields before announcing the site.

## Public Announcement

Before inviting external contributors:

- confirm the data license;
- confirm the code license;
- add author names and contact email;
- test all links from a private browser window;
- add one issue template for dataset submission;
- prepare a short call-for-data message for colleagues and mailing lists.

