# STP Config Flood (`net_stp_conf_flood`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `net_stp_conf_flood`. In the local catalog, the attack is described as: BPDU (Bridge Protocol Data Unit) packet flood with STP topology reconfiguration information and random MAC addresses. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `net_stp_conf_flood` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.1 L2/L3 |
| Target services | local network |
| Image | `attack-stp-conf-flood:latest` |
| Container | `attack-stp-conf-flood` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 199 | 100% | 0% | 4,1 / 4,61 | 5,05 | 9.599 (9.592-9.606) | 43,29 | 3/3 | 0,62% / 0,69% | 140,26 |
| L1 | http | 5 | 200 | 100% | 0% | 4,62 / 6,61 | 49,39 | 260.994 (134.940-404.352) | 57,29 | 3/3 | 0,73% / 0,91% | 142,42 |
| L2 | http | 5 | 200 | 100% | 0% | 5,42 / 7,14 | 41,73 | 217.553 (78.536-420.104) | 55,07 | 3/3 | 0,83% / 1,04% | 144,51 |
| L3 | http | 5 | 200 | 100% | 0% | 5,45 / 7,32 | 36,45 | 187.698 (94.272-321.442) | 53,33 | 3/3 | 0,86% / 1,09% | 146,61 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,62 | 0,04 | 6,06% | 0,59 | 0,68 |
| L0 | Dataset rows | 5 | 9.599,2 | 6,72 | 0,07% | 9.592 | 9.606 |
| L0 | Execution time | 5 | 43,29 | 0,97 | 2,23% | 42,84 | 45,02 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 4,61 | 0,3 | 6,55% | 4,38 | 5,13 |
| L1 | Mean CPU in attack phase | 5 | 0,73 | 0,08 | 10,9% | 0,66 | 0,85 |
| L1 | Dataset rows | 5 | 260.994,4 | 110.048,17 | 42,16% | 134.940 | 404.352 |
| L1 | Execution time | 5 | 57,29 | 6,31 | 11,01% | 50,14 | 65,54 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 6,61 | 1,22 | 18,43% | 5,17 | 8,07 |
| L2 | Mean CPU in attack phase | 5 | 0,83 | 0,05 | 6,26% | 0,78 | 0,92 |
| L2 | Dataset rows | 5 | 217.552,8 | 160.975,85 | 73,99% | 78.536 | 420.104 |
| L2 | Execution time | 5 | 55,07 | 9,16 | 16,63% | 47 | 66,46 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 7,14 | 0,39 | 5,48% | 6,61 | 7,69 |
| L3 | Mean CPU in attack phase | 5 | 0,86 | 0,07 | 8,59% | 0,79 | 0,98 |
| L3 | Dataset rows | 5 | 187.697,6 | 95.071,1 | 50,65% | 94.272 | 321.442 |
| L3 | Execution time | 5 | 53,33 | 5,5 | 10,32% | 47,85 | 60,91 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 7,32 | 0,77 | 10,46% | 6,63 | 8,22 |

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
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F3_v1_timeseries_http_net_stp_conf_flood_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F3_v1_timeseries_http_net_stp_conf_flood_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F3_v1_timeseries_http_net_stp_conf_flood_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F3_v1_timeseries_http_net_stp_conf_flood_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F5_resources_http_net_stp_conf_flood_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F5_resources_http_net_stp_conf_flood_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F4_v2_failrate_http_net_stp_conf_flood_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F4_v2_failrate_http_net_stp_conf_flood_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/stp-conf-flood/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/net_stp_conf_flood`.
