# UDP Flood (`dos_udp_flood`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `dos_udp_flood`. In the local catalog, the attack is described as: UDP packet flood. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `dos_udp_flood` |
| Category | 6) Denial of Service and Impact |
| Subcategory | 6.1 Network/transport floods (ICMP/TCP/UDP) |
| Target services | target IP service |
| Image | `attack-udp-flood:latest` |
| Container | `attack-udp-flood` |
| Catalog max runtime | 10 s |
| Intensity parameters | duration_s, count, rate_pps, payload_size |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,09 / 4,85 | 1,67 | 3.168 (3.160-3.200) | 42,18 | 3/3 | 0,63% / 0,7% | 112,53 |
| L1 | http | 5 | 200 | 100% | 0% | 4,14 / 4,97 | 507,73 | 3.319.656 (3.259.102-3.366.376) | 375,3 | 3/3 | 0,65% / 0,78% | 114,56 |
| L2 | http | 5 | 199 | 100% | 0% | 4,19 / 5,26 | 510,65 | 3.338.827 (3.285.548-3.393.784) | 376,55 | 3/3 | 0,66% / 0,8% | 116,64 |
| L3 | http | 5 | 200 | 100% | 0% | 3,9 / 4,78 | 485,27 | 3.172.456 (2.558.216-3.394.568) | 361,2 | 3/3 | 0,6% / 0,66% | 118,8 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,63 | 0,05 | 7,54% | 0,59 | 0,71 |
| L0 | Dataset rows | 5 | 3.168 | 17,89 | 0,56% | 3.160 | 3.200 |
| L0 | Execution time | 5 | 42,18 | 0,36 | 0,85% | 41,98 | 42,82 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 4,85 | 0,73 | 15,14% | 4,22 | 6,12 |
| L1 | Mean CPU in attack phase | 5 | 0,65 | 0,1 | 15,47% | 0,58 | 0,83 |
| L1 | Dataset rows | 5 | 3.319.655,6 | 49.263,14 | 1,48% | 3.259.102 | 3.366.376 |
| L1 | Execution time | 5 | 375,3 | 4,94 | 1,31% | 368,87 | 380,65 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 4,97 | 0,76 | 15,2% | 4,46 | 6,17 |
| L2 | Mean CPU in attack phase | 5 | 0,66 | 0,08 | 12,33% | 0,57 | 0,78 |
| L2 | Dataset rows | 5 | 3.338.826,8 | 49.514,41 | 1,48% | 3.285.548 | 3.393.784 |
| L2 | Execution time | 5 | 376,55 | 6,19 | 1,64% | 369,91 | 383,25 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 5,26 | 1,04 | 19,78% | 4,25 | 6,81 |
| L3 | Mean CPU in attack phase | 5 | 0,6 | 0,02 | 4,08% | 0,57 | 0,63 |
| L3 | Dataset rows | 5 | 3.172.456,4 | 350.806,33 | 11,06% | 2.558.216 | 3.394.568 |
| L3 | Execution time | 5 | 361,2 | 35,66 | 9,87% | 299,07 | 386,96 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 4,78 | 0,62 | 13,03% | 4,17 | 5,52 |

## Artifact Validation

| Level | Runs | Capture | Probe | Features | Dataset | Resources | Server stats | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| L1 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| L2 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| L3 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |

## Selected Figures

<table>
<tr>
<td><img src="../../assets/campaign_doc/dos_udp_flood/F3_v1_timeseries_http_dos_udp_flood_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_udp_flood/F3_v1_timeseries_http_dos_udp_flood_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_udp_flood/F3_v1_timeseries_http_dos_udp_flood_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_udp_flood/F3_v1_timeseries_http_dos_udp_flood_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_udp_flood/F5_resources_http_dos_udp_flood_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_udp_flood/F5_resources_http_dos_udp_flood_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_udp_flood/F4_v2_failrate_http_dos_udp_flood_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/dos_udp_flood/F4_v2_failrate_http_dos_udp_flood_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/udp-flood/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/dos_udp_flood`.
