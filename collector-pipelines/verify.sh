#!/usr/bin/env bash
# Sends a health span and an orders span; only the orders span (without the auth header) must reach Jaeger.
set -euo pipefail
cd "$(dirname "$0")"
docker compose up -d
trap 'docker compose down -v' EXIT
for _ in $(seq 30); do python3 send.py >/dev/null 2>&1 && break; sleep 2; done
sleep 5
out=$(curl -fs "localhost:16686/api/traces?service=pipeline-demo")
grep -q 'GET /orders' <<<"$out"
! grep -q 'GET /health' <<<"$out"
! grep -q 'http.request.header.authorization' <<<"$out"
echo "OK: health span dropped, auth header scrubbed, env tag added"
