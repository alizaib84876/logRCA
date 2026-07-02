from pathlib import Path

import pytest

from logrca.ingestion import compare_with_dataset_templates, load_hdfs_2k_dataset, mine_hdfs_2k_dataset


@pytest.mark.integration
def test_hdfs_2k_template_mining_runs() -> None:
    dataset = load_hdfs_2k_dataset(Path("data/raw/hdfs_2k"))
    result = mine_hdfs_2k_dataset(dataset)

    assert result.mined_records
    assert result.cluster_templates
    assert result.mined_records[0].mined_template


@pytest.mark.integration
def test_hdfs_2k_dataset_templates_are_found() -> None:
    dataset = load_hdfs_2k_dataset(Path("data/raw/hdfs_2k"))
    result = mine_hdfs_2k_dataset(dataset)
    comparison = compare_with_dataset_templates(result.mined_records, dataset.templates)

    assert comparison["total"] == len(result.mined_records)
    assert comparison["matched"] > 0
