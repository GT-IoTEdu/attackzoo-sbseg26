# PSH Flood (`dos_psh_flood`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `dos_psh_flood`. In the local catalog, the attack is described as: TCP packet flood with the PSH flag set. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `dos_psh_flood` |
| Category | 6) Denial of Service and Impact |
| Subcategory | 6.1 Network/transport floods (ICMP/TCP/UDP) |
| Target services | target IP service |
| Image | `attack-psh-flood:latest` |
| Container | `attack-psh-flood` |
| Catalog max runtime | 10 s |
| Intensity parameters | duration_s, count, rate_pps, payload_size |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 197 | 100% | 0% | 7,48 / 26,57 | 1,65 | 3.114 (3.080-3.130) | 42,67 | 3/3 | 0,65% / 0,77% | 71,48 |
| L1 | http | 5 | 195 | 100% | 0% | 5,47 / 45,59 | 827,36 | 4.560.206 (3.987.792-4.832.552) | 577,78 | 3/3 | 0,67% / 0,79% | 73,63 |
| L2 | http | 5 | 196 | 100% | 0% | 4,92 / 26,36 | 872,49 | 4.809.211 (4.754.062-4.885.358) | 604,65 | 3/3 | 0,67% / 0,82% | 75,56 |
| L3 | http | 5 | 196 | 100% | 0% | 4,19 / 22,4 | 851,1 | 4.691.072 (4.089.574-4.897.544) | 591,97 | 3/3 | 0,62% / 0,75% | 77,7 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,65 | 0,05 | 7,12% | 0,59 | 0,69 |
| L0 | Dataset rows | 5 | 3.114,4 | 19,67 | 0,63% | 3.080 | 3.130 |
| L0 | Execution time | 5 | 42,67 | 1,13 | 2,66% | 42,11 | 44,69 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 26,57 | 7,54 | 28,37% | 20,98 | 39,34 |
| L1 | Mean CPU in attack phase | 5 | 0,67 | 0,03 | 4,74% | 0,64 | 0,7 |
| L1 | Dataset rows | 5 | 4.560.206 | 339.730,25 | 7,45% | 3.987.792 | 4.832.552 |
| L1 | Execution time | 5 | 577,78 | 38,13 | 6,6% | 513,24 | 606,62 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 45,59 | 35,1 | 77,01% | 23,4 | 106,54 |
| L2 | Mean CPU in attack phase | 5 | 0,67 | 0,04 | 6,35% | 0,62 | 0,71 |
| L2 | Dataset rows | 5 | 4.809.211,2 | 47.596,09 | 0,99% | 4.754.062 | 4.885.358 |
| L2 | Execution time | 5 | 604,65 | 5,23 | 0,87% | 597,76 | 612,49 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 26,36 | 4,48 | 17,01% | 22,93 | 34,2 |
| L3 | Mean CPU in attack phase | 5 | 0,62 | 0,04 | 5,76% | 0,58 | 0,68 |
| L3 | Dataset rows | 5 | 4.691.072 | 338.496,59 | 7,22% | 4.089.574 | 4.897.544 |
| L3 | Execution time | 5 | 591,97 | 37,9 | 6,4% | 524,37 | 613,72 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 22,4 | 3,39 | 15,13% | 19,29 | 27,62 |

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
<td><img src="../../assets/campaign_doc/dos_psh_flood/F3_v1_timeseries_http_dos_psh_flood_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_psh_flood/F3_v1_timeseries_http_dos_psh_flood_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_psh_flood/F3_v1_timeseries_http_dos_psh_flood_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_psh_flood/F3_v1_timeseries_http_dos_psh_flood_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_psh_flood/F5_resources_http_dos_psh_flood_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_psh_flood/F5_resources_http_dos_psh_flood_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_psh_flood/F4_v2_failrate_http_dos_psh_flood_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/dos_psh_flood/F4_v2_failrate_http_dos_psh_flood_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/psh-flood/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/dos_psh_flood`.
