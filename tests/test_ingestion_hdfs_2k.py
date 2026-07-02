from pathlib import Path

from logrca.ingestion import load_hdfs_2k_dataset


def test_hdfs_2k_dataset_loads() -> None:
    dataset = load_hdfs_2k_dataset(Path("data/raw/hdfs_2k"))

    assert dataset.log_records
    assert dataset.templates
    assert dataset.log_records[0].template is not None
