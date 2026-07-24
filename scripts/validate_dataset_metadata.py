#!/usr/bin/env python3
"""Lightweight metadata checks for dataset intake pull requests."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "datasets"


REQUIRED_CATALOGUE_FIELDS = [
    "schema_version",
    "id",
    "title",
    "version",
    "status",
    "description",
    "domain",
    "data",
    "license",
    "citation",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def check_catalogue_record(path: Path) -> list[str]:
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        record = json.load(handle)

    for field in REQUIRED_CATALOGUE_FIELDS:
        if field not in record:
            errors.append(f"{path}: missing required field '{field}'")

    data = record.get("data", {})
    if isinstance(data, dict):
        access_url = (
            data.get("public_access_url")
            or data.get("modelscope_url")
            or data.get("kaggle_url")
            or data.get("zenodo_url")
            or data.get("repository_url")
        )
        if not access_url or access_url == "TBD":
            errors.append(f"{path}: data needs a public access URL")
        if not data.get("format"):
            errors.append(f"{path}: data.format is required")
    else:
        errors.append(f"{path}: data must be an object")

    domain = record.get("domain", {})
    if isinstance(domain, dict):
        for field in ["flow_type", "configuration", "interface_method", "spatial_dimension"]:
            if field not in domain:
                errors.append(f"{path}: domain.{field} is required")
    else:
        errors.append(f"{path}: domain must be an object")

    return errors


def main() -> int:
    if not DATASETS.exists():
        fail("datasets/ directory is missing")

    json_files = sorted(DATASETS.glob("*.json"))
    if not json_files:
        fail("No dataset catalogue records found in datasets/")

    errors: list[str] = []
    for path in json_files:
        try:
            errors.extend(check_catalogue_record(path))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON at line {exc.lineno}: {exc.msg}")

    if errors:
        print("Dataset metadata precheck failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Dataset metadata precheck passed for {len(json_files)} record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
