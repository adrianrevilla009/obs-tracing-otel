#!/usr/bin/env bash
# Downloads the pinned agent, starts Jaeger + Orders, sends a request, checks Jaeger has a trace.
set -euo pipefail
cd "$(dirname "$0")"
VERSION=2.10.0
URL=https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v$VERSION/opentelemetry-javaagent.jar
mkdir -p agent
[ -f agent/opentelemetry-javaagent.jar ] || curl -fsSL -o agent/opentelemetry-javaagent.jar "$URL"
docker compose up -d
trap 'docker compose down -v' EXIT
for _ in $(seq 40); do curl -fs localhost:8080/orders/1 >/dev/null && break; sleep 2; done
sleep 5
curl -fs "localhost:16686/api/traces?service=orders&limit=1" | grep -q traceID && echo "OK: trace for service orders found in Jaeger"
