from fastapi.testclient import TestClient
import pytest

from logrca.api.app import app


@pytest.mark.integration
def test_ingestion_status_endpoint_returns_dataset_info() -> None:
    client = TestClient(app)

    response = client.get("/ingestion/hdfs-2k/status")

    assert response.status_code == 200
    body = response.json()
    assert body["dataset_name"] == "HDFS_2k"
    assert body["structured_csv_exists"] is True
