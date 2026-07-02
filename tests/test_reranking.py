import pytest


@pytest.mark.integration
def test_reranked_search_prioritizes_packet_responder_matches() -> None:
    from logrca.retrieval import build_hdfs_2k_fused_bm25_bundle, rerank_fused_result, search_fused_bm25

    bundle = build_hdfs_2k_fused_bm25_bundle()
    fused = search_fused_bm25(bundle, "PacketResponder terminating", top_k=10)
    reranked = rerank_fused_result(fused, top_k=5)

    assert reranked.hits
    assert "packetresponder" in reranked.hits[0].text.lower()
