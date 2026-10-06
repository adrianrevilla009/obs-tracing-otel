# collector-pipelines

An OpenTelemetry Collector (contrib 0.111.0) config, `otelcol.yaml`, with a filter and an attributes processor in front of Jaeger, plus `send.py` to feed it two spans.

## Goal

Show that a Collector pipeline can change telemetry in flight: drop noisy spans, add a tag and remove a sensitive attribute before anything reaches the backend.

## Run it

```bash
./verify.sh
```

`verify.sh` starts Jaeger and the Collector, runs `send.py` (a `/health` span and an `/orders` span, both carrying an authorization header attribute), waits, then queries Jaeger for service `pipeline-demo`. It runs `docker compose down -v` on exit.
Expected last line: `OK: health span dropped, auth header scrubbed, env tag added`.

Not run end to end in this pass: it needs Docker and image pulls. The script's last line also claims the env tag was added, but its checks only cover the dropped span and the scrubbed header.

## What it proves

- `filter/health` drops spans where `http.route` is `/health`, so only `GET /orders` is stored.
- `attributes/env` deletes `http.request.header.authorization`, so the stored trace does not contain it.
- `attributes/env` also upserts `deployment.environment=lab`; open the trace in Jaeger to see the tag.
- The `debug` exporter prints a summary in the Collector log next to the `otlphttp/jaeger` exporter.

## Trade-offs

- Processor order matters: filtering first avoids spending work on spans that are dropped.
- Scrubbing by attribute name only catches the keys you list; new sensitive keys slip through.
- Dropped data is gone for good, so a wrong filter silently loses real traces.

## When not to use it

- When the data must be scrubbed before it leaves the process; do it in the SDK, since the Collector only sees what is sent to it.
- For a single service with no shared pipeline, direct export is simpler.
