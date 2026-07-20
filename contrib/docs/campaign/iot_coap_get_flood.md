# CoAP GET Flood (`iot_coap_get_flood`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `iot_coap_get_flood`. In the local catalog, the attack is described as: Burst of CoAP GET requests against the target CoAP/IoT service to overload the application layer. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `iot_coap_get_flood` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / CoAP |
| Target services | coap-server |
| Image | `attack-coap-get-flood:latest` |
| Container | `attack-coap-get-flood` |
| Catalog max runtime | 10 s |
| Intensity parameters | duration_s, count, delay_ms |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | coap | 5 | 194 | 100% | 0% | 13,96 / 32,24 | 0,21 | 925 (868-948) | 42 | 3/3 | 0,11% / 0,12% | 6,34 |
| L1 | coap | 5 | 200 | 100% | 0% | 0,99 / 6,05 | 4,97 | 24.948 (24.948-24.948) | 45,13 | 3/3 | 2,84% / 27,41% | 6,37 |
| L2 | coap | 5 | 200 | 100% | 0% | 1,2 / 12,18 | 4,97 | 24.948 (24.948-24.948) | 45,23 | 3/3 | 3,43% / 33,07% | 6,39 |
| L3 | coap | 5 | 200 | 100% | 0% | 1,15 / 1,62 | 4,97 | 24.948 (24.948-24.948) | 45,24 | 3/3 | 3,77% / 36,43% | 6,38 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,11 | 0,01 | 4,72% | 0,11 | 0,12 |
| L0 | Dataset rows | 5 | 925,2 | 35,2 | 3,8% | 868 | 948 |
| L0 | Execution time | 5 | 42 | 0,51 | 1,22% | 41,74 | 42,92 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 32,24 | 36,31 | 112,61% | 1,42 | 87,31 |
| L1 | Mean CPU in attack phase | 5 | 2,84 | 1,59 | 55,92% | 0,11 | 3,99 |
| L1 | Dataset rows | 5 | 24.948 | 0 | 0% | 24.948 | 24.948 |
| L1 | Execution time | 5 | 45,13 | 0,09 | 0,2% | 45,03 | 45,23 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 6,05 | 10,15 | 167,89% | 1,08 | 24,2 |
| L2 | Mean CPU in attack phase | 5 | 3,43 | 0,38 | 11,14% | 2,97 | 3,78 |
| L2 | Dataset rows | 5 | 24.948 | 0 | 0% | 24.948 | 24.948 |
| L2 | Execution time | 5 | 45,23 | 0,09 | 0,19% | 45,17 | 45,35 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 12,18 | 17,68 | 145,11% | 1,26 | 42,34 |
| L3 | Mean CPU in attack phase | 5 | 3,77 | 0,33 | 8,82% | 3,28 | 4,13 |
| L3 | Dataset rows | 5 | 24.948 | 0 | 0% | 24.948 | 24.948 |
| L3 | Execution time | 5 | 45,24 | 0,13 | 0,29% | 45,1 | 45,46 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 1,62 | 0,45 | 27,48% | 1,23 | 2,15 |

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
<td><img src="../../assets/campaign_doc/iot_coap_get_flood/F3_v1_timeseries_coap_iot_coap_get_flood_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_get_flood/F3_v1_timeseries_coap_iot_coap_get_flood_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_get_flood/F3_v1_timeseries_coap_iot_coap_get_flood_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_get_flood/F3_v1_timeseries_coap_iot_coap_get_flood_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_get_flood/F5_resources_coap_iot_coap_get_flood_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_get_flood/F5_resources_coap_iot_coap_get_flood_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_get_flood/F4_v2_failrate_coap_iot_coap_get_flood_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_get_flood/F4_v2_failrate_coap_iot_coap_get_flood_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/coap-get-flood/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/iot_coap_get_flood`.
