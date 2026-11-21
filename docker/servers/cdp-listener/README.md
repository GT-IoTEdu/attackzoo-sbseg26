# Server "CDP Listener"

> Keep a CDP neighbor table on the local network, the victim of CDP table flooding.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `cdp-listener` |
| Role | target-server |
| Image | `server-cdp-listener:latest` |
| Container | `server-cdp-listener` |
| Base | `ubuntu:24.04` |
| Service | lldpd in receive-only mode with CDP enabled, keeping a CDP neighbor table for eth0 |
| Protocols | `cdp` |
| Internal ports | none |
| Published ports | none (layer 2 only) |

## Execution

```bash
docker run -d --rm --name server-cdp-listener server-cdp-listener:latest
```

lldpd runs receive-only (`-r`), so it sends no LLDP or CDP frames. It keeps at most 32 neighbors per port and
protocol; a CDP flood with random device IDs fills the table, and new neighbors are dropped until the entries
expire (TTL of the received frame).

## Container IP

```bash
docker container inspect server-cdp-listener --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-cdp-listener
docker exec server-cdp-listener lldpcli show neighbors summary
docker exec server-cdp-listener lldpcli show statistics
```

## Related Attacks

- `net_cdp_table_flood`

## Related Benign Clients

- none

## Testbed Observability

- CDP frames in PCAP
- neighbor table and counters through `lldpcli`

## Notes

- Receive-only (lldpd -r); it sends no LLDP or CDP frames.
- lldpd keeps at most 32 neighbors per port and protocol (max-neighbors); CDP entries expire after the TTL in the frame.

In controlled experiments, use `python3 attackzoo.py experiment --server server-cdp-listener` to associate target-container telemetry with execution artifacts.
