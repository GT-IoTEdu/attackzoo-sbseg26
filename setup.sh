#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

PROFILE="${1:-}"
SETUP_MARKER="${ROOT_DIR}/.attackzoo-setup.ok"
NTLFLOWLYZER_REF="${NTLFLOWLYZER_REF:-d99cd5377faaed53b39450ce262652902501188d}"

case "${PROFILE}" in
    full|redux|dependencies)
        ;;
    *)
        echo "Usage: $0 [full|redux|dependencies]"
        echo "Make sure you have run ./setup.sh dependencies at least once."
        exit 1
        ;;
esac

if [ "${PROFILE}" == "dependencies" ]; then
    echo "Installing required packages..."
    sudo apt update
    sudo DEBIAN_FRONTEND=noninteractive apt install -y tshark tcpdump tree python3-venv ca-certificates curl git
    sudo setcap cap_net_raw,cap_net_admin=eip "$(command -v tcpdump)"

    echo "Installing tools..."
    chmod +x clients.sh docker-install.sh servers.sh build.sh environment.sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    git clone https://github.com/ahlashkari/NTLFlowLyzer.git
    cd NTLFlowLyzer || exit 1
    git checkout "${NTLFLOWLYZER_REF}"

    echo -e "\nsetuptools" >> requirements.txt
    pip install -r requirements.txt
    pip install .
    rm -rf .git/
    cd ../ || exit 1
    pip install -r requirements.txt
    ./docker-install.sh "${PROFILE}"
    echo '1' > "${SETUP_MARKER}"
    echo -e "All dependencies satisfied.\nNow execute \e[92mnewgrp docker\e[0m to reload this shell session and then continue the procedure."
    exit 0
fi

if [ "${PROFILE}" == "redux" ] || [ "${PROFILE}" == "full" ]; then
    if [ ! -f "${SETUP_MARKER}" ]; then
        echo -e "Dependency marker not found: ${SETUP_MARKER}"
        echo -e "Run \e[92m./setup.sh dependencies\e[0m before \e[92m./setup.sh ${PROFILE}\e[0m."
        exit 1
    fi
    if [ ! -f ".venv/bin/activate" ]; then
        echo "Python virtual environment not found: .venv/bin/activate"
        echo -e "Run \e[92m./setup.sh dependencies\e[0m to recreate it."
        exit 1
    fi
    ./build.sh "${PROFILE}"
fi
