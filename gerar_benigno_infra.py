#!/usr/bin/env python3
"""Campanha benigna de INFRAESTRUTURA (ARP/DNS/DHCP) para medir o FP das 4 regras
nao cobertas pelo B8 (9903001 dhcp, 9906001 dns, B7_Net::ARP_Spoof, B7_Net::DHCP_Starvation).

Gera trafego LEGITIMO desses 3 protocolos, isolado em bridges Docker dedicadas, e
captura (capture-sidecar). Tudo local: dnsmasq resolve/serve na propria bridge, sem
consultas externas. Saida: experiments/benign_infra/<svc>/run0N.pcap.

A regressao (rodar as 4 regras e contar FP) e feita por `coletar_fp_infra.py`.

Uso: python3 gerar_benigno_infra.py            # 3 reps de cada servico
     python3 gerar_benigno_infra.py --only arp
"""
from __future__ import annotations
import argparse, subprocess, time, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "experiments" / "benign_infra"
ALPINE = "alpine:latest"
CAP = "capture-sidecar:latest"
APK = "apk add -q dnsmasq bind-tools >/dev/null 2>&1"
# dominios normais (sem rotulo hexadecimal longo -> nao casa 9906001)
DOMS = ["example.com", "api.servico.local", "mail.campus.local", "ntp.pool.local",
        "www.unipampa.local", "repo.pacotes.local", "sensor01.iot.local", "broker.mqtt.local"]


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def net_up(name, subnet, internal=False):
    sh(["docker", "network", "rm", name])
    c = ["docker", "network", "create", "--driver", "bridge", "--subnet", subnet]
    if internal:
        c += ["--internal"]
    sh(c + [name], check=False)


def ip_of(cont, net):
    return sh(["docker", "inspect", "-f",
               '{{(index .NetworkSettings.Networks "' + net + '").IPAddress}}', cont]).stdout.strip()


def start_capture(name, target_cont, outfile):
    sh(["docker", "rm", "-f", name])
    (OUT / outfile).parent.mkdir(parents=True, exist_ok=True)
    sh(["docker", "run", "-d", "--name", name, f"--net=container:{target_cont}",
        "-v", f"{OUT}:/captures", "-e", f"CAPTURE_FILE={outfile}", CAP])
    time.sleep(2)


def stop(*names):
    for n in names:
        sh(["docker", "rm", "-f", n])


def gen_arp(rep: int):
    net = "fp-arp"; net_up(net, "172.30.10.0/24")
    c1, c2, cap = "fp-arp-c1", "fp-arp-c2", "fp-arp-cap"
    stop(c1, c2, cap)
    sh(["docker", "run", "-d", "--name", c1, "--network", net, ALPINE, "sleep", "120"])
    sh(["docker", "run", "-d", "--name", c2, "--network", net, ALPINE, "sleep", "120"])
    time.sleep(2)
    ip2 = ip_of(c2, net); ip1 = ip_of(c1, net)
    svc = OUT / "arp"; svc.mkdir(parents=True, exist_ok=True)
    start_capture(cap, c1, f"arp/run{rep:02d}.pcap")
    # trafego benigno: resolucao ARP repetida (limpa cache e re-pinga -> varias ARP replies normais)
    for _ in range(6):
        sh(["docker", "exec", c1, "sh", "-c", f"ip neigh flush all 2>/dev/null; ping -c 2 -W 1 {ip2}"], timeout=30)
        sh(["docker", "exec", c2, "sh", "-c", f"ip neigh flush all 2>/dev/null; ping -c 2 -W 1 {ip1}"], timeout=30)
        time.sleep(1.5)
    time.sleep(2); stop(cap, c1, c2)
    sh(["docker", "network", "rm", net])
    print(f"  arp run{rep:02d}: MACs esperados 02:42:* (LA) nas ARP replies")


def gen_dns(rep: int):
    net = "fp-dns"; net_up(net, "172.30.11.0/24")
    srv, cli, cap = "fp-dns-srv", "fp-dns-cli", "fp-dns-cap"
    stop(srv, cli, cap)
    # dnsmasq local: responde tudo para um IP fixo, sem upstream (sem consultas externas)
    sh(["docker", "run", "-d", "--name", srv, "--network", net, "--cap-add", "NET_ADMIN", ALPINE,
        "sh", "-c", f"{APK}; dnsmasq -k --no-resolv --no-hosts --address=/#/10.99.99.99 --log-queries"])
    sh(["docker", "run", "-d", "--name", cli, "--network", net, ALPINE, "sh", "-c", f"{APK}; sleep 120"])
    time.sleep(6)
    sip = ip_of(srv, net)
    start_capture(cap, srv, f"dns/run{rep:02d}.pcap")
    # cliente faz queries A de dominios normais em cadencia benigna
    q = "; ".join(f"dig +tries=1 +time=2 @{sip} {d} A >/dev/null 2>&1; sleep 0.7" for d in DOMS * 3)
    sh(["docker", "exec", cli, "sh", "-c", q], timeout=120)
    time.sleep(2); stop(cap, cli, srv)
    sh(["docker", "network", "rm", net])
    print(f"  dns run{rep:02d}: {len(DOMS)*3} queries A de dominios normais")


def gen_dhcp(rep: int):
    net = "fp-dhcp"; net_up(net, "172.30.12.0/24")
    srv, cli, cap = "fp-dhcp-srv", "fp-dhcp-cli", "fp-dhcp-cap"
    stop(srv, cli, cap)
    # dnsmasq como servidor DHCP na bridge
    sh(["docker", "run", "-d", "--name", srv, "--network", net, "--cap-add", "NET_ADMIN", ALPINE,
        "sh", "-c", f"{APK}; dnsmasq -k --port=0 --dhcp-range=172.30.12.100,172.30.12.200,1h --log-dhcp"])
    sh(["docker", "run", "-d", "--name", cli, "--network", net, "--cap-add", "NET_ADMIN", ALPINE,
        "sh", "-c", f"{APK}; sleep 120"])
    time.sleep(6)
    start_capture(cap, srv, f"dhcp/run{rep:02d}.pcap")
    # cliente faz alguns leases legitimos (DISCOVER/OFFER/REQUEST/ACK), cadencia benigna
    for _ in range(3):
        sh(["docker", "exec", cli, "sh", "-c", "udhcpc -i eth0 -n -q -t 2 -T 2 2>/dev/null; sleep 2"], timeout=40)
    time.sleep(2); stop(cap, cli, srv)
    sh(["docker", "network", "rm", net])
    print(f"  dhcp run{rep:02d}: 3 leases benignos (DISCOVER < limiar 12/20s)")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["arp", "dns", "dhcp"])
    ap.add_argument("--reps", type=int, default=3)
    a = ap.parse_args(argv)
    gens = {"arp": gen_arp, "dns": gen_dns, "dhcp": gen_dhcp}
    svcs = [a.only] if a.only else list(gens)
    for svc in svcs:
        print(f"== {svc} ==")
        for r in range(1, a.reps + 1):
            gens[svc](r)
    # relatorio de tamanhos
    print("\nCapturas:")
    for p in sorted(OUT.rglob("*.pcap")):
        print(f"  {p.relative_to(OUT)}  {p.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
