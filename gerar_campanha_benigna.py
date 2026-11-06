#!/usr/bin/env python3
"""Campanha benigna (135 casos) — wrapper fino sobre `attackzoo.py experiment`.

9 servicos x 3 perfis de carga (baixo/medio/alto) x 5 repeticoes = 135 PCAPs,
timing 10/20/10s, capturados no bridge docker0. O gerador benigno e o
`client-super` (um servico por execucao), acionado pelo `--attack-start-hook` do
experiment (a imagem do spec do ataque NAO e usada — o spec serve so para validar
o --attack-id; ver modules/attackzoo/experiment.py). Para nao poluir o registro de
60 ataques, usa-se um attack_id REGISTRADO do mesmo servico apenas como rotulo
transitorio e, ao final, o diretorio e renomeado para o servico e o meta.json e
reescrito com a semantica benigna (condition=benign_control, provenance,
service, profile).

Uso:
  python3 gerar_campanha_benigna.py --dry-run           # imprime o plano
  python3 gerar_campanha_benigna.py --only coap --runs 1  # smoke de 1 servico
  python3 gerar_campanha_benigna.py                      # campanha completa (135)

NAO publica/!= B8: depois de gerar, rodar a regressao B8 (GT+B7) sobre os PCAPs.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # .../attackzoo-sbseg26
OUT_NAME = "benign_135"
WARMUP, ATTACK, COOLDOWN = 10, 20, 10           # timing declarado na proposta
SSH_PASS = "0cGSCgtThAm3bDng8LjIm7t2"

# perfis de carga legitima (NAO niveis de ataque): nome, count, interval_s
PROFILES = [("baixo", 4, 5.0), ("medio", 20, 1.0), ("alto", 100, 0.2)]

# Override por servico (B8): servicos de SESSAO autenticada tem carga legitima pesada BAIXA em
# conexoes novas (clientes reutilizam a sessao). O perfil "alto" uniforme (100/0.2s) e stateless-
# oriented e gerava FP (ex.: 9907001 no ssh/alto). Para SSH, mantem contagem de conexoes novas
# abaixo do limiar da regra (20/30s), ordenada e muito abaixo do ataque (95 conexoes). Metrica:
# nº de conexoes novas por origem na janela. Ver protocolo/criterio_rejeicao_fp_b8.md e B8_RESULTADO.
PROFILE_OVERRIDE = {
    "ssh": [("baixo", 3, 6.0), ("medio", 8, 2.5), ("alto", 15, 1.2)],
}

# por servico: csuper_svc, attack_id REGISTRADO (rotulo transitorio, mesmo servico),
# server_image, extra args de startup do server (lista), porta interna, bpf, env de credenciais
SERVICES = {
    "http":   dict(csuper="web",       label="dos_http_simple",            img="server-http-server",    extra=[], port=80,   bpf="tcp port 80",   creds={}),
    "coap":   dict(csuper="coap",      label="iot_coap_get_flood",         img="server-coap-server",    extra=[], port=5683, bpf="udp port 5683", creds={}),
    "ssh":    dict(csuper="ssh",       label="bf_ssh",                     img="server-ssh-server",     extra=[], port=22,   bpf="tcp port 22",   creds={"BENIGN_SSH_USER":"root","BENIGN_SSH_PASS":SSH_PASS}),
    "mqtt":   dict(csuper="mqtt",      label="iot_mqtt_publisher",         img="server-mqtt-broker",    extra=[], port=1883, bpf="tcp port 1883", creds={"BENIGN_MQTT_USER":"benign","BENIGN_MQTT_PASS":"benignpass"}),
    "smb":    dict(csuper="smb",       label="recon_smb_enum",             img="server-smb-server",     extra=["-g","log level = 3","-s","public;/share","-u","example2;badpass"], port=445, bpf="tcp port 445", creds={"BENIGN_SMB_USER":"example2","BENIGN_SMB_PASS":"badpass"}),
    "telnet": dict(csuper="telnet",    label="bf_telnet",                  img="server-telnet-server",  extra=[], port=23,   bpf="tcp port 23",   creds={}),
    "ssl":    dict(csuper="https",     label="web_https_heartbleed",       img="server-ssl-heartbleed", extra=[], port=443,  bpf="tcp port 443",  creds={}),
    "zenoh":  dict(csuper="zenoh",     label="iot_zenoh_pico_keepalive_flood", img="server-zenoh-router", extra=[], port=7447, bpf="port 7447",  creds={}),
    "xrce":   dict(csuper="xrce-dds",  label="iot_xrce_dds_udp_dos",       img="server-xrce-dds-agent", extra=["udp4","-p","8888"], port=8888, bpf="udp port 8888", creds={}),
}


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def server_name(svc): return f"benign-srv-{svc}"


def start_server(svc, cfg, dry):
    name = server_name(svc)
    sh(["docker", "rm", "-f", name])
    cmd = ["docker", "run", "-d", "--rm", "--name", name, f"{cfg['img']}:latest", *cfg["extra"]]
    if dry:
        print("  [server]", " ".join(cmd)); return "DRYRUN_IP"
    sh(cmd)
    ip = ""
    for _ in range(20):
        ip = sh(["docker","inspect","-f","{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",name]).stdout.strip()
        if ip: break
        time.sleep(1)
    if ip and not wait_ready(svc, cfg, ip):
        print(f"  [AVISO] {svc}: servico nao respondeu ao probe de prontidao (captura pode sair vazia)")
    return ip


def wait_ready(svc, cfg, ip, tries=10):
    """Sonda de prontidao: roda 1 requisicao benigna ate obter ok=1 (garante que o
    servico responde antes da campanha, evitando captura vazia por corrida de startup)."""
    cred_flags = []
    for k, v in cfg["creds"].items():
        cred_flags += ["-e", f"{k}={v}"]
    probe = ["docker","run","--rm",*cred_flags,"client-super:latest",cfg["csuper"],ip,str(cfg["port"]),"1","0","3"]
    for _ in range(tries):
        r = sh(probe, timeout=20)
        if "ok=1" in r.stdout:
            return True
        time.sleep(2)
    return False


def stop_server(svc, dry):
    if not dry: sh(["docker","rm","-f",server_name(svc)])


def run_experiment(svc, cfg, profile, count, interval, ip, runs, dry):
    cred_flags = []
    for k, v in cfg["creds"].items():
        cred_flags += ["-e", f"{k}={v}"]
    hook = ("docker run --rm " + " ".join(cred_flags) +
            f" client-super:latest {cfg['csuper']} {{host}} {{port}} {count} {interval} {ATTACK}")
    argv = ["python3", "attackzoo.py", "experiment",
            "--attack-id", cfg["label"], "--out", OUT_NAME, "--service", svc,
            "--levels", profile, "--runs", str(runs),
            "--warmup", str(WARMUP), "--attack", str(ATTACK), "--cooldown", str(COOLDOWN),
            "--iface", "docker0", "--bpf", f"{cfg['bpf']} and host {ip}",
            "--probes", "", "--host", ip, "--port", str(cfg["port"]),
            "--attack-start-hook", hook, "--attack-stop-hook", "true"]
    if dry:
        print("  [exp]", " ".join(f'"{a}"' if " " in a else a for a in argv)); return
    r = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, timeout=600)
    ok = "[OK]" in r.stdout
    print(f"  {svc}/{profile}: {'OK' if ok else 'FALHOU'}  {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]}")


def postprocess(svc, cfg, dry):
    """Renomeia <label> -> <svc> e reescreve meta.json com semantica benigna."""
    base = ROOT / "experiments" / OUT_NAME
    src = base / cfg["label"]
    dst = base / svc
    if dry or not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for prof_dir in src.iterdir():
        shutil.move(str(prof_dir), str(dst / prof_dir.name))
    src.rmdir()
    for meta in dst.rglob("meta.json"):
        d = json.loads(meta.read_text())
        profile = meta.parent.parent.name
        d["service"] = svc
        d["profile"] = profile
        d["condition"] = "benign_control"
        d["provenance"] = "benign_probe_or_client"
        d["benign_label_source_attack_id"] = cfg["label"]  # rastreabilidade
        d.pop("attack_id", None)
        if d.get("pcap"):  # corrige o caminho do pcap apos o rename <label>-><svc>
            d["pcap"] = d["pcap"].replace(f"/{cfg['label']}/", f"/{svc}/")
        meta.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="apenas este servico (ex.: coap)")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--profiles", help="subset de perfis, ex.: baixo,medio")
    a = ap.parse_args(argv)

    svcs = [a.only] if a.only else list(SERVICES)
    wanted = a.profiles.split(",") if a.profiles else None
    print(f"Campanha benigna: {len(svcs)} servicos x reps={a.runs} "
          f"(out: experiments/{OUT_NAME}/)  {'[DRY-RUN]' if a.dry_run else ''}")
    for svc in svcs:
        cfg = SERVICES[svc]
        base = PROFILE_OVERRIDE.get(svc, PROFILES)
        profs = [p for p in base if (not wanted or p[0] in wanted)]
        ov = " [perfil recalibrado]" if svc in PROFILE_OVERRIDE else ""
        print(f"\n== {svc} (server {cfg['img']}, client-super {cfg['csuper']}:{cfg['port']}){ov} perfis={[p[0]+f'({p[1]}/{p[2]}s)' for p in profs]} ==")
        ip = start_server(svc, cfg, a.dry_run)
        try:
            if not ip and not a.dry_run:
                print(f"  ERRO: servidor {svc} nao subiu"); continue
            for name, count, interval in profs:
                run_experiment(svc, cfg, name, count, interval, ip, a.runs, a.dry_run)
        finally:
            stop_server(svc, a.dry_run)
        postprocess(svc, cfg, a.dry_run)
    print("\nConcluido." if not a.dry_run else "\nDry-run concluido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
