#!/usr/bin/env python3
import base64
import os
import secrets
import socket
import subprocess
import sys
import time
from typing import List, Optional, Tuple
import paramiko

PER_TRY_TIMEOUT_S = 1.0

def _strip_commas(s: str) -> str:
    return s.strip().strip(",").strip()

def _to_int(s: str, name: str) -> int:
    s2 = _strip_commas(s)
    try:
        return int(s2)
    except Exception:
        raise SystemExit(f'Invalid parameter "{name}": {s!r}')


def _to_float(s: str, name: str) -> float:
    s2 = _strip_commas(s)
    try:
        return float(s2)
    except Exception:
        raise SystemExit(f'Invalid parameter "{name}": {s!r}')

def _rand_userpass() -> Tuple[str, str]:
    # Short random username/password values (benign).
    user = "u" + secrets.token_hex(3)
    pw = "p" + secrets.token_hex(6)
    return user, pw


def _creds(service: str) -> Tuple[str, str]:
    # Credenciais benignas configuraveis por ambiente para servicos autenticados
    # (SSH/SMB/MQTT): BENIGN_<SERVICE>_USER / BENIGN_<SERVICE>_PASS. Se nao
    # definidas, mantem o comportamento anterior (usuario/senha aleatorios), que
    # gera apenas TENTATIVA (sem sessao concluida). Com credenciais validas, a
    # sessao benigna autentica e conclui (campanha benigna da frente B8).
    user = os.getenv(f"BENIGN_{service}_USER")
    pw = os.getenv(f"BENIGN_{service}_PASS")
    if user and pw:
        return user, pw
    return _rand_userpass()

def _run_cmd(cmd: List[str], timeout_s: float = PER_TRY_TIMEOUT_S) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except FileNotFoundError:
        return 127, "", f"binary not found: {cmd[0]}"
    except Exception as e:
        return 1, "", str(e)

def _tcp_dialog(ip: str, port: int, payload: bytes, read_first: bool = True) -> Tuple[bool, str]:
    """
    Connects over TCP (1s timeout), optionally reads a banner, sends a payload, and tries to read one short response.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(PER_TRY_TIMEOUT_S)
    try:
        s.connect((ip, port))
        if read_first:
            try:
                _ = s.recv(256)
            except Exception:
                pass
        if payload:
            try:
                s.sendall(payload)
            except Exception:
                pass
        try:
            _ = s.recv(256)
        except Exception:
            pass
        return True, "tcp_ok"
    except Exception as e:
        return False, f"tcp_err={type(e).__name__}"
    finally:
        try:
            s.close()
        except Exception:
            pass

def _udp_probe(ip: str, port: int, payload: bytes) -> Tuple[bool, str]:
    """
    Sends one UDP datagram (1s timeout) and tries to read one response if available.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(PER_TRY_TIMEOUT_S)
    try:
        s.connect((ip, port))
        try:
            s.send(payload)
        except Exception:
            pass
        try:
            _ = s.recv(256)
            return True, "udp_ok_reply"
        except socket.timeout:
            return True, "udp_ok_no_reply"
        except Exception:
            return True, "udp_ok_no_reply"
    except Exception as e:
        return False, f"udp_err={type(e).__name__}"
    finally:
        try:
            s.close()
        except Exception:
            pass

# ---------------------------
# Service implementations
# ---------------------------
def do_web(ip: str, port: int) -> Tuple[bool, str]:
    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{ip}:{port}/"
    cmd = ["curl", "-k", "-sS", "--connect-timeout", "1", "--max-time", "1", "-o", "/dev/null", "-w", "%{http_code}", url]
    rc, out, err = _run_cmd(cmd)
    if rc == 0:
        return True, f"http_code={out or '-'}"
    return False, f"curl_rc={rc} err={err[:80]}"

