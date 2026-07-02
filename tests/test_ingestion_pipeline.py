from pathlib import Path

import pytest


@pytest.mark.integration
def test_hdfs_2k_ingestion_pipeline_writes_processed_outputs(tmp_path: Path) -> None:
    from logrca.ingestion import run_hdfs_2k_ingestion_pipeline

    export_paths = run_hdfs_2k_ingestion_pipeline(
        Path("data/raw/hdfs_2k"),
        base_dir=tmp_path,
    )

    assert export_paths.mined_records_csv.exists()
    assert export_paths.cluster_templates_csv.exists()
    assert export_paths.mined_records_csv.read_text(encoding="utf-8").strip()
    assert export_paths.cluster_templates_csv.read_text(encoding="utf-8").strip()
