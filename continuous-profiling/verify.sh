#!/usr/bin/env bash
# Starts Pyroscope + a busy app, then asks Pyroscope which applications it has profiles for.
set -euo pipefail
cd "$(dirname "$0")"
docker compose up -d
trap 'docker compose down -v' EXIT
for _ in $(seq 40); do
  if curl -fs -X POST -H 'Content-Type: application/json' -d '{"name":"service_name"}' \
      localhost:4040/querier.v1.QuerierService/LabelValues | grep -q 'orders.busy'; then
    echo "OK: Pyroscope has profiles for orders.busy (UI: http://localhost:4040)"; exit 0
  fi
  sleep 5
done
echo "FAIL: no profiles received" >&2; exit 1
