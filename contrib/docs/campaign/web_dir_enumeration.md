# Web Directory Enumeration (`web_dir_enumeration`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `web_dir_enumeration`. In the local catalog, the attack is described as: Web server subdirectory and resource enumeration using a wordlist. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `web_dir_enumeration` |
| Category | 3) Web Application Attacks |
| Subcategory | 3.1 General Web |
| Target services | http-server |
| Image | `attack-web-dir-enumeration:latest` |
| Container | `attack-web-dir-enumeration` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/003/](https://attack.mitre.org/techniques/T1595/003/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,39 / 5,34 | 1,67 | 3.168 (3.160-3.200) | 42,34 | 3/3 | 0,7% / 0,83% | 782,9 |
| L1 | http | 5 | 198 | 100% | 0% | 4,89 / 7,78 | 1.588,8 | 1.900.674 (1.704.782-2.407.134) | 326,79 | 3/3 | 268,21% / 294,43% | 1.301,76 |
| L2 | http | 5 | 200 | 100% | 0% | 4,77 / 7,99 | 1.540,75 | 1.843.304 (1.775.942-1.909.856) | 319,39 | 3/3 | 267,2% / 299,83% | 1.341,23 |
| L3 | http | 5 | 200 | 100% | 0% | 4,94 / 14,14 | 1.471,03 | 1.760.023 (1.583.034-1.905.876) | 306,81 | 3/3 | 271,39% / 308,52% | 989,08 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,7 | 0,05 | 7,3% | 0,67 | 0,8 |
| L0 | Dataset rows | 5 | 3.168 | 17,89 | 0,56% | 3.160 | 3.200 |
| L0 | Execution time | 5 | 42,34 | 0,47 | 1,11% | 42,06 | 43,17 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 5,34 | 0,55 | 10,32% | 4,95 | 6,22 |
| L1 | Mean CPU in attack phase | 5 | 268,21 | 9,59 | 3,57% | 259,89 | 283,64 |
| L1 | Dataset rows | 5 | 1.900.673,6 | 289.220,98 | 15,22% | 1.704.782 | 2.407.134 |
| L1 | Execution time | 5 | 326,79 | 44,67 | 13,67% | 296,06 | 405,18 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 7,78 | 2,37 | 30,42% | 6,22 | 11,75 |
| L2 | Mean CPU in attack phase | 5 | 267,21 | 5,5 | 2,06% | 258,02 | 271,61 |
| L2 | Dataset rows | 5 | 1.843.304 | 50.901,61 | 2,76% | 1.775.942 | 1.909.856 |
| L2 | Execution time | 5 | 319,39 | 7,16 | 2,24% | 309,5 | 328,06 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 7,99 | 1,81 | 22,64% | 5,97 | 10,32 |
| L3 | Mean CPU in attack phase | 5 | 271,39 | 26,18 | 9,65% | 232,8 | 296,15 |
| L3 | Dataset rows | 5 | 1.760.022,8 | 116.958,86 | 6,65% | 1.583.034 | 1.905.876 |
| L3 | Execution time | 5 | 306,81 | 16,8 | 5,48% | 281,13 | 327,44 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 14,14 | 10,54 | 74,54% | 7,18 | 31,49 |

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
<td><img src="../../assets/campaign_doc/web_dir_enumeration/F3_v1_timeseries_http_web_dir_enumeration_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_dir_enumeration/F3_v1_timeseries_http_web_dir_enumeration_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_dir_enumeration/F3_v1_timeseries_http_web_dir_enumeration_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_dir_enumeration/F3_v1_timeseries_http_web_dir_enumeration_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_dir_enumeration/F5_resources_http_web_dir_enumeration_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_dir_enumeration/F5_resources_http_web_dir_enumeration_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_dir_enumeration/F4_v2_failrate_http_web_dir_enumeration_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/web_dir_enumeration/F4_v2_failrate_http_web_dir_enumeration_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/web-dir-enumeration/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/web_dir_enumeration`.
