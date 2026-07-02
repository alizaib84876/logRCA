import pytest


@pytest.mark.integration
def test_bm25_search_endpoint_returns_hits() -> None:
    from fastapi.testclient import TestClient

    from logrca.api.app import app

    client = TestClient(app)

    response = client.get("/retrieval/bm25/search", params={"q": "PacketResponder terminating", "top_k": 3})

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "PacketResponder terminating"
    assert body["hits"]
    assert any("packetresponder" in hit["text"].lower() for hit in body["hits"])
