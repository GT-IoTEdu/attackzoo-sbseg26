# Contrib Scripts Reference

This document describes the scripts in `contrib/scripts/` at a high level. It focuses on what each script does, which option combinations are useful, and practical execution examples.

The examples assume they are run from the repository root:

```bash
cd /path/to/attackzoo
```

Files under `contrib/scripts/__pycache__/` are Python-generated artifacts and are not part of the operational interface documented here.

## Overview

| Script | Main use | Main outputs |
| --- | --- | --- |
| `run_full_campaign.py` | Orchestrate a guarded campaign across catalog attacks. | `experiments/<campaign>/`, `_campaign/campaign_config.json`, logs, PCAPs, features, datasets, and reports. |
| `run_redux_campaign.py` | Run a short campaign with seven representative attacks. | Same outputs as `run_full_campaign.py`, with reduced defaults. |
| `check_attack_smoke.py` | Quickly validate attack containers, entrypoints, parameters, and logs. | `contrib/reports/attack-smoke-<timestamp>/summary.md`, `results.json`, and per-attack logs. |
| `campaign_stats.py` | Summarize an existing campaign and optionally package datasets. | Statistics JSON under `datasets/` or a chosen directory; optional `.tar.gz`. |
| `campaign_traffic_stats.py` | Aggregate traffic statistics from PCAPs or `tshark` feature CSVs. | CSVs, `manifest.json`, per-PCAP cache, and PNGs under `contrib/reports/<campaign>/`. |

## `run_full_campaign.py`

`run_full_campaign.py` runs a complete or filtered campaign over the current attack catalog. It builds one plan per attack, starts target servers when configured, calls `attackzoo.py experiment`, generates reports, monitors disk usage and host load, and records a kill-switch file if any guardrail is exceeded.

This is the right script when you want to produce a reproducible experiment set under `experiments/<out>/`, with PCAPs, features, datasets, telemetry, and per-attack reports.

### What It Does

- Selects attacks from the catalog with `--only` and `--skip`.
- Automatically resolves target service, port, probes, and BPF per attack when possible.
- Starts or restarts servers with `servers.sh`.
- Runs `attackzoo.py experiment` for each planned attack.
- Optionally extracts features, builds datasets, and generates reports.
- Monitors directory guardrails, host load, and free disk space.
- Allows partially completed campaigns to be resumed with `--resume`.
- Saves configuration, catalog snapshot, logs, and per-attack results under `_campaign/`.

### Main Combinations

| Options | When to use |
| --- | --- |
| `--out`, `--runs`, `--levels`, `--warmup`, `--attack`, `--cooldown` | Define campaign identity and timing. |
| `--only`, `--skip`, `--server-profile` | Reduce scope to attack/server subsets. |
| `--dry-run` | Show the `attackzoo.py experiment` commands that would run, without requiring active Docker. |
| `--resume` | Skip attacks that already have `campaign_attack_result.json` with status `completed`. |
| `--stop-on-failure` | Stop the campaign on the first attack or report failure. |
| `--disk-limit-gb`, `--load-limit`, `--min-free-gb`, `--check-interval-s` | Control the kill switch and monitoring frequency. |
| `--extract-features` / `--no-extract-features`, `--feature-tools` | Enable/disable extraction and choose tools such as `ntlflowlyzer,tshark,scapy`. |
| `--build-dataset` / `--no-build-dataset`, `--generate-reports` / `--no-generate-reports` | Control dataset and report generation. |
| `--start-servers` / `--no-start-servers`, `--restart-servers`, `--stop-servers-on-exit` | Control the target server lifecycle. |
| `--iface`, `--bpf-mode`, `--bpf`, `--probes`, `--probe-host`, `--host-target` | Tune packet capture and service availability checks. |

### Examples

Inspect the plan for a small campaign without running containers:

```bash
python3 contrib/scripts/run_full_campaign.py \
  --out smoke_plan \
  --runs 1 \
  --levels L0,L1 \
  --warmup 5 \
  --attack 5 \
  --cooldown 5 \
  --only dos_http_simple,bf_ssh \
  --server-profile redux \
  --dry-run
```

