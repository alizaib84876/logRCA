from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

from logrca.ingestion.models import HDFS2kDataset, HDFS2kTemplate, LogRecord


@dataclass(slots=True)
class MinedLogRecord:
    record_id: str
    raw_message: str
    mined_template: str
    cluster_id: int
    cluster_count: int
    source_file: str | None = None
    service: str | None = None
    severity: str | None = None
    dataset_template: str | None = None
    event_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TemplateMiningResult:
    mined_records: list[MinedLogRecord]
    cluster_templates: list[HDFS2kTemplate]


@dataclass(slots=True)
class MiningExportPaths:
    mined_records_csv: Path
    cluster_templates_csv: Path


def build_template_miner() -> TemplateMiner:
    config = TemplateMinerConfig()
    config.drain_sim_th = 0.4
    config.drain_depth = 4
    config.drain_max_children = 100
    config.parametrize_numeric_tokens = True
    return TemplateMiner(config=config)


def mine_records(records: Iterable[LogRecord]) -> TemplateMiningResult:
    miner = build_template_miner()
    mined_records: list[MinedLogRecord] = []
    cluster_templates: dict[int, str] = {}

    for record in records:
        result = miner.add_log_message(record.raw_message)
        cluster_id = int(result["cluster_id"])
        mined_template = str(result["template_mined"])
        cluster_count = int(result["cluster_count"])
        cluster_templates[cluster_id] = mined_template
        mined_records.append(
            MinedLogRecord(
                record_id=record.record_id,
                raw_message=record.raw_message,
                mined_template=mined_template,
                cluster_id=cluster_id,
                cluster_count=cluster_count,
                source_file=record.source_file,
                service=record.service,
                severity=record.severity,
                dataset_template=record.template,
                event_id=record.metadata.get("event_id") if record.metadata else None,
                metadata=dict(record.metadata),
            )
        )

    return TemplateMiningResult(
        mined_records=mined_records,
        cluster_templates=[
            HDFS2kTemplate(event_id=f"cluster-{cluster_id}", event_template=template)
            for cluster_id, template in sorted(cluster_templates.items())
        ],
    )


def mine_hdfs_2k_dataset(dataset: HDFS2kDataset) -> TemplateMiningResult:
    return mine_records(dataset.log_records)


def save_mined_records_csv(mined_records: Iterable[MinedLogRecord], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "record_id",
        "raw_message",
        "mined_template",
        "cluster_id",
        "cluster_count",
        "source_file",
        "service",
        "severity",
        "dataset_template",
        "event_id",
    ]

    with output_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in mined_records:
            writer.writerow(
                {
                    "record_id": record.record_id,
                    "raw_message": record.raw_message,
                    "mined_template": record.mined_template,
                    "cluster_id": record.cluster_id,
                    "cluster_count": record.cluster_count,
                    "source_file": record.source_file or "",
                    "service": record.service or "",
                    "severity": record.severity or "",
                    "dataset_template": record.dataset_template or "",
                    "event_id": record.event_id or "",
                }
            )


def save_cluster_templates_csv(cluster_templates: Iterable[HDFS2kTemplate], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["event_id", "event_template"])
        writer.writeheader()
        for template in cluster_templates:
            writer.writerow(
                {
                    "event_id": template.event_id,
                    "event_template": template.event_template,
                }
            )


def compare_with_dataset_templates(
    mined_records: Iterable[MinedLogRecord],
    dataset_templates: Iterable[HDFS2kTemplate],
) -> dict[str, int]:
    template_lookup = {template.event_template: template.event_id for template in dataset_templates}
    matched = 0
    total = 0

    for record in mined_records:
        total += 1
        if record.dataset_template and record.dataset_template in template_lookup:
            matched += 1

    return {"matched": matched, "total": total, "unmatched": total - matched}


def persist_hdfs_2k_mining_result(
    result: TemplateMiningResult,
    output_root: Path,
) -> MiningExportPaths:
    output_root.mkdir(parents=True, exist_ok=True)
    mined_records_csv = output_root / "hdfs_2k_mined_records.csv"
    cluster_templates_csv = output_root / "hdfs_2k_cluster_templates.csv"

    save_mined_records_csv(result.mined_records, mined_records_csv)
    save_cluster_templates_csv(result.cluster_templates, cluster_templates_csv)

    return MiningExportPaths(
        mined_records_csv=mined_records_csv,
        cluster_templates_csv=cluster_templates_csv,
    )
