#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

CLAIM3_MODE="${1:-${ATTACKZOO_CLAIM3_MODE:-mini}}"
CLAIM3_MODE="${CLAIM3_MODE,,}"

FIGSHARE_ARTICLE_ID="${FIGSHARE_ARTICLE_ID:-33023765}"
FIGSHARE_DOI="${FIGSHARE_DOI:-10.6084/m9.figshare.33023765}"
FIGSHARE_API="https://api.figshare.com/v2/articles/${FIGSHARE_ARTICLE_ID}"
DATA_DIR="${ATTACKZOO_FIGSHARE_DIR:-downloads/figshare}"
EXTRACT_DIR="${DATA_DIR}/extracted"
CAMPAIGN_OVERRIDE="${ATTACKZOO_CLAIM3_CAMPAIGN_DIR:-}"
REQUIRED_FREE_GB="${ATTACKZOO_FIGSHARE_MIN_FREE_GB:-260}"

PROFILE="${ATTACKZOO_PROFILE:-redux}"
MINI_OUT="${ATTACKZOO_CLAIM3_MINI_OUT:-claim3_mini}"
MINI_ATTACK_ID="${ATTACKZOO_CLAIM3_MINI_ATTACK_ID:-dos_http_simple}"
MINI_SERVICE="${ATTACKZOO_CLAIM3_MINI_SERVICE:-http}"
MINI_LEVELS="${ATTACKZOO_CLAIM3_MINI_LEVELS:-L0,L1}"
MINI_RUN_COUNT="${ATTACKZOO_CLAIM3_MINI_RUNS:-1}"
MINI_WARMUP="${ATTACKZOO_CLAIM3_MINI_WARMUP:-2}"
MINI_ATTACK="${ATTACKZOO_CLAIM3_MINI_ATTACK:-3}"
MINI_COOLDOWN="${ATTACKZOO_CLAIM3_MINI_COOLDOWN:-2}"
MINI_INTERVAL="${ATTACKZOO_CLAIM3_MINI_INTERVAL:-0.5}"
MINI_ATTACK_COUNT="${ATTACKZOO_CLAIM3_MINI_ATTACK_COUNT:-500}"
MINI_CONCURRENCY="${ATTACKZOO_CLAIM3_MINI_CONCURRENCY:-4}"
MINI_DELAY_MS="${ATTACKZOO_CLAIM3_MINI_DELAY_MS:-10}"

REPORT_NAME=""
REPORT_DIR=""
SUMMARY_TITLE=""
EXPECTED_ATTACKS="0"
EXPECTED_LEVELS=""
EXPECTED_RUNS=""
EXPECTED_DATASETS="0"
LINE="══════════════════════════════════════════════════════════════"

archive_name=""
archive_size="0"
archive_md5=""
download_url=""
campaign_dir=""
attacks_done="0"
datasets_done="0"
datasets_ok="0"
pcaps_found="0"
missing_combos="0"
reports_status="no"
report_status="no"
result="FAILED"

csv_count() {
    local value="$1"
    local count=0
    local item
    IFS=',' read -ra items <<< "${value}"
    for item in "${items[@]}"; do
        item="${item//[[:space:]]/}"
        if [[ -n "${item}" ]]; then
            count=$((count + 1))
        fi
    done
    printf '%s' "${count}"
}

runs_csv() {
    local total="$1"
    local out=""
    local index
    local run_id
    for index in $(seq 1 "${total}"); do
        printf -v run_id 'run%02d' "${index}"
        out="${out:+${out},}${run_id}"
    done
    printf '%s' "${out}"
}