Run a short campaign with feature, dataset, and report generation:

```bash
python3 contrib/scripts/run_full_campaign.py \
  --out smoke_campaign \
  --runs 1 \
  --levels L0,L1 \
  --warmup 5 \
  --attack 10 \
  --cooldown 5 \
  --only dos_http_simple,bf_ssh \
  --server-profile redux \
  --disk-limit-gb 20 \
  --load-limit 16 \
  --stop-on-failure
```

Resume an interrupted campaign while preserving already completed attacks:

```bash
python3 contrib/scripts/run_full_campaign.py \
  --out smoke_campaign \
  --runs 1 \
  --levels L0,L1 \
  --warmup 5 \
  --attack 10 \
  --cooldown 5 \
  --only dos_http_simple,bf_ssh \
  --server-profile redux \
  --resume
```

Capture all traffic without an automatic BPF filter:

```bash
python3 contrib/scripts/run_full_campaign.py \
  --out all_capture_campaign \
  --runs 1 \
  --levels L1 \
  --only web_simple_scanner \
  --bpf-mode all
```

Force a specific BPF and explicit HTTP probes:

```bash
python3 contrib/scripts/run_full_campaign.py \
  --out http_filtered_campaign \
  --only web_simple_scanner \
  --runs 1 \
  --levels L1 \
  --iface any \
  --bpf "tcp port 8080" \
  --probes http \
  --probe-host 127.0.0.1 \
  --host-target 127.0.0.1
```

Collect only PCAPs, without heavier post-processing:

```bash
python3 contrib/scripts/run_full_campaign.py \
  --out capture_only_campaign \
  --runs 1 \
  --levels L1 \
  --only dos_http_simple \
  --no-extract-features \
  --no-build-dataset \
  --no-generate-reports
```

## `run_redux_campaign.py`

`run_redux_campaign.py` is a wrapper around `run_full_campaign.py` with reduced defaults. It selects seven representative attacks, one per catalog category, uses `--server-profile redux`, runs only `L1`, performs one run per attack, and uses short timing windows.

Attacks included by default:

- `recon_arp_scan`
- `net_arp_spoof`
- `web_simple_scanner`
- `bf_ssh`
- `exf_icmp_tunnel`
- `dos_http_simple`
- `iot_mqtt_publisher`

### What It Does

- Generates a campaign name in the form `redux_campaign_<timestamp>`.
- Calls `run_full_campaign.py` with short defaults.
- Accepts the same options as `run_full_campaign.py`; user-provided arguments are appended after the defaults and can override scalar options.

### Main Combinations

| Options | When to use |
| --- | --- |
| No options | Run the default reduced campaign. |
| `--dry-run` | Inspect the reduced profile's commands and plans. |
| `--out` | Set a stable name for the reduced campaign. |
| `--runs`, `--levels`, `--attack`, `--warmup`, `--cooldown` | Increase or decrease the redux profile duration. |
| `--only` or `--skip` | Replace or restrict the wrapper's attack subset. |
| `--resume` | Resume a redux campaign with a fixed name. |

### Examples

Inspect the plan without running:

```bash
python3 contrib/scripts/run_redux_campaign.py --dry-run
```

Run the default reduced campaign:

```bash
python3 contrib/scripts/run_redux_campaign.py
```

Run with a fixed name and two repetitions:

```bash
python3 contrib/scripts/run_redux_campaign.py \
  --out redux_review \
  --runs 2
```

Run only two attacks from the reduced profile:

```bash
python3 contrib/scripts/run_redux_campaign.py \
  --out redux_web_dos \
  --only web_simple_scanner,dos_http_simple
```

Resume a named reduced campaign:

```bash
python3 contrib/scripts/run_redux_campaign.py \
  --out redux_review \
  --resume
```

## `check_attack_smoke.py`

`check_attack_smoke.py` runs smoke tests for attack containers. It resolves minimal parameters for each attack, runs `docker run -d`, waits for a short interval, collects logs, classifies obvious failures, and removes the container at the end.

Use this script after image rebuilds or changes to `attack.yaml`, Dockerfiles, and entrypoints. It does not replace a full campaign; its focus is quickly detecting image, argument, container input, and startup problems.

