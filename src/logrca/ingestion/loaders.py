from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from logrca.ingestion.models import HDFS2kDataset, HDFS2kTemplate, LogRecord, PostmortemChunk


def load_log_lines(log_file: Path, service: str | None = None) -> list[LogRecord]:
    records: list[LogRecord] = []
    with log_file.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle, start=1):
            message = line.rstrip("\n")
            if not message:
                continue
            records.append(
                LogRecord(
                    record_id=f"{log_file.stem}:{index}",
                    raw_message=message,
                    service=service,
                    source_file=str(log_file),
                    metadata={"line_number": index},
                )
            )
    return records


def load_json_records(json_file: Path) -> list[dict[str, object]]:
    with json_file.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, list):
        return [record for record in payload if isinstance(record, dict)]

    if isinstance(payload, dict):
        records = payload.get("records")
        if isinstance(records, list):
            return [record for record in records if isinstance(record, dict)]

    raise ValueError(f"Unsupported JSON structure in {json_file}")


def load_csv_rows(csv_file: Path) -> list[dict[str, str]]:
    with csv_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def chunk_postmortem_text(
    source_file: Path,
    text: str,
    incident_id: str | None = None,
) -> list[PostmortemChunk]:
    chunks: list[PostmortemChunk] = []
    sections = [section.strip() for section in text.split("\n\n") if section.strip()]

    for index, section in enumerate(sections, start=1):
        title, _, body = section.partition("\n")
        content = body.strip() if body.strip() else section
        chunks.append(
            PostmortemChunk(
                chunk_id=f"{source_file.stem}:chunk-{index}",
                title=title.strip() or f"Section {index}",
                content=content,
                incident_id=incident_id,
                section_path=str(index),
                source_file=str(source_file),
                metadata={"section_index": index},
            )
        )

    return chunks


def iter_text_files(folder: Path) -> Iterable[Path]:
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".log", ".txt"}:
            yield path


def load_hdfs_2k_dataset(folder: Path) -> HDFS2kDataset:
    structured_csv = folder / "HDFS_2k.log_structured.csv"
    raw_log = folder / "HDFS_2k.log"
    templates_csv = folder / "HDFS_2k.log_templates.csv"

    if structured_csv.exists():
        log_records = _load_hdfs_2k_structured_csv(structured_csv)
    elif raw_log.exists():
        log_records = load_log_lines(raw_log, service="hdfs")
    else:
        raise FileNotFoundError(
            f"Expected HDFS_2k.log_structured.csv or HDFS_2k.log in {folder}"
        )

    templates = _load_hdfs_2k_templates(templates_csv) if templates_csv.exists() else []

    return HDFS2kDataset(
        log_records=log_records,
        templates=templates,
        raw_log_path=str(raw_log) if raw_log.exists() else None,
        structured_csv_path=str(structured_csv) if structured_csv.exists() else None,
        templates_csv_path=str(templates_csv) if templates_csv.exists() else None,
    )


def _load_hdfs_2k_structured_csv(structured_csv: Path) -> list[LogRecord]:
    records: list[LogRecord] = []
    with structured_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            line_id = row.get("LineId") or row.get("lineid") or row.get("line_id")
            if line_id is None:
                continue
            record = LogRecord(
                record_id=str(line_id),
                raw_message=row.get("Content", "") or "",
                template=row.get("EventTemplate") or None,
                service=row.get("Component") or None,
                severity=row.get("Level") or None,
                source_file=str(structured_csv),
                metadata={
                    "line_id": row.get("LineId"),
                    "date": row.get("Date"),
                    "time": row.get("Time"),
                    "pid": row.get("Pid"),
                    "event_id": row.get("EventId"),
                },
            )
            records.append(record)
    return records


def _load_hdfs_2k_templates(templates_csv: Path) -> list[HDFS2kTemplate]:
    templates: list[HDFS2kTemplate] = []
    with templates_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            event_id = row.get("EventId")
            event_template = row.get("EventTemplate")
            if not event_id or not event_template:
                continue
            templates.append(
                HDFS2kTemplate(
                    event_id=event_id,
                    event_template=event_template,
                )
            )
    return templates
