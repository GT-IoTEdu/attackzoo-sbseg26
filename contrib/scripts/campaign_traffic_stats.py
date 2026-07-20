#!/usr/bin/env python3
"""Build traffic statistics and plots for an AttackZoo campaign."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CAMPAIGN_DIR = REPO_ROOT / "experiments" / "all_5runs_4levels"
DEFAULT_FIGSHARE_CAMPAIGN_DIR = REPO_ROOT / "downloads" / "figshare" / "extracted" / "all_5runs_4levels"
DEFAULT_REPORTS_ROOT = REPO_ROOT / "contrib" / "reports"

TSHARK_FIELDS = (
    "frame.time_epoch",
    "frame.len",
    "ip.proto",
    "ipv6.nxt",
    "tcp.srcport",
    "tcp.dstport",
    "udp.srcport",
    "udp.dstport",
    "sctp.srcport",
    "sctp.dstport",
    "icmp.type",
    "icmpv6.type",
    "_ws.col.protocol",
)

FEATURE_FIELD_ALIASES = {
    "time_epoch": ("frame.time_epoch",),
    "frame_len": ("frame.len",),
    "ip_proto": ("ip.proto",),
    "ipv6_nxt": ("ipv6.nxt",),
    "tcp_srcport": ("tcp.srcport",),
    "tcp_dstport": ("tcp.dstport",),
    "udp_srcport": ("udp.srcport",),
    "udp_dstport": ("udp.dstport",),
    "sctp_srcport": ("sctp.srcport",),
    "sctp_dstport": ("sctp.dstport",),
    "icmp_type": ("icmp.type",),
    "icmpv6_type": ("icmpv6.type",),
    "ws_protocol": ("_ws.col.protocol", "_ws.col.Protocol"),
}

IP_PROTOCOLS = {
    "1": "ICMP",
    "2": "IGMP",
    "6": "TCP",
    "17": "UDP",
    "47": "GRE",
    "50": "ESP",
    "51": "AH",
    "58": "ICMPv6",
    "89": "OSPF",
    "132": "SCTP",
}

LEVEL_ORDER = ("L0", "L1", "L2", "L3")
LEVEL_COLORS = {
    "L0": "#1f77b4",
    "L1": "#ff7f0e",
    "L2": "#2ca02c",
    "L3": "#d62728",
}

PLOT_CHOICES = (
    "protocol",
    "ports",
    "pps",
    "bps",
    "heatmap",
    "dataset_rows",
    "stability",
    "phase_metrics",
)
PLOT_ALIASES = {
    "all": set(PLOT_CHOICES),
    "protocols": {"protocol"},
    "port": {"ports"},
    "pps_by_level": {"pps"},
    "bytes": {"bps"},
    "category_heatmap": {"heatmap"},
    "datasets": {"dataset_rows"},
    "dataset": {"dataset_rows"},
    "rows": {"dataset_rows"},
    "reexecution": {"stability"},
    "reproducibility": {"stability"},
    "availability": {"phase_metrics"},
    "latency": {"phase_metrics"},
    "phases": {"phase_metrics"},
}

CATEGORY_SHORT_LABELS = {
    "1) Reconnaissance and Discovery": "Recon. and\nDiscovery",
    "2) Network Interception and Exploitation": "Network\nInterception",
    "3) Web Application Attacks": "Web\nApplications",
    "4) Brute Force Against Remote Access Applications": "Remote Access\nBrute Force",
    "5) Exfiltration and Tunneling": "Exfiltration and\nTunneling",
    "6) Denial of Service and Impact": "DoS and\nImpact",
    "7) IoT": "IoT",
}


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate packet/port/protocol/pps/Bps statistics from campaign PCAPs.",
    )
    parser.add_argument(
        "--campaign-dir",
        type=Path,
        default=None,
        help=(
            "Campaign directory. Default: auto-detects "
            f"{DEFAULT_FIGSHARE_CAMPAIGN_DIR} or {DEFAULT_CAMPAIGN_DIR}."
        ),
    )
    parser.add_argument(
        "--reports-root",
        type=Path,
        default=DEFAULT_REPORTS_ROOT,
        help=f"Root directory for reports. Default: {DEFAULT_REPORTS_ROOT}",
    )
    parser.add_argument(
        "--campaign-name",
        default=None,
        help="Report directory name. Default: basename of --campaign-dir.",
    )
    parser.add_argument(
        "--source",
        choices=("auto", "features", "pcap"),
        default="auto",
        help="Read existing tshark feature CSVs, PCAPs via tshark, or auto fallback. Default: auto.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocess all PCAPs instead of reusing file_summaries cache.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Process only the first N PCAPs; useful for smoke tests.",
    )
    parser.add_argument(
        "--top-ports",
        type=int,
        default=10,
        help="Number of ports shown in the port plot. CSVs include all ports.",
    )
    parser.add_argument(
        "--top-protocols",
        type=int,
        default=10,
        help="Number of protocols shown in the protocol plot. CSV includes all protocols.",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Only write CSV/JSON outputs, without PNG plots.",
    )
    parser.add_argument(
        "--plots",
        default="all",
        help=(
            "Comma-separated plots to generate: all, protocol, ports, pps, bps, heatmap, "
            "dataset_rows, stability, phase_metrics. Example: --plots stability,phase_metrics. Default: all."
        ),
    )
    parser.add_argument(
        "--heatmap-metric",
        choices=("byte_count", "packet_count", "pcap_size_mb"),
        default="byte_count",
        help="Metric used in the category/level heatmap. Default: byte_count.",
    )
    parser.add_argument(
        "--variability-metric",
        default="dataset_rows",
        help="Metric from T6_reexecution_stability.csv used in the textual variability table. Default: dataset_rows.",
    )
    parser.add_argument(
        "--stability-metrics",
        default="dataset_rows,pcap_size_mb,execution_time_s,lat_p95_attack_censored_ms",
        help=(
            "Comma-separated metrics from T6_reexecution_stability.csv used in the cv_pct stability "
            "heatmap. Default: dataset_rows,pcap_size_mb,execution_time_s,lat_p95_attack_censored_ms."
        ),
    )
    parser.add_argument(
        "--progress-interval",
        type=int,
        default=25,
        help="Print progress every N processed PCAPs. Use 0 to disable.",
    )
    return parser.parse_args(argv)


def read_json(path: Path) -> Optional[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def sha1_text(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


def find_dataset_csvs(campaign_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in campaign_dir.glob("*/datasets/*.csv")
        if path.is_file()
    )


def campaign_has_inputs(campaign_dir: Path) -> bool:
    return bool(find_pcaps(campaign_dir) or find_dataset_csvs(campaign_dir))


def resolve_campaign_dir(requested: Optional[Path]) -> Path:
    if requested is not None:
        return requested.resolve()

    candidates = (
        DEFAULT_FIGSHARE_CAMPAIGN_DIR,
        DEFAULT_CAMPAIGN_DIR,
    )
    for candidate in candidates:
        if candidate.is_dir() and campaign_has_inputs(candidate):
            return candidate.resolve()

    for root in (DEFAULT_FIGSHARE_CAMPAIGN_DIR.parent, DEFAULT_CAMPAIGN_DIR.parent):
        if not root.is_dir():
            continue
        for candidate in sorted(root.rglob("all_5runs_4levels")):
            if candidate.is_dir() and campaign_has_inputs(candidate):
                return candidate.resolve()

    return DEFAULT_CAMPAIGN_DIR.resolve()


def find_pcaps(campaign_dir: Path) -> list[Path]:
    return sorted(
        path for path in campaign_dir.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pcap"
    )


def parse_pcap_identity(campaign_dir: Path, pcap: Path) -> dict[str, Any]:
    rel = pcap.relative_to(campaign_dir)
    parts = rel.parts
    attack_id = parts[0] if parts else ""
    level = next((part for part in parts if part in LEVEL_ORDER), "")
    run_id = next((part for part in parts if part.startswith("run")), "")
    service = pcap.name.split("-", 1)[0] if "-" in pcap.name else ""
    meta = read_json(pcap.with_name("meta.json")) or {}
    return {
        "campaign_relative_path": str(rel),
        "attack_id": meta.get("attack_id") or attack_id,
        "level": meta.get("level") or level,
        "run_id": meta.get("run_id") or run_id,
        "service": meta.get("service") or service,
        "started_at_utc": meta.get("started_at_utc"),
        "finished_at_utc": meta.get("finished_at_utc"),
    }


def feature_csv_for_pcap(campaign_dir: Path, pcap: Path) -> Path:
    rel = pcap.relative_to(campaign_dir)
    attack_id = rel.parts[0]
    return campaign_dir / attack_id / "features" / f"tshark-{pcap.stem}.csv"


def summary_path_for_pcap(summary_dir: Path, campaign_dir: Path, pcap: Path) -> Path:
    rel = str(pcap.relative_to(campaign_dir))
    return summary_dir / f"{sha1_text(rel)}.json"


def first_value(value: str) -> str:
    # Tshark can emit multiple occurrences; occurrence=f should avoid this, but keep the parser defensive.
    if not value:
        return ""
    return value.split(",", 1)[0].strip().strip('"')


def to_int(value: str) -> Optional[int]:
    value = first_value(value)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return int(float(value))
        except ValueError:
            return None


def to_float(value: str) -> Optional[float]:
    value = first_value(value)
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def normalize_ws_protocol(value: str) -> str:
    value = first_value(value).strip()
    if not value:
        return "OTHER"
    upper = value.upper()
    if upper in {"TCP", "UDP", "ICMP", "ICMPV6", "ARP", "SCTP"}:
        return "ICMPv6" if upper == "ICMPV6" else upper
    if "ICMPV6" in upper or "ICMPV6" in upper.replace("-", ""):
        return "ICMPv6"
    if "ICMP" in upper:
        return "ICMP"
    if "TCP" in upper:
        return "TCP"
    if "UDP" in upper:
        return "UDP"
    if "ARP" in upper:
        return "ARP"
    return upper


def protocol_name(ip_proto: str, ipv6_nxt: str, ws_protocol: str, icmpv6_type: str) -> str:
    proto = first_value(ip_proto) or first_value(ipv6_nxt)
    if proto in IP_PROTOCOLS:
        return IP_PROTOCOLS[proto]
    if icmpv6_type:
        return "ICMPv6"
    return normalize_ws_protocol(ws_protocol)


def service_port(src: Optional[int], dst: Optional[int]) -> Optional[int]:
    ports = [port for port in (src, dst) if port is not None and port >= 0]
    if not ports:
        return None
    if len(ports) == 1:
        return ports[0]
    # For request and response packets this usually maps traffic back to the server-side port
    # instead of scattering counts across ephemeral client ports.
    return min(ports)


def packet_port(protocol: str, row: dict[str, str]) -> Optional[tuple[str, int]]:
    if protocol == "TCP":
        port = service_port(to_int(row.get("tcp_srcport", "")), to_int(row.get("tcp_dstport", "")))
        return ("TCP", port) if port is not None else None
    if protocol == "UDP":
        port = service_port(to_int(row.get("udp_srcport", "")), to_int(row.get("udp_dstport", "")))
        return ("UDP", port) if port is not None else None
    if protocol == "SCTP":
        port = service_port(to_int(row.get("sctp_srcport", "")), to_int(row.get("sctp_dstport", "")))
        return ("SCTP", port) if port is not None else None
    return None


def empty_summary(campaign_dir: Path, pcap: Path, source_path: Path, source_kind: str) -> dict[str, Any]:
    identity = parse_pcap_identity(campaign_dir, pcap)
    stat = pcap.stat()
    return {
        "schema_version": 1,
        "ok": True,
        "error": "",
        "source_kind": source_kind,
        "source_path": str(source_path),
        "pcap_path": str(pcap),
        "pcap_mtime_ns": stat.st_mtime_ns,
        "pcap_size_bytes": stat.st_size,
        **identity,
        "packet_count": 0,
        "byte_count": 0,
        "first_epoch": None,
        "last_epoch": None,
        "protocol_counts": {},
        "protocol_bytes": {},
        "port_counts": {},
        "port_bytes": {},
        "second_packet_counts": {},
        "second_byte_counts": {},
    }


def update_summary(summary: dict[str, Any], row: dict[str, str]) -> None:
    epoch = to_float(row.get("time_epoch", ""))
    frame_len = to_int(row.get("frame_len", "")) or 0
    protocol = protocol_name(
        row.get("ip_proto", ""),
        row.get("ipv6_nxt", ""),
        row.get("ws_protocol", ""),
        row.get("icmpv6_type", ""),
    )

    summary["packet_count"] += 1
    summary["byte_count"] += frame_len
    summary["protocol_counts"][protocol] = summary["protocol_counts"].get(protocol, 0) + 1
    summary["protocol_bytes"][protocol] = summary["protocol_bytes"].get(protocol, 0) + frame_len

    port_key = packet_port(protocol, row)
    if port_key is not None:
        key = f"{port_key[0]}/{port_key[1]}"
        summary["port_counts"][key] = summary["port_counts"].get(key, 0) + 1
        summary["port_bytes"][key] = summary["port_bytes"].get(key, 0) + frame_len

    if epoch is not None and math.isfinite(epoch):
        second = int(math.floor(epoch))
        second_key = str(second)
        summary["second_packet_counts"][second_key] = summary["second_packet_counts"].get(second_key, 0) + 1
        summary["second_byte_counts"][second_key] = summary["second_byte_counts"].get(second_key, 0) + frame_len
        if summary["first_epoch"] is None or epoch < summary["first_epoch"]:
            summary["first_epoch"] = epoch
        if summary["last_epoch"] is None or epoch > summary["last_epoch"]:
            summary["last_epoch"] = epoch


def read_feature_rows(path: Path) -> Iterable[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        indexes = {}
        for logical_name, aliases in FEATURE_FIELD_ALIASES.items():
            for alias in aliases:
                if alias in header:
                    indexes[logical_name] = header.index(alias)
                    break
        for row in reader:
            yield {
                logical_name: row[index] if index < len(row) else ""
                for logical_name, index in indexes.items()
            }


def read_tshark_rows(pcap: Path) -> Iterable[dict[str, str]]:
    tshark = shutil.which("tshark")
    if not tshark:
        raise RuntimeError("tshark not found in PATH")
    cmd = [
        tshark,
        "-r",
        str(pcap),
        "-T",
        "fields",
        "-E",
        "separator=,",
        "-E",
        "occurrence=f",
    ]
    for field in TSHARK_FIELDS:
        cmd.extend(["-e", field])
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        newline="",
    )
    assert proc.stdout is not None
    reader = csv.reader(proc.stdout)
    try:
        for row in reader:
            padded = row + [""] * (len(TSHARK_FIELDS) - len(row))
            yield {
                "time_epoch": padded[0],
                "frame_len": padded[1],
                "ip_proto": padded[2],
                "ipv6_nxt": padded[3],
                "tcp_srcport": padded[4],
                "tcp_dstport": padded[5],
                "udp_srcport": padded[6],
                "udp_dstport": padded[7],
                "sctp_srcport": padded[8],
                "sctp_dstport": padded[9],
                "icmp_type": padded[10],
                "icmpv6_type": padded[11],
                "ws_protocol": padded[12],
            }
    finally:
        stderr = proc.stderr.read() if proc.stderr is not None else ""
        returncode = proc.wait()
        if returncode != 0:
            raise RuntimeError(f"tshark exited with status {returncode}: {stderr.strip()}")


def process_pcap(campaign_dir: Path, pcap: Path, source: str) -> dict[str, Any]:
    feature_csv = feature_csv_for_pcap(campaign_dir, pcap)
    if source in {"auto", "features"} and feature_csv.exists():
        source_path = feature_csv
        source_kind = "features"
        rows = read_feature_rows(source_path)
    elif source == "features":
        raise FileNotFoundError(f"tshark feature CSV not found for {pcap}: {feature_csv}")
    else:
        source_path = pcap
        source_kind = "pcap"
        rows = read_tshark_rows(pcap)

    summary = empty_summary(campaign_dir, pcap, source_path, source_kind)
    for row in rows:
        update_summary(summary, row)
    return summary


def cached_summary_is_valid(summary: dict[str, Any], pcap: Path) -> bool:
    try:
        stat = pcap.stat()
    except OSError:
        return False
    return (
        summary.get("schema_version") == 1
        and summary.get("pcap_mtime_ns") == stat.st_mtime_ns
        and summary.get("pcap_size_bytes") == stat.st_size
    )


def load_or_process_summary(
    campaign_dir: Path,
    pcap: Path,
    summary_path: Path,
    source: str,
    force: bool,
) -> dict[str, Any]:
    if not force and summary_path.exists():
        cached = read_json(summary_path)
        if cached and cached_summary_is_valid(cached, pcap):
            return cached
    try:
        summary = process_pcap(campaign_dir, pcap, source)
    except Exception as exc:
        summary = empty_summary(campaign_dir, pcap, pcap, "error")
        summary["ok"] = False
        summary["error"] = str(exc)
    write_json(summary_path, summary)
    return summary


def add_counter(counter: Counter[str], payload: dict[str, int]) -> None:
    for key, value in payload.items():
        counter[key] += int(value)


def write_csv(path: Path, header: Sequence[str], rows: Iterable[Sequence[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def split_port_key(key: str) -> tuple[str, int]:
    protocol, port = key.split("/", 1)
    return protocol, int(port)


def sort_category_key(category: str) -> tuple[int, str]:
    prefix = category.split(")", 1)[0]
    try:
        return (int(prefix), category)
    except ValueError:
        return (999, category)


def short_category_label(category: str) -> str:
    if category in CATEGORY_SHORT_LABELS:
        return CATEGORY_SHORT_LABELS[category]
    return category.split(")", 1)[-1].strip() or category


def load_categories_from_campaign_config(campaign_dir: Path) -> dict[str, str]:
    config = read_json(campaign_dir / "_campaign" / "campaign_config.json") or {}
    categories: dict[str, str] = {}
    for plan in config.get("plans", []):
        if not isinstance(plan, dict):
            continue
        attack_id = str(plan.get("attack_id") or "")
        category = str(plan.get("category") or "")
        if attack_id and category:
            categories[attack_id] = category
    return categories


def load_categories_from_catalog_snapshot(campaign_dir: Path) -> dict[str, str]:
    snapshot = read_json(campaign_dir / "_campaign" / "catalog_snapshot.json") or {}
    catalog = snapshot.get("stdout_json")
    categories: dict[str, str] = {}
    if not isinstance(catalog, dict):
        return categories
    for category, attacks in catalog.items():
        if not isinstance(attacks, list):
            continue
        for attack in attacks:
            if not isinstance(attack, dict):
                continue
            attack_id = str(attack.get("id") or "")
            if attack_id:
                categories[attack_id] = str(category)
    return categories


def load_categories_from_attack_yaml(repo_root: Path) -> dict[str, str]:
    categories: dict[str, str] = {}
    for path in sorted((repo_root / "docker" / "attackers").glob("*/attack.yaml")):
        attack_id = ""
        category = ""
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            if line.startswith("id:"):
                attack_id = line.split(":", 1)[1].strip().strip("'\"")
            elif line.startswith("category:"):
                category = line.split(":", 1)[1].strip().strip("'\"")
            if attack_id and category:
                categories[attack_id] = category
                break
    return categories


def load_attack_categories(campaign_dir: Path) -> dict[str, str]:
    categories = load_categories_from_catalog_snapshot(campaign_dir)
    categories.update(load_categories_from_campaign_config(campaign_dir))
    fallback = load_categories_from_attack_yaml(REPO_ROOT)
    fallback.update(categories)
    return fallback


def parse_plot_selection(value: str) -> set[str]:
    selected: set[str] = set()
    for raw_item in value.split(","):
        item = raw_item.strip().lower()
        if not item:
            continue
        if item in PLOT_ALIASES:
            selected.update(PLOT_ALIASES[item])
        elif item in PLOT_CHOICES:
            selected.add(item)
        else:
            valid = ", ".join(("all", *PLOT_CHOICES))
            raise ValueError(f"unknown plot '{item}'. Valid values: {valid}")
    return selected or set(PLOT_CHOICES)


def parse_csv_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def read_csv_dicts(path: Path) -> Iterable[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        yield from reader


def csv_has_data_rows(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            return next(reader, None) is not None
    except OSError:
        return False


def table_paths(campaign_dir: Path, table_name: str) -> list[Path]:
    return sorted(campaign_dir.glob(f"*/reports/tables/{table_name}"))


def csv_data_row_count(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return max(sum(1 for _ in handle) - 1, 0)
    except OSError:
        return 0


def dataset_csv_identity(campaign_dir: Path, path: Path) -> dict[str, str]:
    rel = path.relative_to(campaign_dir)
    attack_id = rel.parts[0] if rel.parts else path.parents[1].name
    tokens = path.stem.split("-")
    level = next((token for token in tokens if token in LEVEL_ORDER), "")
    run_id = next((token for token in tokens if token.startswith("run")), "")
    return {
        "attack_id": attack_id,
        "level": level,
        "run_id": run_id,
    }


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def write_markdown_table(path: Path, header: Sequence[str], rows: Iterable[Sequence[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row_list = [tuple(str(value) for value in row) for row in rows]
    widths = [len(str(value)) for value in header]
    for row in row_list:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def render_row(values: Sequence[Any]) -> str:
        return "| " + " | ".join(str(value).ljust(widths[index]) for index, value in enumerate(values)) + " |"

    with path.open("w", encoding="utf-8") as handle:
        handle.write(render_row(header) + "\n")
        handle.write("| " + " | ".join("-" * width for width in widths) + " |\n")
        for row in row_list:
            handle.write(render_row(row) + "\n")


def write_dataset_and_variability_outputs(
    campaign_dir: Path,
    report_dir: Path,
    attack_categories: dict[str, str],
    variability_metric: str,
) -> dict[str, Path]:
    data_dir = report_dir / "data"
    tables_dir = report_dir / "tables"
    known_categories = set(attack_categories.values())

    dataset_by_category_level: dict[tuple[str, str], dict[str, float]] = {}
    table_rows = 0
    for path in table_paths(campaign_dir, "T8_artifact_summary.csv"):
        for row in read_csv_dicts(path):
            attack_id = row.get("attack_id", "")
            level = row.get("level", "")
            if not level:
                continue
            table_rows += 1
            category = attack_categories.get(attack_id, "Unmapped")
            known_categories.add(category)
            key = (category, level)
            bucket = dataset_by_category_level.setdefault(
                key,
                {
                    "run_count": 0.0,
                    "dataset_rows": 0.0,
                },
            )
            rows_value = to_float(row.get("dataset_rows", "")) or 0.0
            bucket["run_count"] += 1
            bucket["dataset_rows"] += rows_value

    if table_rows == 0:
        for path in find_dataset_csvs(campaign_dir):
            identity = dataset_csv_identity(campaign_dir, path)
            attack_id = identity["attack_id"]
            level = identity["level"]
            if not level:
                continue
            category = attack_categories.get(attack_id, "Unmapped")
            known_categories.add(category)
            key = (category, level)
            bucket = dataset_by_category_level.setdefault(
                key,
                {
                    "run_count": 0.0,
                    "dataset_rows": 0.0,
                },
            )
            bucket["run_count"] += 1
            bucket["dataset_rows"] += csv_data_row_count(path)

    dataset_rows = []
    for category in sorted(known_categories, key=sort_category_key):
        for level in LEVEL_ORDER:
            values = dataset_by_category_level.get((category, level), {"run_count": 0.0, "dataset_rows": 0.0})
            run_count = int(values["run_count"])
            dataset_count = int(values["dataset_rows"])
            dataset_rows.append(
                (
                    category,
                    short_category_label(category).replace("\n", " "),
                    level,
                    run_count,
                    dataset_count,
                    dataset_count / run_count if run_count else 0.0,
                )
            )

    dataset_rows_csv = data_dir / "category_level_dataset_rows.csv"
    write_csv(
        dataset_rows_csv,
        ("category", "category_label", "level", "run_count", "dataset_rows", "mean_dataset_rows_per_run"),
        dataset_rows,
    )

    variability_by_level: dict[str, dict[str, list[float]]] = {
        level: {"means": [], "std_devs": [], "cv_pcts": [], "n_runs": []}
        for level in LEVEL_ORDER
    }
    for path in table_paths(campaign_dir, "T6_reexecution_stability.csv"):
        for row in read_csv_dicts(path):
            if row.get("metric") != variability_metric:
                continue
            level = row.get("level", "")
            if level not in variability_by_level:
                continue
            std_dev = to_float(row.get("std_dev", "")) or 0.0
            cv_pct = to_float(row.get("cv_pct", "")) or 0.0
            mean_value = to_float(row.get("mean", "")) or 0.0
            n_runs = to_float(row.get("n_runs", "")) or 0.0
            variability_by_level[level]["means"].append(mean_value)
            variability_by_level[level]["std_devs"].append(std_dev)
            variability_by_level[level]["cv_pcts"].append(cv_pct)
            variability_by_level[level]["n_runs"].append(n_runs)

    variability_rows = []
    variability_markdown_rows = []
    for level in LEVEL_ORDER:
        values = variability_by_level[level]
        attack_count = len(values["means"])
        mean_value = mean(values["means"])
        std_dev_mean = mean(values["std_devs"])
        cv_pct_mean = mean(values["cv_pcts"])
        n_runs_mean = mean(values["n_runs"])
        variability_rows.append(
            (
                level,
                variability_metric,
                attack_count,
                n_runs_mean,
                mean_value,
                std_dev_mean,
                cv_pct_mean,
            )
        )
        variability_markdown_rows.append(
            (
                level,
                attack_count,
                f"{n_runs_mean:.1f}",
                f"{mean_value:.1f}",
                f"{std_dev_mean:.2f}",
                f"{cv_pct_mean:.2f}%",
            )
        )

    variability_csv = data_dir / f"{variability_metric}_run_variability_by_level.csv"
    write_csv(
        variability_csv,
        (
            "level",
            "metric",
            "attack_count",
            "mean_n_runs",
            "mean_value",
            "mean_std_dev_between_runs",
            "mean_cv_pct_between_runs",
        ),
        variability_rows,
    )

    variability_md = tables_dir / f"{variability_metric}_run_variability_by_level.md"
    mean_column = "Mean dataset rows" if variability_metric == "dataset_rows" else f"Mean {variability_metric}"
    write_markdown_table(
        variability_md,
        (
            "Level",
            "Attacks",
            "Runs",
            mean_column,
            "Std. dev.",
            "CV",
        ),
        variability_markdown_rows,
    )

    return {
        "category_level_dataset_rows_csv": dataset_rows_csv,
        "run_variability_csv": variability_csv,
        "run_variability_markdown": variability_md,
    }


def write_stability_and_phase_outputs(
    campaign_dir: Path,
    report_dir: Path,
    attack_categories: dict[str, str],
    stability_metrics: Sequence[str],
) -> dict[str, Path]:
    data_dir = report_dir / "data"
    selected_metrics = set(stability_metrics)

    stability_rows = []
    for path in table_paths(campaign_dir, "T6_reexecution_stability.csv"):
        for row in read_csv_dicts(path):
            metric = row.get("metric", "")
            if selected_metrics and metric not in selected_metrics:
                continue
            attack_id = row.get("attack_id", "")
            category = attack_categories.get(attack_id, "Unmapped")
            stability_rows.append(
                (
                    category,
                    short_category_label(category).replace("\n", " "),
                    row.get("service", ""),
                    attack_id,
                    row.get("level", ""),
                    metric,
                    int(to_float(row.get("n_runs", "")) or 0),
                    to_float(row.get("mean", "")) or 0.0,
                    to_float(row.get("std_dev", "")) or 0.0,
                    to_float(row.get("cv_pct", "")) or 0.0,
                    to_float(row.get("min", "")) or 0.0,
                    to_float(row.get("max", "")) or 0.0,
                    to_float(row.get("range", "")) or 0.0,
                )
            )

    stability_csv = data_dir / "reexecution_stability_cv_pct.csv"
    write_csv(
        stability_csv,
        (
            "category",
            "category_label",
            "service",
            "attack_id",
            "level",
            "metric",
            "n_runs",
            "mean",
            "std_dev",
            "cv_pct",
            "min",
            "max",
            "range",
        ),
        stability_rows,
    )

    phase_rows = []
    phase_summary: dict[tuple[str, str], dict[str, list[float]]] = {}
    for path in table_paths(campaign_dir, "T6_run_metrics.csv"):
        for row in read_csv_dicts(path):
            attack_id = row.get("attack_id", "")
            category = attack_categories.get(attack_id, "Unmapped")
            level = row.get("level", "")
            for phase in ("warmup", "attack", "cooldown"):
                success_rate = to_float(row.get(f"success_rate_{phase}_pct", "")) or 0.0
                lat_p95 = (
                    to_float(row.get(f"lat_p95_{phase}_censored_ms", ""))
                    or to_float(row.get(f"lat_p95_{phase}_ms", ""))
                    or 0.0
                )
                phase_rows.append(
                    (
                        category,
                        short_category_label(category).replace("\n", " "),
                        row.get("service", ""),
                        attack_id,
                        level,
                        row.get("run_id", ""),
                        phase,
                        success_rate,
                        lat_p95,
                    )
                )
                key = (level, phase)
                bucket = phase_summary.setdefault(key, {"success": [], "lat_p95": []})
                bucket["success"].append(success_rate)
                bucket["lat_p95"].append(lat_p95)

    phase_metrics_csv = data_dir / "phase_success_latency_metrics.csv"
    write_csv(
        phase_metrics_csv,
        (
            "category",
            "category_label",
            "service",
            "attack_id",
            "level",
            "run_id",
            "phase",
            "success_rate_pct",
            "lat_p95_ms",
        ),
        phase_rows,
    )

    phase_summary_rows = []
    for level in LEVEL_ORDER:
        for phase in ("warmup", "attack", "cooldown"):
            values = phase_summary.get((level, phase), {"success": [], "lat_p95": []})
            phase_summary_rows.append(
                (
                    level,
                    phase,
                    len(values["success"]),
                    mean(values["success"]),
                    mean(values["lat_p95"]),
                )
            )
    phase_summary_csv = data_dir / "phase_success_latency_summary_by_level.csv"
    write_csv(
        phase_summary_csv,
        ("level", "phase", "sample_count", "mean_success_rate_pct", "mean_lat_p95_ms"),
        phase_summary_rows,
    )

    return {
        "reexecution_stability_cv_pct_csv": stability_csv,
        "phase_success_latency_metrics_csv": phase_metrics_csv,
        "phase_success_latency_summary_csv": phase_summary_csv,
    }


def aggregate_summaries(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    protocol_counts: Counter[str] = Counter()
    protocol_bytes: Counter[str] = Counter()
    port_counts: Counter[str] = Counter()
    port_bytes: Counter[str] = Counter()
    level_second_packets: Counter[tuple[str, int]] = Counter()
    level_second_bytes: Counter[tuple[str, int]] = Counter()
    first_second: Optional[int] = None
    last_second: Optional[int] = None

    for summary in summaries:
        if not summary.get("ok", False):
            continue
        add_counter(protocol_counts, summary.get("protocol_counts", {}))
        add_counter(protocol_bytes, summary.get("protocol_bytes", {}))
        add_counter(port_counts, summary.get("port_counts", {}))
        add_counter(port_bytes, summary.get("port_bytes", {}))
        level = summary.get("level") or "UNKNOWN"
        for second_text, count in summary.get("second_packet_counts", {}).items():
            second = int(second_text)
            level_second_packets[(level, second)] += int(count)
            if first_second is None or second < first_second:
                first_second = second
            if last_second is None or second > last_second:
                last_second = second
        for second_text, byte_count in summary.get("second_byte_counts", {}).items():
            level_second_bytes[(level, int(second_text))] += int(byte_count)

    return {
        "protocol_counts": protocol_counts,
        "protocol_bytes": protocol_bytes,
        "port_counts": port_counts,
        "port_bytes": port_bytes,
        "level_second_packets": level_second_packets,
        "level_second_bytes": level_second_bytes,
        "first_second": first_second,
        "last_second": last_second,
    }


def write_outputs(
    report_dir: Path,
    summaries: list[dict[str, Any]],
    aggregate: dict[str, Any],
    attack_categories: dict[str, str],
) -> dict[str, Path]:
    data_dir = report_dir / "data"
    protocol_counts: Counter[str] = aggregate["protocol_counts"]
    protocol_bytes: Counter[str] = aggregate["protocol_bytes"]
    port_counts: Counter[str] = aggregate["port_counts"]
    port_bytes: Counter[str] = aggregate["port_bytes"]
    total_packets = sum(protocol_counts.values())
    total_bytes = sum(protocol_bytes.values())

    protocol_rows = []
    for protocol, packet_count in protocol_counts.most_common():
        byte_count = protocol_bytes[protocol]
        protocol_rows.append(
            (
                protocol,
                packet_count,
                byte_count,
                packet_count / total_packets if total_packets else 0.0,
                byte_count / total_bytes if total_bytes else 0.0,
            )
        )
    protocol_csv = data_dir / "protocol_packet_counts.csv"
    write_csv(
        protocol_csv,
        ("protocol", "packet_count", "byte_count", "packet_fraction", "byte_fraction"),
        protocol_rows,
    )

    port_rows = []
    by_port_counts: Counter[str] = Counter()
    by_port_bytes: Counter[str] = Counter()
    for key, packet_count in port_counts.most_common():
        protocol, port = split_port_key(key)
        byte_count = port_bytes[key]
        by_port_counts[str(port)] += packet_count
        by_port_bytes[str(port)] += byte_count
        port_rows.append(
            (
                protocol,
                port,
                f"{protocol}/{port}",
                packet_count,
                byte_count,
                packet_count / total_packets if total_packets else 0.0,
                byte_count / total_bytes if total_bytes else 0.0,
            )
        )
    port_csv = data_dir / "port_packet_counts.csv"
    write_csv(
        port_csv,
        ("transport", "port", "port_label", "packet_count", "byte_count", "packet_fraction", "byte_fraction"),
        port_rows,
    )

    by_port_rows = [
        (
            int(port),
            packet_count,
            by_port_bytes[port],
            packet_count / total_packets if total_packets else 0.0,
            by_port_bytes[port] / total_bytes if total_bytes else 0.0,
        )
        for port, packet_count in by_port_counts.most_common()
    ]
    port_aggregate_csv = data_dir / "port_packet_counts_by_port.csv"
    write_csv(
        port_aggregate_csv,
        ("port", "packet_count", "byte_count", "packet_fraction", "byte_fraction"),
        by_port_rows,
    )

    first_second = aggregate["first_second"]
    level_rows = []
    for (level, epoch_second), packet_count in sorted(aggregate["level_second_packets"].items()):
        byte_count = aggregate["level_second_bytes"].get((level, epoch_second), 0)
        campaign_second = epoch_second - first_second if first_second is not None else 0
        level_rows.append((level, campaign_second, epoch_second, packet_count, byte_count, packet_count, byte_count))
    level_csv = data_dir / "level_second_rates.csv"
    write_csv(
        level_csv,
        ("level", "campaign_second", "epoch_second", "packet_count", "byte_count", "pps", "Bps"),
        level_rows,
    )

    campaign_second_packets: Counter[int] = Counter()
    campaign_second_bytes: Counter[int] = Counter()
    campaign_second_epoch: dict[int, int] = {}
    for (level, epoch_second), packet_count in aggregate["level_second_packets"].items():
        byte_count = aggregate["level_second_bytes"].get((level, epoch_second), 0)
        campaign_second = epoch_second - first_second if first_second is not None else 0
        campaign_second_packets[campaign_second] += int(packet_count)
        campaign_second_bytes[campaign_second] += int(byte_count)
        campaign_second_epoch[campaign_second] = epoch_second

    campaign_rate_rows = [
        (
            campaign_second,
            campaign_second_epoch[campaign_second],
            campaign_second_packets[campaign_second],
            campaign_second_bytes[campaign_second],
            campaign_second_packets[campaign_second],
            campaign_second_bytes[campaign_second],
        )
        for campaign_second in sorted(campaign_second_packets)
    ]
    campaign_rate_csv = data_dir / "campaign_second_rates.csv"
    write_csv(
        campaign_rate_csv,
        ("campaign_second", "epoch_second", "packet_count", "byte_count", "pps", "Bps"),
        campaign_rate_rows,
    )

    file_rows = []
    for summary in summaries:
        file_rows.append(
            (
                summary.get("ok"),
                summary.get("level"),
                summary.get("attack_id"),
                summary.get("run_id"),
                summary.get("service"),
                summary.get("packet_count"),
                summary.get("byte_count"),
                summary.get("first_epoch"),
                summary.get("last_epoch"),
                summary.get("source_kind"),
                summary.get("campaign_relative_path"),
                summary.get("error"),
            )
        )
    file_csv = data_dir / "pcap_file_summaries.csv"
    write_csv(
        file_csv,
        (
            "ok",
            "level",
            "attack_id",
            "run_id",
            "service",
            "packet_count",
            "byte_count",
            "first_epoch",
            "last_epoch",
            "source_kind",
            "campaign_relative_path",
            "error",
        ),
        file_rows,
    )

    category_level: dict[tuple[str, str], dict[str, float]] = {}
    for summary in summaries:
        if not summary.get("ok", False):
            continue
        attack_id = str(summary.get("attack_id") or "")
        level = str(summary.get("level") or "UNKNOWN")
        category = attack_categories.get(attack_id, "Unmapped")
        key = (category, level)
        bucket = category_level.setdefault(
            key,
            {
                "file_count": 0.0,
                "packet_count": 0.0,
                "byte_count": 0.0,
                "pcap_size_mb": 0.0,
            },
        )
        bucket["file_count"] += 1
        bucket["packet_count"] += float(summary.get("packet_count") or 0)
        bucket["byte_count"] += float(summary.get("byte_count") or 0)
        bucket["pcap_size_mb"] += float(summary.get("pcap_size_bytes") or 0) / (1024 * 1024)

    known_categories = set(attack_categories.values())
    known_categories.update(key[0] for key in category_level)
    category_rows = []
    for category in sorted(known_categories, key=sort_category_key):
        for level in LEVEL_ORDER:
            values = category_level.get(
                (category, level),
                {
                    "file_count": 0.0,
                    "packet_count": 0.0,
                    "byte_count": 0.0,
                    "pcap_size_mb": 0.0,
                },
            )
            category_rows.append(
                (
                    category,
                    short_category_label(category).replace("\n", " "),
                    level,
                    int(values["file_count"]),
                    int(values["packet_count"]),
                    int(values["byte_count"]),
                    values["pcap_size_mb"],
                )
            )
    category_level_csv = data_dir / "category_level_traffic.csv"
    write_csv(
        category_level_csv,
        (
            "category",
            "category_label",
            "level",
            "file_count",
            "packet_count",
            "byte_count",
            "pcap_size_mb",
        ),
        category_rows,
    )

    return {
        "protocol_csv": protocol_csv,
        "port_csv": port_csv,
        "port_aggregate_csv": port_aggregate_csv,
        "level_csv": level_csv,
        "campaign_rate_csv": campaign_rate_csv,
        "file_csv": file_csv,
        "category_level_csv": category_level_csv,
    }


def import_plotting():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    return plt, pd


def plot_outputs(
    report_dir: Path,
    csv_paths: dict[str, Path],
    top_ports: int,
    top_protocols: int,
    selected_plots: set[str],
    heatmap_metric: str,
    stability_metrics: Sequence[str],
) -> dict[str, Path]:
    plt, pd = import_plotting()
    figures_dir = report_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}
    colors = plt.get_cmap("tab20").colors

    if "protocol" in selected_plots:
        protocol_df = pd.read_csv(csv_paths["protocol_csv"]).head(top_protocols)
        fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
        ax.bar(protocol_df["protocol"], protocol_df["packet_count"], color=colors[: len(protocol_df)])
        ax.set_title("Packet Count by Protocol")
        ax.set_xlabel("Protocol")
        ax.set_ylabel("Packet count")
        ax.ticklabel_format(axis="y", style="plain")
        ax.grid(axis="y", alpha=0.25)
        ax.tick_params(axis="x", rotation=35)
        path = figures_dir / "01_protocol_packet_counts.png"
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs["protocol_plot"] = path

    if "ports" in selected_plots:
        port_df = pd.read_csv(csv_paths["port_aggregate_csv"]).head(top_ports)
        fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
        ax.bar(port_df["port"].astype(str), port_df["packet_count"], color=colors[: len(port_df)])
        ax.set_title("Packet Count by Port")
        ax.set_xlabel("Port")
        ax.set_ylabel("Packet count")
        ax.ticklabel_format(axis="y", style="plain")
        ax.grid(axis="y", alpha=0.25)
        ax.tick_params(axis="x", rotation=45)
        path = figures_dir / "02_port_packet_counts.png"
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs["port_plot"] = path

    if "pps" in selected_plots:
        rates_df = pd.read_csv(csv_paths["level_csv"])
        fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
        for level in LEVEL_ORDER:
            sub = rates_df[rates_df["level"] == level].sort_values("campaign_second")
            if sub.empty:
                continue
            ax.plot(
                sub["campaign_second"],
                sub["pps"],
                label=level,
                color=LEVEL_COLORS.get(level),
                linewidth=1.2,
                alpha=0.85,
            )
        ax.set_title("PPS by Level over Campaign Seconds")
        ax.set_xlabel("Campaign second")
        ax.set_ylabel("Packets per second (pps)")
        ax.ticklabel_format(axis="y", style="plain")
        ax.grid(alpha=0.25)
        handles, labels = ax.get_legend_handles_labels()
        if handles and labels:
            ax.legend(handles, labels, title="Level")
        path = figures_dir / "03_pps_by_level_over_campaign_seconds.png"
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs["pps_plot"] = path

    if "bps" in selected_plots:
        campaign_rates_df = pd.read_csv(csv_paths["campaign_rate_csv"]).sort_values("campaign_second")
        fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
        ax.plot(
            campaign_rates_df["campaign_second"],
            campaign_rates_df["Bps"],
            color="#4c9ed9",
            linewidth=0.9,
            alpha=0.9,
        )
        ax.set_xlabel("Time in seconds")
        ax.set_ylabel("Bytes per second")
        ax.ticklabel_format(axis="y", style="plain")
        ax.grid(False)
        fig.text(
            0.5,
            -0.03,
            "(d) Experiment Bytes rate (BPS)",
            ha="center",
            va="top",
            fontsize=14,
            fontweight="bold",
            family="serif",
        )
        path = figures_dir / "04_Bps_over_campaign_seconds.png"
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs["Bps_plot"] = path

    if "heatmap" in selected_plots:
        category_df = pd.read_csv(csv_paths["category_level_csv"])
        category_order = sorted(category_df["category"].dropna().unique(), key=sort_category_key)
        category_labels = [short_category_label(category) for category in category_order]
        pivot = (
            category_df.pivot_table(
                index="category",
                columns="level",
                values=heatmap_metric,
                aggfunc="sum",
                fill_value=0,
            )
            .reindex(index=category_order, columns=list(LEVEL_ORDER), fill_value=0)
        )

        values = pivot.astype(float)
        if heatmap_metric == "byte_count":
            values = values / (1024 ** 3)
            colorbar_label = "Traffic volume (GiB)"
        elif heatmap_metric == "pcap_size_mb":
            values = values / 1024
            colorbar_label = "PCAP size (GiB)"
        else:
            values = values / 1_000_000
            colorbar_label = "Packets (millions)"
        max_value = float(values.to_numpy().max()) if not values.empty else 0.0
        annotation_format = "{:.3f}" if 0 < max_value < 1 else "{:.1f}"

        fig, ax = plt.subplots(figsize=(10, 5.8), constrained_layout=True)
        image = ax.imshow(values.to_numpy(), cmap="YlGnBu", aspect="auto")
        ax.set_title("Traffic Volume by Attack Category and Level")
        ax.set_xlabel("Experiment level")
        ax.set_ylabel("Attack category")
        ax.set_xticks(range(len(LEVEL_ORDER)), labels=LEVEL_ORDER)
        ax.set_yticks(range(len(category_labels)), labels=category_labels)
        ax.tick_params(axis="y", labelsize=9)
        colorbar = fig.colorbar(image, ax=ax, shrink=0.88)
        colorbar.set_label(colorbar_label)

        threshold = max_value * 0.55
        for row_index, category in enumerate(values.index):
            for col_index, level in enumerate(values.columns):
                value = float(values.loc[category, level])
                text_color = "white" if value > threshold else "black"
                ax.text(
                    col_index,
                    row_index,
                    annotation_format.format(value),
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=8,
                )
        path = figures_dir / "04_category_level_heatmap.png"
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs["category_level_heatmap_plot"] = path

    if "dataset_rows" in selected_plots:
        dataset_df = pd.read_csv(csv_paths["category_level_dataset_rows_csv"])
        category_order = sorted(dataset_df["category"].dropna().unique(), key=sort_category_key)
        category_labels = [short_category_label(category) for category in category_order]
        pivot = (
            dataset_df.pivot_table(
                index="category",
                columns="level",
                values="dataset_rows",
                aggfunc="sum",
                fill_value=0,
            )
            .reindex(index=category_order, columns=list(LEVEL_ORDER), fill_value=0)
        )
        values = pivot.astype(float) / 1_000_000
        max_value = float(values.to_numpy().max()) if not values.empty else 0.0
        annotation_format = "{:.3f}" if 0 < max_value < 1 else "{:.1f}"

        fig, ax = plt.subplots(figsize=(10, 5.8), constrained_layout=True)
        image = ax.imshow(values.to_numpy(), cmap="PuBuGn", aspect="auto")
        ax.set_title("Dataset Rows by Attack Category and Level")
        ax.set_xlabel("Experiment level")
        ax.set_ylabel("Attack category")
        ax.set_xticks(range(len(LEVEL_ORDER)), labels=LEVEL_ORDER)
        ax.set_yticks(range(len(category_labels)), labels=category_labels)
        ax.tick_params(axis="y", labelsize=9)
        colorbar = fig.colorbar(image, ax=ax, shrink=0.88)
        colorbar.set_label("Dataset rows (millions)")

        threshold = max_value * 0.55
        for row_index, category in enumerate(values.index):
            for col_index, level in enumerate(values.columns):
                value = float(values.loc[category, level])
                text_color = "white" if value > threshold else "black"
                ax.text(
                    col_index,
                    row_index,
                    annotation_format.format(value),
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=8,
                )
        path = figures_dir / "05_category_level_dataset_rows.png"
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs["category_level_dataset_rows_plot"] = path

    if "stability" in selected_plots:
        stability_df = pd.read_csv(csv_paths["reexecution_stability_cv_pct_csv"])
        metric_order = [metric for metric in stability_metrics if metric in set(stability_df["metric"])]
        if not metric_order:
            metric_order = sorted(stability_df["metric"].dropna().unique())
        attack_order_df = (
            stability_df[["category", "attack_id"]]
            .drop_duplicates()
            .sort_values(["category", "attack_id"], key=lambda series: series.map(sort_category_key) if series.name == "category" else series)
        )
        attack_order = attack_order_df["attack_id"].tolist()

        fig_height = max(8.0, len(attack_order) * 0.22)
        fig, axes = plt.subplots(
            1,
            len(metric_order),
            figsize=(max(5.0 * len(metric_order), 8.0), fig_height),
            constrained_layout=True,
            squeeze=False,
        )
        all_values = stability_df["cv_pct"].astype(float)
        vmax = float(all_values.quantile(0.95)) if not all_values.empty else 1.0
        vmax = max(vmax, 1.0)

        for index, metric in enumerate(metric_order):
            ax = axes[0][index]
            metric_df = stability_df[stability_df["metric"] == metric]
            pivot = (
                metric_df.pivot_table(
                    index="attack_id",
                    columns="level",
                    values="cv_pct",
                    aggfunc="mean",
                    fill_value=0,
                )
                .reindex(index=attack_order, columns=list(LEVEL_ORDER), fill_value=0)
            )
            image = ax.imshow(pivot.to_numpy(dtype=float), cmap="YlOrRd", aspect="auto", vmin=0, vmax=vmax)
            ax.set_title(metric.replace("_", " "))
            ax.set_xlabel("Level")
            ax.set_xticks(range(len(LEVEL_ORDER)), labels=LEVEL_ORDER)
            if index == 0:
                ax.set_ylabel("Attack")
                ax.set_yticks(range(len(attack_order)), labels=attack_order)
                ax.tick_params(axis="y", labelsize=5)
            else:
                ax.set_yticks([])
        colorbar = fig.colorbar(image, ax=axes.ravel().tolist(), shrink=0.75)
        colorbar.set_label("Coefficient of variation (%)")
        path = figures_dir / "06_reexecution_cv_pct_heatmap.png"
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs["reexecution_cv_pct_heatmap_plot"] = path

    if "phase_metrics" in selected_plots:
        phase_df = pd.read_csv(csv_paths["phase_success_latency_metrics_csv"])
        phase_order = ("warmup", "attack", "cooldown")
        phase_labels = ("Warmup", "Attack", "Cooldown")
        success_data = [
            phase_df[phase_df["phase"] == phase]["success_rate_pct"].astype(float).dropna().to_numpy()
            for phase in phase_order
        ]
        latency_data = [
            phase_df[phase_df["phase"] == phase]["lat_p95_ms"].astype(float).dropna().to_numpy()
            for phase in phase_order
        ]

        fig, axes = plt.subplots(1, 2, figsize=(11, 5), constrained_layout=True)
        boxprops = {"linewidth": 1.1}
        medianprops = {"color": "#222222", "linewidth": 1.3}
        success_box = axes[0].boxplot(
            success_data,
            tick_labels=phase_labels,
            patch_artist=True,
            boxprops=boxprops,
            medianprops=medianprops,
        )
        for patch, color in zip(success_box["boxes"], ("#b8e1ff", "#fdd49e", "#c7e9c0")):
            patch.set_facecolor(color)
        axes[0].set_title("Service Availability by Phase")
        axes[0].set_ylabel("Success rate (%)")
        axes[0].set_ylim(-2, 102)
        axes[0].grid(axis="y", alpha=0.25)

        latency_box = axes[1].boxplot(
            latency_data,
            tick_labels=phase_labels,
            patch_artist=True,
            boxprops=boxprops,
            medianprops=medianprops,
        )
        for patch, color in zip(latency_box["boxes"], ("#b8e1ff", "#fdd49e", "#c7e9c0")):
            patch.set_facecolor(color)
        axes[1].set_title("P95 Latency by Phase")
        axes[1].set_ylabel("P95 latency (ms)")
        axes[1].grid(axis="y", alpha=0.25)

        path = figures_dir / "07_phase_success_latency_boxplots.png"
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs["phase_success_latency_boxplots_plot"] = path

    return outputs


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        selected_plots = parse_plot_selection(args.plots)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    stability_metrics = parse_csv_list(args.stability_metrics)

    campaign_dir = resolve_campaign_dir(args.campaign_dir)
    if not campaign_dir.is_dir():
        print(f"[ERROR] Campaign directory not found: {campaign_dir}", file=sys.stderr)
        return 2

    report_name = args.campaign_name or campaign_dir.name
    report_dir = (args.reports_root.resolve() / report_name)
    summary_dir = report_dir / "file_summaries"
    report_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    dataset_csvs = find_dataset_csvs(campaign_dir)
    pcaps = find_pcaps(campaign_dir)
    if args.max_files is not None:
        pcaps = pcaps[: args.max_files]
    if not pcaps and not dataset_csvs:
        print(f"[ERROR] No PCAP files or dataset CSVs found under {campaign_dir}", file=sys.stderr)
        return 2
    if not pcaps:
        print(f"[INFO] No PCAP files found under {campaign_dir}; generating dataset-only outputs.", file=sys.stderr)

    summaries: list[dict[str, Any]] = []
    for index, pcap in enumerate(pcaps, start=1):
        summary_path = summary_path_for_pcap(summary_dir, campaign_dir, pcap)
        summary = load_or_process_summary(campaign_dir, pcap, summary_path, args.source, args.force)
        summaries.append(summary)
        if args.progress_interval > 0 and (index % args.progress_interval == 0 or index == len(pcaps)):
            status = "ok" if summary.get("ok") else "error"
            print(f"[progress] {index}/{len(pcaps)} {status} {pcap.relative_to(campaign_dir)}", file=sys.stderr)

    aggregate = aggregate_summaries(summaries)
    attack_categories = load_attack_categories(campaign_dir)
    csv_paths = write_outputs(report_dir, summaries, aggregate, attack_categories)
    csv_paths.update(
        write_dataset_and_variability_outputs(
            campaign_dir,
            report_dir,
            attack_categories,
            args.variability_metric,
        )
    )
    csv_paths.update(
        write_stability_and_phase_outputs(
            campaign_dir,
            report_dir,
            attack_categories,
            stability_metrics,
        )
    )
    if "stability" in selected_plots and not csv_has_data_rows(csv_paths["reexecution_stability_cv_pct_csv"]):
        selected_plots.discard("stability")
    if "phase_metrics" in selected_plots and not csv_has_data_rows(csv_paths["phase_success_latency_metrics_csv"]):
        selected_plots.discard("phase_metrics")

    plot_paths: dict[str, Path] = {}
    plot_error = ""
    if not args.no_plots:
        try:
            plot_paths = plot_outputs(
                report_dir,
                csv_paths,
                args.top_ports,
                args.top_protocols,
                selected_plots,
                args.heatmap_metric,
                stability_metrics,
            )
        except ModuleNotFoundError as exc:
            plot_error = f"plot dependencies missing: {exc}"
            print(f"[WARN] {plot_error}; CSV outputs were still written.", file=sys.stderr)

    ok_count = sum(1 for summary in summaries if summary.get("ok"))
    packet_total = sum(aggregate["protocol_counts"].values())
    byte_total = sum(aggregate["protocol_bytes"].values())
    manifest = {
        "generated_at_utc": utc_now(),
        "campaign_dir": str(campaign_dir),
        "report_dir": str(report_dir),
        "source": args.source,
        "processed_pcap_count": len(summaries),
        "ok_pcap_count": ok_count,
        "error_pcap_count": len(summaries) - ok_count,
        "dataset_csv_count": len(dataset_csvs),
        "packet_total": packet_total,
        "byte_total": byte_total,
        "selected_plots": sorted(selected_plots),
        "heatmap_metric": args.heatmap_metric,
        "variability_metric": args.variability_metric,
        "stability_metrics": stability_metrics,
        "first_epoch_second": aggregate["first_second"],
        "last_epoch_second": aggregate["last_second"],
        "csv_outputs": {key: str(value) for key, value in csv_paths.items()},
        "plot_outputs": {key: str(value) for key, value in plot_paths.items()},
        "plot_error": plot_error,
    }
    write_json(report_dir / "manifest.json", manifest)

    print("Traffic statistics")
    print(f"- Report dir: {report_dir}")
    print(f"- PCAPs processed: {ok_count}/{len(summaries)}")
    print(f"- Dataset CSVs found: {len(dataset_csvs)}")
    print(f"- Packets counted: {packet_total}")
    print(f"- Bytes counted: {byte_total}")
    print(f"- CSV outputs: {report_dir / 'data'}")
    if plot_paths:
        print(f"- Plot outputs: {report_dir / 'figures'}")
    return 0 if ok_count == len(summaries) else 1


if __name__ == "__main__":
    raise SystemExit(main())
