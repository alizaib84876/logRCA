from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from rank_bm25 import BM25Okapi

from logrca.retrieval.bm25_index import (
    BM25SearchResult,
    build_bm25_index,
    load_hdfs_2k_processed_records,
    search_bm25,
    tokenize_text,
)
from logrca.retrieval.models import BM25Index, FusedRetrievalResult, RetrievalHit


@dataclass(slots=True)
class FusedBM25Bundle:
    raw_index: BM25Index
    raw_bm25: BM25Okapi
    template_index: BM25Index
    template_bm25: BM25Okapi


def build_hdfs_2k_fused_bm25_bundle(base_dir: Path | None = None) -> FusedBM25Bundle:
    records = load_hdfs_2k_processed_records(base_dir=base_dir)

    raw_records: list[RetrievalHit] = []
    template_records: list[RetrievalHit] = []

    for record in records:
        raw_records.append(
            RetrievalHit(
                record_id=record.record_id,
                score=0.0,
                text=record.text,
                source_file=record.source_file,
                cluster_id=record.cluster_id,
                event_id=record.event_id,
                metadata=dict(record.metadata),
            )
        )

        template_text = record.metadata.get("dataset_template") or record.text
        template_records.append(
            RetrievalHit(
                record_id=record.record_id,
                score=0.0,
                text=str(template_text),
                source_file=record.source_file,
                cluster_id=record.cluster_id,
                event_id=record.event_id,
                metadata=dict(record.metadata),
            )
        )

    raw_index, raw_bm25 = build_bm25_index(raw_records)
    template_index, template_bm25 = build_bm25_index(template_records)
    return FusedBM25Bundle(
        raw_index=raw_index,
        raw_bm25=raw_bm25,
        template_index=template_index,
        template_bm25=template_bm25,
    )


def reciprocal_rank_fusion(results: list[BM25SearchResult], rrf_k: int = 60) -> FusedRetrievalResult:
    fused_scores: dict[str, float] = defaultdict(float)
    hit_lookup: dict[str, RetrievalHit] = {}

    for result in results:
        for rank, hit in enumerate(result.hits, start=1):
            fused_scores[hit.record_id] += 1.0 / (rrf_k + rank)
            hit_lookup[hit.record_id] = hit

    ranked_hits = sorted(
        hit_lookup.values(),
        key=lambda hit: fused_scores[hit.record_id],
        reverse=True,
    )

    fused_hits = [
        RetrievalHit(
            record_id=hit.record_id,
            score=fused_scores[hit.record_id],
            text=hit.text,
            source_file=hit.source_file,
            cluster_id=hit.cluster_id,
            event_id=hit.event_id,
            metadata=dict(hit.metadata),
        )
        for hit in ranked_hits
    ]

    query = results[0].query if results else ""
    return FusedRetrievalResult(query=query, hits=fused_hits)


def search_fused_bm25(
    bundle: FusedBM25Bundle,
    query: str,
    top_k: int = 5,
    rrf_k: int = 60,
) -> FusedRetrievalResult:
    raw_result = search_bm25(bundle.raw_index, bundle.raw_bm25, query, top_k=top_k)
    template_result = search_bm25(bundle.template_index, bundle.template_bm25, query, top_k=top_k)
    fused = reciprocal_rank_fusion([raw_result, template_result], rrf_k=rrf_k)
    fused.hits = fused.hits[:top_k]
    return fused
