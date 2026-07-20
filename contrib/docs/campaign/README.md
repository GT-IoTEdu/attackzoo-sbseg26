# Campaign `all_5runs_4levels`

This folder documents the published full campaign `all_5runs_4levels` in one file per attack. The full `experiments/all_5runs_4levels` directory is not versioned in Git because of its size; retrieve and validate the generated dataset CSVs from the Figshare dataset below with `ATTACKZOO_CLAIM3_MODE=figshare bash run_claim3.sh` from the repository root. The Figshare archive does not contain raw PCAP captures. The per-attack pages summarize the published campaign, and the selected figures are copied under `contrib/assets/campaign_doc`.

- Documented attacks: **60**
- Raw PCAP captures in the Figshare archive: **0**
- Original full-campaign captures before dataset packaging: **1200**
- Original capture volume before dataset packaging: **672.1 GB**
- Resulting datasets: **225.4 GB**
- [High-compressed single-file](https://doi.org/10.6084/m9.figshare.33023765) : **16.9 GB**

>[!IMPORTANT]
>[https://doi.org/10.6084/m9.figshare.33023765](https://doi.org/10.6084/m9.figshare.33023765)

## Documents

| Attack | ID | Summary | Copied figures | Aggregated tables |
| --- | --- | --- | --- | --- |
| [SSH Bruteforce](bf_ssh.md) | `bf_ssh` | yes | 8 | yes |
| [Telnet Bruteforce](bf_telnet.md) | `bf_telnet` | yes | 8 | yes |
| [FIN Flood](dos_fin_flood.md) | `dos_fin_flood` | yes | 8 | yes |
| [DoS HTTP Simple](dos_http_simple.md) | `dos_http_simple` | yes | 8 | yes |
| [DoS HTTP Slowloris](dos_http_slowloris.md) | `dos_http_slowloris` | yes | 8 | yes |
| [ICMP Flood](dos_icmp_flood.md) | `dos_icmp_flood` | yes | 8 | yes |
| [PSH Flood](dos_psh_flood.md) | `dos_psh_flood` | yes | 8 | yes |
| [RST Flood](dos_rst_flood.md) | `dos_rst_flood` | yes | 8 | yes |
| [SYN Flood](dos_syn_flood.md) | `dos_syn_flood` | yes | 8 | yes |
| [UDP Flood](dos_udp_flood.md) | `dos_udp_flood` | yes | 8 | yes |
| [DNS Tunneling](exf_dns_tunneling.md) | `exf_dns_tunneling` | yes | 8 | yes |
| [ICMP Tunnel](exf_icmp_tunnel.md) | `exf_icmp_tunnel` | yes | 8 | yes |
| [CoAP GET Flood](iot_coap_get_flood.md) | `iot_coap_get_flood` | yes | 8 | yes |
| [CoAP Resource Discovery Exhaustion](iot_coap_resource_exhaustion.md) | `iot_coap_resource_exhaustion` | yes | 8 | yes |
| [CoAP Response Fuzzing](iot_coap_response_fuzz.md) | `iot_coap_response_fuzz` | yes | 8 | yes |
| [CoAP Token Collision](iot_coap_token_collision.md) | `iot_coap_token_collision` | yes | 8 | yes |
| [MQTT Bruteforce](iot_mqtt_bruteforce.md) | `iot_mqtt_bruteforce` | yes | 8 | yes |
| [MQTT LWT Abuse](iot_mqtt_lwt_abuse.md) | `iot_mqtt_lwt_abuse` | yes | 8 | yes |
| [MQTT Publisher Flood](iot_mqtt_publisher.md) | `iot_mqtt_publisher` | yes | 8 | yes |
| [MQTT QoS 2 Amplification](iot_mqtt_qos_amplification.md) | `iot_mqtt_qos_amplification` | yes | 8 | yes |
| [XRCE-DDS Discovery Poisoning](iot_xrce_dds_discovery_poison.md) | `iot_xrce_dds_discovery_poison` | yes | 8 | yes |
| [XRCE-DDS Entity Flood](iot_xrce_dds_entity_flood.md) | `iot_xrce_dds_entity_flood` | yes | 8 | yes |
| [XRCE-DDS Fragment Abuse](iot_xrce_dds_fragment_abuse.md) | `iot_xrce_dds_fragment_abuse` | yes | 8 | yes |
| [XRCE-DDS Malformed Injection](iot_xrce_dds_malformed_inject.md) | `iot_xrce_dds_malformed_inject` | yes | 8 | yes |
| [XRCE-DDS Session Hijack](iot_xrce_dds_session_hijack.md) | `iot_xrce_dds_session_hijack` | yes | 8 | yes |
| [XRCE-DDS Time Desynchronization](iot_xrce_dds_time_desync.md) | `iot_xrce_dds_time_desync` | yes | 8 | yes |
| [XRCE-DDS UDP DoS](iot_xrce_dds_udp_dos.md) | `iot_xrce_dds_udp_dos` | yes | 8 | yes |
| [Zenoh-Pico Fragment Reassembly Flood](iot_zenoh_pico_fragments_reassembly.md) | `iot_zenoh_pico_fragments_reassembly` | yes | 8 | yes |
| [Zenoh-Pico Keepalive Flood](iot_zenoh_pico_keepalive_flood.md) | `iot_zenoh_pico_keepalive_flood` | yes | 8 | yes |
| [Zenoh-Pico Memory Exhaustion](iot_zenoh_pico_memory_exhaustion.md) | `iot_zenoh_pico_memory_exhaustion` | yes | 8 | yes |
| [Zenoh-Pico Protocol Fuzzer](iot_zenoh_pico_proto_fuzzer.md) | `iot_zenoh_pico_proto_fuzzer` | yes | 8 | yes |
| [Zenoh-Pico Sequence Exhaustion](iot_zenoh_pico_sequence_exhaustion.md) | `iot_zenoh_pico_sequence_exhaustion` | yes | 8 | yes |
| [Zenoh-Pico Timestamp Manipulation Flood](iot_zenoh_pico_timestamp_mess.md) | `iot_zenoh_pico_timestamp_mess` | yes | 8 | yes |
| [ARP Spoof](net_arp_spoof.md) | `net_arp_spoof` | yes | 8 | yes |
| [CDP Table Flood](net_cdp_table_flood.md) | `net_cdp_table_flood` | yes | 0 | no |
| [DHCP Starvation](net_dhcp_starvation.md) | `net_dhcp_starvation` | yes | 0 | no |
| [IPv6 MLD Flood](net_ipv6_mld_flood.md) | `net_ipv6_mld_flood` | yes | 0 | no |
| [IPv6 NS Flood](net_ipv6_ns_flood.md) | `net_ipv6_ns_flood` | yes | 8 | yes |
| [IPv6 RA Flood](net_ipv6_ra_flood.md) | `net_ipv6_ra_flood` | yes | 8 | yes |
| [STP Config Flood](net_stp_conf_flood.md) | `net_stp_conf_flood` | yes | 8 | yes |
| [STP TCN Flood](net_stp_tcn_flood.md) | `net_stp_tcn_flood` | yes | 0 | no |
| [PHP LFI Enumeration](php_lfi_enumeration.md) | `php_lfi_enumeration` | yes | 8 | yes |
| [ARP Scan](recon_arp_scan.md) | `recon_arp_scan` | yes | 8 | yes |
| [Ping Sweep](recon_ping_sweep.md) | `recon_ping_sweep` | yes | 8 | yes |
| [Port Scanner Aggressive](recon_port_scanner_aggressive.md) | `recon_port_scanner_aggressive` | yes | 8 | yes |
| [Port Scanner OS](recon_port_scanner_os.md) | `recon_port_scanner_os` | yes | 8 | yes |
| [Port Scanner TCP](recon_port_scanner_tcp.md) | `recon_port_scanner_tcp` | yes | 8 | yes |
| [Port Scanner UDP](recon_port_scanner_udp.md) | `recon_port_scanner_udp` | yes | 8 | yes |
| [Port Scanner Vulnerabilities](recon_port_scanner_vuln.md) | `recon_port_scanner_vuln` | yes | 8 | yes |
| [SMB Enumerating](recon_smb_enum.md) | `recon_smb_enum` | yes | 8 | yes |
| [SNMP Scanner](recon_snmp_scanner.md) | `recon_snmp_scanner` | yes | 8 | yes |
| [Web Directory Enumeration](web_dir_enumeration.md) | `web_dir_enumeration` | yes | 8 | yes |
| [HTTPS Heartbleed](web_https_heartbleed.md) | `web_https_heartbleed` | yes | 8 | yes |
| [IDOR Path Traversal](web_idor_path_traversal.md) | `web_idor_path_traversal` | yes | 8 | yes |
| [IDOR URL Parameter](web_idor_url_parameter.md) | `web_idor_url_parameter` | yes | 8 | yes |
| [Web POST Bruteforce](web_post_bruteforce.md) | `web_post_bruteforce` | yes | 8 | yes |
| [Web Simple Scanner](web_simple_scanner.md) | `web_simple_scanner` | yes | 8 | yes |
| [SQL Injection](web_sql_injection.md) | `web_sql_injection` | yes | 8 | yes |
| [Web Wide Scanner](web_wide_scanner.md) | `web_wide_scanner` | yes | 8 | yes |
| [XSS Scanner](web_xss_scanner.md) | `web_xss_scanner` | yes | 8 | yes |
