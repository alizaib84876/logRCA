from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RetrievalHit:
    record_id: str
    score: float
    text: str
    source_file: str | None = None
    cluster_id: int | None = None
    event_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BM25Index:
    corpus: list[str]
    tokenized_corpus: list[list[str]]
    records: list[RetrievalHit]


@dataclass(slots=True)
class FusedRetrievalResult:
    query: str
    hits: list[RetrievalHit]


@dataclass(slots=True)
class RerankedRetrievalResult:
    query: str
    hits: list[RetrievalHit]

