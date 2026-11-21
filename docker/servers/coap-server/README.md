# Server "CoAP Server"

> Serve as a target for CoAP GET requests, resource discovery, fuzzing, and token collisions.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `coap-server` |
| Role | target-server |
| Image | `server-coap-server:latest` |
| Container | `server-coap-server` |
| Base | `python:3.11-alpine` |
| Service | Python CoAP server based on CoAPServer |
| Protocols | `coap` |
| Internal ports | `5683/tcp`, `5683/udp` |
| Published ports | `5683:5683/tcp`, `5683:5683/udp` |

## Execution

```bash
docker run -d --restart on-failure --name server-coap-server -p 5683:5683 -p 5683:5683/udp server-coap-server:latest
```

## Container IP

```bash
docker container inspect server-coap-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-coap-server
```

## Related Attacks

- `iot_coap_get_flood`
- `iot_coap_resource_exhaustion`
- `iot_coap_response_fuzz`
- `iot_coap_token_collision`

## Related Benign Clients

- `client-random:coap`
- `client-super:coap`

## Testbed Observability

- CoAP UDP/TCP traffic
- server stdout logs
- responses to /.well-known/core

In controlled experiments, use `python3 attackzoo.py experiment --server server-coap-server` to associate target-container telemetry with execution artifacts.
