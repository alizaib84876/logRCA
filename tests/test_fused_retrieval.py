import pytest


@pytest.mark.integration
def test_hdfs_2k_fused_search_returns_packet_responder_hits() -> None:
    from logrca.retrieval import build_hdfs_2k_fused_bm25_bundle, search_fused_bm25

    bundle = build_hdfs_2k_fused_bm25_bundle()
    result = search_fused_bm25(bundle, "PacketResponder terminating", top_k=5)

    assert result.hits
    assert any("packetresponder" in hit.text.lower() for hit in result.hits)
