import pytest

from logrca.ingestion import build_hdfs_2k_ingestion_status


@pytest.mark.integration
def test_hdfs_2k_ingestion_status_reports_present_files() -> None:
    status = build_hdfs_2k_ingestion_status()

    assert status.dataset_name == "HDFS_2k"
    assert status.raw_log_exists
    assert status.structured_csv_exists
    assert status.templates_csv_exists
    assert status.structured_rows > 0
    assert status.raw_log_rows > 0
