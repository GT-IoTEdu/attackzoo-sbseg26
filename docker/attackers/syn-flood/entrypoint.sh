#!/bin/sh
if [ "${#}" -ge 1 ]; then
	TARGET="${1}"
    PORT="${2:-8080}"
    COUNT="${COUNT:-9999999999}"
    RATE_PPS="${RATE_PPS:-${RATE:-0}}"
    DURATION_S="${DURATION_S:-0}"
    DELAY_MS="${DELAY_MS:-0}"
    PAYLOAD_SIZE="${PAYLOAD_SIZE:-0}"
    set -e
    set -- python3 /tmp/sf.py -t "${TARGET}" -p "${PORT}" -c "${COUNT}" \
        --rate-pps "${RATE_PPS}" \
        --delay-ms "${DELAY_MS}" \
        --payload-size "${PAYLOAD_SIZE}"

    if [ "${DURATION_S}" -gt 0 ]; then
        timeout "${DURATION_S}" "$@"
    else
        exec "$@"
    fi
fi
