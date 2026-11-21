#!/bin/sh
if [ "${#}" -eq 2 ]; then
	TARGET="${1}"
    if [ -n "${2}" ]; then
        PORT="${2}"
    else
        PORT="8080"
    fi
    DURATION_S="${DURATION_S:-0}"
    set -e
    if [ "${DURATION_S}" -gt 0 ]; then
        timeout "${DURATION_S}" python3 /slowloris/slowloris.py "${TARGET}" -p "${PORT}"
    else
        exec python3 /slowloris/slowloris.py "${TARGET}" -p "${PORT}"
    fi
fi
