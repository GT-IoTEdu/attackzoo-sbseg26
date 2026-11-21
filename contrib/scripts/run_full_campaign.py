#!/usr/bin/env python3
"""Run a full AttackZoo campaign with all catalog attacks and guardrails.

The script orchestrates one long experiment per attack, keeps raw PCAPs and
per-run metadata under experiments/<campaign>/, enables feature extraction,
dataset generation, reports, figures, host telemetry, and target container
telemetry whenever the current AttackZoo CLI supports them.

It also monitors campaign directory size and host load while each subprocess is
running. If a guardrail is exceeded, the current experiment is terminated, the
active attack container is stopped, and a kill-switch record is written.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import ipaddress
import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import yaml
except Exception as exc:  # pragma: no cover - dependency failure path.
    print(f"[ERROR] PyYAML is required to read attack/server metadata: {exc}", file=sys.stderr)
    raise SystemExit(2)


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.attackzoo.attacks import _all_specs, _find_port_param, _find_target_param  # noqa: E402
from modules.registry import CATEGORIES  # noqa: E402


DEFAULT_CAMPAIGN_PREFIX = "full_campaign"
DEFAULT_DISK_LIMIT_GB = 2048.0
DEFAULT_LOAD_LIMIT = 30.0
DEFAULT_CHECK_INTERVAL_S = 30.0
DEFAULT_RUNS = 10
DEFAULT_LEVELS = "L0,L1,L2,L3"
DEFAULT_WARMUP_S = 60.0
DEFAULT_ATTACK_S = 120.0
DEFAULT_COOLDOWN_S = 60.0
DEFAULT_PROBE_TIMEOUT_S = 2.0
DEFAULT_RESOURCE_INTERVAL_S = 1.0
DEFAULT_IFACE = "any"

AUTO_BPF_BY_ATTACK: Dict[str, str] = {
    # --iface any (the default) has no Ethernet header, so "ether dst" cannot compile; keep only non-IP frames.
    "net_cdp_table_flood": "not ip and not ip6 and not arp",
    "net_dhcp_starvation": "udp port 67 or udp port 68",
    "net_ipv6_mld_flood": "icmp6",
    "net_ipv6_ns_flood": "icmp6 and ip6[40] == 135",
    "net_ipv6_ra_flood": "icmp6 and ip6[40] == 134",
    # On any (cooked v2) libpcap compiles "stp" as protocol == 0x42, which never matches a BPDU.
    "net_stp_conf_flood": "(not ip and not ip6 and not arp) or port 8080",
    "net_stp_tcn_flood": "(not ip and not ip6 and not arp) or port 8080",
}

SERVICE_OVERRIDES: Dict[str, str] = {
    "bf_ssh": "ssh-server",
    "bf_telnet": "telnet-server",
    "exf_icmp_tunnel": "ssh-server",
    "iot_coap_get_flood": "coap-server",
    "iot_coap_resource_exhaustion": "coap-server",
    "iot_coap_response_fuzz": "coap-server",
    "iot_coap_token_collision": "coap-server",
    "iot_mqtt_bruteforce": "mqtt-broker",
    "iot_mqtt_lwt_abuse": "mqtt-broker",
    "iot_mqtt_publisher": "mqtt-broker",
    "iot_mqtt_qos_amplification": "mqtt-broker",
    "iot_xrce_dds_discovery_poison": "xrce-dds-agent",
    "iot_xrce_dds_entity_flood": "xrce-dds-agent",
    "iot_xrce_dds_fragment_abuse": "xrce-dds-agent",
    "iot_xrce_dds_malformed_inject": "xrce-dds-agent",
    "iot_xrce_dds_session_hijack": "xrce-dds-agent",
    "iot_xrce_dds_time_desync": "xrce-dds-agent",
    "iot_xrce_dds_udp_dos": "xrce-dds-agent",
    "iot_zenoh_pico_fragments_reassembly": "zenoh-router",
    "iot_zenoh_pico_keepalive_flood": "zenoh-router",
    "iot_zenoh_pico_memory_exhaustion": "zenoh-router",
    "iot_zenoh_pico_proto_fuzzer": "zenoh-router",
    "iot_zenoh_pico_sequence_exhaustion": "zenoh-router",
    "iot_zenoh_pico_timestamp_mess": "zenoh-router",
    "php_lfi_enumeration": "http-server",
    "recon_smb_enum": "smb-server",
    "web_dir_enumeration": "http-server",
    "web_https_heartbleed": "ssl-heartbleed",
    "web_idor_path_traversal": "http-server",
    "web_idor_url_parameter": "http-server",
    "web_post_bruteforce": "http-server",
    "web_simple_scanner": "http-server",
    "web_sql_injection": "http-server",
    "web_wide_scanner": "http-server",
    "web_xss_scanner": "http-server",
}

GENERIC_SERVICE_BY_CATEGORY_PREFIX: Tuple[Tuple[str, str], ...] = (
    ("1)", "http-server"),
    ("2)", "http-server"),
    ("3)", "http-server"),
    ("5)", "http-server"),
    ("6)", "http-server"),
)

SERVICE_PROBE: Dict[str, str] = {
    "coap-server": "coap",
    "http-server": "http",
    "mqtt-broker": "mqtt",
    "smb-server": "smb",
    "ssh-server": "ssh",
    "ssl-heartbleed": "https",
    "telnet-server": "telnet",
    "xrce-dds-agent": "xrce",
    "zenoh-router": "zenoh",
}

SERVICE_DEFAULT_PORT_BY_PROBE: Dict[str, int] = {
    "coap": 5683,
    "http": 80,
    "https": 443,
    "mqtt": 1883,
    "smb": 445,
    "ssh": 22,
    "telnet": 23,
    "xrce": 8888,
    "zenoh": 7447,
}

SMB_PORTS = {137, 138, 139, 445}


@dataclasses.dataclass(frozen=True)
class ServerSpec:
    service_id: str
    container_name: str
    protocols: Tuple[str, ...]
    internal_ports: Tuple[Tuple[int, str], ...]
    published_ports: Tuple[Tuple[int, int, str], ...]


@dataclasses.dataclass(frozen=True)
class AttackMeta:
    attack_id: str
    name: str
    category: str
    target_services: Tuple[str, ...]
    yaml_path: str


@dataclasses.dataclass(frozen=True)
class AttackPlan:
    attack_id: str
    name: str
    category: str
    out_arg: str
    experiment_dir: str
    service_id: str
    service_label: str
    target_value: str
    target_port: Optional[int]
    target_param: Optional[str]
    port_param: Optional[str]
    server_container: str
    probes: Tuple[str, ...]
    probe_endpoints: Dict[str, str]
    bpf: str
    features_dir: str
    datasets_dir: str
    attack_start_hook: str
    attack_stop_hook: str


@dataclasses.dataclass
class GuardSnapshot:
    timestamp_utc: str
    directory_bytes: int
    directory_gb: float
    disk_limit_gb: float
    load1: float
    load5: float
    load15: float
    load_limit: float
    free_gb: float
    min_free_gb: float
    ok: bool
    reason: str = ""


class KillSwitchTriggered(RuntimeError):
    def __init__(self, snapshot: GuardSnapshot):
        super().__init__(snapshot.reason)
        self.snapshot = snapshot


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def campaign_name() -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{DEFAULT_CAMPAIGN_PREFIX}_{stamp}"


def gb_to_bytes(value: float) -> int:
    return int(value * 1024**3)


def bytes_to_gb(value: int) -> float:
    return value / float(1024**3)


def run_quiet(cmd: Sequence[str], timeout_s: Optional[float] = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(cmd),
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=timeout_s,
    )


def load_yaml(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def parse_port_token(token: str) -> Tuple[int, str]:
    raw = str(token).strip()
    port_s, _, proto = raw.partition("/")
    return int(port_s), (proto or "tcp").lower()


def parse_published_port(token: str) -> Tuple[int, int, str]:
    raw = str(token).strip()
    host_part, _, container_part = raw.partition(":")
    port, proto = parse_port_token(container_part or host_part)
    return int(host_part), port, proto


def load_server_specs() -> Dict[str, ServerSpec]:
    servers: Dict[str, ServerSpec] = {}
    for path in sorted((REPO_ROOT / "docker" / "servers").glob("*/server.yaml")):
        data = load_yaml(path)
        service_id = str(data.get("id") or path.parent.name)
        internal_ports = tuple(parse_port_token(x) for x in data.get("internal_ports", []) or [])
        published_ports = tuple(parse_published_port(x) for x in data.get("published_ports", []) or [])
        servers[service_id] = ServerSpec(
            service_id=service_id,
            container_name=str(data.get("container_name") or ""),
            protocols=tuple(str(x) for x in data.get("protocols", []) or []),
            internal_ports=internal_ports,
            published_ports=published_ports,
        )
    return servers


def load_attack_metadata() -> Dict[str, AttackMeta]:
    metas: Dict[str, AttackMeta] = {}
    for path in sorted((REPO_ROOT / "docker" / "attackers").glob("*/attack.yaml")):
        data = load_yaml(path)
        attack_id = str(data["id"])
        metas[attack_id] = AttackMeta(
            attack_id=attack_id,
            name=str(data.get("name") or attack_id),
            category=str(data.get("category") or ""),
            target_services=tuple(str(x) for x in data.get("target_services", []) or []),
            yaml_path=str(path.relative_to(REPO_ROOT)),
        )
    return metas


def attack_category_by_id() -> Dict[str, str]:
    out: Dict[str, str] = {}
    for category, specs in CATEGORIES.items():
        for spec in specs:
            out[spec.id] = category
    return out


def split_csv(value: str) -> List[str]:
    return [x.strip() for x in (value or "").split(",") if x.strip()]


def docker_available() -> bool:
    return run_quiet(["docker", "version"], timeout_s=10).returncode == 0


def docker_container_ip(container_name: str) -> str:
    if not container_name:
        return ""
    cmd = [
        "docker",
        "inspect",
        "-f",
        "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
        container_name,
    ]
    result = run_quiet(cmd, timeout_s=10)
    if result.returncode != 0:
        return ""
    return (result.stdout or "").strip()


def docker0_network() -> Tuple[str, str]:
    result = run_quiet(["ip", "-j", "addr", "show", "docker0"], timeout_s=10)
    if result.returncode == 0 and result.stdout:
        try:
            data = json.loads(result.stdout)
            for item in data:
                for addr in item.get("addr_info", []):
                    if addr.get("family") != "inet":
                        continue
                    local = addr.get("local")
                    prefixlen = addr.get("prefixlen")
                    if local and prefixlen is not None:
                        network = ipaddress.ip_interface(f"{local}/{prefixlen}").network
                        return str(network), str(ipaddress.ip_address(local))
        except Exception:
            pass
    return "172.17.0.0/16", "172.17.0.1"


def port_for_service(service: Optional[ServerSpec], probe: str, published: bool) -> int:
    default = SERVICE_DEFAULT_PORT_BY_PROBE.get(probe, 0)
    if not service:
        return default
    if published:
        for host_port, container_port, _proto in service.published_ports:
            if container_port == default or host_port == default:
                return host_port
        if service.published_ports:
            return service.published_ports[0][0]
    else:
        for port, _proto in service.internal_ports:
            if port == default:
                return port
        if service.internal_ports:
            return service.internal_ports[0][0]
    return default


def resolve_service_id(meta: AttackMeta, servers: Dict[str, ServerSpec]) -> str:
    if meta.attack_id in SERVICE_OVERRIDES:
        return SERVICE_OVERRIDES[meta.attack_id]
    for raw in meta.target_services:
        if raw in servers:
            return raw
    lower_targets = " ".join(meta.target_services).lower()
    for service_id in servers:
        if service_id in lower_targets:
            return service_id
    for prefix, service_id in GENERIC_SERVICE_BY_CATEGORY_PREFIX:
        if meta.category.startswith(prefix):
            return service_id
    return "http-server"


def target_for_plan(
    *,
    args: argparse.Namespace,
    spec: Any,
    target_param: Any,
    port_param: Any,
    service: Optional[ServerSpec],
    service_ip: str,
    probe: str,
    target_net: str,
) -> Tuple[str, Optional[int]]:
    if target_param is None:
        return "", None

    if target_param.kind == "cidr":
        return target_net, None

    target_port: Optional[int] = None
    if port_param is not None:
        target_port = int(port_param.default) if port_param.default is not None else port_for_service(service, probe, True)
        return args.host_target, target_port

    if service_ip:
        return service_ip, None
    return args.fallback_target_ip, None


def extra_run_args(
    *,
    args: argparse.Namespace,
    spec: Any,
    target_param: Any,
    port_param: Any,
    target_net: str,
    spoof_gw: str,
) -> List[str]:
    out: List[str] = []
    target_key = target_param.key if target_param is not None else ""
    port_key = port_param.key if port_param is not None else ""
    for param in spec.params:
        if param.key in {target_key, port_key}:
            continue
        if param.key == "duration_s":
            continue
        if param.key == "rate_pps":
            continue
        if not param.required and param.default is not None:
            continue

        value: Any
        if param.key == "spoof_gw":
            value = spoof_gw
        elif param.kind == "cidr":
            value = target_net
        elif param.kind == "ip":
            value = args.fallback_target_ip
        elif param.kind == "port":
            value = args.fallback_target_port
        elif param.kind == "int":
            value = 1
        elif param.kind == "float":
            value = 1.0
        else:
            value = args.fallback_text
        out.extend([f"--{param.key}", str(value)])
    return out


def shell_join(parts: Iterable[str]) -> str:
    return " ".join(shlex.quote(str(x)) for x in parts)


def build_hook(
    *,
    args: argparse.Namespace,
    spec: Any,
    target_param: Any,
    port_param: Any,
    target_value: str,
    target_port: Optional[int],
    extras: List[str],
) -> str:
    cmd: List[str] = [
        args.python,
        "attackzoo.py",
        "run",
        spec.id,
        "--duration",
        "{duration_s}",
    ]
    if args.attack_rate_pps is not None:
        cmd.extend(["--rate", str(args.attack_rate_pps)])
    if target_param is not None and target_value:
        cmd.extend(["--target", target_value])
    if port_param is not None and target_port is not None:
        cmd.extend(["--port", str(target_port)])
    cmd.extend(extras)
    return shell_join(cmd)


def build_stop_hook(args: argparse.Namespace, attack_id: str) -> str:
    return shell_join([args.python, "attackzoo.py", "stop", attack_id])


def probe_endpoint_args(probe: str, endpoint: str) -> List[str]:
    if probe == "http":
        return ["--http-url", endpoint]
    if probe == "https":
        return ["--https-url", endpoint]
    if probe == "mqtt":
        host, port_s = endpoint.rsplit(":", 1)
        return ["--mqtt-host", host, "--mqtt-port", port_s]
    return ["--probe-endpoint", f"{probe}={endpoint}"]


def build_bpf(args: argparse.Namespace, attack_id: str, plan_ports: Iterable[int], local_link: bool) -> str:
    if args.bpf_mode == "all":
        return ""
    if args.bpf:
        return args.bpf
    if attack_id in AUTO_BPF_BY_ATTACK:
        return AUTO_BPF_BY_ATTACK[attack_id]
    if local_link:
        return ""
    ports = sorted({int(p) for p in plan_ports if p})
    if not ports:
        return ""
    return " or ".join(f"port {p}" for p in ports)


def is_local_link_attack(meta: AttackMeta, target_param: Any) -> bool:
    targets = " ".join(meta.target_services).lower()
    if "local network" in targets or "local ipv6 network" in targets:
        return True
    return bool(target_param is not None and target_param.kind == "cidr")


def build_plans(args: argparse.Namespace, campaign_root: Path) -> List[AttackPlan]:
    specs = _all_specs()
    metas = load_attack_metadata()
    categories = attack_category_by_id()
    servers = load_server_specs()

    target_net = args.target_net
    spoof_gw = args.spoof_gw
    if not target_net or not spoof_gw:
        detected_net, detected_gw = docker0_network()
        target_net = target_net or detected_net
        spoof_gw = spoof_gw or detected_gw

    only = set(split_csv(args.only))
    skip = set(split_csv(args.skip))
    service_ips = {sid: docker_container_ip(s.container_name) for sid, s in servers.items()}

    plans: List[AttackPlan] = []
    for attack_id in sorted(specs):
        if only and attack_id not in only:
            continue
        if attack_id in skip:
            continue
        spec = specs[attack_id]
        meta = metas.get(
            attack_id,
            AttackMeta(
                attack_id=attack_id,
                name=spec.name,
                category=categories.get(attack_id, ""),
                target_services=(),
                yaml_path="",
            ),
        )
        service_id = resolve_service_id(meta, servers)
        service = servers.get(service_id)
        probe = SERVICE_PROBE.get(service_id, "http")
        service_ip = service_ips.get(service_id, "")
        target_param = _find_target_param(spec)
        port_param = _find_port_param(spec)
        target_value, target_port = target_for_plan(
            args=args,
            spec=spec,
            target_param=target_param,
            port_param=port_param,
            service=service,
            service_ip=service_ip,
            probe=probe,
            target_net=target_net,
        )

        published_probe_port = port_for_service(service, probe, True)
        endpoint_host = args.probe_host
        endpoint = f"{endpoint_host}:{published_probe_port}"
        if probe == "http":
            endpoint = f"http://{endpoint_host}:{published_probe_port}/"
        elif probe == "https":
            endpoint = f"https://{endpoint_host}:{published_probe_port}/"

        probes = tuple(split_csv(args.probes)) if args.probes else (probe,)
        probe_endpoints: Dict[str, str] = {}
        for probe_name in probes:
            p = probe_name.strip()
            if not p or p == "none":
                continue
            if p == probe:
                probe_endpoints[p] = endpoint
            else:
                aux_service_id = next((sid for sid, candidate in SERVICE_PROBE.items() if candidate == p), "")
                aux_service = servers.get(aux_service_id)
                aux_port = port_for_service(aux_service, p, True)
                if p == "http":
                    probe_endpoints[p] = f"http://{endpoint_host}:{aux_port}/"
                elif p == "https":
                    probe_endpoints[p] = f"https://{endpoint_host}:{aux_port}/"
                else:
                    probe_endpoints[p] = f"{endpoint_host}:{aux_port}"

        local_link = is_local_link_attack(meta, target_param)
        capture_all = local_link or port_param is None
        bpf_ports = set()
        if target_port:
            bpf_ports.add(target_port)
        if service_id == "smb-server":
            bpf_ports.update(SMB_PORTS)
        for ep_probe, ep_value in probe_endpoints.items():
            if ep_probe in {"http", "https"}:
                try:
                    bpf_ports.add(int(ep_value.rstrip("/").rsplit(":", 1)[1]))
                except Exception:
                    pass
            else:
                try:
                    bpf_ports.add(int(ep_value.rsplit(":", 1)[1]))
                except Exception:
                    pass

        out_arg = f"{args.out}/{attack_id}"
        experiment_dir = campaign_root / attack_id
        features_dir = experiment_dir / "features"
        datasets_dir = experiment_dir / "datasets"
        extras = extra_run_args(
            args=args,
            spec=spec,
            target_param=target_param,
            port_param=port_param,
            target_net=target_net,
            spoof_gw=spoof_gw,
        )
        start_hook = build_hook(
            args=args,
            spec=spec,
            target_param=target_param,
            port_param=port_param,
            target_value=target_value,
            target_port=target_port,
            extras=extras,
        )
        plan = AttackPlan(
            attack_id=attack_id,
            name=spec.name,
            category=meta.category,
            out_arg=out_arg,
            experiment_dir=str(experiment_dir),
            service_id=service_id,
            service_label=SERVICE_PROBE.get(service_id, service_id).replace("-", "_"),
            target_value=target_value,
            target_port=target_port,
            target_param=target_param.key if target_param else None,
            port_param=port_param.key if port_param else None,
            server_container=service.container_name if service else "",
            probes=tuple(probe_endpoints.keys()),
            probe_endpoints=probe_endpoints,
            bpf=build_bpf(args, attack_id, bpf_ports, local_link=capture_all),
            features_dir=str(features_dir),
            datasets_dir=str(datasets_dir),
            attack_start_hook=start_hook,
            attack_stop_hook=build_stop_hook(args, attack_id),
        )
        plans.append(plan)

    return plans


def command_for_experiment(args: argparse.Namespace, plan: AttackPlan) -> List[str]:
    cmd: List[str] = [
        args.python,
        "attackzoo.py",
        "experiment",
        "--attack-id",
        plan.attack_id,
        "--out",
        plan.out_arg,
        "--service",
        plan.service_label,
        "--runs",
        str(args.runs),
        "--levels",
        args.levels,
        "--warmup",
        str(args.warmup),
        "--attack",
        str(args.attack),
        "--cooldown",
        str(args.cooldown),
        "--interval",
        str(args.probe_interval),
        "--probe-timeout",
        str(args.probe_timeout),
        "--probes",
        ",".join(plan.probes) if plan.probes else "none",
        "--host",
        plan.target_value or args.fallback_target_ip,
        "--iface",
        args.iface,
        "--bpf",
        plan.bpf,
        "--resource-interval",
        str(args.resource_interval),
        "--features-dir",
        plan.features_dir,
        "--dataset-dir",
        plan.datasets_dir,
        "--attack-start-hook",
        plan.attack_start_hook,
        "--attack-stop-hook",
        plan.attack_stop_hook,
    ]
    if plan.target_port is not None:
        cmd.extend(["--port", str(plan.target_port)])
    for probe, endpoint in plan.probe_endpoints.items():
        cmd.extend(probe_endpoint_args(probe, endpoint))
    if args.collect_resources:
        cmd.append("--collect-resources")
    if args.collect_server_stats and plan.server_container:
        cmd.extend(["--server", plan.server_container])
    if args.extract_features:
        cmd.append("--extract-features")
        tools = set(split_csv(args.feature_tools))
        if "ntlflowlyzer" in tools:
            cmd.append("--tools-ntl")
        if "tshark" in tools:
            cmd.append("--tools-tshark")
        if "scapy" in tools:
            cmd.append("--tools-scapy")
    if args.build_dataset:
        cmd.append("--build-dataset")
    return cmd


def command_for_report(args: argparse.Namespace, input_dir: Path, outdir: Optional[Path] = None) -> List[str]:
    cmd = [
        args.python,
        "attackzoo.py",
        "report",
        "--input",
        str(input_dir),
        "--warmup",
        str(args.warmup),
        "--attack",
        str(args.attack),
        "--cooldown",
        str(args.cooldown),
    ]
    if outdir is not None:
        cmd.extend(["--outdir", str(outdir)])
    return cmd


def directory_size_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    result = run_quiet(["du", "-sb", str(path)], timeout_s=300)
    if result.returncode == 0 and result.stdout:
        try:
            return int(result.stdout.split()[0])
        except Exception:
            pass
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            try:
                total += (Path(root) / name).stat().st_size
            except OSError:
                pass
    return total


def guard_snapshot(args: argparse.Namespace, campaign_root: Path) -> GuardSnapshot:
    used = directory_size_bytes(campaign_root)
    load1, load5, load15 = os.getloadavg()
    usage = shutil.disk_usage(campaign_root if campaign_root.exists() else campaign_root.parent)
    snap = GuardSnapshot(
        timestamp_utc=utc_now(),
        directory_bytes=used,
        directory_gb=bytes_to_gb(used),
        disk_limit_gb=float(args.disk_limit_gb),
        load1=float(load1),
        load5=float(load5),
        load15=float(load15),
        load_limit=float(args.load_limit),
        free_gb=bytes_to_gb(usage.free),
        min_free_gb=float(args.min_free_gb),
        ok=True,
    )
    if used > gb_to_bytes(float(args.disk_limit_gb)):
        snap.ok = False
        snap.reason = f"campaign directory exceeded {args.disk_limit_gb:g} GiB"
    elif load1 > float(args.load_limit):
        snap.ok = False
        snap.reason = f"load1 exceeded {args.load_limit:g}"
    elif float(args.min_free_gb) > 0 and snap.free_gb < float(args.min_free_gb):
        snap.ok = False
        snap.reason = f"free filesystem space below {args.min_free_gb:g} GiB"
    return snap


def append_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def terminate_process_group(proc: subprocess.Popen[Any], timeout_s: float = 30.0) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait(timeout=10)


def cleanup_attack(args: argparse.Namespace, attack_id: str) -> None:
    run_quiet([args.python, "attackzoo.py", "stop", attack_id], timeout_s=30)


def run_monitored(
    *,
    args: argparse.Namespace,
    cmd: Sequence[str],
    log_path: Path,
    campaign_root: Path,
    monitor_log: Path,
    current_attack_id: Optional[str],
) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    append_jsonl(
        monitor_log,
        {
            "event": "start_process",
            "timestamp_utc": utc_now(),
            "attack_id": current_attack_id,
            "cmd": list(cmd),
            "log": str(log_path),
        },
    )
    with log_path.open("a", encoding="utf-8", errors="replace") as log:
        log.write(f"\n[{utc_now()}] $ {shell_join(cmd)}\n")
        log.flush()
        proc = subprocess.Popen(
            list(cmd),
            cwd=REPO_ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
        )
        while True:
            rc = proc.poll()
            if rc is not None:
                append_jsonl(
                    monitor_log,
                    {
                        "event": "finish_process",
                        "timestamp_utc": utc_now(),
                        "attack_id": current_attack_id,
                        "returncode": rc,
                        "cmd": list(cmd),
                    },
                )
                return int(rc)

            time.sleep(float(args.check_interval_s))
            snap = guard_snapshot(args, campaign_root)
            append_jsonl(monitor_log, {"event": "guard", **dataclasses.asdict(snap)})
            if not snap.ok:
                append_jsonl(
                    monitor_log,
                    {
                        "event": "kill_switch",
                        "attack_id": current_attack_id,
                        **dataclasses.asdict(snap),
                    },
                )
                terminate_process_group(proc)
                if current_attack_id:
                    cleanup_attack(args, current_attack_id)
                raise KillSwitchTriggered(snap)


def start_servers(args: argparse.Namespace) -> None:
    if args.restart_servers:
        action = "restart"
    elif args.start_servers:
        action = "start"
    else:
        return
    result = subprocess.run([str(REPO_ROOT / "servers.sh"), action, args.server_profile], cwd=REPO_ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def stop_servers(args: argparse.Namespace) -> None:
    if args.stop_servers_on_exit:
        subprocess.run([str(REPO_ROOT / "servers.sh"), "stop", args.server_profile], cwd=REPO_ROOT)


def save_catalog_snapshot(args: argparse.Namespace, campaign_root: Path) -> None:
    result = run_quiet([args.python, "attackzoo.py", "list", "--json"], timeout_s=60)
    payload = {
        "cmd": [args.python, "attackzoo.py", "list", "--json"],
        "returncode": result.returncode,
        "stdout_json": None,
        "stderr": result.stderr,
    }
    if result.stdout:
        try:
            payload["stdout_json"] = json.loads(result.stdout)
        except Exception:
            payload["stdout_text"] = result.stdout
    write_json(campaign_root / "_campaign" / "catalog_snapshot.json", payload)


def result_path_for(plan: AttackPlan) -> Path:
    return Path(plan.experiment_dir) / "campaign_attack_result.json"


def is_completed(plan: AttackPlan) -> bool:
    path = result_path_for(plan)
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return data.get("status") == "completed"


def run_campaign(args: argparse.Namespace) -> int:
    campaign_root = REPO_ROOT / "experiments" / args.out
    campaign_meta_dir = campaign_root / "_campaign"
    logs_dir = campaign_meta_dir / "logs"
    monitor_log = campaign_meta_dir / "monitor.jsonl"
    campaign_root.mkdir(parents=True, exist_ok=True)

    if not args.dry_run and not docker_available():
        print("[ERROR] Docker is not available. Aborting before campaign start.", file=sys.stderr)
        return 2

    if not args.dry_run:
        start_servers(args)

    plans = build_plans(args, campaign_root)
    write_json(
        campaign_meta_dir / "campaign_config.json",
        {
            "started_at_utc": utc_now(),
            "repo_root": str(REPO_ROOT),
            "args": vars(args),
            "attack_count": len(plans),
            "plans": [dataclasses.asdict(p) for p in plans],
        },
    )
    save_catalog_snapshot(args, campaign_root)

    print(f"[INFO] Campaign root: {campaign_root}")
    print(f"[INFO] Planned attacks: {len(plans)}")
    print(f"[INFO] Guardrails: directory <= {args.disk_limit_gb:g} GiB, load1 <= {args.load_limit:g}")

    if args.dry_run:
        for plan in plans:
            print(f"[DRY-RUN] {plan.attack_id}: {shell_join(command_for_experiment(args, plan))}")
        return 0

    exit_code = 0
    try:
        for index, plan in enumerate(plans, start=1):
            if args.resume and is_completed(plan):
                print(f"[SKIP] {index}/{len(plans)} {plan.attack_id} already completed")
                append_jsonl(
                    monitor_log,
                    {"event": "skip_completed", "timestamp_utc": utc_now(), "attack_id": plan.attack_id},
                )
                continue

            snap = guard_snapshot(args, campaign_root)
            append_jsonl(monitor_log, {"event": "pre_attack_guard", "attack_id": plan.attack_id, **dataclasses.asdict(snap)})
            if not snap.ok:
                raise KillSwitchTriggered(snap)

            attack_start = time.time()
            print(f"[RUN] {index}/{len(plans)} {plan.attack_id} ({plan.name})")
            exp_cmd = command_for_experiment(args, plan)
            exp_log = logs_dir / f"{plan.attack_id}.experiment.log"
            rc_exp = run_monitored(
                args=args,
                cmd=exp_cmd,
                log_path=exp_log,
                campaign_root=campaign_root,
                monitor_log=monitor_log,
                current_attack_id=plan.attack_id,
            )

            rc_report: Optional[int] = None
            report_log = logs_dir / f"{plan.attack_id}.report.log"
            if args.generate_reports:
                rc_report = run_monitored(
                    args=args,
                    cmd=command_for_report(args, Path(plan.experiment_dir)),
                    log_path=report_log,
                    campaign_root=campaign_root,
                    monitor_log=monitor_log,
                    current_attack_id=plan.attack_id,
                )

            status = "completed" if rc_exp == 0 and (rc_report in {None, 0}) else "failed"
            result = {
                "attack_id": plan.attack_id,
                "status": status,
                "finished_at_utc": utc_now(),
                "elapsed_s": round(time.time() - attack_start, 3),
                "experiment_returncode": rc_exp,
                "report_returncode": rc_report,
                "experiment_log": str(exp_log),
                "report_log": str(report_log) if args.generate_reports else "",
                "plan": dataclasses.asdict(plan),
            }
            write_json(result_path_for(plan), result)
            append_jsonl(monitor_log, {"event": "attack_result", **result})
            if status != "completed":
                exit_code = 1
                print(f"[WARN] {plan.attack_id} finished with status={status}")
                cleanup_attack(args, plan.attack_id)
                if args.stop_on_failure:
                    break

        if args.generate_reports:
            final_log = logs_dir / "campaign.report.log"
            final_rc = run_monitored(
                args=args,
                cmd=command_for_report(args, campaign_root, campaign_root / "reports"),
                log_path=final_log,
                campaign_root=campaign_root,
                monitor_log=monitor_log,
                current_attack_id=None,
            )
            if final_rc != 0:
                exit_code = max(exit_code, 1)

        write_json(
            campaign_meta_dir / "campaign_finished.json",
            {
                "finished_at_utc": utc_now(),
                "exit_code": exit_code,
                "final_guard": dataclasses.asdict(guard_snapshot(args, campaign_root)),
            },
        )
        return exit_code

    except KillSwitchTriggered as exc:
        kill_path = campaign_meta_dir / "kill_switch.json"
        write_json(
            kill_path,
            {
                "triggered_at_utc": utc_now(),
                "reason": exc.snapshot.reason,
                "snapshot": dataclasses.asdict(exc.snapshot),
            },
        )
        print(f"[KILL-SWITCH] {exc.snapshot.reason}. Details: {kill_path}", file=sys.stderr)
        return 3
    finally:
        stop_servers(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a guarded full AttackZoo campaign across the current attack catalog.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--out", default=campaign_name(), help="Campaign subdirectory under experiments/.")
    parser.add_argument("--python", default=sys.executable, help="Python executable used to invoke attackzoo.py.")
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    parser.add_argument("--levels", default=DEFAULT_LEVELS)
    parser.add_argument("--warmup", type=float, default=DEFAULT_WARMUP_S)
    parser.add_argument("--attack", type=float, default=DEFAULT_ATTACK_S)
    parser.add_argument("--cooldown", type=float, default=DEFAULT_COOLDOWN_S)
    parser.add_argument("--probe-interval", type=float, default=0.5)
    parser.add_argument("--probe-timeout", type=float, default=DEFAULT_PROBE_TIMEOUT_S)
    parser.add_argument("--resource-interval", type=float, default=DEFAULT_RESOURCE_INTERVAL_S)
    parser.add_argument("--iface", default=DEFAULT_IFACE, help="Interface passed to tcpdump.")
    parser.add_argument("--bpf-mode", choices=["auto", "all"], default="auto")
    parser.add_argument("--bpf", default="", help="Force one BPF filter for every attack. Overrides --bpf-mode auto.")
    parser.add_argument("--probes", default="", help="Comma-separated probes for every attack. Empty means per-target auto.")
    parser.add_argument("--probe-host", default="127.0.0.1", help="Host used by availability probes.")
    parser.add_argument("--host-target", default="127.0.0.1", help="Host target for attacks with target+port parameters.")
    parser.add_argument("--fallback-target-ip", default="172.17.0.1")
    parser.add_argument("--fallback-target-port", type=int, default=8080)
    parser.add_argument("--fallback-text", default="attackzoo")
    parser.add_argument("--target-net", default="", help="CIDR used by target_net attacks. Empty auto-detects docker0.")
    parser.add_argument("--spoof-gw", default="", help="Gateway IP for ARP spoof. Empty auto-detects docker0.")
    parser.add_argument("--attack-rate-pps", type=float, default=None, help="Optional --rate value passed to attackzoo.py run.")

    parser.add_argument("--disk-limit-gb", type=float, default=DEFAULT_DISK_LIMIT_GB)
    parser.add_argument("--load-limit", type=float, default=DEFAULT_LOAD_LIMIT)
    parser.add_argument("--min-free-gb", type=float, default=0.0)
    parser.add_argument("--check-interval-s", type=float, default=DEFAULT_CHECK_INTERVAL_S)

    parser.add_argument("--feature-tools", default="ntlflowlyzer,tshark,scapy")
    parser.add_argument("--extract-features", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--build-dataset", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--generate-reports", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--collect-resources", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--collect-server-stats", action=argparse.BooleanOptionalAction, default=True)

    parser.add_argument("--start-servers", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--restart-servers", action="store_true")
    parser.add_argument("--server-profile", choices=["all", "full", "redux"], default="all")
    parser.add_argument("--stop-servers-on-exit", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--stop-on-failure", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", default="", help="Comma-separated attack IDs to include.")
    parser.add_argument("--skip", default="", help="Comma-separated attack IDs to skip.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run_campaign(args)


if __name__ == "__main__":
    raise SystemExit(main())
