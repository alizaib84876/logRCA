from pathlib import Path

import pytest


@pytest.mark.integration
def test_hdfs_2k_bm25_search_finds_packet_responder() -> None:
    from logrca.retrieval import build_hdfs_2k_bm25_index, search_bm25

    index, bm25 = build_hdfs_2k_bm25_index(Path("."))
    result = search_bm25(index, bm25, "PacketResponder block terminating", top_k=5)

    assert result.hits
    assert any("packetresponder" in hit.text.lower() for hit in result.hits)
