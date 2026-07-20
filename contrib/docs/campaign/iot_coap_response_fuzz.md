# CoAP Response Fuzzing (`iot_coap_response_fuzz`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `iot_coap_response_fuzz`. In the local catalog, the attack is described as: Burst of randomized or mutated CoAP messages intended to trigger errors, exceptions, or crashes on the target. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `iot_coap_response_fuzz` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / CoAP |
| Target services | coap-server |
| Image | `attack-coap-response-fuzz:latest` |
| Container | `attack-coap-response-fuzz` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/004/](https://attack.mitre.org/techniques/T1499/004/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | coap | 5 | 200 | 100% | 0% | 1 / 1,17 | 0,21 | 948 (948-948) | 41,91 | 3/3 | 0,11% / 0,13% | 6,37 |
| L1 | coap | 5 | 196 | 1,1% | 98,9% | 2.000,44 / 2.000,44 | 0,22 | 380 (326-594) | 41,89 | 3/3 | 0,39% / 2,19% | 7,21 |
| L2 | coap | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 0,22 | 326 (326-326) | 42,06 | 3/3 | 0,33% / 2,82% | 1.459,5 |
| L3 | coap | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 0,22 | 326 (326-326) | 42,15 | 3/3 | 0,34% / 3,12% | 1.462,01 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,11 | 0,01 | 5,37% | 0,11 | 0,12 |
| L0 | Dataset rows | 5 | 948 | 0 | 0% | 948 | 948 |
| L0 | Execution time | 5 | 41,91 | 0,36 | 0,85% | 41,7 | 42,55 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 1,17 | 0,11 | 9,18% | 1,09 | 1,36 |
| L1 | Mean CPU in attack phase | 5 | 0,39 | 0,23 | 59,28% | 0,25 | 0,79 |
| L1 | Dataset rows | 5 | 379,6 | 119,85 | 31,57% | 326 | 594 |
| L1 | Execution time | 5 | 41,89 | 0,21 | 0,5% | 41,53 | 42,08 |
| L1 | Failure in attack phase | 5 | 98,89 | 2,48 | 2,51% | 94,44 | 100 |
| L1 | Censored p95 latency | 5 | 2.000,44 | 0,98 | 0,05% | 2.000 | 2.002,18 |
| L2 | Mean CPU in attack phase | 5 | 0,33 | 0,05 | 15,96% | 0,29 | 0,41 |
| L2 | Dataset rows | 5 | 326 | 0 | 0% | 326 | 326 |
| L2 | Execution time | 5 | 42,06 | 0,06 | 0,14% | 42 | 42,15 |
| L2 | Failure in attack phase | 5 | 100 | 0 | 0% | 100 | 100 |
| L2 | Censored p95 latency | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L3 | Mean CPU in attack phase | 5 | 0,34 | 0,06 | 18,09% | 0,28 | 0,44 |
| L3 | Dataset rows | 5 | 326 | 0 | 0% | 326 | 326 |
| L3 | Execution time | 5 | 42,15 | 0,1 | 0,25% | 42 | 42,26 |
| L3 | Failure in attack phase | 5 | 100 | 0 | 0% | 100 | 100 |
| L3 | Censored p95 latency | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |

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
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F3_v1_timeseries_coap_iot_coap_response_fuzz_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F3_v1_timeseries_coap_iot_coap_response_fuzz_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F3_v1_timeseries_coap_iot_coap_response_fuzz_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F3_v1_timeseries_coap_iot_coap_response_fuzz_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F5_resources_coap_iot_coap_response_fuzz_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F5_resources_coap_iot_coap_response_fuzz_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F4_v2_failrate_coap_iot_coap_response_fuzz_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F4_v2_failrate_coap_iot_coap_response_fuzz_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/coap-response-fuzz/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/iot_coap_response_fuzz`.