### What It Does

- Loads attacks from the Python catalog.
- Selects attacks by ID, category, or exclusion.
- Fills required parameters with conservative values.
- Allows global or per-attack parameter overrides.
- Detects patterns such as traceback, exception, command not found, permission denied, failed, and error.
- Writes a Markdown report, detailed JSON, and individual logs.

### Main Combinations

| Options | When to use |
| --- | --- |
| `--dry-run` | Validate parameter resolution and Docker commands without running containers. |
| `--attack`, `--skip`, `--category` | Choose exactly which attacks will be tested. |
| `--skip-local-link` | Avoid ARP/CDP/DHCP/STP/IPv6 local-link tests. |
| `--timeout-s`, `--docker-run-timeout-s`, `--logs-tail` | Adjust wait time, `docker run` timeout, and collected log volume. |
| `--target-ip`, `--target-net`, `--target-port`, `--spoof-gw`, `--text-value` | Set fallback values for required parameters. |
| `--intensity-duration-s`, `--intensity-count`, `--intensity-rate-pps`, `--intensity-concurrency`, `--intensity-threads`, `--intensity-delay-ms`, `--intensity-payload-size` | Control minimum test intensity. |
| `--param KEY=VALUE` | Override a parameter for every attack that has it. |
| `--attack-param ATTACK_ID:KEY=VALUE` | Override a parameter only for a specific attack. |
| `--fail-on-log-warnings` | Treat suspicious log lines as smoke test failures. |
| `--keep-containers` | Preserve containers for manual debugging. |
| `--out-dir` | Choose the report directory. |

### Examples

Generate commands without Docker:

```bash
python3 contrib/scripts/check_attack_smoke.py \
  --dry-run \
  --attack dos_http_simple \
  --attack bf_ssh
```

Test web attacks and fail on log warnings:

```bash
python3 contrib/scripts/check_attack_smoke.py \
  --category web \
  --skip-local-link \
  --fail-on-log-warnings \
  --timeout-s 8 \
  --logs-tail 200
```

Test one attack with a specific target and port:

```bash
python3 contrib/scripts/check_attack_smoke.py \
  --attack dos_http_simple \
  --target-ip 127.0.0.1 \
  --target-port 8080 \
  --intensity-duration-s 3
```

Apply global intensity overrides:

```bash
python3 contrib/scripts/check_attack_smoke.py \
  --skip-local-link \
  --param duration_s=2 \
  --param rate_pps=1 \
  --out-dir contrib/reports/smoke-low-intensity
```

Apply an attack-specific override:

```bash
python3 contrib/scripts/check_attack_smoke.py \
  --attack iot_mqtt_publisher \
  --attack-param iot_mqtt_publisher:target_port=1883 \
  --attack-param iot_mqtt_publisher:duration_s=4
```

Keep the container for inspection after the test:

```bash
python3 contrib/scripts/check_attack_smoke.py \
  --attack bf_ssh \
  --keep-containers
```

## `campaign_stats.py`

`campaign_stats.py` summarizes an existing campaign. It counts PCAPs and dataset CSVs, calculates time windows from metadata and filesystem timestamps, writes a JSON report, and can create a `.tar.gz` file containing all campaign datasets.

Use this script to produce high-level campaign statistics and prepare datasets for archiving or sharing.

### What It Does

- Reads `experiments/<campaign>/`.
- Counts `.pcap` files and CSVs under `*/datasets/*.csv`.
- Calculates total PCAP and dataset sizes.
- Estimates duration from the filesystem using `--first-attack` and `--last-attack`.
- Reads `campaign_attack_result.json`, `_campaign/campaign_config.json`, and `_campaign/campaign_finished.json` when available.
- Writes a statistics JSON file.
- Optionally packages datasets into `.tar.gz`, using `pigz` if available.

### Main Combinations

