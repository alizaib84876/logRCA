from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class LogRecord:
    record_id: str
    raw_message: str
    template: str | None = None
    timestamp: datetime | None = None
    service: str | None = None
    severity: str | None = None
    source_file: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PostmortemChunk:
    chunk_id: str
    title: str
    content: str
    incident_id: str | None = None
    section_path: str | None = None
    source_file: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class HDFS2kTemplate:
    event_id: str
    event_template: str


@dataclass(slots=True)
class HDFS2kDataset:
    log_records: list[LogRecord]
    templates: list[HDFS2kTemplate]
    raw_log_path: str | None = None
    structured_csv_path: str | None = None
    templates_csv_path: str | None = None
