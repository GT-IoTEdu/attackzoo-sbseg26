# Docker Containers

This directory contains the Docker assets used by AttackZoo to build target servers, benign clients, and attack containers for controlled experiments.

## Directory Layout

- `attackers/`: attack container definitions. Each subdirectory includes an `attack.yaml`, a `README.md`, and the container implementation files.
- `servers/`: target server definitions. Each subdirectory includes a `server.yaml`, a `README.md`, and the files needed to build or run the service.
- `clients/`: benign client definitions. Each subdirectory includes a `client.yaml`, a `README.md`, and the traffic generator implementation.

## Build All Images

From this `docker/` directory:

```bash
chmod +x build-images.sh
./build-images.sh
```

The script builds all server, attacker, and client images. It also starts the standard target servers and a Dozzle container for log monitoring.

## Attack Catalog

| Directory | ID | Image | Description |
|---|---|---|---|
| [`attackers/arp-scan/`](attackers/arp-scan/) | `recon_arp_scan` | `attack-arp-scan:latest` | Host enumeration through ARP on the target network. |
| [`attackers/arp-spoof/`](attackers/arp-spoof/) | `net_arp_spoof` | `attack-arp-spoof:latest` | Network gateway interception attack through ARP spoofing. |
| [`attackers/cdp-table-flood/`](attackers/cdp-table-flood/) | `net_cdp_table_flood` | `attack-cdp-table-flood:latest` | CDP (Cisco Discovery Protocol) table flood on the local network. |
| [`attackers/coap-get-flood/`](attackers/coap-get-flood/) | `iot_coap_get_flood` | `attack-coap-get-flood:latest` | Burst of CoAP GET requests against the target CoAP/IoT service to overload the application layer. |
| [`attackers/coap-resource-exhaustion/`](attackers/coap-resource-exhaustion/) | `iot_coap_resource_exhaustion` | `attack-coap-resource-exhaustion:latest` | Burst of CoAP resource discovery/mapping messages, typically against /.well-known/core, intended to exhaust target resources. |
| [`attackers/coap-response-fuzz/`](attackers/coap-response-fuzz/) | `iot_coap_response_fuzz` | `attack-coap-response-fuzz:latest` | Burst of randomized or mutated CoAP messages intended to trigger errors, exceptions, or crashes on the target. |
| [`attackers/coap-token-collision/`](attackers/coap-token-collision/) | `iot_coap_token_collision` | `attack-coap-token-collision:latest` | Burst of CoAP messages that forces token reuse or collisions to degrade target state tracking and transaction correlation. |
| [`attackers/dhcp-starvation/`](attackers/dhcp-starvation/) | `net_dhcp_starvation` | `attack-dhcp-starvation:latest` | DHCP lease exhaustion on the local network. |
| [`attackers/dns-tunneling/`](attackers/dns-tunneling/) | `exf_dns_tunneling` | `attack-dns-tunneling:latest` | DNS tunneling exfiltration behavior through random domain name resolution. |
| [`attackers/dos-http-simple/`](attackers/dos-http-simple/) | `dos_http_simple` | `attack-dos-http-simple:latest` | Simple HTTP application DoS. |
| [`attackers/dos-http-slowloris/`](attackers/dos-http-slowloris/) | `dos_http_slowloris` | `attack-dos-http-slowloris:latest` | Slowloris-style HTTP application DoS. |
| [`attackers/fin-flood/`](attackers/fin-flood/) | `dos_fin_flood` | `attack-fin-flood:latest` | TCP packet flood with the FIN flag set. |
| [`attackers/icmp-flood/`](attackers/icmp-flood/) | `dos_icmp_flood` | `attack-icmp-flood:latest` | ICMP packet flood. |
| [`attackers/icmp-tunnel/`](attackers/icmp-tunnel/) | `exf_icmp_tunnel` | `attack-icmp-tunnel:latest` | TCP port 22 (SSH) tunnel over ICMP (pings). |
| [`attackers/idor-path-traversal/`](attackers/idor-path-traversal/) | `web_idor_path_traversal` | `attack-idor-path-traversal:latest` | Attempts to access local files through the web server using a wordlist. |
| [`attackers/idor-url-parameter/`](attackers/idor-url-parameter/) | `web_idor_url_parameter` | `attack-idor-url-parameter:latest` | Attempts to access resources through URL parameter manipulation using a wordlist. |
| [`attackers/ipv6-mld-flood/`](attackers/ipv6-mld-flood/) | `net_ipv6_mld_flood` | `attack-ipv6-mld-flood:latest` | ICMPv6 Multicast Listener Report MLD (131) flood on the local network. |
| [`attackers/ipv6-ns-flood/`](attackers/ipv6-ns-flood/) | `net_ipv6_ns_flood` | `attack-ipv6-ns-flood:latest` | ICMPv6 Neighbor Solicitation NS (135) flood on the local network. |
| [`attackers/ipv6-ra-flood/`](attackers/ipv6-ra-flood/) | `net_ipv6_ra_flood` | `attack-ipv6-ra-flood:latest` | ICMPv6 Router Advertisement RA (134) flood on the local network. |
| [`attackers/mqtt-bruteforce/`](attackers/mqtt-bruteforce/) | `iot_mqtt_bruteforce` | `attack-mqtt-bruteforce:latest` | MQTT authentication brute force against the target broker using a controlled wordlist. |
| [`attackers/mqtt-lwt-abuse/`](attackers/mqtt-lwt-abuse/) | `iot_mqtt_lwt_abuse` | `attack-mqtt-lwt-abuse:latest` | Abuse of the MQTT Last Will and Testament mechanism to force critical publications or false alarms on sensitive topics. |
| [`attackers/mqtt-publisher-flood/`](attackers/mqtt-publisher-flood/) | `iot_mqtt_publisher` | `attack-mqtt-publisher:latest` | MQTT publish flood to evaluate broker availability and behavior under load. |
| [`attackers/mqtt-qos-amplification/`](attackers/mqtt-qos-amplification/) | `iot_mqtt_qos_amplification` | `attack-mqtt-qos-amplification:latest` | Traffic and state-load amplification on the MQTT broker through multiple QoS 2 handshakes. |
| [`attackers/php-lfi-enumeration/`](attackers/php-lfi-enumeration/) | `php_lfi_enumeration` | `attack-php-lfi-enumeration:latest` | Controlled enumeration of Local File Inclusion (LFI) vectors in a vulnerable PHP application. |
| [`attackers/ping-sweep/`](attackers/ping-sweep/) | `recon_ping_sweep` | `attack-ping-sweep:latest` | ICMP sweep for host discovery. |
| [`attackers/port-scanner-aggressive/`](attackers/port-scanner-aggressive/) | `recon_port_scanner_aggressive` | `attack-port-scanner-aggressive:latest` | Aggressive-profile port and service scan. |
| [`attackers/port-scanner-os/`](attackers/port-scanner-os/) | `recon_port_scanner_os` | `attack-port-scanner-os:latest` | Target operating system detection (fingerprinting). |
| [`attackers/port-scanner-tcp/`](attackers/port-scanner-tcp/) | `recon_port_scanner_tcp` | `attack-port-scanner-tcp:latest` | TCP port scan of the target. |
| [`attackers/port-scanner-udp/`](attackers/port-scanner-udp/) | `recon_port_scanner_udp` | `attack-port-scanner-udp:latest` | UDP port scan of the target. |
| [`attackers/port-scanner-vulnerabilities/`](attackers/port-scanner-vulnerabilities/) | `recon_port_scanner_vuln` | `attack-port-scanner-vulnerabilities:latest` | Port scan and known-vulnerability checks. |
| [`attackers/psh-flood/`](attackers/psh-flood/) | `dos_psh_flood` | `attack-psh-flood:latest` | TCP packet flood with the PSH flag set. |
| [`attackers/rst-flood/`](attackers/rst-flood/) | `dos_rst_flood` | `attack-rst-flood:latest` | TCP packet flood with the RST flag set. |
| [`attackers/smb-enumerating/`](attackers/smb-enumerating/) | `recon_smb_enum` | `attack-smb-enumerating:latest` | Enumeration of SMB share directories and vulnerabilities. |
| [`attackers/snmp-scanner/`](attackers/snmp-scanner/) | `recon_snmp_scanner` | `attack-snmp-scanner:latest` | SNMP scan across all hosts in a network using a community-string wordlist. |
| [`attackers/sql-injection/`](attackers/sql-injection/) | `web_sql_injection` | `attack-sql-injection:latest` | SQL injection exploitation tests. |
| [`attackers/ssh-bruteforce/`](attackers/ssh-bruteforce/) | `bf_ssh` | `attack-ssh-bruteforce:latest` | SSH authentication brute force. |
| [`attackers/stp-conf-flood/`](attackers/stp-conf-flood/) | `net_stp_conf_flood` | `attack-stp-conf-flood:latest` | BPDU (Bridge Protocol Data Unit) packet flood with STP topology reconfiguration information and random MAC addresses. |
| [`attackers/stp-tcn-flood/`](attackers/stp-tcn-flood/) | `net_stp_tcn_flood` | `attack-stp-tcn-flood:latest` | BPDU (Bridge Protocol Data Unit) packet flood with STP topology change information and random MAC addresses. |
| [`attackers/syn-flood/`](attackers/syn-flood/) | `dos_syn_flood` | `attack-syn-flood:latest` | TCP packet flood with the SYN flag set. |
| [`attackers/telnet-bruteforce/`](attackers/telnet-bruteforce/) | `bf_telnet` | `attack-telnet-bruteforce:latest` | Telnet authentication brute force. |
| [`attackers/udp-flood/`](attackers/udp-flood/) | `dos_udp_flood` | `attack-udp-flood:latest` | UDP packet flood. |
| [`attackers/web-dir-enumeration/`](attackers/web-dir-enumeration/) | `web_dir_enumeration` | `attack-web-dir-enumeration:latest` | Web server subdirectory and resource enumeration using a wordlist. |
| [`attackers/web-https-heartbleed/`](attackers/web-https-heartbleed/) | `web_https_heartbleed` | `attack-web-https-heartbleed:latest` | Heartbleed scanner/exploitation against a vulnerable HTTPS server. |
| [`attackers/web-post-bruteforce/`](attackers/web-post-bruteforce/) | `web_post_bruteforce` | `attack-web-post-bruteforce:latest` | Web application POST authentication brute force using a wordlist. |
| [`attackers/web-simple-scanner/`](attackers/web-simple-scanner/) | `web_simple_scanner` | `attack-web-simple-scanner:latest` | Simplified scanner for known web vulnerabilities. |
| [`attackers/web-wide-scanner/`](attackers/web-wide-scanner/) | `web_wide_scanner` | `attack-web-wide-scanner:latest` | Broad scanner for known web vulnerabilities. |
| [`attackers/xrce-dds-discovery-poison/`](attackers/xrce-dds-discovery-poison/) | `iot_xrce_dds_discovery_poison` | `attack-xrce-dds-discovery-poison:latest` | Poisoning or manipulation of XRCE-DDS agent discovery messages to induce incorrect association, redirection, or discovery degradation. |
| [`attackers/xrce-dds-entity-flood/`](attackers/xrce-dds-entity-flood/) | `iot_xrce_dds_entity_flood` | `attack-xrce-dds-entity-flood:latest` | Mass creation of XRCE-DDS entities to consume session, memory, and control resources on the agent. |
| [`attackers/xrce-dds-fragment-abuse/`](attackers/xrce-dds-fragment-abuse/) | `iot_xrce_dds_fragment_abuse` | `attack-xrce-dds-fragment-abuse:latest` | Fragmented, incomplete, or overlapping XRCE-DDS publications that stress reassembly, queues, and fragment handling on the agent. |
| [`attackers/xrce-dds-malformed-inject/`](attackers/xrce-dds-malformed-inject/) | `iot_xrce_dds_malformed_inject` | `attack-xrce-dds-malformed-inject:latest` | Injection of malformed XRCE-DDS publications or messages against the agent to trigger errors, exceptions, or crashes. |
| [`attackers/xrce-dds-session-hijack/`](attackers/xrce-dds-session-hijack/) | `iot_xrce_dds_session_hijack` | `attack-xrce-dds-session-hijack:latest` | XRCE-DDS session hijacking or collision attempts through manipulation of identifiers, keys, or session fields. |
| [`attackers/xrce-dds-time-desync/`](attackers/xrce-dds-time-desync/) | `iot_xrce_dds_time_desync` | `attack-xrce-dds-time-desync:latest` | Manipulation of XRCE-DDS messages and time-related fields to induce logical desynchronization between client and agent. |
| [`attackers/xrce-dds-udp-dos/`](attackers/xrce-dds-udp-dos/) | `iot_xrce_dds_udp_dos` | `attack-xrce-dds-udp-dos:latest` | UDP packet flood against the XRCE-DDS agent to degrade network or service availability. |
| [`attackers/xss-scanner/`](attackers/xss-scanner/) | `web_xss_scanner` | `attack-xss-scanner:latest` | Automated scan and analysis of parameter flaws susceptible to XSS. |
| [`attackers/zenoh-pico-fragments-reassembly/`](attackers/zenoh-pico-fragments-reassembly/) | `iot_zenoh_pico_fragments_reassembly` | `attack-zenoh-pico-fragments-reassembly:latest` | Flood of incomplete Zenoh/Zenoh-Pico fragments to stress router or peer buffers and reassembly logic. |
| [`attackers/zenoh-pico-keepalive-flood/`](attackers/zenoh-pico-keepalive-flood/) | `iot_zenoh_pico_keepalive_flood` | `attack-zenoh-pico-keepalive-flood:latest` | Flood of Zenoh/Zenoh-Pico keepalive messages to consume processing and session-handling capacity. |
| [`attackers/zenoh-pico-memory-exhaustion/`](attackers/zenoh-pico-memory-exhaustion/) | `iot_zenoh_pico_memory_exhaustion` | `attack-zenoh-pico-memory-exhaustion:latest` | Memory exhaustion of the Zenoh router/peer through mass creation of resources, sessions, declarations, or pending messages. |
| [`attackers/zenoh-pico-proto-fuzzer/`](attackers/zenoh-pico-proto-fuzzer/) | `iot_zenoh_pico_proto_fuzzer` | `attack-zenoh-pico-proto-fuzzer:latest` | Sending malformed or mutated Zenoh/Zenoh-Pico messages to trigger errors, exceptions, or crashes on the target. |
| [`attackers/zenoh-pico-sequence-exhaustion/`](attackers/zenoh-pico-sequence-exhaustion/) | `iot_zenoh_pico_sequence_exhaustion` | `attack-zenoh-pico-sequence-exhaustion:latest` | Exhaustion or intensive manipulation of Zenoh/Zenoh-Pico sequence numbers to degrade ordering, reliability, or session-state control. |
| [`attackers/zenoh-pico-timestamp-mess/`](attackers/zenoh-pico-timestamp-mess/) | `iot_zenoh_pico_timestamp_mess` | `attack-zenoh-pico-timestamp-mess:latest` | Flood of Zenoh/Zenoh-Pico packets with manipulated timestamps to affect target ordering, expiration, or time logic. |

