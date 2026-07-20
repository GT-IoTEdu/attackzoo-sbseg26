# XRCE-DDS Entity Flood (`iot_xrce_dds_entity_flood`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `iot_xrce_dds_entity_flood`. In the local catalog, the attack is described as: Mass creation of XRCE-DDS entities to consume session, memory, and control resources on the agent. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `iot_xrce_dds_entity_flood` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / XRCE-DDS |
| Target services | xrce-dds-agent |
| Image | `attack-xrce-dds-entity-flood:latest` |
| Container | `attack-xrce-dds-entity-flood` |
| Catalog max runtime | 10 s |
| Intensity parameters | duration_s |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | xrce | 5 | 100 | 100% | 0% | 500,81 / 501,13 | 0,05 | 234 (234-234) | 41,95 | 3/3 | 0,03% / 0,05% | 2,24 |
| L1 | xrce | 5 | 100 | 100% | 0% | 500,72 / 501,05 | 11,72 | 19.849 (14.604-24.212) | 44,64 | 3/3 | 238,33% / 1.306,79% | 1.302,53 |
| L2 | xrce | 5 | 100 | 100% | 0% | 500,7 / 500,77 | 10,64 | 18.411 (14.580-22.992) | 44,38 | 3/3 | 250,31% / 1.229,64% | 1.703,62 |
| L3 | xrce | 5 | 100 | 100% | 0% | 500,69 / 500,85 | 9,78 | 17.335 (15.228-19.604) | 44,16 | 3/3 | 254,18% / 1.387,37% | 1.750,07 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Mean CPU in attack phase | 5 | 0,03 | 0 | 14,53% | 0,03 | 0,04 |
| L0 | Dataset rows | 5 | 234 | 0 | 0% | 234 | 234 |
| L0 | Execution time | 5 | 41,95 | 0,37 | 0,87% | 41,71 | 42,59 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 501,13 | 0,28 | 0,06% | 500,75 | 501,49 |
| L1 | Mean CPU in attack phase | 5 | 238,33 | 29,17 | 12,24% | 191,81 | 262,89 |
| L1 | Dataset rows | 5 | 19.848,8 | 3.750,48 | 18,9% | 14.604 | 24.212 |
| L1 | Execution time | 5 | 44,64 | 0,59 | 1,32% | 43,94 | 45,46 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 501,05 | 0,19 | 0,04% | 500,81 | 501,26 |
| L2 | Mean CPU in attack phase | 5 | 250,31 | 12,41 | 4,96% | 240,14 | 271,78 |
| L2 | Dataset rows | 5 | 18.410,8 | 3.344,91 | 18,17% | 14.580 | 22.992 |
| L2 | Execution time | 5 | 44,38 | 0,46 | 1,03% | 43,76 | 44,94 |
| L2 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 5 | 500,77 | 0,01 | 0% | 500,76 | 500,79 |
| L3 | Mean CPU in attack phase | 5 | 254,18 | 10,18 | 4% | 238,2 | 263,26 |
| L3 | Dataset rows | 5 | 17.334,8 | 1.985,4 | 11,45% | 15.228 | 19.604 |
| L3 | Execution time | 5 | 44,16 | 0,3 | 0,67% | 43,82 | 44,45 |
| L3 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L3 | Censored p95 latency | 5 | 500,85 | 0,13 | 0,03% | 500,7 | 501,02 |

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
<td><img src="../../assets/campaign_doc/iot_xrce_dds_entity_flood/F3_v1_timeseries_xrce_iot_xrce_dds_entity_flood_L0_run01.png" alt="Time series L0 run01" width="420"><br><sub>Time series L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_entity_flood/F3_v1_timeseries_xrce_iot_xrce_dds_entity_flood_L1_run01.png" alt="Time series L1 run01" width="420"><br><sub>Time series L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_entity_flood/F3_v1_timeseries_xrce_iot_xrce_dds_entity_flood_L2_run01.png" alt="Time series L2 run01" width="420"><br><sub>Time series L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_entity_flood/F3_v1_timeseries_xrce_iot_xrce_dds_entity_flood_L3_run01.png" alt="Time series L3 run01" width="420"><br><sub>Time series L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_entity_flood/F5_resources_xrce_iot_xrce_dds_entity_flood_L0_run01.png" alt="Resources L0 run01" width="420"><br><sub>Resources L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_entity_flood/F5_resources_xrce_iot_xrce_dds_entity_flood_L3_run01.png" alt="Resources L3 run01" width="420"><br><sub>Resources L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_entity_flood/F4_v2_failrate_xrce_iot_xrce_dds_entity_flood_L0.png" alt="Failure rate L0" width="420"><br><sub>Failure rate L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_entity_flood/F4_v2_failrate_xrce_iot_xrce_dds_entity_flood_L3.png" alt="Failure rate L3" width="420"><br><sub>Failure rate L3</sub></td>
</tr>
</table>

## Sources Used

- Attack catalog: `docker/attackers/xrce-dds-entity-flood/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/iot_xrce_dds_entity_flood`.
