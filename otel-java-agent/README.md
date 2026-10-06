# otel-java-agent

A single-file Java 21 Orders HTTP service (`App.java`) run with the OpenTelemetry Java agent 2.10.0 and Jaeger 1.62.0 via `compose.yaml`.

## Goal

Get distributed traces out of a plain Java service with zero code changes. The agent is attached with `-javaagent` and configured only through `OTEL_*` environment variables.

## Run it

```bash
./verify.sh
```

`verify.sh` downloads the pinned agent jar into `agent/` (needs curl and network), runs `docker compose up -d`, requests `localhost:8080/orders/1`, then queries the Jaeger API. It runs `docker compose down -v` on exit. The Jaeger UI is at http://localhost:16686 while it runs.
Expected last line: `OK: trace for service orders found in Jaeger`.

Not run end to end in this pass: it needs Docker, image pulls and a download from GitHub releases.

## What it proves

- `App.java` has no OpenTelemetry imports, yet requests to `/orders/{id}` show up in Jaeger as service `orders`.
- The exporter settings (`OTEL_EXPORTER_OTLP_ENDPOINT`, protocol `http/protobuf`, metrics and logs exporters off) live entirely in `compose.yaml`.
- The 25 ms sleep in the handler gives each server span a visible, non-zero duration.

## Trade-offs

- The agent adds startup time and some runtime overhead.
- Automatic spans are coarse: they describe the HTTP request, with no business attributes until you add manual spans.
- The jar is downloaded at run time, not vendored, so the first run needs network access.

## When not to use it

- When you only need custom domain spans; use the OpenTelemetry API and SDK directly.
- On runtimes that disallow bytecode agents, such as GraalVM native image.