configure_mode() {
    local level_count
    local run_count

    case "${CLAIM3_MODE}" in
        mini)
            SUMMARY_TITLE="Mini local dataset campaign"
            REPORT_NAME="${ATTACKZOO_CLAIM3_REPORT:-claim3_mini_dataset}"
            EXPECTED_ATTACKS="${ATTACKZOO_EXPECTED_ATTACKS:-1}"
            EXPECTED_LEVELS="${ATTACKZOO_EXPECTED_LEVELS:-${MINI_LEVELS}}"
            EXPECTED_RUNS="${ATTACKZOO_EXPECTED_RUNS:-$(runs_csv "${MINI_RUN_COUNT}")}"
            ;;
        figshare|full)
            CLAIM3_MODE="figshare"
            SUMMARY_TITLE="Published Figshare datasets"
            REPORT_NAME="${ATTACKZOO_CLAIM3_REPORT:-claim3_figshare_dataset}"
            EXPECTED_ATTACKS="${ATTACKZOO_EXPECTED_ATTACKS:-60}"
            EXPECTED_LEVELS="${ATTACKZOO_EXPECTED_LEVELS:-L0,L1,L2,L3}"
            EXPECTED_RUNS="${ATTACKZOO_EXPECTED_RUNS:-run01,run02,run03,run04,run05}"
            ;;
        *)
            printf '[ERROR] Unsupported Claim 3 mode: %s\n' "${CLAIM3_MODE}" >&2
            printf 'Use ATTACKZOO_CLAIM3_MODE=mini or ATTACKZOO_CLAIM3_MODE=figshare.\n' >&2
            exit 2
            ;;
    esac

    REPORT_DIR="contrib/reports/${REPORT_NAME}"
    level_count="$(csv_count "${EXPECTED_LEVELS}")"
    run_count="$(csv_count "${EXPECTED_RUNS}")"
    EXPECTED_DATASETS=$((EXPECTED_ATTACKS * level_count * run_count))
}

print_summary() {
    printf '%s\n' "${LINE}"
    printf 'Claim 3 — %s\n' "${SUMMARY_TITLE:-not configured}"
    printf 'Mode                : %s\n' "${CLAIM3_MODE}"
    if [[ "${CLAIM3_MODE}" == "figshare" ]]; then
        printf 'DOI Figshare        : %s\n' "${FIGSHARE_DOI}"
        printf 'Compressed archive  : %s\n' "${archive_name:-not resolved}"
    else
        printf 'Mini experiment     : experiments/%s\n' "${MINI_OUT}"
        printf 'Attack              : %s\n' "${MINI_ATTACK_ID}"
        printf 'Profile             : %s\n' "${PROFILE}"
    fi
    printf 'Campaign directory  : %s\n' "${campaign_dir:-not found}"
    printf 'Attacks             : %s/%s\n' "${attacks_done}" "${EXPECTED_ATTACKS}"
    printf 'Dataset CSVs        : %s/%s\n' "${datasets_done}" "${EXPECTED_DATASETS}"
    printf 'Readable CSV headers: %s/%s\n' "${datasets_ok}" "${EXPECTED_DATASETS}"
    printf 'Missing level/runs  : %s\n' "${missing_combos}"
    printf 'Raw PCAPs required  : no'
    if [[ "${pcaps_found}" != "0" ]]; then
        printf ' (%s generated locally)' "${pcaps_found}"
    fi
    printf '\n'
    printf 'Campaign reports    : %s\n' "${reports_status}"
    printf 'Manifest            : %s\n' "${report_status}"
    printf 'Expected result     : %s attacks / %s dataset CSVs / manifest OK → %s\n' "${EXPECTED_ATTACKS}" "${EXPECTED_DATASETS}" "${result}"
    printf '%s\n' "${LINE}"
}

fail() {
    printf '[ERROR] %s\n' "$*" >&2
    print_summary
    exit 1
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || fail "Required command is missing: $1"
}

require_image() {
    local image="$1"
    docker image inspect "${image}:latest" >/dev/null 2>&1 || \
        fail "Missing image: ${image}:latest. Run ./build.sh redux or ./build.sh full before this claim."
}

activate_venv_if_available() {
    if [[ -z "${VIRTUAL_ENV:-}" && -f ".venv/bin/activate" ]]; then
        source ".venv/bin/activate"
    fi
}

