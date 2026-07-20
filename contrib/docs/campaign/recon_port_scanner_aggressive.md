# Port Scanner Aggressive (`recon_port_scanner_aggressive`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `recon_port_scanner_aggressive`. In the local catalog, the attack is described as: Aggressive-profile port and service scan. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `recon_port_scanner_aggressive` |
| Category | 1) Reconnaissance and Discovery |
| Subcategory | 1.2 Port, service, OS, and vulnerability scanning |
| Target services | target IP service |
| Image | `attack-port-scanner-aggressive:latest` |
| Container | `attack-port-scanner-aggressive` |
| Catalog max runtime | 180 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1592/](https://attack.mitre.org/techniques/T1592/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/001/](https://attack.mitre.org/techniques/T1595/001/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,33 / 5,4 | 5,06 | 9.622 (9.584-9.716) | 43,06 | 3/3 | 0,67% / 0,76% | 718,75 |
| L1 | http | 5 | 200 | 100% | 0% | 4,31 / 5,56 | 7,12 | 19.320 (19.212-19.424) | 44,08 | 3/3 | 0,72% / 1,17% | 721,08 |
| L2 | http | 5 | 199 | 100% | 0% | 4,28 / 4,98 | 7,18 | 19.506 (19.414-19.856) | 44,11 | 3/3 | 0,67% / 0,82% | 723,51 |
| L3 | http | 5 | 200 | 100% | 0% | 5,41 / 6,76 | 7,19 | 19.524 (19.300-20.158) | 44,27 | 3/3 | 0,86% / 1,03% | 726,19 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,67 | 0,01 | 1,1% | 0,67 | 0,69 |
| L0 | Dataset rows | 5 | 9.621,6 | 53,56 | 0,56% | 9.584 | 9.716 |
| L0 | Execution time | 5 | 43,06 | 0,38 | 0,88% | 42,86 | 43,74 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 5,4 | 0,62 | 11,46% | 4,82 | 6,38 |
| L1 | Mean CPU in attack phase | 5 | 0,72 | 0,09 | 12,36% | 0,63 | 0,83 |
| L1 | Dataset rows | 5 | 19.320,4 | 77,71 | 0,4% | 19.212 | 19.424 |
| L1 | Execution time | 5 | 44,08 | 0,04 | 0,1% | 44,04 | 44,13 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 5,56 | 1,32 | 23,65% | 4,57 | 7,75 |
| L2 | Mean CPU in attack phase | 5 | 0,67 | 0,03 | 3,86% | 0,64 | 0,71 |
| L2 | Dataset rows | 5 | 19.505,6 | 195,93 | 1% | 19.414 | 19.856 |
| L2 | Execution time | 5 | 44,11 | 0,07 | 0,17% | 44,02 | 44,19 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 4,98 | 0,79 | 15,91% | 4,46 | 6,38 |
| L3 | Mean CPU in attack phase | 5 | 0,86 | 0,1 | 11,81% | 0,73 | 1,01 |
| L3 | Dataset rows | 5 | 19.524 | 357,93 | 1,83% | 19.300 | 20.158 |
| L3 | Execution time | 5 | 44,27 | 0,06 | 0,14% | 44,19 | 44,37 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 6,76 | 0,62 | 9,19% | 6,13 | 7,75 |

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
<td><img src="../../assets/campaign_doc/recon_port_scanner_aggressive/F3_v1_timeseries_http_recon_port_scanner_aggressive_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_aggressive/F3_v1_timeseries_http_recon_port_scanner_aggressive_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_aggressive/F3_v1_timeseries_http_recon_port_scanner_aggressive_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_aggressive/F3_v1_timeseries_http_recon_port_scanner_aggressive_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_aggressive/F5_resources_http_recon_port_scanner_aggressive_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_aggressive/F5_resources_http_recon_port_scanner_aggressive_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_aggressive/F4_v2_failrate_http_recon_port_scanner_aggressive_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_aggressive/F4_v2_failrate_http_recon_port_scanner_aggressive_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/port-scanner-aggressive/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/recon_port_scanner_aggressive`.
