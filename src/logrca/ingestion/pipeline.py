from __future__ import annotations

from pathlib import Path

from logrca.ingestion.catalog import processed_data_root
from logrca.ingestion.loaders import load_hdfs_2k_dataset
from logrca.ingestion.template_mining import (
    MiningExportPaths,
    persist_hdfs_2k_mining_result,
    mine_hdfs_2k_dataset,
)


def run_hdfs_2k_ingestion_pipeline(
    raw_data_folder: Path,
    base_dir: Path | None = None,
) -> MiningExportPaths:
    dataset = load_hdfs_2k_dataset(raw_data_folder)
    mining_result = mine_hdfs_2k_dataset(dataset)
    output_root = processed_data_root(base_dir) / "hdfs_2k"
    return persist_hdfs_2k_mining_result(mining_result, output_root)
