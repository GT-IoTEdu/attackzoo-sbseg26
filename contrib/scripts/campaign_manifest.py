#!/usr/bin/env python3
"""Audit an AttackZoo campaign without modifying its source artifacts."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CAMPAIGN_DIR = REPO_ROOT / "experiments" / "all_5runs_4levels"
EXTRACTORS = ("ntlflowlyzer", "tshark", "scapy")
LEVELS = tuple(f"L{number}" for number in range(4))
RUNS = tuple(f"run{number:02d}" for number in range(1, 6))
SPLITS = {
    "run01": "development",
    "run02": "development",
    "run03": "development",
    "run04": "validation",
    "run05": "test",
}
CHUNK_SIZE = 8 * 1024 * 1024


@dataclass(frozen=True)
class FileInspection:
    exists: bool
    bytes: Optional[int] = None
    sha256: Optional[str] = None
    physical_lines: Optional[int] = None
    data_lines: Optional[int] = None
    column_count: Optional[int] = None
    schema_sha256: Optional[str] = None
    error: Optional[str] = None


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a one-row-per-execution manifest and a campaign audit summary. "
            "Source artifacts are opened read-only."
        ),
    )
    parser.add_argument(
        "--campaign-dir",
        type=Path,
        default=DEFAULT_CAMPAIGN_DIR,
        help=f"Campaign directory. Default: {DEFAULT_CAMPAIGN_DIR}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory. Default: contrib/reports/<campaign>/audit",
    )
    parser.add_argument(
        "--content",
        choices=("metadata", "hashes", "full"),
        default="metadata",
        help=(
            "metadata: paths and sizes; hashes: also SHA-256; full: also CSV line "
            "counts and schemas. Default: metadata"
        ),
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=min(8, os.cpu_count() or 1),
        help="Concurrent file readers for hashes/full mode. Default: min(8, CPU count)",
    )
    parser.add_argument(
        "--progress-interval",
        type=int,
        default=100,
        help="Report progress every N inspected files; 0 disables it. Default: 100",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Audit only the first N metadata files (smoke testing only).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace manifest.csv and summary.json if they already exist.",
    )
    parser.add_argument(
        "--fail-on-issues",
        action="store_true",
        help="Exit with status 1 when any execution has an audit issue.",
    )
    return parser.parse_args(argv)


def read_json(path: Path) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(payload, dict):
        return None, "top-level JSON value is not an object"
    return payload, None


def relative(path: Path, campaign_dir: Path) -> str:
    try:
        return path.relative_to(campaign_dir).as_posix()
    except ValueError:
        return str(path)


def resolved_artifact(
    recorded: Any,
    parent: Path,
    fallback_name: str,
) -> Path:
    """Resolve by basename so stale absolute repository prefixes are harmless."""
    if isinstance(recorded, str) and recorded:
        return parent / Path(recorded).name
    return parent / fallback_name


def inspect_file(path: Path, content: str, is_csv: bool) -> FileInspection:
    try:
        size = path.stat().st_size
    except FileNotFoundError:
        return FileInspection(exists=False)
    except OSError as exc:
        return FileInspection(exists=False, error=str(exc))

    if not path.is_file():
        return FileInspection(exists=False, error="path is not a regular file")
    if content == "metadata":
        return FileInspection(exists=True, bytes=size)

    digest = hashlib.sha256()
    physical_lines = 0
    last_byte = b""
    header = bytearray()
    header_finished = False
    try:
        with path.open("rb") as handle:
            while chunk := handle.read(CHUNK_SIZE):
                digest.update(chunk)
                if is_csv:
                    physical_lines += chunk.count(b"\n")
                    last_byte = chunk[-1:]
                    if content == "full" and not header_finished:
                        newline_at = chunk.find(b"\n")
                        if newline_at >= 0:
                            header.extend(chunk[:newline_at])
                            header_finished = True
                        else:
                            header.extend(chunk)
    except OSError as exc:
        return FileInspection(exists=True, bytes=size, error=str(exc))

    if content != "full" or not is_csv:
        return FileInspection(exists=True, bytes=size, sha256=digest.hexdigest())

    if size and last_byte != b"\n":
        physical_lines += 1
    data_lines = max(0, physical_lines - 1)
    schema_sha256: Optional[str] = None
    column_count: Optional[int] = None
    error: Optional[str] = None
    if header:
        schema_sha256 = hashlib.sha256(bytes(header)).hexdigest()
        try:
            decoded = header.decode("utf-8-sig")
            column_count = len(next(csv.reader([decoded])))
        except (UnicodeDecodeError, csv.Error, StopIteration) as exc:
            error = f"could not parse CSV header: {exc}"
    return FileInspection(
        exists=True,
        bytes=size,
        sha256=digest.hexdigest(),
        physical_lines=physical_lines,
        data_lines=data_lines,
        column_count=column_count,
        schema_sha256=schema_sha256,
        error=error,
    )


def inspect_paths(
    path_kinds: dict[Path, bool],
    content: str,
    workers: int,
    progress_interval: int,
) -> dict[Path, FileInspection]:
    if workers < 1:
        raise ValueError("--workers must be at least 1")
    if content == "metadata":
        return {
            path: inspect_file(path, content=content, is_csv=is_csv)
            for path, is_csv in path_kinds.items()
        }

    results: dict[Path, FileInspection] = {}
    total = len(path_kinds)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(inspect_file, path, content, is_csv): path
            for path, is_csv in path_kinds.items()
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            path = futures[future]
            results[path] = future.result()
            if progress_interval > 0 and (completed % progress_interval == 0 or completed == total):
                print(f"[audit] inspected {completed}/{total} files", file=sys.stderr, flush=True)
    return results


def add_file_fields(
    row: dict[str, Any],
    prefix: str,
    path: Path,
    inspection: FileInspection,
    campaign_dir: Path,
) -> None:
    row[f"{prefix}_path"] = relative(path, campaign_dir)
    for name, value in asdict(inspection).items():
        row[f"{prefix}_{name}"] = value


def parse_records(
    campaign_dir: Path,
    meta_paths: list[Path],
) -> tuple[list[dict[str, Any]], dict[Path, bool]]:
    records: list[dict[str, Any]] = []
    path_kinds: dict[Path, bool] = {}

    for meta_path in meta_paths:
        meta, meta_error = read_json(meta_path)
        meta = meta or {}
        attack_root = meta_path.parents[3]
        attack_id = str(meta.get("attack_id") or attack_root.name)
        service = str(meta.get("service") or meta_path.parents[2].name)
        level = str(meta.get("level") or meta_path.parent.parent.name)
        run_id = str(meta.get("run_id") or meta_path.parent.name)
        stem = f"{service}-{attack_id}-{level}-{run_id}"

        pcap_path = resolved_artifact(meta.get("pcap"), meta_path.parent, f"{stem}.pcap")
        dataset_path = resolved_artifact(
            meta.get("dataset"),
            attack_root / "datasets",
            f"unsupervised-{stem}.csv",
        )
        feature_paths: dict[str, Path] = {}
        feature_meta = meta.get("features") if isinstance(meta.get("features"), dict) else {}
        for extractor in EXTRACTORS:
            extractor_meta = feature_meta.get(extractor) if isinstance(feature_meta.get(extractor), dict) else {}
            feature_paths[extractor] = resolved_artifact(
                extractor_meta.get("output"),
                attack_root / "features",
                f"{extractor}-{stem}.csv",
            )

        path_kinds[meta_path] = False
        path_kinds[pcap_path] = False
        path_kinds[dataset_path] = True
        for path in feature_paths.values():
            path_kinds[path] = True

        records.append(
            {
                "meta": meta,
                "meta_error": meta_error,
                "meta_path_obj": meta_path,
                "attack_id": attack_id,
                "service": service,
                "level": level,
                "run_id": run_id,
                "pcap_path_obj": pcap_path,
                "dataset_path_obj": dataset_path,
                "feature_paths": feature_paths,
            }
        )
    return records, path_kinds


def build_rows(
    campaign_dir: Path,
    records: list[dict[str, Any]],
    inspections: dict[Path, FileInspection],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        meta = record["meta"]
        issues: list[str] = []
        if record["meta_error"]:
            issues.append("invalid_meta_json")
        if record["level"] not in LEVELS:
            issues.append("unexpected_level")
        if record["run_id"] not in RUNS:
            issues.append("unexpected_run_id")

        row: dict[str, Any] = {
            "campaign_id": campaign_dir.name,
            "attack_id": record["attack_id"],
            "service": record["service"],
            "level": record["level"],
            "run_id": record["run_id"],
            "split": SPLITS.get(record["run_id"], "unknown"),
            "started_at_utc": meta.get("started_at_utc"),
            "finished_at_utc": meta.get("finished_at_utc"),
            "warmup_s": meta.get("warmup_s"),
            "attack_s": meta.get("attack_s"),
            "cooldown_s": meta.get("cooldown_s"),
        }
        for prefix, path in (
            ("meta", record["meta_path_obj"]),
            ("pcap", record["pcap_path_obj"]),
            ("dataset", record["dataset_path_obj"]),
        ):
            inspection = inspections[path]
            add_file_fields(row, prefix, path, inspection, campaign_dir)
            if not inspection.exists:
                issues.append(f"missing_{prefix}")
            elif inspection.bytes == 0:
                issues.append(f"empty_{prefix}")
            if inspection.error:
                issues.append(f"unreadable_{prefix}")

        feature_meta = meta.get("features") if isinstance(meta.get("features"), dict) else {}
        for extractor in EXTRACTORS:
            path = record["feature_paths"][extractor]
            inspection = inspections[path]
            add_file_fields(row, extractor, path, inspection, campaign_dir)
            extractor_meta = feature_meta.get(extractor) if isinstance(feature_meta.get(extractor), dict) else {}
            reported_ok = extractor_meta.get("ok")
            row[f"{extractor}_reported_ok"] = reported_ok
            row[f"{extractor}_returncode"] = extractor_meta.get("returncode")
            if not inspection.exists:
                issues.append(f"missing_{extractor}")
            elif inspection.bytes == 0:
                issues.append(f"empty_{extractor}")
            elif inspection.data_lines == 0:
                issues.append(f"no_data_{extractor}")
            if reported_ok is False:
                issues.append(f"reported_failure_{extractor}")
            if inspection.error:
                issues.append(f"unreadable_{extractor}")

        row["audit_pass"] = not issues
        row["issue_codes"] = ";".join(sorted(set(issues)))
        rows.append(row)

    return sorted(rows, key=lambda row: (row["attack_id"], row["level"], row["run_id"]))


def build_summary(
    campaign_dir: Path,
    rows: list[dict[str, Any]],
    content: str,
    partial: bool,
) -> dict[str, Any]:
    attacks = sorted({str(row["attack_id"]) for row in rows})
    keys = [(row["attack_id"], row["level"], row["run_id"]) for row in rows]
    key_counts = Counter(keys)
    duplicates = [list(key) for key, count in key_counts.items() if count > 1]
    missing: list[list[str]] = []
    if not partial:
        actual = set(keys)
        missing = [
            [attack, level, run_id]
            for attack in attacks
            for level in LEVELS
            for run_id in RUNS
            if (attack, level, run_id) not in actual
        ]

    issue_counts: Counter[str] = Counter()
    for row in rows:
        issue_counts.update(code for code in str(row["issue_codes"]).split(";") if code)

    artifact_summary: dict[str, dict[str, Any]] = {}
    for prefix in ("meta", "pcap", *EXTRACTORS, "dataset"):
        artifact: dict[str, Any] = {
            "present": sum(bool(row[f"{prefix}_exists"]) for row in rows),
            "missing": sum(not bool(row[f"{prefix}_exists"]) for row in rows),
            "bytes": sum(int(row[f"{prefix}_bytes"] or 0) for row in rows),
        }
        hashes = [str(row[f"{prefix}_sha256"]) for row in rows if row[f"{prefix}_sha256"]]
        if hashes:
            artifact["unique_sha256_count"] = len(set(hashes))
        if prefix in (*EXTRACTORS, "dataset") and content == "full":
            data_lines = [int(row[f"{prefix}_data_lines"] or 0) for row in rows]
            schemas = Counter(
                (str(row[f"{prefix}_schema_sha256"]), int(row[f"{prefix}_column_count"]))
                for row in rows
                if row[f"{prefix}_schema_sha256"] and row[f"{prefix}_column_count"] is not None
            )
            artifact.update(
                {
                    "total_data_lines": sum(data_lines),
                    "min_data_lines": min(data_lines, default=None),
                    "max_data_lines": max(data_lines, default=None),
                    "schema_variant_count": len(schemas),
                    "schemas": [
                        {
                            "sha256": schema_hash,
                            "column_count": column_count,
                            "execution_count": count,
                        }
                        for (schema_hash, column_count), count in sorted(schemas.items())
                    ],
                }
            )
        artifact_summary[prefix] = artifact

    starts = sorted(str(row["started_at_utc"]) for row in rows if row["started_at_utc"])
    finishes = sorted(str(row["finished_at_utc"]) for row in rows if row["finished_at_utc"])
    return {
        "schema_version": "1.0",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "campaign_id": campaign_dir.name,
        "campaign_dir": str(campaign_dir),
        "content_mode": content,
        "partial": partial,
        "execution_count": len(rows),
        "attack_count": len(attacks),
        "expected_execution_count": None if partial else len(attacks) * len(LEVELS) * len(RUNS),
        "duplicate_execution_keys": duplicates,
        "missing_execution_keys": missing,
        "split_counts": dict(sorted(Counter(str(row["split"]) for row in rows).items())),
        "started_at_utc_min": starts[0] if starts else None,
        "finished_at_utc_max": finishes[-1] if finishes else None,
        "audit_pass_count": sum(bool(row["audit_pass"]) for row in rows),
        "audit_issue_count": sum(not bool(row["audit_pass"]) for row in rows),
        "issue_counts": dict(sorted(issue_counts.items())),
        "artifacts": artifact_summary,
    }


def write_outputs(
    output_dir: Path,
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
    overwrite: bool,
) -> tuple[Path, Path]:
    manifest_path = output_dir / "manifest.csv"
    summary_path = output_dir / "summary.json"
    existing = [path for path in (manifest_path, summary_path) if path.exists()]
    if existing and not overwrite:
        names = ", ".join(str(path) for path in existing)
        raise FileExistsError(f"output already exists: {names}; use --overwrite")
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_tmp = manifest_path.with_suffix(".csv.tmp")
    summary_tmp = summary_path.with_suffix(".json.tmp")
    fieldnames = list(rows[0]) if rows else []
    with manifest_tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    with summary_tmp.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    manifest_tmp.replace(manifest_path)
    summary_tmp.replace(summary_path)
    return manifest_path, summary_path


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    campaign_dir = args.campaign_dir.resolve()
    if not campaign_dir.is_dir():
        print(f"[ERROR] Campaign directory not found: {campaign_dir}", file=sys.stderr)
        return 2
    if args.limit is not None and args.limit < 1:
        print("[ERROR] --limit must be at least 1", file=sys.stderr)
        return 2

    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else REPO_ROOT / "contrib" / "reports" / campaign_dir.name / "audit"
    )
    meta_paths = sorted(campaign_dir.rglob("meta.json"))
    if args.limit is not None:
        meta_paths = meta_paths[: args.limit]
    if not meta_paths:
        print(f"[ERROR] No meta.json files found under {campaign_dir}", file=sys.stderr)
        return 2

    records, path_kinds = parse_records(campaign_dir, meta_paths)
    try:
        inspections = inspect_paths(
            path_kinds,
            content=args.content,
            workers=args.workers,
            progress_interval=args.progress_interval,
        )
        rows = build_rows(campaign_dir, records, inspections)
        summary = build_summary(
            campaign_dir,
            rows,
            content=args.content,
            partial=args.limit is not None,
        )
        manifest_path, summary_path = write_outputs(output_dir, rows, summary, args.overwrite)
    except (FileExistsError, OSError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    print("Campaign audit")
    print(f"- Campaign: {campaign_dir}")
    print(f"- Executions: {summary['execution_count']}")
    print(f"- Attacks: {summary['attack_count']}")
    print(f"- Audit pass/issues: {summary['audit_pass_count']}/{summary['audit_issue_count']}")
    print(f"- Manifest: {manifest_path}")
    print(f"- Summary: {summary_path}")
    if args.fail_on_issues and summary["audit_issue_count"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