## Target Servers

| Directory | ID | Image | Purpose |
|---|---|---|---|
| [`servers/cdp-listener/`](servers/cdp-listener/) | `cdp-listener` | `server-cdp-listener:latest` | Keep a CDP neighbor table on the local network, the victim of CDP table flooding. |
| [`servers/coap-server/`](servers/coap-server/) | `coap-server` | `server-coap-server:latest` | Serve as a target for CoAP GET requests, resource discovery, fuzzing, and token collisions. |
| [`servers/dhcp-server/`](servers/dhcp-server/) | `dhcp-server` | `server-dhcp-server:latest` | Serve as the DHCP server of the local network, the victim of DHCP starvation. |
| [`servers/http-server/`](servers/http-server/) | `http-server` | `server-http-server:latest` | Provide a vulnerable web application for web attacks, scanners, enumeration, and controlled HTTP DoS. |
| [`servers/mqtt-broker/`](servers/mqtt-broker/) | `mqtt-broker` | `server-mqtt-broker:latest` | Act as an MQTT broker for publishing, brute force, LWT abuse, and QoS amplification in IoT experiments. |
| [`servers/smb-server/`](servers/smb-server/) | `smb-server` | `server-smb-server:latest` | Provide an SMB/Samba share for enumeration and benign share-listing traffic. |
| [`servers/ssh-server/`](servers/ssh-server/) | `ssh-server` | `server-ssh-server:latest` | Serve as a target for SSH brute force and ICMP/SSH tunneling in controlled experiments. |
| [`servers/ssl-heartbleed/`](servers/ssl-heartbleed/) | `ssl-heartbleed` | `server-ssl-heartbleed:latest` | Provide a vulnerable HTTPS target for Heartbleed attack validation and observable TLS traffic generation. |
| [`servers/telnet-server/`](servers/telnet-server/) | `telnet-server` | `server-telnet-server:latest` | Serve as a target for Telnet brute force and simple benign login traffic. |
| [`servers/xrce-dds-agent/`](servers/xrce-dds-agent/) | `xrce-dds-agent` | `server-xrce-dds-agent:latest` | Serve as an XRCE-DDS agent for IoT attacks involving discovery, entities, fragments, sessions, timing, and UDP DoS. |
| [`servers/zenoh-router/`](servers/zenoh-router/) | `zenoh-router` | `server-zenoh-router:latest` | Serve as a Zenoh router for Zenoh-Pico attacks against fragmentation, keepalive, memory, fuzzing, sequence, and timestamp behavior. |

