# Server "DHCP Server"

> Serve as the DHCP server of the local network, the victim of DHCP starvation.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `dhcp-server` |
| Role | target-server |
| Image | `server-dhcp-server:latest` |
| Container | `server-dhcp-server` |
| Base | `ubuntu:24.04` |
| Service | busybox udhcpd serving a 10-address pool on the container network |
| Protocols | `dhcp` |
| Internal ports | `67/udp` |
| Published ports | none (layer 2 only) |

## Execution

```bash
docker run -d --rm --name server-dhcp-server server-dhcp-server:latest
```

The pool is `.240`-`.249` of the container's own /24 block (on docker0, `172.17.0.240`-`172.17.0.249`).
Set `POOL_START` and `POOL_END` to change it. udhcpd reserves an address for 60 s (`offer_time`) on each
OFFER, so a DISCOVER flood with random client MACs exhausts the pool.

## Container IP

```bash
docker container inspect server-dhcp-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-dhcp-server
```

A legitimate client check (the lease is only requested, no address is configured):

```bash
docker run --rm busybox udhcpc -i eth0 -f -n -q -s /bin/true -t 3 -T 2
```

## Related Attacks

- `net_dhcp_starvation`

## Related Benign Clients

- none

## Testbed Observability

- DHCP DISCOVER/OFFER/ACK traffic in PCAP
- OFFER and "no free IP addresses" messages on stdout
- a client that gets (or does not get) a lease

Do not send SIGUSR1 to udhcpd during an attack window to dump leases: it restarts udhcpd's 2 s ARP check of each
address and delays its OFFERs.

## Notes

- No published port; DHCP works only on the layer-2 segment of the container (docker0).
- The pool is .240-.249 of the container's /24 block; override with POOL_START and POOL_END.

In controlled experiments, use `python3 attackzoo.py experiment --server server-dhcp-server` to associate target-container telemetry with execution artifacts.
