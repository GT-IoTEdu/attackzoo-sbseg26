<p align="center">
  <img src="./contrib/assets/attackzoo.png" width="666"/>
</p>
<p align="center">
  <a href="https://www.linux.org/"><img src="https://img.shields.io/badge/Linux-8d2b01?logo=Linux&logoColor=white" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-7ed321?logo=python&logoColor=white" /></a>
  <a href="https://docker.com/"><img src="https://img.shields.io/badge/Docker-257bd6?logo=docker&logoColor=white" /></a>
  <a href="https://www.sbseg2026.uff.br/chamadas/sf/"><img src="https://img.shields.io/badge/SBSeg2026-SF-blue" /></a>
  <img src="https://img.shields.io/badge/SeloD-41824a" /></a>
  <img src="https://img.shields.io/badge/SeloF-5b9de3" /></a>
  <img src="https://img.shields.io/badge/SeloS-d34e55" /></a>
  <img src="https://img.shields.io/badge/SeloR-e8aa3f" /></a>
  <a href="https://opensource.org/license/bsd-3-clause"><img src="https://img.shields.io/badge/BSD-License-003001.svg" /></a>
</p>

<a id="project-summary-and-artifact-scope"></a>

# AttackZoo: A Reproducible Testbed for Attack Execution and Network Traffic Datasets Generation

This repository contains **AttackZoo**, a Docker-based testbed for building and running controlled network, application, and IoT attack scenarios. The artifact automates target servers, benign clients, attack containers, traffic capture, feature extraction, dataset generation, and experiment reporting through both a command-line (CLI) interface and an optional Streamlit Web UI.

The associated paper, `"AttackZoo: A Reproducible Testbed for Attack Execution and Network Traffic Datasets Generation"` presents an environment for producing reproducible traffic evidence from parameterized Docker attacks. The artifact is intended to let reviewers inspect the testbed, run attacks in an isolated lab, capture PCAP files, extract traffic features, generate datasets, telemetry metrics, reports, charts and experimental campaigns metadata.

**Paper abstract**: _The recurring generation of network traffic datasets for cybersecurity research is constrained by fragmented experimental workflows, limited reproducibility, and restricted coverage of attack vectors. This paper presents AttackZoo, a reproducible testbed that integrates a containerized repository of 60 attacks categorized according to the MITRE ATT&CK framework and a CLI-centered orchestration layer, complemented by an optional Streamlit UI, that automates the full cycle of execution, data collection, and consolidation. The pipeline incorporates traffic capture, log inspection, and feature extraction using multiple tools, producing structured and traceable datasets. By providing broad coverage of attacks, techniques, and tactics among existing testbeds, AttackZoo reduces the operational overhead of experiments and enables the systematic generation of comparable datasets, with all artifacts openly available._

## README Structure

This document is organized as follows:

1. [Project summary and artifact scope](#project-summary-and-artifact-scope)
2. [This README Structure](#readme-structure)
3. [Artifact Badges Considered](#artifact-badges-considered)
4. [Basic environment information, components, and requirements](#basic-information)
5. [Dependencies and external resources used during installation](#dependencies)
6. [Safety and isolation guidance](#safety-considerations)
7. [Installation on a clean machine](#installation-process)
8. [Minimal validation test](#minimal-test)
9. [Reproducible experiment claims](#reproducible-experiment-claims)
10. [Additional documentation](#additional-documentation)
11. [License](#license)

## Artifact Badges Considered

The artifact is intended to support the following review badges:

- Available Artifacts: **`SeloD`** <img src="./contrib/assets/SeloD.png" width="23"/>
- Functional Artifacts: **`SeloF`** <img src="./contrib/assets/SeloF.png" width="23"/>
- Sustainable Artifacts: **`SeloS`** <img src="./contrib/assets/SeloS.png" width="23"/>
- Reproducible Experiments: **`SeloR`** <img src="./contrib/assets/SeloR.png" width="23"/>

## Basic Information

### Main Components

| Component | Location | Purpose |
| --- | --- | --- |
| Main CLI | `attackzoo.py` | Command-line entry point for the AttackZoo Testbed. |
| CLI parser and commands | `modules/attackzoo/` | Implementation of `status`, `list`, `run`, `stop`, `ps`, `logs`, `captures`, `features`, `dataset`, `experiment`, and `report`. |
| Reviewer claim scripts | `run_claim1.sh`, `run_claim2.sh`, `run_claim3.sh`, `run_claim_figures.sh` | One-command checks for the reproducible experiment claims and published dataset validation. |
| Dynamic attack catalog | `docker/attackers/*/attack.yaml` | Plug-and-play attack definitions loaded automatically by the tool. |
| Target servers | `docker/servers/` | Docker images for HTTP, SSH, SMB, MQTT, CoAP, XRCE-DDS, Zenoh, Telnet, and SSL/Heartbleed services. |
| Benign clients | `docker/clients/` | Containers that generate benign background traffic. |
| Web UI | `modules/attackzoo_st.py` | Streamlit interface for interactive use. |
| Helper scripts | `setup.sh`, `build.sh`, `servers.sh`, `clients.sh`, `environment.sh` | Dependency installation, Docker image builds, server/client control, environment control and Streamlit optional Web UI. |
| Outputs | `captures/`, `features/`, `datasets/`, `experiments/`, `logs/` | Artifacts generated during runs and experiments. |

### Current Catalog

The current repository contains 60 attacks declared through individual `attack.yaml` files.
The complete catalog coverage, category counts, and MITRE ATT&CK mapping are maintained in [contrib/docs/MITRE_ATTACK_MAPPING.md](contrib/docs/MITRE_ATTACK_MAPPING.md).

### Target Servers

| Server | Container | Host-exposed port(s) |
| --- | --- | --- |
| HTTP/DVWA | `server-http-server` | `8080/tcp -> 80/tcp` |
| SSH | `server-ssh-server` | `2222/tcp -> 22/tcp` |
| SMB/Samba | `server-smb-server` | `139/tcp`, `445/tcp`, `137/udp`, `138/udp` |
| MQTT/Mosquitto | `server-mqtt-broker` | `1883/tcp`, `9001/tcp` |
| CoAP | `server-coap-server` | `5683/tcp`, `5683/udp` |
| XRCE-DDS Agent | `server-xrce-dds-agent` | `8888/udp` |
| Zenoh Router | `server-zenoh-router` | `7447/tcp` |
| Telnet | `server-telnet-server` | `2323/tcp -> 23/tcp` |
| SSL/Heartbleed | `server-ssl-heartbleed` | `8443/tcp -> 443/tcp` |

>[!NOTE]
>More details about [Safety and port isolation guidance](#safety-considerations).

### Recommended Execution Environment

Environment used for local validation:

| Resource | Tested configuration |
| --- | --- |
| CPU | AMD Ryzen 5 5600X 6-Core Processor |
| Memory | 32 GB DDR4 |
| Storage | NVMe |
| Operating system | Ubuntu 24.04.4 LTS |
| Python | Python 3.12.3 with `venv` |
| Docker | Docker Engine 29.6.1; setup accepts Docker Engine 27.0 or newer |

>[!WARNING]
>**Minimum recommended environment for review:**

| Resource | Recommended minimum |
| --- | --- |
| Operating system | Ubuntu 24.04 LTS or a compatible Linux distribution with the `apt` package manager |
| Packages | Docker Engine 27.0 or newer and Python 3 |
| CPU | 4 vCPUs |
| Memory | 4 GB RAM for reduced tests; 8 GB for full experiment |
| Storage | 30 GB free for installation and images; 50 GB or more for PCAP captures and repeated standalone experiments; 250 GB or more for full Claim 3 reproduction |
| Network | Isolated environment, preferably a dedicated host or lab environment without direct Internet exposure |

## Dependencies

### System Dependencies

`setup.sh` installs and/or configures the main dependencies on Ubuntu/Debian-like systems:

- `ca-certificates`
- `curl`
- `git`
- `tree`
- `python3-venv`
- `tcpdump`
- `tshark`
- Docker Engine 27.0 or newer (`docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`)

Tested package versions on Ubuntu 24.04.4 LTS:

| Package | Tested version |
| --- | --- |
| `ca-certificates` | `20260601~24.04.1` |
| `curl` | `8.5.0-2ubuntu10.11` |
| `git` | `1:2.43.0-1ubuntu7.3` |
|`tree` | `2.1.1-2ubuntu3.24.04.2` |
| `python3-venv` | `3.12.3-0ubuntu2.1` |
| `tcpdump` | `4.99.4-3ubuntu4.24.04.1` |
| `tshark` | `4.2.2-1.1build3` |
| `docker-ce` | `5:29.6.1-1~ubuntu.24.04~noble` |
| `docker-ce-cli` | `5:29.6.1-1~ubuntu.24.04~noble` |
| `containerd.io` | `2.2.6-1~ubuntu.24.04~noble` |
| `docker-buildx-plugin` | `0.35.0-1~ubuntu.24.04~noble` |

>[!CAUTION]
>Please note that **this repository depends** on `Docker Engine` being installed as described in the [official documentation](https://docs.docker.com/engine/install/ubuntu/) and also on the [post-installation instructions for Linux](https://docs.docker.com/engine/install/linux-postinstall). Be advised that installation via `apt install` **might not be compatible**.

The script also adds the current user to the `docker` group, configures capture permissions for `tcpdump`, creates `.venv/`, installs Python dependencies, and installs NTLFlowLyzer Project directly from its GitHub repository at commit `86d0102466ea42ba03ddda5c649ac7e533fb25d9` by default.

### Python Dependencies

`requirements.txt` is frozen with exact versions from the validated `.venv`.
Primary runtime dependencies include:

```text
streamlit==1.58.0
pandas==3.0.4
numpy==2.5.0
matplotlib==3.11.0
scapy==2.7.0
PyYAML==6.0.3
```

The validated `.venv` also contains `NTLFlowLyzer==0.1.0`; `setup.sh` installs it separately from the upstream GitHub repository listed below.

### External Resources Used During Installation

- The official Docker repository for Ubuntu.
- Operating-system package indexes.
- PyPI for Python packages.
- `https://github.com/ahlashkari/NTLFlowLyzer.git` at commit `86d0102466ea42ba03ddda5c649ac7e533fb25d9`.
- Base images and packages referenced by Dockerfiles under `docker/`.
- Dozzle (`docker.io/amir20/dozzle`, pinned by digest) for the optional full-profile container log viewer.

>[!NOTE]
> The time required to complete the process may vary depending on the host's resources and the available internet speed.

## Safety Considerations

This artifact runs scanners, brute-force tools, fuzzers, floods, and other attack behaviors. **Use it only in an environment that you own, isolate, and are authorized to test.**

Safe review recommendations:

- Run the artifact on an isolated dedicated machine or disposable lab environment.
- Avoid installing the testbed on a workstation or shared host.
- Do not point attacks at external addresses, third-party networks, or services without explicit authorization.
- Prefer internal testbed targets, such as the `server-*` containers.
- Avoid exposing the host directly to the Internet during review.
- Check for port conflicts before starting servers.
- Use short durations for DoS/flood attacks during initial tests.
- Stop attack containers after validation with `python3 attackzoo.py stop <attack_id>` or `docker rm -f <container>`.
- The full image build starts Dozzle on host port `11080` and mounts `/var/run/docker.sock`. Access to that port should be treated as Docker host control; keep it inside the isolated lab and remove it with `docker rm -f suporte-dozzle` if it is not needed.

Ports that may be exposed on the host:
**TCP**: 139, 445, 1883, 2222, 2323, 5683, 7447, 8080, 8443, 9001, 11080.
**UDP**: 137, 138, 5683, 8888.

>[!NOTE]
> Weak passwords and intentionally vulnerable configurations in the containers are disposable lab values. Do not reuse them anywhere else.

## Installation process

### Demonstration video of the installation process

[![installation-process-video](contrib/assets/thumb.png)](https://www.youtube.com/watch?v=Jl6E-RwcYDA)

>[!TIP]
>This video demonstrates and follows all the steps listed below.

The steps below assume a **clean Ubuntu 24.04 LTS machine** or an equivalent environment.

### 1. Clone the repository and enters it

```bash
git clone git@github.com:GT-IoTEdu/attackzoo-sbseg26.git
cd attackzoo-sbseg26
```

### 2. Install system and Python dependencies with an _`one-script-setup`_

```bash
chmod +x setup.sh
./setup.sh dependencies
```

After installation, apply the new Docker group permission:

```bash
newgrp docker
```

>[!NOTE]
> This command will reload the shell session. It's mandatory to reload the current shell before continue.

_Logging out and back in also applies the group change._

### 3. Build the Docker Images Catalog and Start Servers

Here we have 2 options:
- A `Full Version`: (60 attackers, 9 servers, 2 client types and all dependencies); or
- A `Reduced Version`: (7 attackers, 3 servers and dependencies).

#### \*\* Full Version Installation \*\*

To evaluate all claims, it is necessary to install this full version.

>[!CAUTION]
> This builds all server, attacker, and client images, starts target servers, and other elements. The first build depends on machine and network speed: on a machine similar to the one previously described as the test environment used by the authors, **reserve 15 to 30 minutes** because many Docker images and packages will be downloaded and compiled.

```bash
./setup.sh full
```

#### \*\* Reduced Version Installation \*\* 

>[!TIP]
>For a faster reviewer demonstration, the repository provides this reduced profile with seven attacks, one from each catalog category, and only the HTTP, SSH, and MQTT target servers: yet they still manage to demonstrate all of the tool's capabilities. Even so, the installation typically takes **at least 2 to 5 minutes**. 

```bash
./setup.sh redux
```

The reduced testbed profile does not build benign client images. See [contrib/docs/REDUX_LAB.md](contrib/docs/REDUX_LAB.md) for more information about the included attack list, server profile, and campaign defaults.

### 4. Activate The Python Environment

```bash
cd /path/to/attackzoo-sbseg26
if [[ -z "${VIRTUAL_ENV}" ]]; then
  source .venv/bin/activate
fi
```

### 5. Simples Installation Check

```bash
python3 attackzoo.py status
```

Expected output: `docker_available=true`

>[!NOTE]
>If Docker is not accessible, check whether the service is running and whether Docker group permissions have been applied. See [Troubleshooting](contrib/docs/TROUBLESHOOTING.md) for common checks.

## Minimal Test

This section runs a short validation to confirm that the CLI loads the catalog, that target servers are active, and a simple attack can be launched against a testbed server.

### 1. Prepare The Session

```bash
cd /path/to/attackzoo-sbseg26
if [[ -z "${VIRTUAL_ENV}" ]]; then
  source .venv/bin/activate
fi
```

### 2. Confirm Docker And The Catalog

```bash
python3 attackzoo.py status
python3 attackzoo.py list --category "Denial"
```

Expected results:

- `docker_available=true`.
- A list of attacks from `6) Denial of Service and Impact`, including `dos_http_simple`.

### 3. Confirm That The HTTP Server Is Active

```bash
./servers.sh start
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep server-http-server
curl -I http://127.0.0.1:8080/
```

>[!IMPORTANT]
> If you installed the reduced version, pass `redux` as the second argument to `servers.sh`:
> `./servers.sh start redux`


Expected result:

- The `server-http-server` container is `Up`.
- The HTTP server responds through host port `8080`.

### 4. Run A Short HTTP Attack

Use the internal IP of the HTTP container and its internal port `80`:

```bash
HTTP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)
python3 attackzoo.py run dos_http_simple --target "$HTTP_IP" --port 80
```

Expected result:

```text
[OK] Container started: <container_id>
```

`dos_http_simple` is a one-shot attack: it sends a short burst of HTTP requests and exits on its own. To inspect active or previous attack containers:

```bash
python3 attackzoo.py ps
python3 attackzoo.py ps --all
```

### 5. Run A Short Baseline Experiment

This command validates the `experiment` workflow without launching a real attack by using only level `L0`:

```bash
python3 attackzoo.py experiment \
  --attack-id dos_http_simple \
  --out smoke_http \
  --runs 1 \
  --levels L0 \
  --warmup 3 \
  --attack 3 \
  --cooldown 3 \
  --probes http \
  --http-url http://127.0.0.1:8080/ \
  --iface lo \
  --bpf "tcp port 8080"
```

Expected outputs:

- `experiments/smoke_http/dos_http_simple/L0/run01/`.
- `probe_http.csv` with HTTP probe data.
- A `.pcap` file if `tcpdump` is installed and authorized.
- `experiments/smoke_http/reports/` with tables and charts when enough data is available.

Accepted availability probes for `--probes` are `http`, `https`, `ssh`, `smb`, `mqtt`, `coap`, `xrce`, `zenoh`, and `telnet`. Use `all` to enable all probes or `none` to disable them. For service-specific endpoints, repeat `--probe-endpoint`, for example `--probe-endpoint ssh=172.17.0.3:22`.

## Reproducible Experiment Claims

The claims below are automated reviewer checks. Run each command from the repository root after completing the installation and image build. Each script activates `.venv` automatically when it is available and prints a final comparison block.

For reduced installations, Claim 2 uses the HTTP subset and can be run with the default `ATTACKZOO_PROFILE=redux`. For a full installation, prefix the command with `ATTACKZOO_PROFILE=full`, for example `ATTACKZOO_PROFILE=full bash run_claim2.sh`.

Live traffic contains scheduler, Docker startup, TCP timing, and target-response variance; the reproducibility target is therefore the generated evidence shape and aggregate paper metrics, not byte-identical packet timing. See [Reproducibility notes](contrib/docs/REPRODUCIBILITY_NOTES.md) for the variance discussion, dataset audit trail, and dependency provenance.

### Claim 1: The Artifact Provides An Extensible Catalog Of Containerized Attacks

Goal: show that the CLI automatically discovers attacks declared in `docker/attackers/*/attack.yaml`, groups them by category, and exposes the expected JSON fields.

Configuration files to edit: none.

Command:

```bash
bash run_claim1.sh
```

Flags used:

- `attackzoo.py list --json` inside the script.

Expected time: less than 1 minute.

Expected resources: one Python process; less than 512 MB RAM; no Docker containers or new datasets.

Expected result:

```text
══════════════════════════════════════════════════════════════
Claim 1 — Attack catalog
Attacks in catalog  : 60
Categories          : 7
JSON fields         : yes
Expected result     : 60 attacks / 7 categories / JSON fields → OK
══════════════════════════════════════════════════════════════
```

### Claim 2: The Environment Runs Attacks Against Containerized Target Servers

Goal: demonstrate functional attack execution against a Dockerized HTTP target inside the testbed.

Configuration files to edit: none.

Command:

```bash
bash run_claim2.sh
```

Flags used:

- Optional environment flag: `ATTACKZOO_PROFILE=redux` by default, or `ATTACKZOO_PROFILE=full`.
- `attackzoo.py run dos_http_simple --target <server-ip> --port 80 --duration 3 --count 500 --concurrency 4 --delay_ms 50`.

Expected time: 1 to 5 minutes after images have already been built.

Expected resources: Docker daemon access, the HTTP server image and `dos_http_simple` attack image already built, host port `8080`, and less than 2 GB RAM during the short run.

Expected result:

```text
══════════════════════════════════════════════════════════════
Claim 2 — Execution against a Docker server
Docker available    : yes
HTTP server         : Up
Attack started      : yes
Attack stopped      : yes
Stop confirmation   : [OK] Stopped: attack-dos-http-simple
Expected result     : Docker + active HTTP server + executed attack → OK
══════════════════════════════════════════════════════════════
```

### Claim 3: Dataset Campaign Generation And Published Dataset Validation

Goal: provide a quick local reproducibility check that generates a tiny dataset campaign, and an optional full validation path for the published Figshare archive. The Figshare archive contains generated dataset CSVs under each attack's `datasets/` directory; it does not contain raw PCAP captures.

Configuration files to edit: none.

Quick local mini campaign, **default and recomended mode for evaluation purposes**:

```bash
bash run_claim3.sh
```
>[!TIP]
>This `mini` mode starts the HTTP server, runs a short `dos_http_simple` experiment for `L0,L1`, extracts Scapy features, builds datasets under `experiments/claim3_mini/dos_http_simple/datasets/`, generates local reports, and writes `contrib/reports/claim3_mini_dataset/manifest.json`. All process should finish under `1 minute`.

Full validation when the archive must be downloaded (from Figshare):

```bash
ATTACKZOO_CLAIM3_MODE=figshare ATTACKZOO_CONFIRM_LARGE_DOWNLOAD=1 bash run_claim3.sh
```

Full validation when the archive is already downloaded (from Figshare) or extracted:

```bash
ATTACKZOO_CLAIM3_MODE=figshare bash run_claim3.sh
```

>[!CAUTION]
>In `figshare` mode, the script resolves the Figshare DOI, downloads the archive when explicitly confirmed, verifies the MD5 checksum, unpacks it under `downloads/figshare/extracted/`, finds `all_5runs_4levels`, validates the `60 x 4 x 5` dataset matrix, and writes `contrib/reports/claim3_figshare_dataset/manifest.json`. This mode downloads about **16.9 GB** from Figshare Dataset archive (compressed) and needs roughly **225 GB** for the extraction process. Download and extraction time depend on network and disk speed and could takes more than `60 minutes`.

Flags used:

- Mode selector: `ATTACKZOO_CLAIM3_MODE=mini` by default, or `ATTACKZOO_CLAIM3_MODE=figshare`.
- Mini-mode environment flags: `ATTACKZOO_PROFILE`, `ATTACKZOO_CLAIM3_MINI_OUT`, `ATTACKZOO_CLAIM3_MINI_LEVELS`, `ATTACKZOO_CLAIM3_MINI_RUNS`, `ATTACKZOO_CLAIM3_MINI_WARMUP`, `ATTACKZOO_CLAIM3_MINI_ATTACK`, and `ATTACKZOO_CLAIM3_MINI_COOLDOWN`.
- Figshare-mode environment flags: `ATTACKZOO_CONFIRM_LARGE_DOWNLOAD`, `FIGSHARE_ARTICLE_ID`, `FIGSHARE_DOI`, `ATTACKZOO_FIGSHARE_DIR`, `ATTACKZOO_CLAIM3_CAMPAIGN_DIR`, and `ATTACKZOO_FIGSHARE_MIN_FREE_GB`.
- Shared validation flags: `ATTACKZOO_CLAIM3_REPORT`, `ATTACKZOO_EXPECTED_ATTACKS`, `ATTACKZOO_EXPECTED_LEVELS`, and `ATTACKZOO_EXPECTED_RUNS`.
- `run_claim_figures.sh` is kept as a compatibility alias and delegates to `ATTACKZOO_CLAIM3_MODE=figshare bash run_claim3.sh`, because the Figshare package is dataset-only.

Expected `mini` result:

```text
══════════════════════════════════════════════════════════════
Claim 3 — Mini local dataset campaign
Mode                : mini
Mini experiment     : experiments/claim3_mini
Attack              : dos_http_simple
Profile             : redux
Campaign directory  : experiments/claim3_mini
Attacks             : 1/1
Dataset CSVs        : 2/2
Readable CSV headers: 2/2
Missing level/runs  : 0
Raw PCAPs required  : no (2 generated locally)
Campaign reports    : yes
Manifest            : contrib/reports/claim3_mini_dataset/manifest.json
Expected result     : 1 attacks / 2 dataset CSVs / manifest OK → OK
══════════════════════════════════════════════════════════════
```

Expected `Full Figshare` result:

```text
══════════════════════════════════════════════════════════════
Claim 3 — Published Figshare datasets
Mode                : figshare
DOI Figshare        : 10.6084/m9.figshare.33023765
Compressed archive  : all_5runs_4levels_datasets.tar.gz
Campaign directory  : downloads/figshare/extracted/all_5runs_4levels
Attacks             : 60/60
Dataset CSVs        : 1200/1200
Readable CSV headers: 1200/1200
Missing level/runs  : 0
Raw PCAPs required  : no
Campaign reports    : <yes/no>
Manifest            : contrib/reports/claim3_figshare_dataset/manifest.json
Expected result     : 60 attacks / 1200 dataset CSVs / manifest OK → OK
══════════════════════════════════════════════════════════════
```

To regenerate traffic figures from raw captures, run a local campaign that preserves PCAPs and then use `contrib/scripts/campaign_traffic_stats.py` against that local campaign directory.

## Additional Documentation

- [CLI reference](contrib/docs/CLI.md)
- [Repository overview](contrib/docs/REPOSITORY_OVERVIEW.md)
- [Attack catalog maintenance and `attack.yaml` schema](contrib/docs/CATALOG_MAINTENANCE.md)
- [MITRE ATT&CK mapping](contrib/docs/MITRE_ATTACK_MAPPING.md)
- [Reduced reviewer lab profile](contrib/docs/REDUX_LAB.md)
- [Reproducibility notes](contrib/docs/REPRODUCIBILITY_NOTES.md)
- [Troubleshooting](contrib/docs/TROUBLESHOOTING.md)

## License

This project is licensed under the BSD 3-Clause License. See `LICENSE` in the repository root for the full terms.
