# jaeger-zipkin

A Collector config (`otelcol.yaml`) that exports every trace to both Jaeger 1.62.0 and Zipkin 3.4.2, with `send.py` producing a test trace.

## Goal

Show that the instrumentation side does not depend on the backend: one OTLP trace is sent once, and the Collector delivers it to two different systems.

## Run it

```bash
./verify.sh
```

`verify.sh` starts Jaeger, Zipkin and the Collector, runs `send.py`, then fetches trace `1af7651916cd43dd8448eb211c80319d` from each backend's query API. It runs `docker compose down -v` on exit. UIs: http://localhost:16686 (Jaeger) and http://localhost:9411 (Zipkin).
Expected last line: `OK: same trace visible in Jaeger and Zipkin`.

Not run end to end in this pass: it needs Docker and image pulls.

## What it proves

- A single `traces` pipeline in `otelcol.yaml` lists two exporters, `otlphttp/jaeger` and `zipkin`.
- The span `GET /orders` is retrievable by the same trace id from `localhost:16686/api/traces/...` and `localhost:9411/api/v2/trace/...`.
- The sender only knows the Collector's OTLP/HTTP port 4318, not either backend.

## Trade-offs

- Exporting to two backends doubles the Collector's outbound work and failure modes.
- The two UIs model the data a little differently, so views are not identical.
- Both backends here use in-memory storage, so traces disappear on restart.

## When not to use it

- When you have already chosen a single backend; skip the second exporter.
- For long-term storage; neither container is configured with persistence (see `tempo` for a storage-backed option).
