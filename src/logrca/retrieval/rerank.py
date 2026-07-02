from __future__ import annotations

from dataclasses import dataclass

from logrca.retrieval.bm25_index import tokenize_text
from logrca.retrieval.fusion import FusedRetrievalResult
from logrca.retrieval.models import RetrievalHit


@dataclass(slots=True)
class RerankedRetrievalResult:
    query: str
    hits: list[RetrievalHit]


def rerank_hits(query: str, hits: list[RetrievalHit], top_k: int = 5) -> RerankedRetrievalResult:
    query_tokens = tokenize_text(query)
    query_text = query.lower().strip()
    reranked_hits: list[RetrievalHit] = []

    for hit in hits:
        text_tokens = tokenize_text(hit.text)
        text_set = set(text_tokens)
        query_set = set(query_tokens)

        overlap_count = sum(1 for token in query_tokens if token in text_set)
        unique_overlap = len(query_set & text_set)
        exact_phrase_bonus = 2.0 if query_text and query_text in hit.text.lower() else 0.0
        sequence_bonus = 1.0 if _contains_query_sequence(query_tokens, text_tokens) else 0.0

        reranked_score = hit.score + (0.3 * overlap_count) + (0.5 * unique_overlap) + exact_phrase_bonus + sequence_bonus
        reranked_hits.append(
            RetrievalHit(
                record_id=hit.record_id,
                score=reranked_score,
                text=hit.text,
                source_file=hit.source_file,
                cluster_id=hit.cluster_id,
                event_id=hit.event_id,
                metadata=dict(hit.metadata),
            )
        )

    reranked_hits = sorted(reranked_hits, key=lambda hit: hit.score, reverse=True)[:top_k]
    return RerankedRetrievalResult(query=query, hits=reranked_hits)


def rerank_fused_result(result: FusedRetrievalResult, top_k: int = 5) -> RerankedRetrievalResult:
    return rerank_hits(result.query, result.hits, top_k=top_k)


def _contains_query_sequence(query_tokens: list[str], text_tokens: list[str]) -> bool:
    if not query_tokens or not text_tokens or len(query_tokens) > len(text_tokens):
        return False

    for start_index in range(len(text_tokens) - len(query_tokens) + 1):
        if text_tokens[start_index : start_index + len(query_tokens)] == query_tokens:
            return True
    return False
