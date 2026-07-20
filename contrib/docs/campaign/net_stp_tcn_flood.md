# STP TCN Flood (`net_stp_tcn_flood`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `net_stp_tcn_flood`. In the local catalog, the attack is described as: BPDU (Bridge Protocol Data Unit) packet flood with STP topology change information and random MAC addresses. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `net_stp_tcn_flood` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.1 L2/L3 |
| Target services | local network |
| Image | `attack-stp-tcn-flood:latest` |
| Container | `attack-stp-tcn-flood` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 5,29 / 6,81 | 5,02 | 9.552 (9.470-9.722) | 40 | 2/3 | 0,17% / 0,99% | 148,81 |
| L1 | http | 1 | 40 | 100% | 0% | 6,48 / 8,43 | 2,77 | 95.674 (95.674-95.674) | 40 | 2/3 | 5,26% / 64,73% | 150,04 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Dataset rows | 5 | 9.551,6 | 98,5 | 1,03% | 9.470 | 9.722 |
| L0 | Execution time | 5 | 40 | 0 | 0% | 40 | 40 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 6,81 | 0,78 | 11,44% | 5,73 | 7,8 |
| L0 | Mean CPU in attack phase | 5 | 0,17 | 0,05 | 29,26% | 0,12 | 0,23 |
| L1 | Dataset rows | 1 | 95.674 | 0 | 0% | 95.674 | 95.674 |
| L1 | Execution time | 1 | 40 | 0 | 0% | 40 | 40 |
| L1 | Failure in attack phase | 1 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 1 | 8,43 | 0 | 0% | 8,43 | 8,43 |
| L1 | Mean CPU in attack phase | 1 | 5,26 | 0 | 0% | 5,26 | 5,26 |

## Artifact Validation

No aggregated artifact validation table was found for this attack.

## Selected Figures

No aggregated figure was found in `reports/figs` for this attack.

## Sources Used

- Attack catalog: `docker/attackers/stp-tcn-flood/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/net_stp_tcn_flood`.