free_gib() {
    local path="$1"
    df -Pk "${path}" | awk 'NR == 2 { printf "%.0f", $4 / 1024 / 1024 }'
}

check_free_space() {
    mkdir -p "${DATA_DIR}"
    local available_gib
    available_gib="$(free_gib "${DATA_DIR}")"
    if (( available_gib < REQUIRED_FREE_GB )); then
        fail "Not enough free space under ${DATA_DIR}: ${available_gib} GiB available; ${REQUIRED_FREE_GB} GiB recommended."
    fi
}

resolve_figshare_metadata() {
    mapfile -t metadata < <(python3 - "${FIGSHARE_API}" <<'PY'
import json
import sys
import urllib.request

url = sys.argv[1]
with urllib.request.urlopen(url, timeout=60) as response:
    payload = json.load(response)

files = payload.get("files") or []
if not files:
    raise SystemExit("Figshare article has no files")

file_info = files[0]
print(file_info.get("name", ""))
print(file_info.get("size", 0))
print(file_info.get("supplied_md5") or file_info.get("computed_md5") or "")
print(file_info.get("download_url", ""))
PY
    )
    archive_name="${metadata[0]}"
    archive_size="${metadata[1]}"
    archive_md5="${metadata[2]}"
    download_url="${metadata[3]}"

    [[ -n "${archive_name}" ]] || fail "Figshare file name was not resolved."
    [[ -n "${download_url}" ]] || fail "Figshare download URL was not resolved."
}

dataset_count_for_dir() {
    local path="$1"
    if [[ ! -d "${path}" ]]; then
        printf '0'
        return
    fi
    find "${path}" -type f -path '*/datasets/*.csv' | wc -l | tr -d ' '
}

find_figshare_campaign_dir() {
    if [[ -n "${CAMPAIGN_OVERRIDE}" ]]; then
        campaign_dir="${CAMPAIGN_OVERRIDE}"
        return
    fi

    local candidate
    local first_existing=""
    local -a candidates=(
        "${EXTRACT_DIR}/all_5runs_4levels"
        "experiments/all_5runs_4levels"
    )

    while IFS= read -r candidate; do
        candidates+=("${candidate}")
    done < <(find "${EXTRACT_DIR}" "experiments" -type d -name "all_5runs_4levels" -print 2>/dev/null || true)

    for candidate in "${candidates[@]}"; do
        [[ -d "${candidate}" ]] || continue
        if [[ -z "${first_existing}" ]]; then
            first_existing="${candidate}"
        fi
        if [[ "$(dataset_count_for_dir "${candidate}")" == "${EXPECTED_DATASETS}" ]]; then
            campaign_dir="${candidate}"
            return
        fi
    done

    campaign_dir="${first_existing}"
}

download_archive() {
    local archive_path="${DATA_DIR}/${archive_name}"
    if [[ "${ATTACKZOO_CONFIRM_LARGE_DOWNLOAD:-0}" != "1" && ! -f "${archive_path}" ]]; then
        fail "This step downloads a large published dataset archive. Run it with ATTACKZOO_CONFIRM_LARGE_DOWNLOAD=1, or set ATTACKZOO_CLAIM3_CAMPAIGN_DIR to an already extracted campaign."
    fi

    check_free_space

    if [[ -f "${archive_path}" ]] && [[ "$(stat -c '%s' "${archive_path}")" == "${archive_size}" ]]; then
        printf '[INFO] Reusing existing archive: %s\n' "${archive_path}"
    else
        printf '[INFO] Downloading %s from Figshare...\n' "${archive_name}"
        curl -L --fail --continue-at - --output "${archive_path}" "${download_url}"
    fi

    if [[ -n "${archive_md5}" ]]; then
        printf '%s  %s\n' "${archive_md5}" "${archive_path}" | md5sum -c - >/dev/null || \
            fail "MD5 verification failed for ${archive_path}."
    fi
}

