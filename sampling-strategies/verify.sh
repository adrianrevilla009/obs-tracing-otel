#!/usr/bin/env bash
# Error and slow traces must always be kept; OK traces are sampled at ~10%.
set -euo pipefail
cd "$(dirname "$0")"
docker compose up -d
trap 'docker compose down -v' EXIT
for _ in $(seq 30); do python3 load.py >/dev/null 2>&1 && break; sleep 2; done
sleep 12
count() { curl -fs "localhost:16686/api/traces?service=sampling-demo&operation=$1&limit=200" | grep -o '"traceID":"[0-9a-f]*"' | sort -u | wc -l; }
errors=$(count error); slow=$(count slow); ok=$(count ok)
echo "kept: error=$errors/5 slow=$slow/5 ok=$ok/100"
[ "$errors" -eq 5 ] && [ "$slow" -eq 5 ] && [ "$ok" -lt 50 ] && echo "OK: tail sampling kept every error and slow trace"