## Benign Clients

| Directory | ID | Image | Purpose |
|---|---|---|---|
| [`clients/client-random/`](clients/client-random/) | `client-random` | `client-random:latest` | Generate continuous benign noise during experiments by randomly choosing among supported protocol clients. |
| [`clients/client-super/`](clients/client-super/) | `client-super` | `client-super:latest` | Generate controlled benign traffic with count, interval, and duration defined by parameters. |
| [`clients/client-xrce-dds/`](clients/client-xrce-dds/) | `client-xrce-dds` | `client-xrce-dds:latest` | Generate legitimate XRCE-DDS traffic (session, entity creation, reliable writes) that the XRCE-DDS attacks can act on. Built and started on demand, not by `build-images.sh` or `clients.sh`. |

From the repository root, use `clients.sh` to control client containers:

```bash
./clients.sh start all
./clients.sh restart random
./clients.sh stop super
CLIENT_SUPER_SERVICE=coap ./clients.sh start super
```

## Running Individual Attacks

Prefer the project CLI when possible because it keeps the run tied to the declarative catalog:

```bash
python3 attackzoo.py run <ATTACK_ID> --target <TARGET>
```

Each attacker subdirectory README also includes a direct `docker run` example for isolated validation.

## Inspecting Target Servers

Use Docker directly to inspect target server IP addresses and logs:

```bash
docker container inspect server-http-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
docker logs server-mqtt-broker
```

For controlled experiments, prefer:

```bash
python3 attackzoo.py experiment
```

Expected artifacts include PCAP files, probe CSVs, optional telemetry, generated features, datasets, and reports under `experiments/`.

## Cleanup

Containers created by this directory use the catalog names declared in the YAML files, such as `server-*`, `attack-*`, and `client-*`.

```bash
docker ps -a --format "{{.Names}}" | grep -E '^(server|attack|client)-' | xargs -r docker rm -f
```
