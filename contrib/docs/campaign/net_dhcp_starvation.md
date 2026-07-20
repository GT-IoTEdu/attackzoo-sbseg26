# DHCP Starvation (`net_dhcp_starvation`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `net_dhcp_starvation`. In the local catalog, the attack is described as: DHCP lease exhaustion on the local network. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `net_dhcp_starvation` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.1 L2/L3 |
| Target services | local network |
| Image | `attack-dhcp-starvation:latest` |
| Container | `attack-dhcp-starvation` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 5,66 / 6,87 | 5,51 | 10.304 (10.072-10.796) | 40 | 2/3 | 0,27% / 1,06% | 137,99 |
| L1 | http | 2 | 80 | 100% | 0% | 6,35 / 7,34 | 14,64 | 53.796 (12.848-94.744) | 40 | 2/3 | 2,41% / 28,74% | 140,07 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Dataset rows | 5 | 10.303,6 | 261,34 | 2,54% | 10.072 | 10.796 |
| L0 | Execution time | 5 | 40 | 0 | 0% | 40 | 40 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 6,87 | 0,47 | 6,87% | 6,32 | 7,69 |
| L0 | Mean CPU in attack phase | 5 | 0,27 | 0,06 | 20,37% | 0,22 | 0,35 |
| L1 | Dataset rows | 2 | 53.796 | 40.948 | 76,12% | 12.848 | 94.744 |
| L1 | Execution time | 2 | 40 | 0 | 0% | 40 | 40 |
| L1 | Failure in attack phase | 2 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 2 | 7,34 | 0,19 | 2,64% | 7,15 | 7,53 |
| L1 | Mean CPU in attack phase | 2 | 2,41 | 0,61 | 25,27% | 1,8 | 3,02 |

## Artifact Validation

No aggregated artifact validation table was found for this attack.

## Selected Figures

No aggregated figure was found in `reports/figs` for this attack.

## Sources Used

- Attack catalog: `docker/attackers/dhcp-starvation/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/net_dhcp_starvation`.
