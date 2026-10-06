#!/usr/bin/env bash
# Sends a trace straight to Tempo's OTLP receiver and fetches it by id via the Tempo API.
set -euo pipefail
cd "$(dirname "$0")"
docker compose up -d
trap 'docker compose down -v' EXIT
for _ in $(seq 30); do python3 send.py >/dev/null 2>&1 && break; sleep 2; done
for _ in $(seq 20); do
  if curl -fs "localhost:3200/api/traces/1af7651916cd43dd8448eb211c80319d" | grep -q 'GET /orders'; then
    echo "OK: trace retrieved from Tempo by id"; exit 0
  fi
  sleep 3
done
echo "FAIL: trace not found" >&2; exit 1
