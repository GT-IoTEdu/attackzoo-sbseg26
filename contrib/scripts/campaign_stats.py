#!/usr/bin/env python3
"""Summarize an AttackZoo campaign and optionally package generated datasets."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CAMPAIGN_DIR = REPO_ROOT / "experiments" / "all_5runs_4levels"
DEFAULT_DATASETS_DIR = REPO_ROOT / "datasets"
DEFAULT_FIRST_ATTACK = "bf_ssh"
DEFAULT_LAST_ATTACK = "web_xss_scanner"


@dataclass(frozen=True)
class FileSet:
    count: int
    bytes: int


@dataclass(frozen=True)
class TimeSpan:
    start: Optional[dt.datetime]
    end: Optional[dt.datetime]
    seconds: Optional[float]


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate campaign statistics and optionally a tar.gz with generated dataset CSVs.",
    )
    parser.add_argument(
        "--campaign-dir",
        type=Path,
        default=DEFAULT_CAMPAIGN_DIR,
        help=f"Campaign directory to summarize. Default: {DEFAULT_CAMPAIGN_DIR}",
    )
    parser.add_argument(
        "--datasets-output-dir",
        type=Path,
        default=DEFAULT_DATASETS_DIR,
        help=f"Directory where report/archive files are written. Default: {DEFAULT_DATASETS_DIR}",
    )
    parser.add_argument(
        "--first-attack",
        default=DEFAULT_FIRST_ATTACK,
        help="Attack directory used for the earliest filesystem timestamp estimate.",
    )
    parser.add_argument(
        "--last-attack",
        default=DEFAULT_LAST_ATTACK,
        help="Attack directory used for the latest filesystem timestamp estimate.",
    )
    parser.add_argument(
        "--archive-name",
        default=None,
        help="Output archive filename. Default: <campaign-name>_datasets.tar.gz",
    )
    parser.add_argument(
        "--report-name",
        default=None,
        help="Output JSON report filename. Default: <campaign-name>_campaign_stats.json",
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Also create a tar.gz archive with all generated dataset CSVs.",
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing archive/report with the same name.",
    )
    parser.add_argument(
        "--compresslevel",
        type=int,
        choices=range(1, 10),
        default=1,
        metavar="1-9",
        help="Gzip compression level for the dataset archive. Default: 1 (fast).",
    )
    parser.add_argument(
        "--progress-interval",
        type=int,
        default=100,
        help="Print archive progress every N dataset CSV files. Use 0 to disable.",
    )
    return parser.parse_args(argv)


def utc_from_iso(value: Any) -> Optional[dt.datetime]:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def utc_from_mtime(path: Path) -> dt.datetime:
    return dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc)


def read_json(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[WARN] Could not read JSON {path}: {exc}", file=sys.stderr)
        return None
    if isinstance(data, dict):
        return data
    return None


def all_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*") if path.is_file())


def fileset(paths: Iterable[Path]) -> FileSet:
    total = 0
    count = 0
    for path in paths:
        try:
            total += path.stat().st_size
        except OSError as exc:
            print(f"[WARN] Could not stat {path}: {exc}", file=sys.stderr)
            continue
        count += 1
    return FileSet(count=count, bytes=total)


def span(start: Optional[dt.datetime], end: Optional[dt.datetime]) -> TimeSpan:
    if start is None or end is None:
        return TimeSpan(start=start, end=end, seconds=None)
    return TimeSpan(start=start, end=end, seconds=max(0.0, (end - start).total_seconds()))


def filesystem_span(campaign_dir: Path, first_attack: str, last_attack: str) -> TimeSpan:
    first_files = all_files(campaign_dir / first_attack)
    last_files = all_files(campaign_dir / last_attack)
    start = min((utc_from_mtime(path) for path in first_files), default=None)
    end = max((utc_from_mtime(path) for path in last_files), default=None)
    return span(start, end)


def attack_metadata_span(campaign_dir: Path) -> tuple[TimeSpan, list[dict[str, Any]], float]:
    starts: list[dt.datetime] = []
    finishes: list[dt.datetime] = []
    results: list[dict[str, Any]] = []
    elapsed_sum = 0.0

    for path in sorted(campaign_dir.glob("*/campaign_attack_result.json")):
        data = read_json(path)
        if not data:
            continue
        attack_id = data.get("attack_id") or path.parent.name
        finished = utc_from_iso(data.get("finished_at_utc"))
        elapsed_s = data.get("elapsed_s")
        started = None
        if finished is not None and isinstance(elapsed_s, (int, float)):
            started = finished - dt.timedelta(seconds=float(elapsed_s))
            elapsed_sum += float(elapsed_s)
        if started is not None:
            starts.append(started)
        if finished is not None:
            finishes.append(finished)
        results.append(
            {
                "attack_id": attack_id,
                "status": data.get("status"),
                "started_at_utc_estimated": iso(started),
                "finished_at_utc": iso(finished),
                "elapsed_s": elapsed_s,
            }
        )

    return span(min(starts, default=None), max(finishes, default=None)), results, elapsed_sum


def campaign_config_span(campaign_dir: Path) -> tuple[TimeSpan, Optional[dict[str, Any]], Optional[dict[str, Any]]]:
    campaign_meta_dir = campaign_dir / "_campaign"
    config = read_json(campaign_meta_dir / "campaign_config.json")
    finished = read_json(campaign_meta_dir / "campaign_finished.json")
    start = utc_from_iso(config.get("started_at_utc")) if config else None
    end = utc_from_iso(finished.get("finished_at_utc")) if finished else None
    return span(start, end), config, finished


def campaign_finished_span(start: Optional[dt.datetime], campaign_dir: Path) -> TimeSpan:
    finished = read_json(campaign_dir / "_campaign" / "campaign_finished.json")
    end = utc_from_iso(finished.get("finished_at_utc")) if finished else None
    return span(start, end)


def dataset_csvs(campaign_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in campaign_dir.glob("*/datasets/*.csv")
        if path.is_file()
    )


def pcap_files(campaign_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in campaign_dir.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pcap"
    )


def iso(value: Optional[dt.datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.astimezone(dt.timezone.utc).isoformat(timespec="seconds")


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    amount = float(value)
    for unit in units:
        if abs(amount) < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(amount)} {unit}"
            return f"{amount:.2f} {unit}"
        amount /= 1024.0
    return f"{value} B"


def hours(seconds: Optional[float]) -> Optional[float]:
    if seconds is None:
        return None
    return seconds / 3600.0


def serialize_timespan(value: TimeSpan) -> dict[str, Any]:
    return {
        "start_utc": iso(value.start),
        "end_utc": iso(value.end),
        "seconds": value.seconds,
        "hours": hours(value.seconds),
    }


def add_csvs_to_tar(
    tar: tarfile.TarFile,
    campaign_dir: Path,
    csv_paths: list[Path],
    progress_interval: int,
) -> None:
    total = len(csv_paths)
    for index, path in enumerate(csv_paths, start=1):
        archive_name = Path(campaign_dir.name) / path.relative_to(campaign_dir)
        tar.add(path, arcname=str(archive_name), recursive=False)
        if progress_interval > 0 and (index % progress_interval == 0 or index == total):
            print(f"[archive] added {index}/{total} dataset CSVs", file=sys.stderr, flush=True)


def create_dataset_archive(
    campaign_dir: Path,
    csv_paths: list[Path],
    output_path: Path,
    overwrite: bool,
    compresslevel: int,
    progress_interval: int,
) -> FileSet:
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} already exists; use --overwrite to replace it")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pigz = shutil.which("pigz")
    if pigz:
        print(f"[archive] using pigz -{compresslevel} for parallel gzip compression", file=sys.stderr)
        with output_path.open("wb") as output:
            proc = subprocess.Popen(
                [pigz, f"-{compresslevel}", "-c"],
                stdin=subprocess.PIPE,
                stdout=output,
            )
            assert proc.stdin is not None
            try:
                with tarfile.open(fileobj=proc.stdin, mode="w|") as tar:
                    add_csvs_to_tar(tar, campaign_dir, csv_paths, progress_interval)
            except Exception:
                proc.kill()
                proc.wait()
                raise
            returncode = proc.wait()
            if returncode != 0:
                raise RuntimeError(f"pigz exited with status {returncode}")
    else:
        print(f"[archive] pigz not found; using Python gzip compresslevel={compresslevel}", file=sys.stderr)
        with tarfile.open(output_path, mode="w:gz", compresslevel=compresslevel) as tar:
            add_csvs_to_tar(tar, campaign_dir, csv_paths, progress_interval)
    return fileset([output_path])


def write_report(output_path: Path, payload: dict[str, Any], overwrite: bool) -> None:
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} already exists; use --overwrite to replace it")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def print_summary(report: dict[str, Any]) -> None:
    runtime = report["runtime"]
    files = report["files"]
    archive = report.get("archive")

    print("Campaign statistics")
    print(f"- Campaign dir: {report['campaign_dir']}")
    print(
        "- Execution estimate (filesystem): "
        f"{runtime['filesystem_first_to_last']['hours']:.2f} h "
        f"({runtime['filesystem_first_to_last']['start_utc']} -> {runtime['filesystem_first_to_last']['end_utc']})"
    )
    if runtime["attack_metadata"]["hours"] is not None:
        print(
            "- Attack metadata window: "
            f"{runtime['attack_metadata']['hours']:.2f} h "
            f"({runtime['attack_metadata']['start_utc']} -> {runtime['attack_metadata']['end_utc']})"
        )
    if runtime["attack_metadata_to_campaign_finished"]["hours"] is not None:
        print(
            "- Attack metadata to campaign finished: "
            f"{runtime['attack_metadata_to_campaign_finished']['hours']:.2f} h "
            f"({runtime['attack_metadata_to_campaign_finished']['start_utc']} -> "
            f"{runtime['attack_metadata_to_campaign_finished']['end_utc']})"
        )
    if runtime["campaign_config_to_finished"]["hours"] is not None:
        print(
            "- Last campaign config to finished: "
            f"{runtime['campaign_config_to_finished']['hours']:.2f} h "
            f"({runtime['campaign_config_to_finished']['start_utc']} -> "
            f"{runtime['campaign_config_to_finished']['end_utc']})"
        )
    print(f"- PCAP files: {files['pcap']['count']} ({files['pcap']['human_size']})")
    print(f"- Dataset CSV files: {files['dataset_csv']['count']} ({files['dataset_csv']['human_size']})")
    if archive:
        print(f"- Dataset archive: {archive['path']} ({archive['human_size']})")
    print(f"- JSON report: {report['report_path']}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    campaign_dir = args.campaign_dir.resolve()
    output_dir = args.datasets_output_dir.resolve()

    if not campaign_dir.is_dir():
        print(f"[ERROR] Campaign directory not found: {campaign_dir}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_name = args.archive_name or f"{campaign_dir.name}_datasets.tar.gz"
    report_name = args.report_name or f"{campaign_dir.name}_campaign_stats.json"
    archive_path = output_dir / archive_name
    report_path = output_dir / report_name

    pcaps = pcap_files(campaign_dir)
    csvs = dataset_csvs(campaign_dir)
    pcap_stats = fileset(pcaps)
    csv_stats = fileset(csvs)

    fs_span = filesystem_span(campaign_dir, args.first_attack, args.last_attack)
    attack_span, attack_results, attack_elapsed_sum = attack_metadata_span(campaign_dir)
    config_span, config, finished = campaign_config_span(campaign_dir)
    attack_to_finished = campaign_finished_span(attack_span.start, campaign_dir)

    report: dict[str, Any] = {
        "campaign_dir": str(campaign_dir),
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "runtime": {
            "filesystem_first_to_last": serialize_timespan(fs_span),
            "filesystem_first_attack": args.first_attack,
            "filesystem_last_attack": args.last_attack,
            "attack_metadata": serialize_timespan(attack_span),
            "attack_metadata_to_campaign_finished": serialize_timespan(attack_to_finished),
            "campaign_config_to_finished": serialize_timespan(config_span),
            "sum_attack_elapsed_s": attack_elapsed_sum,
            "sum_attack_elapsed_hours": hours(attack_elapsed_sum),
        },
        "files": {
            "pcap": {
                "count": pcap_stats.count,
                "bytes": pcap_stats.bytes,
                "human_size": human_bytes(pcap_stats.bytes),
            },
            "dataset_csv": {
                "count": csv_stats.count,
                "bytes": csv_stats.bytes,
                "human_size": human_bytes(csv_stats.bytes),
            },
        },
        "metadata": {
            "campaign_config_started_at_utc": iso(utc_from_iso(config.get("started_at_utc"))) if config else None,
            "campaign_config_attack_count": config.get("attack_count") if config else None,
            "campaign_finished_at_utc": iso(utc_from_iso(finished.get("finished_at_utc"))) if finished else None,
            "campaign_finished_exit_code": finished.get("exit_code") if finished else None,
            "attack_result_count": len(attack_results),
            "attack_results": attack_results,
        },
        "report_path": str(report_path),
    }

    should_archive = args.archive and not args.no_archive
    if should_archive:
        archive_stats = create_dataset_archive(
            campaign_dir,
            csvs,
            archive_path,
            args.overwrite,
            args.compresslevel,
            args.progress_interval,
        )
        report["archive"] = {
            "path": str(archive_path),
            "bytes": archive_stats.bytes,
            "human_size": human_bytes(archive_stats.bytes),
            "format": "tar.gz",
            "dataset_csv_count": len(csvs),
        }

    write_report(report_path, report, args.overwrite)
    print_summary(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