extract_archive_if_needed() {
    local archive_path="${DATA_DIR}/${archive_name}"
    mkdir -p "${EXTRACT_DIR}"
    find_figshare_campaign_dir

    if [[ -n "${campaign_dir}" && -d "${campaign_dir}" ]] && [[ "$(dataset_count_for_dir "${campaign_dir}")" == "${EXPECTED_DATASETS}" ]]; then
        printf '[INFO] Reusing existing extracted dataset campaign: %s\n' "${campaign_dir}"
        return
    fi

    check_free_space
    printf '[INFO] Extracting %s under %s...\n' "${archive_path}" "${EXTRACT_DIR}"
    tar -xzf "${archive_path}" -C "${EXTRACT_DIR}"
    find_figshare_campaign_dir
    [[ -n "${campaign_dir}" && -d "${campaign_dir}" ]] || fail "Directory all_5runs_4levels was not found after extraction."
}

prepare_figshare_campaign() {
    local dataset_count

    mkdir -p "${EXTRACT_DIR}"
    find_figshare_campaign_dir
    if [[ -n "${campaign_dir}" && -d "${campaign_dir}" ]]; then
        dataset_count="$(dataset_count_for_dir "${campaign_dir}")"
        if [[ "${dataset_count}" -gt 0 ]]; then
            printf '[INFO] Reusing existing extracted dataset campaign: %s\n' "${campaign_dir}"
            return
        fi

        if [[ "${ATTACKZOO_CONFIRM_LARGE_DOWNLOAD:-0}" != "1" ]]; then
            attacks_done="$(find "${campaign_dir}" -mindepth 1 -maxdepth 1 -type d ! -name '_campaign' ! -name 'reports' | wc -l | tr -d ' ')"
            datasets_done="${dataset_count}"
            fail "Found extracted campaign at ${campaign_dir}, but it has ${dataset_count}/${EXPECTED_DATASETS} dataset CSVs. Fix/re-extract it, set ATTACKZOO_CLAIM3_CAMPAIGN_DIR to a complete extraction, or rerun with ATTACKZOO_CONFIRM_LARGE_DOWNLOAD=1 to allow re-download/re-extraction."
        fi
    fi

    if [[ -n "${CAMPAIGN_OVERRIDE}" ]]; then
        fail "ATTACKZOO_CLAIM3_CAMPAIGN_DIR does not contain the expected ${EXPECTED_DATASETS} dataset CSVs: ${CAMPAIGN_OVERRIDE}"
    fi

    require_command curl
    require_command tar
    require_command md5sum

    resolve_figshare_metadata
    download_archive
    extract_archive_if_needed
}

