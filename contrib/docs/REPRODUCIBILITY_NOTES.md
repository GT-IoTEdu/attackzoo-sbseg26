# Reproducibility Notes

This document records the operational assumptions behind the reproducible-experiment claims in the root `README.md`.

## Official Review Mapping

The root `README.md` follows the SBSeg artifact template: each claim lists the command, flags, expected time, expected resources, and expected result. The scripts `run_claim1.sh`, `run_claim2.sh`, `run_claim3.sh`, and `run_claim_figures.sh` are the reviewer-facing entry points.

## Stochastic Traffic And Variance

AttackZoo executes live network traffic inside Docker containers. Some packet timing, TCP state, scheduler timing, Docker startup latency, and target response timing are inherently stochastic and are not controlled by a single global random seed. For that reason, exact packet timing should not be interpreted as the reproducibility target.

The reproducibility target is the generated evidence shape and the aggregate paper metrics:

- the attack catalog and category structure;
- successful target-server and attack-container orchestration;
- PCAP, feature, dataset, and report generation;
- the published full-campaign dataset counts and aggregate documentation.

The full campaign used five runs for each attack-level pair where supported. The campaign documentation reports per-level means, min/max values, and coefficient-of-variation tables to make run-to-run variability explicit.

## Published Dataset Audit Trail

The full raw campaign is intentionally not versioned in Git because it is too large. The published Figshare archive contains the generated datasets from that campaign, not the raw PCAP captures:

- DOI: `10.6084/m9.figshare.33023765`
- Archive: `attackzoo-full_campaign_5runs_4levels.tar.gz`
- Compressed size: `16.9 GB`
- Expected extracted campaign: `60` attacks and `1200` dataset CSV files under `*/datasets/*.csv`

`run_claim3.sh` supports two modes. The default `mini` mode runs a short local `dos_http_simple` campaign, generates PCAPs, Scapy features, dataset CSVs, reports, and writes `contrib/reports/claim3_mini_dataset/manifest.json`. The explicit `figshare` mode resolves the Figshare metadata through the public API, verifies the archive MD5 provided by Figshare, requires the extracted campaign to contain exactly `1200` generated dataset CSVs, validates the expected four levels and five runs per attack, and writes `contrib/reports/claim3_figshare_dataset/manifest.json`.

## Reduced Versus Complete Paths

`run_claim3.sh` is the quick reviewer path by default. It proves the local generation pipeline at reduced scale and validates that the resulting campaign has the same dataset-directory shape as the published package.

`ATTACKZOO_CLAIM3_MODE=figshare bash run_claim3.sh` is the published-dataset audit path. It validates the public Figshare dataset package without requiring Docker, `tcpdump`, or raw PCAP captures. `run_claim_figures.sh` is kept as a compatibility alias for older instructions and delegates to that Figshare mode. To regenerate traffic figures from raw captures, run a local campaign that preserves PCAP files and use `contrib/scripts/campaign_traffic_stats.py` against that local campaign directory.

## Dependency Provenance

Python dependencies are pinned in `requirements.txt`. Docker base images that previously used mutable `latest` references are pinned by digest. NTLFlowLyzer is installed from the upstream Git repository at commit `d99cd5377faaed53b39450ce262652902501188d` by default; override `NTLFLOWLYZER_REF` only when intentionally testing another revision.

Local validation after the artifact cleanup used Ubuntu 24.04.4 LTS, Linux `6.8.0-134-generic`, Python `3.12.3`, and Docker Engine `29.6.1`. The setup accepts Docker Engine `27.0` or newer.
