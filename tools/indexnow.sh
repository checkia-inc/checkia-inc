#!/usr/bin/env bash
# Submit published URLs to Bing via IndexNow (also forwarded to Yandex, Naver,
# Seznam and every IndexNow engine). Run after the site is deployed.
# Usage: tools/indexnow.sh https://checkia.fr/blog/<serie>/<slug>/ [more URLs…]
# HTTP 200 or 202 = accepted. The key file /d9440be4ca8eae53a8ce34b12c67331d.txt must stay deployed at the site root.
set -euo pipefail
KEY="d9440be4ca8eae53a8ce34b12c67331d"
HOST="checkia.fr"
[ $# -ge 1 ] || { echo "Usage: $0 <url> [url…]"; exit 1; }
LIST=$(printf '"%s",' "$@"); LIST="[${LIST%,}]"
curl -sS -X POST "https://www.bing.com/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"host\":\"$HOST\",\"key\":\"$KEY\",\"keyLocation\":\"https://$HOST/$KEY.txt\",\"urlList\":$LIST}" \
  -w "\nHTTP %{http_code}\n"