prepare_mini_campaign() {
    local http_ip
    local experiment_rc
    local experiment_output

    activate_venv_if_available
    require_command curl
    require_command tcpdump
    docker version >/dev/null 2>&1 || fail "Docker is not accessible for the current user."
    require_image "server-http-server"
    require_image "attack-dos-http-simple"

    mkdir -p ".tmp"
    ./servers.sh start "${PROFILE}" > ".tmp/claim3-mini-servers.log" 2>&1 || \
        fail "Could not start the servers. See .tmp/claim3-mini-servers.log."

    for _ in $(seq 1 20); do
        if docker ps --format '{{.Names}}' | grep -qx "server-http-server" && \
           curl -fsS "http://127.0.0.1:8080/" >/dev/null 2>&1; then
            break
        fi
        sleep 1
    done
    curl -fsS "http://127.0.0.1:8080/" >/dev/null 2>&1 || \
        fail "server-http-server did not become reachable at http://127.0.0.1:8080/."

    http_ip="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)"
    [[ -n "${http_ip}" ]] || fail "Could not resolve the server-http-server container IP address."

    campaign_dir="experiments/${MINI_OUT}"
    rm -rf "${campaign_dir}"
    python3 attackzoo.py stop "${MINI_ATTACK_ID}" >/dev/null 2>&1 || true

    set +e
    experiment_output="$(
        python3 attackzoo.py experiment \
            --attack-id "${MINI_ATTACK_ID}" \
            --out "${MINI_OUT}" \
            --service "${MINI_SERVICE}" \
            --runs "${MINI_RUN_COUNT}" \
            --levels "${EXPECTED_LEVELS}" \
            --warmup "${MINI_WARMUP}" \
            --attack "${MINI_ATTACK}" \
            --cooldown "${MINI_COOLDOWN}" \
            --interval "${MINI_INTERVAL}" \
            --probe-timeout 1 \
            --probes http \
            --http-url "http://127.0.0.1:8080/" \
            --host "${http_ip}" \
            --port 80 \
            --iface lo \
            --bpf "tcp port 8080" \
            --extract-features \
            --build-dataset \
            --features-dir "${campaign_dir}/${MINI_ATTACK_ID}/features" \
            --dataset-dir "${campaign_dir}/${MINI_ATTACK_ID}/datasets" \
            --tools-scapy \
            --attack-start-hook "python3 attackzoo.py run ${MINI_ATTACK_ID} --target {host} --port {port} --duration {duration_s} --count ${MINI_ATTACK_COUNT} --concurrency ${MINI_CONCURRENCY} --delay_ms ${MINI_DELAY_MS}" \
            --attack-stop-hook "python3 attackzoo.py stop ${MINI_ATTACK_ID}" 2>&1
    )"
    experiment_rc=$?
    set -e
    printf '%s\n' "${experiment_output}" > ".tmp/claim3-mini-experiment.log"
    python3 attackzoo.py stop "${MINI_ATTACK_ID}" >/dev/null 2>&1 || true

    if [[ "${experiment_rc}" -ne 0 ]]; then
        fail "The mini experiment failed. See .tmp/claim3-mini-experiment.log."
    fi
}

collect_metrics() {
    mkdir -p "${REPORT_DIR}"
    mapfile -t metrics < <(
        python3 - "${campaign_dir}" "${REPORT_DIR}" "${CLAIM3_MODE}" "${EXPECTED_ATTACKS}" "${EXPECTED_DATASETS}" "${EXPECTED_LEVELS}" "${EXPECTED_RUNS}" <<'PY'
import datetime as dt
import json
import re
import sys
from pathlib import Path

campaign_dir = Path(sys.argv[1]).resolve()
report_dir = Path(sys.argv[2]).resolve()
mode = sys.argv[3]
expected_attacks = int(sys.argv[4])
expected_datasets = int(sys.argv[5])
levels = tuple(item for item in sys.argv[6].split(",") if item)
runs = tuple(item for item in sys.argv[7].split(",") if item)
expected_pairs = {(level, run) for level in levels for run in runs}

attack_dirs = sorted(
    path for path in campaign_dir.iterdir()
    if path.is_dir() and not path.name.startswith("_") and path.name != "reports"
)
dataset_paths = sorted(campaign_dir.glob("*/datasets/*.csv"))
pcap_paths = sorted(campaign_dir.rglob("*.pcap"))
report_paths = [
    path for pattern in ("reports/**/*", "*/reports/**/*")
    for path in campaign_dir.glob(pattern)
    if path.is_file()
]

filename_re = re.compile(r"-(L[0-3])-(run[0-9]{2})\.csv$")
by_attack = {path.name: set() for path in attack_dirs}
bad_names = []
readable_headers = 0
empty_or_unreadable = []

for path in dataset_paths:
    attack_id = path.parents[1].name
    match = filename_re.search(path.name)
    if match:
        by_attack.setdefault(attack_id, set()).add((match.group(1), match.group(2)))
    else:
        bad_names.append(str(path.relative_to(campaign_dir)))

    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            header = handle.readline().strip()
    except OSError:
        header = ""
    if header and "," in header:
        readable_headers += 1
    else:
        empty_or_unreadable.append(str(path.relative_to(campaign_dir)))

missing_by_attack = {
    attack_id: [f"{level}-{run}" for level, run in sorted(expected_pairs - combos)]
    for attack_id, combos in sorted(by_attack.items())
    if expected_pairs - combos
}
missing_combo_count = sum(len(values) for values in missing_by_attack.values())

manifest = {
    "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    "mode": mode,
    "campaign_dir": str(campaign_dir),
    "expected": {
        "attacks": expected_attacks,
        "dataset_csvs": expected_datasets,
        "levels": levels,
        "runs": runs,
        "raw_pcaps_required": False,
    },
    "observed": {
        "attack_dirs": len(attack_dirs),
        "dataset_csvs": len(dataset_paths),
        "readable_csv_headers": readable_headers,
        "raw_pcaps": len(pcap_paths),
        "report_files": len(report_paths),
        "missing_level_run_combos": missing_combo_count,
        "bad_dataset_filenames": len(bad_names),
        "empty_or_unreadable_csvs": len(empty_or_unreadable),
    },
    "attack_ids": [path.name for path in attack_dirs],
    "missing_by_attack": missing_by_attack,
    "bad_dataset_filenames_sample": bad_names[:20],
    "empty_or_unreadable_csvs_sample": empty_or_unreadable[:20],
}

report_dir.mkdir(parents=True, exist_ok=True)
manifest_path = report_dir / "manifest.json"
with manifest_path.open("w", encoding="utf-8") as handle:
    json.dump(manifest, handle, indent=2, sort_keys=True)
    handle.write("\n")

print(len(attack_dirs))
print(len(dataset_paths))
print(readable_headers)
print(len(pcap_paths))
print(missing_combo_count)
print("yes" if report_paths else "no")
print(manifest_path)
PY
    )
    attacks_done="${metrics[0]}"
    datasets_done="${metrics[1]}"
    datasets_ok="${metrics[2]}"
    pcaps_found="${metrics[3]}"
    missing_combos="${metrics[4]}"
    reports_status="${metrics[5]}"
    if [[ -f "${metrics[6]}" ]]; then
        report_status="${metrics[6]}"
    fi
}

