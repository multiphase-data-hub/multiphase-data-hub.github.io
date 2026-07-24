#!/usr/bin/env python3
"""Generate website/dataset-{id}.html pages from datasets/*.json records.

Run this script whenever you add or update a JSON record in datasets/.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = ROOT / "datasets"
PAGES_DIR = ROOT / "website"

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} | Multiphase Data Hub</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header class="page-header">
      <nav class="nav" aria-label="Primary navigation">
        <a class="brand" href="index.html">Multiphase Data Hub</a>
        <div class="nav-links">
          <a href="datasets.html">Datasets</a>
          <a href="standard.html">Standard</a>
          <a href="contribute.html">Contribute</a>
          <a href="hosting.html">Hosting</a>
          <a href="governance.html">Governance</a>
          <a href="about.html">About</a>
        </div>
      </nav>
      <div class="page-title">
        <p class="eyebrow">{status_label}</p>
        <h1>{title}</h1>
        <p>{summary}</p>
      </div>
    </header>

    <main>
      <section class="section detail-hero">
        <div>
          <p class="eyebrow">Description</p>
          <p class="section-copy">{description}</p>
          <div class="download-actions">
            <a class="button primary" href="{data_url}">Open on {host_platform}</a>
          </div>
        </div>
        <img src="{image_url}" alt="{title}" />
      </section>

      <section class="section band">
        <h2>Quick Info</h2>
        <ul class="quick-info-list">
          {quick_info_items}
        </ul>
      </section>
    </main>

    <footer class="footer">
      <span>Multiphase Data Hub</span>
      <span>{title}</span>
    </footer>
  </body>
</html>
"""


def build_page(record: dict) -> str | None:
    data = record.get("data", {})
    citation = record.get("citation", {})
    visuals = record.get("visuals", {})
    license_info = record.get("license", {})

    dataset_id = record.get("id", "")
    if not dataset_id:
        print("Skipping record without id")
        return None

    title = record.get("title", "Untitled")
    summary = record.get("description", "")
    status = record.get("status", "seed").replace("_dataset", "")
    status_label = status.capitalize() + " dataset"

    # Image (strip website/ prefix)
    image = visuals.get("main", "assets/placeholder.png")
    if image.startswith("website/"):
        image = image[len("website/"):]

    # Data URL
    data_url = (
        data.get("modelscope_url")
        or data.get("kaggle_url")
        or data.get("zenodo_url")
        or data.get("repository_url")
        or "#"
    )
    if data_url in ("TBD",):
        data_url = "#"

    host_platform = data.get("primary_host", "ModelScope")

    # Quick Info items
    items: list[str] = []

    if data_url and data_url != "#":
        items.append(f'<li><a class="text-link" href="{data_url}">{host_platform} Link</a></li>')

    authors = citation.get("authors", [])
    if authors:
        items.append(f"<li>Contributors: {', '.join(authors)}</li>")

    grid = data.get("grid", {})
    cell_shape = grid.get("cell_shape", [])
    if cell_shape:
        dims = " x ".join(str(n) for n in cell_shape)
        items.append(f"<li><em>N</em>x = {dims.replace(' x ', '</em>, <em>N</em>y = ').replace(',', ', <em>N</em>z =', 1) if len(cell_shape) >= 3 else f'<li>Grid: {dims}'}</em></li>")
    else:
        # Simple grid fallback
        pass

    doi = citation.get("related_paper_doi", "")
    if doi:
        items.append(f'<li><a class="text-link" href="https://doi.org/{doi}">DOI</a></li>')

    license_str = license_info.get("data_license", "")
    if license_str:
        items.append(f"<li>License: {license_str}</li>")

    quick_info_items = "\n          ".join(items)

    return HTML_TEMPLATE.format(
        title=title,
        summary=summary,
        description=summary,
        status_label=status_label,
        data_url=data_url,
        host_platform=host_platform,
        image_url=image,
        quick_info_items=quick_info_items,
    )


def main() -> int:
    if not DATASETS_DIR.exists():
        print("datasets/ directory not found")
        return 1

    json_files = sorted(DATASETS_DIR.glob("*.json"))
    if not json_files:
        print("No dataset JSON files found")
        return 0

    generated = 0
    for path in json_files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"Skipping {path.name}: invalid JSON ({exc})")
            continue

        page = build_page(record)
        if page is None:
            continue

        dataset_id = record.get("id", "")
        output_path = PAGES_DIR / f"dataset-{dataset_id}.html"
        output_path.write_text(page, encoding="utf-8")
        print(f"Generated {output_path.name}")
        generated += 1

    print(f"Generated {generated} dataset detail page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
