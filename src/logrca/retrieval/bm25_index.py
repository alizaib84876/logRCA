from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from rank_bm25 import BM25Okapi

from logrca.ingestion.catalog import processed_data_root
from logrca.retrieval.models import BM25Index, RetrievalHit


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")


@dataclass(slots=True)
class BM25SearchResult:
    query: str
    hits: list[RetrievalHit]


def tokenize_text(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def load_hdfs_2k_processed_records(base_dir: Path | None = None) -> list[RetrievalHit]:
    root = processed_data_root(base_dir) / "hdfs_2k"
    mined_records_csv = root / "hdfs_2k_mined_records.csv"

    if not mined_records_csv.exists():
        raise FileNotFoundError(
            f"Missing processed HDFS_2k records at {mined_records_csv}"
        )

    hits: list[RetrievalHit] = []
    with mined_records_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            text = " ".join(
                part
                for part in [row.get("raw_message", ""), row.get("mined_template", "")]
                if part
            ).strip()
            if not text:
                continue

            cluster_id = row.get("cluster_id")
            event_id = row.get("event_id")
            hits.append(
                RetrievalHit(
                    record_id=row.get("record_id", ""),
                    score=0.0,
                    text=text,
                    source_file=row.get("source_file") or None,
                    cluster_id=int(cluster_id) if cluster_id else None,
                    event_id=event_id or None,
                    metadata={
                        "dataset_template": row.get("dataset_template") or None,
                        "service": row.get("service") or None,
                        "severity": row.get("severity") or None,
                    },
                )
            )

    return hits


def build_bm25_index(records: list[RetrievalHit]) -> tuple[BM25Index, BM25Okapi]:
    corpus = [record.text for record in records]
    tokenized_corpus = [tokenize_text(text) for text in corpus]
    index = BM25Index(corpus=corpus, tokenized_corpus=tokenized_corpus, records=records)
    bm25 = BM25Okapi(tokenized_corpus)
    return index, bm25


def build_hdfs_2k_bm25_index(base_dir: Path | None = None) -> tuple[BM25Index, BM25Okapi]:
    records = load_hdfs_2k_processed_records(base_dir=base_dir)
    return build_bm25_index(records)


def search_bm25(
    index: BM25Index,
    bm25: BM25Okapi,
    query: str,
    top_k: int = 5,
) -> BM25SearchResult:
    tokenized_query = tokenize_text(query)
    scores = bm25.get_scores(tokenized_query)
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    hits = [
        RetrievalHit(
            record_id=index.records[i].record_id,
            score=float(scores[i]),
            text=index.records[i].text,
            source_file=index.records[i].source_file,
            cluster_id=index.records[i].cluster_id,
            event_id=index.records[i].event_id,
            metadata=dict(index.records[i].metadata),
        )
        for i in ranked_indices
    ]

    return BM25SearchResult(query=query, hits=hits)
