# Port Scanner TCP (`recon_port_scanner_tcp`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `recon_port_scanner_tcp`. In the local catalog, the attack is described as: TCP port scan of the target. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `recon_port_scanner_tcp` |
| Category | 1) Reconnaissance and Discovery |
| Subcategory | 1.2 Port, service, OS, and vulnerability scanning |
| Target services | target IP service |
| Image | `attack-port-scanner-tcp:latest` |
| Container | `attack-port-scanner-tcp` |
| Catalog max runtime | 120 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/001/](https://attack.mitre.org/techniques/T1595/001/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,39 / 5,14 | 5,06 | 9.625 (9.600-9.720) | 43,08 | 3/3 | 0,67% / 0,74% | 739,97 |
| L1 | http | 5 | 200 | 100% | 0% | 4,82 / 5,92 | 6,73 | 17.863 (17.856-17.872) | 43,96 | 3/3 | 0,75% / 0,92% | 742,05 |
| L2 | http | 5 | 200 | 100% | 0% | 4,49 / 5,54 | 6,73 | 17.861 (17.858-17.862) | 43,98 | 3/3 | 0,72% / 0,86% | 744,05 |
| L3 | http | 5 | 200 | 100% | 0% | 4,96 / 6,33 | 6,72 | 17.832 (17.732-17.860) | 44,02 | 3/3 | 0,77% / 0,92% | 746,17 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,67 | 0,04 | 5,65% | 0,63 | 0,72 |
| L0 | Dataset rows | 5 | 9.624,8 | 53,25 | 0,55% | 9.600 | 9.720 |
| L0 | Execution time | 5 | 43,08 | 0,35 | 0,81% | 42,86 | 43,69 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 5,14 | 0,66 | 12,79% | 4,63 | 6,25 |
| L1 | Mean CPU in attack phase | 5 | 0,75 | 0,09 | 11,43% | 0,65 | 0,88 |
| L1 | Dataset rows | 5 | 17.862,8 | 6,87 | 0,04% | 17.856 | 17.872 |
| L1 | Execution time | 5 | 43,96 | 0,05 | 0,11% | 43,91 | 44 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 5,92 | 1 | 16,82% | 4,75 | 7,08 |
| L2 | Mean CPU in attack phase | 5 | 0,72 | 0,06 | 8,85% | 0,63 | 0,78 |
| L2 | Dataset rows | 5 | 17.861,2 | 1,79 | 0,01% | 17.858 | 17.862 |
| L2 | Execution time | 5 | 43,98 | 0,07 | 0,16% | 43,9 | 44,05 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 5,54 | 0,83 | 14,93% | 4,59 | 6,33 |
| L3 | Mean CPU in attack phase | 5 | 0,77 | 0,11 | 14,43% | 0,67 | 0,95 |
| L3 | Dataset rows | 5 | 17.832 | 55,95 | 0,31% | 17.732 | 17.860 |
| L3 | Execution time | 5 | 44,02 | 0,06 | 0,13% | 43,95 | 44,11 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 6,33 | 1,36 | 21,55% | 4,72 | 8,46 |

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
<td><img src="../../assets/campaign_doc/recon_port_scanner_tcp/F3_v1_timeseries_http_recon_port_scanner_tcp_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_tcp/F3_v1_timeseries_http_recon_port_scanner_tcp_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_tcp/F3_v1_timeseries_http_recon_port_scanner_tcp_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_tcp/F3_v1_timeseries_http_recon_port_scanner_tcp_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_tcp/F5_resources_http_recon_port_scanner_tcp_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_tcp/F5_resources_http_recon_port_scanner_tcp_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_tcp/F4_v2_failrate_http_recon_port_scanner_tcp_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_tcp/F4_v2_failrate_http_recon_port_scanner_tcp_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/port-scanner-tcp/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/recon_port_scanner_tcp`.
