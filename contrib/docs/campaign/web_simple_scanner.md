# Web Simple Scanner (`web_simple_scanner`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `web_simple_scanner`. In the local catalog, the attack is described as: Simplified scanner for known web vulnerabilities. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `web_simple_scanner` |
| Category | 3) Web Application Attacks |
| Subcategory | 3.1 General Web |
| Target services | http-server |
| Image | `attack-web-simple-scanner:latest` |
| Container | `attack-web-simple-scanner` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/techniques/T1592/](https://attack.mitre.org/techniques/T1592/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 5,34 / 6,89 | 1,66 | 3.144 (3.120-3.160) | 42,31 | 3/3 | 0,8% / 1,01% | 971,99 |
| L1 | http | 5 | 199 | 100% | 0% | 4,35 / 5,81 | 93,69 | 99.088 (99.084-99.098) | 56,48 | 3/3 | 11,88% / 17,73% | 953,63 |
| L2 | http | 5 | 197 | 100% | 0% | 4,35 / 5,77 | 93,68 | 99.069 (99.006-99.086) | 56,55 | 3/3 | 11,82% / 17,01% | 908,77 |
| L3 | http | 5 | 200 | 100% | 0% | 4,56 / 5,79 | 93,69 | 99.086 (99.084-99.092) | 56,29 | 3/3 | 12,16% / 17,22% | 885,14 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,8 | 0,09 | 10,83% | 0,74 | 0,94 |
| L0 | Dataset rows | 5 | 3.144 | 21,91 | 0,7% | 3.120 | 3.160 |
| L0 | Execution time | 5 | 42,31 | 0,41 | 0,96% | 42,08 | 43,03 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 6,89 | 0,78 | 11,32% | 5,87 | 7,72 |
| L1 | Mean CPU in attack phase | 5 | 11,88 | 0,55 | 4,63% | 11,58 | 12,86 |
| L1 | Dataset rows | 5 | 99.088 | 5,83 | 0,01% | 99.084 | 99.098 |
| L1 | Execution time | 5 | 56,48 | 0,12 | 0,21% | 56,33 | 56,65 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 5,81 | 0,97 | 16,76% | 5,06 | 7,5 |
| L2 | Mean CPU in attack phase | 5 | 11,82 | 0,38 | 3,23% | 11,39 | 12,28 |
| L2 | Dataset rows | 5 | 99.069,2 | 35,34 | 0,04% | 99.006 | 99.086 |
| L2 | Execution time | 5 | 56,55 | 0,38 | 0,68% | 56,24 | 57,2 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 5,77 | 0,69 | 11,93% | 5,03 | 6,73 |
| L3 | Mean CPU in attack phase | 5 | 12,16 | 0,21 | 1,71% | 11,82 | 12,38 |
| L3 | Dataset rows | 5 | 99.086 | 3,46 | 0% | 99.084 | 99.092 |
| L3 | Execution time | 5 | 56,29 | 0,1 | 0,19% | 56,22 | 56,48 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 5,79 | 0,54 | 9,28% | 5,22 | 6,47 |

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
<td><img src="../../assets/campaign_doc/web_simple_scanner/F3_v1_timeseries_http_web_simple_scanner_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_simple_scanner/F3_v1_timeseries_http_web_simple_scanner_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_simple_scanner/F3_v1_timeseries_http_web_simple_scanner_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_simple_scanner/F3_v1_timeseries_http_web_simple_scanner_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_simple_scanner/F5_resources_http_web_simple_scanner_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_simple_scanner/F5_resources_http_web_simple_scanner_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_simple_scanner/F4_v2_failrate_http_web_simple_scanner_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/web_simple_scanner/F4_v2_failrate_http_web_simple_scanner_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/web-simple-scanner/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/web_simple_scanner`.
