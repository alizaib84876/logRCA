from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class IngestionStatus:
    dataset_name: str
    raw_log_exists: bool
    structured_csv_exists: bool
    templates_csv_exists: bool
    mined_records_csv_exists: bool
    cluster_templates_csv_exists: bool
    raw_log_rows: int
    structured_rows: int
    mined_rows: int
    cluster_template_rows: int


def _count_csv_rows(csv_file: Path) -> int:
    if not csv_file.exists():
        return 0

    with csv_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for _ in reader)


def _count_text_rows(text_file: Path) -> int:
    if not text_file.exists():
        return 0

    with text_file.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def build_hdfs_2k_ingestion_status(base_dir: Path | None = None) -> IngestionStatus:
    root = base_dir if base_dir is not None else Path.cwd()
    raw_root = root / "data" / "raw" / "hdfs_2k"
    processed_root = root / "data" / "processed" / "hdfs_2k"

    raw_log = raw_root / "HDFS_2k.log"
    structured_csv = raw_root / "HDFS_2k.log_structured.csv"
    templates_csv = raw_root / "HDFS_2k.log_templates.csv"
    mined_records_csv = processed_root / "hdfs_2k_mined_records.csv"
    cluster_templates_csv = processed_root / "hdfs_2k_cluster_templates.csv"

    return IngestionStatus(
        dataset_name="HDFS_2k",
        raw_log_exists=raw_log.exists(),
        structured_csv_exists=structured_csv.exists(),
        templates_csv_exists=templates_csv.exists(),
        mined_records_csv_exists=mined_records_csv.exists(),
        cluster_templates_csv_exists=cluster_templates_csv.exists(),
        raw_log_rows=_count_text_rows(raw_log),
        structured_rows=_count_csv_rows(structured_csv),
        mined_rows=_count_csv_rows(mined_records_csv),
        cluster_template_rows=_count_csv_rows(cluster_templates_csv),
    )
