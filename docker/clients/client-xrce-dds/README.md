# XRCE-DDS Client

> Generate legitimate XRCE-DDS traffic (session, entity creation, reliable writes) that the XRCE-DDS attacks can act on.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `client-xrce-dds` |
| Role | benign-client |
| Image | `client-xrce-dds:latest` |
| Container pattern | `client-xrce-dds-<N>` |
| Base | `ubuntu:24.04` |
| Entrypoint | `/usr/local/bin/xrce-client` |
| Protocols | `xrce-dds`, `udp` |

## Parameters

| Mode | Arguments |
|---|---|
| `publish` | `<agent_ip> <agent_port> <count> <interval_ms>` |
| `discover` | `<attempts> <period_ms> <count> <interval_ms>` |

- `publish` opens a session on the given agent and writes `count` HelloWorld samples, one every `interval_ms`.
- `discover` sends XRCE GET_INFO to `239.255.0.2:7400` (`attempts` times, `period_ms` apart), keeps the first
  advertised agent on which a session opens (as micro-ROS does), then publishes like `publish`. The agent answers
  discovery only when started with `-d 7400`.
- `count 0` publishes until the container stops or the session is lost.
- Session key `0xAAAABBBB`, topic `HelloWorldTopic`, type `HelloWorld`: the same as the `PublishHelloWorld`
  example of Micro-XRCE-DDS-Client.
- Exit code: `0` all samples written, `1` no agent or no session, `2` usage, `3` session lost.

## Execution

Build from `docker/`:

```bash
docker build -t client-xrce-dds -f clients/client-xrce-dds/Dockerfile .
```

Start it on demand (it is not built by `build-images.sh` nor started by `clients.sh`):

```bash
AGENT_IP=$(docker container inspect server-xrce-dds-agent --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
docker run -d --rm --name client-xrce-dds-1 client-xrce-dds:latest publish "$AGENT_IP" 8888 0 1000
docker run -d --rm --name client-xrce-dds-2 client-xrce-dds:latest discover 10 1000 0 1000
docker rm -f client-xrce-dds-1 client-xrce-dds-2
```

## Typical Target Services

- `xrce-dds-agent`: Micro XRCE-DDS Agent

## Related Attacks

- `iot_xrce_dds_session_hijack`: its first key, `0xAAAABBBB`, is the key of this client.
- `iot_xrce_dds_discovery_poison`: answers the GET_INFO of `discover`.

## Testbed Observability

- stdout with the discovered agents, the session, each write id, and a lost session
- XRCE-DDS/UDP datagrams in PCAP

## Notes

- Same session key (0xAAAABBBB), topic (HelloWorldTopic) and type (HelloWorld) as the PublishHelloWorld example of Micro-XRCE-DDS-Client.
- count 0 publishes until the container stops or the session is lost; exit code 3 means the session was lost.
- discover sends GET_INFO to 239.255.0.2:7400 and keeps the first agent on which a session opens; the agent answers discovery only when started with -d 7400.
- Not built by build-images.sh nor started by clients.sh; build and start it on demand.

Use this client to generate benign XRCE-DDS traffic before, during, or after the attack window in controlled experiments. Container logs report each write and help correlate benign traffic with captured PCAP files.
