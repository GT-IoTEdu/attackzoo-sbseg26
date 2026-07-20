# PHP LFI Enumeration (`php_lfi_enumeration`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `php_lfi_enumeration`. In the local catalog, the attack is described as: Controlled enumeration of Local File Inclusion (LFI) vectors in a vulnerable PHP application. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `php_lfi_enumeration` |
| Category | 3) Web Application Attacks |
| Subcategory | 3.2 Insecure Direct Object Reference (IDOR) |
| Target services | http-server |
| Image | `attack-php-lfi-enumeration:latest` |
| Container | `attack-php-lfi-enumeration` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/tactics/TA0009/](https://attack.mitre.org/tactics/TA0009/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/003/](https://attack.mitre.org/techniques/T1595/003/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1005/](https://attack.mitre.org/techniques/T1005/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 5,41 / 6,38 | 1,67 | 3.152 (3.120-3.200) | 42,41 | 3/3 | 0,84% / 0,95% | 420,58 |
| L1 | http | 5 | 200 | 100% | 0% | 3,34 / 4,69 | 74,89 | 137.978 (132.220-144.056) | 61,28 | 3/3 | 49,78% / 54,36% | 468,79 |
| L2 | http | 5 | 200 | 100% | 0% | 3,11 / 4,09 | 76,54 | 141.010 (138.478-143.216) | 60,47 | 3/3 | 49,83% / 54,28% | 562,11 |
| L3 | http | 5 | 200 | 100% | 0% | 2,99 / 4 | 77,67 | 143.094 (141.860-143.676) | 61,39 | 3/3 | 49,59% / 53,55% | 656,33 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,84 | 0,11 | 13,22% | 0,69 | 0,97 |
| L0 | Dataset rows | 5 | 3.152 | 33,47 | 1,06% | 3.120 | 3.200 |
| L0 | Execution time | 5 | 42,41 | 0,28 | 0,65% | 42,23 | 42,89 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 6,38 | 1,15 | 18,03% | 4,82 | 7,55 |
| L1 | Mean CPU in attack phase | 5 | 49,78 | 1,97 | 3,95% | 46,89 | 51,85 |
| L1 | Dataset rows | 5 | 137.977,6 | 5.296,44 | 3,84% | 132.220 | 144.056 |
| L1 | Execution time | 5 | 61,28 | 0,66 | 1,08% | 60,49 | 61,99 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 4,69 | 0,67 | 14,28% | 3,86 | 5,56 |
| L2 | Mean CPU in attack phase | 5 | 49,83 | 0,82 | 1,65% | 48,61 | 50,8 |
| L2 | Dataset rows | 5 | 141.010,4 | 2.199,35 | 1,56% | 138.478 | 143.216 |
| L2 | Execution time | 5 | 60,47 | 0,39 | 0,64% | 60,07 | 60,97 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 4,09 | 0,25 | 6,01% | 3,79 | 4,33 |
| L3 | Mean CPU in attack phase | 5 | 49,59 | 0,28 | 0,56% | 49,3 | 50,03 |
| L3 | Dataset rows | 5 | 143.093,6 | 748,51 | 0,52% | 141.860 | 143.676 |
| L3 | Execution time | 5 | 61,39 | 0,5 | 0,81% | 60,71 | 61,91 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 4 | 0,29 | 7,19% | 3,65 | 4,29 |

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
<td><img src="../../assets/campaign_doc/php_lfi_enumeration/F3_v1_timeseries_http_php_lfi_enumeration_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/php_lfi_enumeration/F3_v1_timeseries_http_php_lfi_enumeration_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/php_lfi_enumeration/F3_v1_timeseries_http_php_lfi_enumeration_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/php_lfi_enumeration/F3_v1_timeseries_http_php_lfi_enumeration_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/php_lfi_enumeration/F5_resources_http_php_lfi_enumeration_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/php_lfi_enumeration/F5_resources_http_php_lfi_enumeration_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/php_lfi_enumeration/F4_v2_failrate_http_php_lfi_enumeration_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/php_lfi_enumeration/F4_v2_failrate_http_php_lfi_enumeration_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/php-lfi-enumeration/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/php_lfi_enumeration`.
