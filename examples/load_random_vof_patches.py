"""Minimal loader for the random VOF patch seed dataset."""

from __future__ import annotations

from pathlib import Path

import numpy as np


def load_npz(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    archive = np.load(path)
    return archive["x_hr"], archive["y_lr"]


if __name__ == "__main__":
    x_hr, y_lr = load_npz("random_interfaces_n256_to_n64_interface_patches_v2.npz")
    print("x_hr:", x_hr.shape, x_hr.dtype)
    print("y_lr:", y_lr.shape, y_lr.dtype)
