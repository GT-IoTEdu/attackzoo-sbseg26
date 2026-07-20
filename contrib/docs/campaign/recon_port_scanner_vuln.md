# Port Scanner Vulnerabilities (`recon_port_scanner_vuln`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `recon_port_scanner_vuln`. In the local catalog, the attack is described as: Port scan and known-vulnerability checks. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `recon_port_scanner_vuln` |
| Category | 1) Reconnaissance and Discovery |
| Subcategory | 1.2 Port, service, OS, and vulnerability scanning |
| Target services | target IP service |
| Image | `attack-port-scanner-vulnerabilities:latest` |
| Container | `attack-port-scanner-vulnerabilities` |
| Catalog max runtime | 300 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1592/](https://attack.mitre.org/techniques/T1592/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,65 / 6,14 | 5,04 | 9.594 (9.590-9.602) | 43,12 | 3/3 | 0,74% / 0,95% | 756,7 |
| L1 | http | 5 | 200 | 100% | 0% | 5,03 / 7,14 | 20,62 | 27.446 (27.354-27.534) | 45,54 | 3/3 | 1,91% / 5,28% | 763,67 |
| L2 | http | 5 | 200 | 100% | 0% | 4,59 / 5,73 | 19,7 | 27.110 (26.636-27.366) | 45,23 | 3/3 | 1,69% / 4,47% | 769,62 |
| L3 | http | 5 | 200 | 100% | 0% | 4,34 / 5,5 | 20,6 | 27.400 (27.358-27.456) | 45,25 | 3/3 | 1,66% / 4,71% | 772,27 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,74 | 0,08 | 10,73% | 0,66 | 0,85 |
| L0 | Dataset rows | 5 | 9.594,4 | 4,56 | 0,05% | 9.590 | 9.602 |
| L0 | Execution time | 5 | 43,12 | 0,41 | 0,96% | 42,85 | 43,85 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 6,14 | 1,11 | 18,12% | 4,72 | 7,41 |
| L1 | Mean CPU in attack phase | 5 | 1,91 | 0,15 | 7,86% | 1,73 | 2,07 |
| L1 | Dataset rows | 5 | 27.446 | 80,11 | 0,29% | 27.354 | 27.534 |
| L1 | Execution time | 5 | 45,54 | 0,1 | 0,21% | 45,45 | 45,66 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 7,14 | 0,58 | 8,12% | 6,17 | 7,62 |
| L2 | Mean CPU in attack phase | 5 | 1,69 | 0,16 | 9,34% | 1,53 | 1,94 |
| L2 | Dataset rows | 5 | 27.110,4 | 349,79 | 1,29% | 26.636 | 27.366 |
| L2 | Execution time | 5 | 45,23 | 0,07 | 0,16% | 45,18 | 45,35 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 5,73 | 1,11 | 19,44% | 4,51 | 7 |
| L3 | Mean CPU in attack phase | 5 | 1,66 | 0,14 | 8,38% | 1,52 | 1,84 |
| L3 | Dataset rows | 5 | 27.399,6 | 46,46 | 0,17% | 27.358 | 27.456 |
| L3 | Execution time | 5 | 45,25 | 0,06 | 0,12% | 45,17 | 45,33 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 5,5 | 1,05 | 19,08% | 4,62 | 6,72 |

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
<td><img src="../../assets/campaign_doc/recon_port_scanner_vuln/F3_v1_timeseries_http_recon_port_scanner_vuln_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_vuln/F3_v1_timeseries_http_recon_port_scanner_vuln_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_vuln/F3_v1_timeseries_http_recon_port_scanner_vuln_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_vuln/F3_v1_timeseries_http_recon_port_scanner_vuln_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_vuln/F5_resources_http_recon_port_scanner_vuln_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_vuln/F5_resources_http_recon_port_scanner_vuln_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_vuln/F4_v2_failrate_http_recon_port_scanner_vuln_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_vuln/F4_v2_failrate_http_recon_port_scanner_vuln_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/port-scanner-vulnerabilities/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/recon_port_scanner_vuln`.
