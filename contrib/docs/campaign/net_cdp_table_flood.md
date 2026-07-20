# CDP Table Flood (`net_cdp_table_flood`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `net_cdp_table_flood`. In the local catalog, the attack is described as: CDP (Cisco Discovery Protocol) table flood on the local network. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `net_cdp_table_flood` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.1 L2/L3 |
| Target services | local network |
| Image | `attack-cdp-table-flood:latest` |
| Container | `attack-cdp-table-flood` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 199 | 100% | 0% | 5,33 / 17,74 | 44,28 | 39.466 (39.162-40.060) | 40 | 2/3 | 1,27% / 2,3% | 117,25 |
| L1 | http | 1 | 40 | 100% | 0% | 5 / 22,02 | 8,82 | 39.366 (39.366-39.366) | 40 | 2/3 | 5,47% / 57,73% | 118,42 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Dataset rows | 5 | 39.466,4 | 331,3 | 0,84% | 39.162 | 40.060 |
| L0 | Execution time | 5 | 40 | 0 | 0% | 40 | 40 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 17,74 | 5,37 | 30,29% | 7,17 | 21,76 |
| L0 | Mean CPU in attack phase | 5 | 1,27 | 0,1 | 7,55% | 1,16 | 1,42 |
| L1 | Dataset rows | 1 | 39.366 | 0 | 0% | 39.366 | 39.366 |
| L1 | Execution time | 1 | 40 | 0 | 0% | 40 | 40 |
| L1 | Failure in attack phase | 1 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 1 | 22,02 | 0 | 0% | 22,02 | 22,02 |
| L1 | Mean CPU in attack phase | 1 | 5,47 | 0 | 0% | 5,47 | 5,47 |

## Artifact Validation

No aggregated artifact validation table was found for this attack.

## Selected Figures

No aggregated figure was found in `reports/figs` for this attack.

## Sources Used

- Attack catalog: `docker/attackers/cdp-table-flood/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/net_cdp_table_flood`.