| Options | When to use |
| --- | --- |
| `--campaign-dir` | Choose the input campaign. |
| `--datasets-output-dir` | Choose where to write the JSON and `.tar.gz` file. |
| `--report-name`, `--archive-name` | Give outputs predictable names. |
| `--archive` | Create a `.tar.gz` file with dataset CSVs. |
| `--overwrite` | Replace an existing report or archive. |
| `--compresslevel 1-9` | Adjust gzip compression; `1` is faster, `9` compresses more. |
| `--progress-interval` | Control archive progress messages. |
| `--first-attack`, `--last-attack` | Adjust the filesystem-based time estimate. |

### Examples

Generate only the JSON report for the default campaign:

```bash
python3 contrib/scripts/campaign_stats.py
```

Generate a report for a named campaign in a specific directory:

```bash
python3 contrib/scripts/campaign_stats.py \
  --campaign-dir experiments/redux_review \
  --datasets-output-dir datasets/redux_review \
  --report-name redux_review_campaign_stats.json
```

Generate a report and package datasets:

```bash
python3 contrib/scripts/campaign_stats.py \
  --campaign-dir experiments/redux_review \
  --datasets-output-dir datasets/redux_review \
  --archive \
  --archive-name redux_review_datasets.tar.gz
```

Replace existing outputs and increase compression:

```bash
python3 contrib/scripts/campaign_stats.py \
  --campaign-dir experiments/redux_review \
  --datasets-output-dir datasets/redux_review \
  --archive \
  --overwrite \
  --compresslevel 6 \
  --progress-interval 50
```

Adjust the filesystem-estimated window:

```bash
python3 contrib/scripts/campaign_stats.py \
  --campaign-dir experiments/all_5runs_4levels \
  --first-attack bf_ssh \
  --last-attack web_xss_scanner
```

## `campaign_traffic_stats.py`

`campaign_traffic_stats.py` aggregates campaign traffic statistics from PCAPs or previously extracted `tshark` feature CSVs. It produces analytical CSVs, a per-PCAP cache, auxiliary tables, a manifest, and PNG figures.

Use this script after a campaign to answer questions such as: which protocols dominate, which ports appear most often, how PPS/Bps vary over time, how much traffic exists per category/level, and how many dataset rows were generated per category/level.

### What It Does

- Finds all `.pcap` files under `--campaign-dir`.
- For each PCAP, uses an existing `tshark` feature CSV when `--source auto` finds `*/features/tshark-<pcap-stem>.csv`.
- With `--source pcap`, processes PCAPs directly through the `tshark` binary.
- With `--source features`, requires existing feature CSVs.
- Maintains a cache under `file_summaries/`, invalidated by PCAP size and `mtime`.
- Generates CSVs for protocols, ports, per-second rates, per-file summaries, and category/level traffic.
- Reads `T8_artifact_summary.csv` and `T6_reexecution_stability.csv` from campaign reports when they exist.
- Generates figures with `matplotlib` and `pandas`, except when `--no-plots` is used.

### Generated Outputs

By default, outputs are written under `contrib/reports/<campaign-name>/`:

- `manifest.json`
- `file_summaries/*.json`
- `data/protocol_packet_counts.csv`
- `data/port_packet_counts.csv`
- `data/port_packet_counts_by_port.csv`
- `data/level_second_rates.csv`
- `data/campaign_second_rates.csv`
- `data/pcap_file_summaries.csv`
- `data/category_level_traffic.csv`
- `data/category_level_dataset_rows.csv`
- `data/<metric>_run_variability_by_level.csv`
- `tables/<metric>_run_variability_by_level.md`
- `figures/*.png`, when plots are enabled

### Main Combinations

| Options | When to use |
| --- | --- |
| `--campaign-dir`, `--reports-root`, `--campaign-name` | Control input and output directory. |
| `--source auto` | Prefer existing features and fall back to PCAP via `tshark` when needed. |
| `--source features` | Ensure the analysis uses only already generated `tshark` CSVs. |
| `--source pcap` | Reprocess PCAPs directly with `tshark`. |
| `--force` | Ignore the `file_summaries` cache and recalculate everything. |
| `--max-files` | Run a smoke test or small sample. |
| `--no-plots` | Produce only CSV/JSON, useful in environments without plotting dependencies. |
| `--plots` | Choose figures: `all`, `protocol`, `ports`, `pps`, `bps`, `heatmap`, `dataset_rows`. |
| `--top-ports`, `--top-protocols` | Adjust how many items appear in bar charts. |
| `--heatmap-metric` | Choose `byte_count`, `packet_count`, or `pcap_size_mb` for the category/level heatmap. |
| `--variability-metric` | Choose the metric from `T6_reexecution_stability.csv` for the textual variability table. |
| `--progress-interval` | Control progress messages per PCAP. |

