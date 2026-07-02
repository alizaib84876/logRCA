from __future__ import annotations

from pathlib import Path


def raw_data_root(base_dir: Path | None = None) -> Path:
    root = base_dir if base_dir is not None else Path.cwd()
    return root / "data" / "raw"


def processed_data_root(base_dir: Path | None = None) -> Path:
    root = base_dir if base_dir is not None else Path.cwd()
    return root / "data" / "processed"


def indexes_root(base_dir: Path | None = None) -> Path:
    root = base_dir if base_dir is not None else Path.cwd()
    return root / "data" / "indexes"