validate_metrics() {
    if [[ "${CLAIM3_MODE}" == "figshare" ]]; then
        if [[ "${datasets_done}" == "0" ]]; then
            fail "No dataset CSVs were found under ${campaign_dir}."
        fi
        if [[ "${datasets_ok}" == "0" ]]; then
            fail "No readable dataset CSV headers were found under ${campaign_dir}."
        fi
        if [[ "${report_status}" == "no" ]]; then
            fail "Manifest was not generated under ${REPORT_DIR}."
        fi
        return
    fi

    if [[ "${attacks_done}" != "${EXPECTED_ATTACKS}" ]]; then
        fail "Unexpected attack count in the dataset: ${attacks_done}."
    fi
    if [[ "${datasets_done}" != "${EXPECTED_DATASETS}" ]]; then
        fail "Unexpected dataset CSV count: ${datasets_done}."
    fi
    if [[ "${datasets_ok}" != "${EXPECTED_DATASETS}" ]]; then
        fail "Unexpected readable dataset CSV header count: ${datasets_ok}."
    fi
    if [[ "${missing_combos}" != "0" ]]; then
        fail "Missing level/run dataset combinations: ${missing_combos}. See ${REPORT_DIR}/manifest.json."
    fi
    if [[ "${CLAIM3_MODE}" == "mini" && "${reports_status}" != "yes" ]]; then
        fail "Mini experiment reports were not generated under ${campaign_dir}/reports."
    fi
    if [[ "${report_status}" == "no" ]]; then
        fail "Manifest was not generated under ${REPORT_DIR}."
    fi
}

configure_mode

case "${CLAIM3_MODE}" in
    mini)
        prepare_mini_campaign
        ;;
    figshare)
        prepare_figshare_campaign
        ;;
esac

collect_metrics
validate_metrics

result="OK"

case "${CLAIM3_MODE}" in
    mini)
        print_summary
        tree experiments/claim3_mini
        ;;
    figshare)
        print_summary
        ;;
esac