### Examples

Generate complete statistics for the default campaign:

```bash
python3 contrib/scripts/campaign_traffic_stats.py
```

Analyze a specific campaign and save it under a stable report name:

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/redux_review \
  --campaign-name redux_review
```

Generate only CSV/JSON outputs, without PNGs:

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/redux_review \
  --campaign-name redux_review_csv_only \
  --no-plots
```

Run a quick five-PCAP sample and recalculate the cache:

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/redux_review \
  --campaign-name redux_review_sample \
  --max-files 5 \
  --force \
  --no-plots
```

Use only existing feature CSVs:

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/redux_review \
  --source features
```

Reprocess PCAPs directly through `tshark`:

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/redux_review \
  --source pcap \
  --force
```

Generate only protocol, port, and PPS charts:

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/redux_review \
  --plots protocol,ports,pps \
  --top-protocols 12 \
  --top-ports 20
```

Generate a heatmap by packet count:

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/redux_review \
  --plots heatmap \
  --heatmap-metric packet_count
```

Generate the dataset-row heatmap and a variability table for another metric:

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/redux_review \
  --plots dataset_rows \
  --variability-metric dataset_rows
```

## Practical Workflows Combining Scripts

### Validate Images Before A Campaign

```bash
python3 contrib/scripts/check_attack_smoke.py \
  --skip-local-link \
  --dry-run

python3 contrib/scripts/check_attack_smoke.py \
  --skip-local-link \
  --timeout-s 8 \
  --fail-on-log-warnings
```

The first command checks parameter resolution. The second actually runs containers and produces `summary.md` and `results.json`.

### Run A Redux Campaign And Summarize Artifacts

```bash
python3 contrib/scripts/run_redux_campaign.py \
  --out redux_review

python3 contrib/scripts/campaign_stats.py \
  --campaign-dir experiments/redux_review \
  --datasets-output-dir datasets/redux_review \
  --archive \
  --overwrite
```

This workflow generates experiments and then creates a statistics JSON file and a `.tar.gz` containing the datasets.

### Run A Short Campaign And Generate Traffic Figures

```bash
python3 contrib/scripts/run_full_campaign.py \
  --out short_http_campaign \
  --only dos_http_simple,web_simple_scanner \
  --server-profile redux \
  --runs 1 \
  --levels L0,L1 \
  --warmup 5 \
  --attack 10 \
  --cooldown 5

python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/short_http_campaign \
  --campaign-name short_http_campaign \
  --plots protocol,ports,pps,heatmap,dataset_rows
```

This workflow creates a small campaign and then generates CSVs and PNGs for traffic analysis.

### Reprocess Statistics Without Rerunning Attacks

```bash
python3 contrib/scripts/campaign_traffic_stats.py \
  --campaign-dir experiments/short_http_campaign \
  --campaign-name short_http_campaign_reprocessed \
  --source pcap \
  --force \
  --plots all
```

Use this when PCAPs already exist and you only want to recalculate aggregations or regenerate figures.

## Operational Dependencies

Some scripts call external tools depending on the selected mode:

- `run_full_campaign.py` and `run_redux_campaign.py`: Docker, `servers.sh`, `attackzoo.py`, and locally built servers/attacks.
- `check_attack_smoke.py`: Docker and available attack images.
- `campaign_stats.py`: standard Python; automatically uses `pigz` if installed to speed up compression.
- `campaign_traffic_stats.py`: `tshark` when `--source pcap` is used or when `--source auto` needs to fall back to PCAP; `matplotlib` and `pandas` for PNGs.

When the goal is only to validate arguments or planning, prefer `--dry-run` in scripts that support it.
