# SNMP Scanner (`recon_snmp_scanner`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `recon_snmp_scanner`. In the local catalog, the attack is described as: SNMP scan across all hosts in a network using a community-string wordlist. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `recon_snmp_scanner` |
| Category | 1) Reconnaissance and Discovery |
| Subcategory | 1.2 Port, service, OS, and vulnerability scanning |
| Target services | target IP service |
| Image | `attack-snmp-scanner:latest` |
| Container | `attack-snmp-scanner` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/001/](https://attack.mitre.org/techniques/T1595/001/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/)<br>[https://attack.mitre.org/techniques/T1110/](https://attack.mitre.org/techniques/T1110/)<br>[https://attack.mitre.org/techniques/T1110/003/](https://attack.mitre.org/techniques/T1110/003/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,64 / 5,96 | 5,06 | 9.626 (9.592-9.742) | 43,14 | 3/3 | 0,73% / 0,84% | 774,48 |
| L1 | http | 5 | 200 | 100% | 0% | 5,07 / 6,56 | 5,17 | 10.177 (10.108-10.226) | 43,25 | 3/3 | 0,81% / 0,98% | 776,51 |
| L2 | http | 5 | 200 | 100% | 0% | 5,45 / 7,22 | 5,15 | 10.131 (10.100-10.226) | 43,31 | 3/3 | 0,87% / 1,02% | 778,57 |
| L3 | http | 5 | 200 | 100% | 0% | 5,34 / 6,92 | 5,17 | 10.182 (10.104-10.242) | 43,24 | 3/3 | 0,81% / 1,04% | 780,83 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,73 | 0,04 | 5,91% | 0,68 | 0,79 |
| L0 | Dataset rows | 5 | 9.626,4 | 64,74 | 0,67% | 9.592 | 9.742 |
| L0 | Execution time | 5 | 43,14 | 0,39 | 0,91% | 42,84 | 43,81 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 5,96 | 1,04 | 17,46% | 4,9 | 7,47 |
| L1 | Mean CPU in attack phase | 5 | 0,81 | 0,06 | 7,75% | 0,74 | 0,91 |
| L1 | Dataset rows | 5 | 10.177,2 | 62,3 | 0,61% | 10.108 | 10.226 |
| L1 | Execution time | 5 | 43,25 | 0,05 | 0,12% | 43,2 | 43,31 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 6,56 | 0,73 | 11,15% | 5,44 | 7,47 |
| L2 | Mean CPU in attack phase | 5 | 0,87 | 0,1 | 11,05% | 0,78 | 1,02 |
| L2 | Dataset rows | 5 | 10.130,8 | 53,84 | 0,53% | 10.100 | 10.226 |
| L2 | Execution time | 5 | 43,31 | 0,05 | 0,11% | 43,24 | 43,35 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 7,22 | 0,58 | 7,99% | 6,75 | 8,16 |
| L3 | Mean CPU in attack phase | 5 | 0,81 | 0,08 | 9,85% | 0,72 | 0,93 |
| L3 | Dataset rows | 5 | 10.182 | 66,33 | 0,65% | 10.104 | 10.242 |
| L3 | Execution time | 5 | 43,24 | 0,09 | 0,2% | 43,11 | 43,35 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 6,92 | 0,82 | 11,8% | 5,78 | 8,02 |

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
<td><img src="../../assets/campaign_doc/recon_snmp_scanner/F3_v1_timeseries_http_recon_snmp_scanner_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_snmp_scanner/F3_v1_timeseries_http_recon_snmp_scanner_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_snmp_scanner/F3_v1_timeseries_http_recon_snmp_scanner_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_snmp_scanner/F3_v1_timeseries_http_recon_snmp_scanner_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_snmp_scanner/F5_resources_http_recon_snmp_scanner_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_snmp_scanner/F5_resources_http_recon_snmp_scanner_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_snmp_scanner/F4_v2_failrate_http_recon_snmp_scanner_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_snmp_scanner/F4_v2_failrate_http_recon_snmp_scanner_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/snmp-scanner/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/recon_snmp_scanner`.
