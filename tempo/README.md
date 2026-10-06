# tempo

Grafana Tempo 2.6.1 configured in `tempo.yaml` with local storage, plus Grafana 11.3.0 with a provisioned Tempo datasource (`grafana-datasource.yaml`).

## Goal

Show Tempo as a trace backend that accepts OTLP directly and returns traces by id, with Grafana ready to browse them.

## Run it

```bash
./verify.sh
```

`verify.sh` starts Tempo and Grafana, runs `send.py` against Tempo's OTLP/HTTP receiver on port 4318, then polls `localhost:3200/api/traces/<id>` for up to about a minute. It runs `docker compose down -v` on exit. Grafana is at http://localhost:3000 (anonymous admin) while it runs.
Expected last line: `OK: trace retrieved from Tempo by id`.

Not run end to end in this pass: it needs Docker and image pulls.

## What it proves

- Tempo's `distributor` receives OTLP over HTTP with no Collector in between.
- A trace sent by `send.py` can be fetched by id (`1af7651916cd43dd8448eb211c80319d`) from the Tempo API.
- Grafana starts with Tempo already set as its default datasource, so no UI setup is needed.

## Trade-offs

- Storage is `backend: local` under `/tmp/tempo`, which is fine for a lab but not for several instances or restarts.
- Tempo is looked up by trace id; searching by attributes needs TraceQL and extra configuration not set up here.
- Grafana runs with anonymous admin access, which is only acceptable locally.

## When not to use it

- For production: use object storage and authentication instead of local disk and anonymous admin.
- When you need to browse traces without knowing an id and want the simplest setup; Jaeger's search UI is easier.