def do_smb(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _creds("SMB")
    # -L lists shares; -t is the internal timeout; subprocess also has a 1s timeout.
    cmd = ["smbclient", "-L", f"//{ip}", "-p", str(port), "-U", f"{user}%{pw}", "-m", "SMB3", "-t", "1"]
    rc, out, err = _run_cmd(cmd)
    return (rc == 0), (f"smbclient_rc={rc} err={err[:80]}" if rc != 0 else "smb_ok")

def do_ssh(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _creds("SSH")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=ip,
            port=port,
            username=user,
            password=pw,
            timeout=PER_TRY_TIMEOUT_S,
            banner_timeout=PER_TRY_TIMEOUT_S,
            auth_timeout=PER_TRY_TIMEOUT_S,
            allow_agent=False,
            look_for_keys=False,
        )
        client.close()
        return True, "ssh_connected"
    except Exception as e:
        try:
            client.close()
        except Exception:
            pass
        return False, f"ssh_err={type(e).__name__}"

def do_rdp(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _rand_userpass()
    # +auth-only exists in FreeRDP (xfreerdp). Keep subprocess timeout=1s either way.
    cmd = ["xfreerdp", f"/v:{ip}:{port}", f"/u:{user}", f"/p:{pw}", "+auth-only", "/cert:ignore"]
    rc, out, err = _run_cmd(cmd)
    # In some versions, returncode is not reliable; the goal here is benign traffic.
    return (rc == 0 or rc == 124), (f"xfreerdp_rc={rc} err={err[:80]}" if rc not in (0, 124) else "rdp_attempted")

def do_telnet(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _rand_userpass()
    payload = (f"{user}\r\n{pw}\r\nexit\r\n").encode("utf-8", errors="ignore")
    ok, info = _tcp_dialog(ip, port, payload, read_first=True)
    return ok, info

def do_smtp(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _rand_userpass()
    u64 = base64.b64encode(user.encode()).decode()
    p64 = base64.b64encode(pw.encode()).decode()
    payload = (
        "EHLO SBSeg26.local\r\n"
        "AUTH LOGIN\r\n"
        f"{u64}\r\n"
        f"{p64}\r\n"
        "QUIT\r\n"
    ).encode()
    ok, info = _tcp_dialog(ip, port, payload, read_first=True)
    return ok, info

def do_imap(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _rand_userpass()
    payload = (f"a1 LOGIN {user} {pw}\r\na2 LOGOUT\r\n").encode()
    ok, info = _tcp_dialog(ip, port, payload, read_first=True)
    return ok, info

def do_pop3(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _rand_userpass()
    payload = (f"USER {user}\r\nPASS {pw}\r\nQUIT\r\n").encode()
    ok, info = _tcp_dialog(ip, port, payload, read_first=True)
    return ok, info

def do_ftp(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _rand_userpass()
    payload = (f"USER {user}\r\nPASS {pw}\r\nQUIT\r\n").encode()
    ok, info = _tcp_dialog(ip, port, payload, read_first=True)
    return ok, info

def do_dns(ip: str, port: int) -> Tuple[bool, str]:
    # Simple A query (tries/time = 1s).
    cmd = ["dig", f"@{ip}", "-p", str(port), "+time=1", "+tries=1", "example.com", "A"]
    rc, out, err = _run_cmd(cmd)
    return (rc == 0), (f"dig_rc={rc} err={err[:80]}" if rc != 0 else "dns_ok")

def do_snmp(ip: str, port: int) -> Tuple[bool, str]:
    # SNMP community = "credential" -> randomize it.
    community = "c" + secrets.token_hex(4)
    # sysUpTime.0 (test default).
    cmd = ["snmpget", "-v2c", "-c", community, "-t", "1", "-r", "0", "-p", str(port), ip, "sysUpTime.0"]
    rc, out, err = _run_cmd(cmd)
    return (rc == 0), (f"snmp_rc={rc} err={err[:80]}" if rc != 0 else "snmp_ok")

def do_sip(ip: str, port: int) -> Tuple[bool, str]:
    # SIP OPTIONS over UDP (simple and generates traffic).
    branch = "z9hG4bK" + secrets.token_hex(6)
    tag = secrets.token_hex(4)
    callid = secrets.token_hex(8)
    from_user = "u" + secrets.token_hex(3)
    # Discover the local IP/port by "connecting" UDP.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(PER_TRY_TIMEOUT_S)
    try:
        s.connect((ip, port))
        local_ip, local_port = s.getsockname()
        msg = (
            f"OPTIONS sip:{ip} SIP/2.0\r\n"
            f"Via: SIP/2.0/UDP {local_ip}:{local_port};branch={branch}\r\n"
            f"Max-Forwards: 70\r\n"
            f"To: <sip:{ip}>\r\n"
            f"From: <sip:{from_user}@{local_ip}>;tag={tag}\r\n"
            f"Call-ID: {callid}@{local_ip}\r\n"
            f"CSeq: 1 OPTIONS\r\n"
            f"Contact: <sip:{from_user}@{local_ip}:{local_port}>\r\n"
            f"Content-Length: 0\r\n"
            f"\r\n"
        ).encode()
        try:
            s.send(msg)
        except Exception:
            pass
        try:
            _ = s.recv(256)
            return True, "sip_ok_reply"
        except socket.timeout:
            return True, "sip_ok_no_reply"
        except Exception:
            return True, "sip_ok_no_reply"
    except Exception as e:
        return False, f"sip_err={type(e).__name__}"
    finally:
        try:
            s.close()
        except Exception:
            pass

def do_coap(ip: str, port: int) -> Tuple[bool, str]:
    # Confirmable GET /sensors with a four-byte token and one Uri-Path option.
    # A raw minimal request avoids Request-Tag (option 292), unsupported by the
    # deliberately small CoAP target used by the controlled environment.
    message_id = secrets.token_bytes(2)
    token = secrets.token_bytes(4)
    request = b"\x44\x01" + message_id + token + b"\xb7sensors"
    ok, info = _udp_probe(ip, port, request)
    return ok, ("coap_ok_reply" if info == "udp_ok_reply" else info)

def do_mqtt(ip: str, port: int) -> Tuple[bool, str]:
    user, pw = _creds("MQTT")
    topic = f"SBSeg26/benign/{secrets.token_hex(3)}"
    payload = secrets.token_hex(8)
    client_id = f"{secrets.token_hex(4)}"
    cmd = [
        "mosquitto_pub",
        "-h", ip,
        "-p", str(port),
        "-t", topic,
        "-m", payload,
        "-i", client_id,
        "-u", user,
        "-P", pw,
        "-q", "0",
    ]
    rc, out, err = _run_cmd(cmd)
    return (rc == 0), (f"mqtt_rc={rc} err={err[:80]}" if rc != 0 else "mqtt_ok")

def do_zenoh_pico(ip: str, port: int) -> Tuple[bool, str]:
    # Simple Zenoh probe: try a TCP connect, then close; fall back to a UDP probe.
    ok, info = _tcp_dialog(ip, port, b"", read_first=False)
    if ok:
        return True, "zenoh_tcp_ok"
    ok2, info2 = _udp_probe(ip, port, b"zn_scout_" + secrets.token_bytes(6))
    return ok2, ("zenoh_udp_ok" if ok2 else info2)

def do_xrce_dds(ip: str, port: int) -> Tuple[bool, str]:
    # Micro XRCE-DDS is typically UDP: send a benign probe datagram.
    payload = b"uxrce_probe_" + secrets.token_bytes(8)
    ok, info = _udp_probe(ip, port, payload)
    return ok, info

SERVICE_MAP = {
    "web": do_web,
    "http": do_web,
    "https": do_web,

    "smb": do_smb,
    "ssh": do_ssh,
    "rdp": do_rdp,
    "telnet": do_telnet,

    "smtp": do_smtp,
    "imap": do_imap,
    "pop3": do_pop3,

    "ftp": do_ftp,
    "dns": do_dns,
    "snmp": do_snmp,
    "sip": do_sip,

    "coap": do_coap,
    "mqtt": do_mqtt,

    "zenoh-pico": do_zenoh_pico,
    "zenoh": do_zenoh_pico,

    "xrce-dds": do_xrce_dds,
    "uxrce-dds": do_xrce_dds,
}

DEFAULT_PORTS = {
    # Common defaults. If 0 is provided, use these defaults.
    "web": 80,
    "http": 80,
    "https": 443,
    "smb": 445,
    "ssh": 22,
    "rdp": 3389,
    "telnet": 23,
    "smtp": 25,
    "imap": 143,
    "pop3": 110,
    "ftp": 21,
    "dns": 53,
    "snmp": 161,
    "sip": 5060,
    "coap": 5683,
    "mqtt": 1883,
    "zenoh-pico": 7447,
    "zenoh": 7447,
    "xrce-dds": 8888,
    "uxrce-dds": 8888,
}

def usage() -> None:
    print(
        "Usage:\n"
        "  super-client.py <service> <ip> <port|0> <count> <interval_s> <total_time_s>\n\n"
        "Example:\n"
        "  docker run --rm image:latest web 172.17.0.2 443 10 1 15\n",
        file=sys.stderr,
    )

def main() -> int:
    if len(sys.argv) != 7:
        usage()
        return 2

    service = _strip_commas(sys.argv[1]).lower()
    ip = _strip_commas(sys.argv[2])
    port = _to_int(sys.argv[3], "port")
    count = _to_int(sys.argv[4], "count")
    interval_s = _to_float(sys.argv[5], "interval_s")
    total_s = _to_int(sys.argv[6], "total_time_s")

    if service not in SERVICE_MAP:
        print(f"Unknown service: {service!r}", file=sys.stderr)
        print("Supported services:", ", ".join(sorted(set(SERVICE_MAP.keys()))), file=sys.stderr)
        return 2

    if port == 0:
        port = DEFAULT_PORTS.get(service, 0)
        if port == 0:
            print("Port=0 but there is no known default port for this service.", file=sys.stderr)
            return 2

    if count < 1 or total_s < 1:
        print("count and total_time_s must be >= 1", file=sys.stderr)
        return 2

    interval_s = max(0, interval_s)

    fn = SERVICE_MAP[service]
    start = time.monotonic()
    deadline = start + float(total_s)

    print(f"[benign] service={service} target={ip}:{port} count={count} interval={interval_s}s total={total_s}s timeout_per_try={PER_TRY_TIMEOUT_S}s")

    done = 0
    ok_n = 0

    for i in range(1, count + 1):
        now = time.monotonic()
        if now >= deadline:
            break

        ok, info = fn(ip, port)
        done += 1
        ok_n += 1 if ok else 0

        elapsed = time.monotonic() - start
        print(f"[{i:03d}] ok={int(ok)} info={info} elapsed={elapsed:.2f}s")

        if interval_s > 0:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(float(interval_s), remaining))

    print(f"[benign] finished attempts={done}/{count} ok={ok_n} elapsed={time.monotonic()-start:.2f}s")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
