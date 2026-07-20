# IPv6 MLD Flood (`net_ipv6_mld_flood`)

[Campaign index](README.md)

This document summarizes the published campaign execution of attack `net_ipv6_mld_flood`. In the local catalog, the attack is described as: ICMPv6 Multicast Listener Report MLD (131) flood on the local network. The full execution artifacts are not versioned in this repository; retrieve the generated dataset CSVs from the Figshare dataset linked in the campaign index. Raw PCAP captures are not included in that archive. The selected figures below are stored under `contrib/assets/campaign_doc`.

## Attack Metadata

| Field | Value |
| --- | --- |
| ID | `net_ipv6_mld_flood` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.2 IPv6 |
| Target services | local IPv6 network |
| Image | `attack-ipv6-mld-flood:latest` |
| Container | `attack-ipv6-mld-flood` |
| Catalog max runtime | 10 s |
| Intensity parameters | n/a |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Statistical Summary by Level

| Level | Service | Runs | Attack samples | Mean success | Mean failure | Lat p50/p95 ms | Total PCAP MB | Mean dataset (min-max) | Mean exec s | Extractors ok/total | Mean/max CPU | Mean mem MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,84 / 6,32 | 9,64 | 18.084 (11.370-20.238) | 40 | 2/3 | 0,32% / 1,44% | 153,86 |
| L1 | http | 5 | 200 | 100% | 0% | 4,83 / 6,36 | 3.917,75 | 15.228.693 (13.952.550-17.001.768) | 40 | 2/3 | 7,76% / 9,57% | 122,47 |
| L2 | http | 4 | 160 | 100% | 0% | 4,87 / 6,97 | 3.367,33 | 16.336.531 (15.818.810-16.750.290) | 40 | 2/3 | 7,68% / 8,77% | 116,12 |

## Stability Across Reruns

| Level | Metric | Runs | Mean | Deviation | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Dataset rows | 5 | 18.084,4 | 3.367,82 | 18,62% | 11.370 | 20.238 |
| L0 | Execution time | 5 | 40 | 0 | 0% | 40 | 40 |
| L0 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L0 | Censored p95 latency | 5 | 6,32 | 0,21 | 3,26% | 5,99 | 6,61 |
| L0 | Mean CPU in attack phase | 5 | 0,32 | 0,05 | 16,55% | 0,25 | 0,38 |
| L1 | Dataset rows | 5 | 15.228.692,8 | 1.034.970,63 | 6,8% | 13.952.550 | 17.001.768 |
| L1 | Execution time | 5 | 40 | 0 | 0% | 40 | 40 |
| L1 | Failure in attack phase | 5 | 0 | 0 | n/a | 0 | 0 |
| L1 | Censored p95 latency | 5 | 6,36 | 0,77 | 12,17% | 5,41 | 7,51 |
| L1 | Mean CPU in attack phase | 5 | 7,76 | 0,45 | 5,85% | 7,4 | 8,57 |
| L2 | Dataset rows | 4 | 16.336.531 | 415.821,61 | 2,55% | 15.818.810 | 16.750.290 |
| L2 | Execution time | 4 | 40 | 0 | 0% | 40 | 40 |
| L2 | Failure in attack phase | 4 | 0 | 0 | n/a | 0 | 0 |
| L2 | Censored p95 latency | 4 | 6,97 | 0,79 | 11,39% | 6,15 | 8,08 |
| L2 | Mean CPU in attack phase | 4 | 7,68 | 0,09 | 1,16% | 7,54 | 7,78 |

## Artifact Validation

No aggregated artifact validation table was found for this attack.

## Selected Figures

No aggregated figure was found in `reports/figs` for this attack.

## Sources Used

- Attack catalog: `docker/attackers/ipv6-mld-flood/attack.yaml`
- Full campaign artifacts: available from the Figshare dataset linked in the campaign index; when extracted locally, expected under `experiments/all_5runs_4levels/net_ipv6_mld_flood`.
