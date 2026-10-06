#!/usr/bin/env bash
# One OTLP trace fans out to both backends; both query APIs must return it.
set -euo pipefail
cd "$(dirname "$0")"
docker compose up -d
trap 'docker compose down -v' EXIT
for _ in $(seq 30); do python3 send.py >/dev/null 2>&1 && break; sleep 2; done
sleep 5
curl -fs "localhost:16686/api/traces/1af7651916cd43dd8448eb211c80319d" | grep -q 'GET /orders'
curl -fs "localhost:9411/api/v2/trace/1af7651916cd43dd8448eb211c80319d" | grep -q 'GET /orders'
echo "OK: same trace visible in Jaeger and Zipkin"
