#!/usr/bin/env bash
set -e
mkdir -p bin
mkdir -p logs

C_ATTACKS=(
    "attack_session_hijack"
)

DDS_CFLAGS="-Wall -Wextra -O2 -I/usr/local/include -I/usr/local/microcdr-2.0.2/include"
DDS_LIBS="-L/usr/local/lib -L/usr/local/microcdr-2.0.2/lib -lmicroxrcedds_client -lmicrocdr -lpthread"

SPECIAL_CFLAGS="-Wall -Wextra -O2"
SPECIAL_LIBS="-lpthread"

for attack in "${C_ATTACKS[@]}"; do
    gcc ${attack}.c -o bin/$attack ${DDS_CFLAGS} ${DDS_LIBS}
    chmod +x bin/$attack
    [ -x bin/$attack ] || { echo "ERROR: bin/$attack was not built" >&2; exit 1; }
done
