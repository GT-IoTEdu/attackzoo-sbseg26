# IDOR Path Traversal (`web_idor_path_traversal`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `web_idor_path_traversal`. In the local catalog, the attack is described as: Attempts to access local files through the web server using a wordlist. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `web_idor_path_traversal` |
| Category | 3) Web Application Attacks |
| Subcategory | 3.2 Insecure Direct Object Reference (IDOR) |
| Target services | http-server |
| Image | `attack-idor-path-traversal:latest` |
| Container | `attack-idor-path-traversal` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/tactics/TA0009/](https://attack.mitre.org/tactics/TA0009/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/003/](https://attack.mitre.org/techniques/T1595/003/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1005/](https://attack.mitre.org/techniques/T1005/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 198 | 100% | 0% | 5,52 / 15,78 | 1,65 | 3.120 (3.080-3.160) | 42,3 | 3/3 | 0,77% / 0,94% | 725,29 |
| L1 | http | 5 | 179 | 98,8% | 1,2% | 6,39 / 126,38 | 4,46 | 8.684 (8.612-8.748) | 42,9 | 3/3 | 1,92% / 7,57% | 731,39 |
| L2 | http | 5 | 174 | 97,7% | 2,3% | 5,87 / 191,5 | 4,43 | 8.669 (8.618-8.746) | 42,83 | 3/3 | 2,02% / 8,61% | 734,94 |
| L3 | http | 5 | 176 | 97,7% | 2,3% | 5,6 / 128,69 | 4,44 | 8.675 (8.638-8.706) | 42,85 | 3/3 | 2% / 8,81% | 735,74 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,77 | 0,09 | 11,13% | 0,68 | 0,88 |
| L0 | Dataset rows | 5 | 3.120,4 | 28,3 | 0,91% | 3.080 | 3.160 |
| L0 | Execution time | 5 | 42,3 | 0,32 | 0,76% | 42,06 | 42,85 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 15,78 | 12,22 | 77,46% | 6,51 | 32 |
| L1 | Mean CPU in attack phase | 5 | 1,92 | 0,59 | 30,89% | 0,93 | 2,42 |
| L1 | Dataset rows | 5 | 8.683,6 | 59,37 | 0,68% | 8.612 | 8.748 |
| L1 | Execution time | 5 | 42,9 | 0,05 | 0,11% | 42,85 | 42,97 |
| L1 | Failure in attack phase | 5 | 1,18 | 1,61 | 136,93% | 0 | 2,94 |
| L1 | Censored p95 latency | 5 | 126,38 | 155,55 | 123,08% | 11,63 | 334,29 |
| L2 | Mean CPU in attack phase | 5 | 2,02 | 0,25 | 12,44% | 1,77 | 2,44 |
| L2 | Dataset rows | 5 | 8.669,2 | 48,47 | 0,56% | 8.618 | 8.746 |
| L2 | Execution time | 5 | 42,83 | 0,1 | 0,23% | 42,77 | 43,01 |
| L2 | Failure in attack phase | 5 | 2,32 | 1,3 | 55,93% | 0 | 2,94 |
| L2 | Censored p95 latency | 5 | 191,5 | 158,09 | 82,56% | 9,17 | 388,04 |
| L3 | Mean CPU in attack phase | 5 | 2 | 0,11 | 5,61% | 1,87 | 2,14 |
| L3 | Dataset rows | 5 | 8.674,8 | 30,94 | 0,36% | 8.638 | 8.706 |
| L3 | Execution time | 5 | 42,85 | 0,06 | 0,14% | 42,77 | 42,91 |
| L3 | Failure in attack phase | 5 | 2,29 | 1,28 | 55,96% | 0 | 2,94 |
| L3 | Censored p95 latency | 5 | 128,69 | 140,01 | 108,79% | 21,2 | 354,15 |

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
<td><img src="../../assets/campaign_doc/web_idor_path_traversal/F3_v1_timeseries_http_web_idor_path_traversal_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_idor_path_traversal/F3_v1_timeseries_http_web_idor_path_traversal_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_idor_path_traversal/F3_v1_timeseries_http_web_idor_path_traversal_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_idor_path_traversal/F3_v1_timeseries_http_web_idor_path_traversal_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_idor_path_traversal/F5_resources_http_web_idor_path_traversal_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_idor_path_traversal/F5_resources_http_web_idor_path_traversal_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_idor_path_traversal/F4_v2_failrate_http_web_idor_path_traversal_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/web_idor_path_traversal/F4_v2_failrate_http_web_idor_path_traversal_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/idor-path-traversal/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/web_idor_path_traversal`.
