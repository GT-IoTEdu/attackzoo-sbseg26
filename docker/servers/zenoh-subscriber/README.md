# Server "Zenoh Subscriber"

> Subscribe to `attackzoo/**` on the Zenoh router, so that the router forwards published samples to a receiver whose timestamps and order can be observed.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `zenoh-subscriber` |
| Role | target-server |
| Image | `server-zenoh-subscriber:latest` |
| Container | `server-zenoh-subscriber` |
| Base | `python:3.11-slim` |
| Service | Eclipse Zenoh 1.7.2 subscriber (zenoh-python client) |
| Protocols | `zenoh`, `tcp` |
| Internal ports | none (it connects to the router) |
| Published ports | none |

## Parameters

`<router_ip> [port] [key_expr]`: router address (required), router port (default `7447`), key expression
(default `attackzoo/**`).

With the default `attackzoo/**`, the router also forwards the samples of `iot_zenoh_pico_memory_exhaustion`
(`attackzoo/memory-exhaustion`, about 64 KB each) to this subscriber, which roughly doubles that attack's traffic on
TCP/7447. To receive only the timestamp attack, pass `attackzoo/timestamp-mess` as the key expression.

Each received sample prints one line: receive order, receive time (UNIX seconds), sample kind, key, sample
timestamp as NTP64 and as RFC 3339 followed by `/` and the timestamp id, payload size in bytes. On `docker stop`
it prints the number of samples received.

## Execution

Build from `docker/`:

```bash
docker build -t server-zenoh-subscriber -f servers/zenoh-subscriber/Dockerfile .
```

Start it on demand (it is not started by `servers.sh` or `build-images.sh`), after `server-zenoh-router`:

```bash
ROUTER_IP=$(docker container inspect server-zenoh-router --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
docker run -d --rm --name server-zenoh-subscriber server-zenoh-subscriber:latest "$ROUTER_IP"
```

## Container IP

```bash
docker container inspect server-zenoh-subscriber --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-zenoh-subscriber
```

## Related Attacks

- `iot_zenoh_pico_timestamp_mess`: the router checks and forwards the attack samples, with their timestamps, only
  when someone subscribes to their key (`attackzoo/timestamp-mess`).

## Related Benign Clients

- none

## Testbed Observability

- one stdout line per received sample
- Zenoh TCP/7447 session with the router
- while idle, one KEEP_ALIVE each way every 2.5 s (Zenoh lease 10 s, 4 keep-alives per lease)

## Notes

- Not started by servers.sh or build-images.sh; start it on demand, after server-zenoh-router.
- While idle it keeps one Zenoh session with the router, with one KEEP_ALIVE each way every 2.5 s.

In controlled experiments, use `python3 attackzoo.py experiment --server server-zenoh-subscriber` to associate target-container telemetry with execution artifacts.
