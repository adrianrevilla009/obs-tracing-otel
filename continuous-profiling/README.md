# continuous-profiling

A CPU-bound Python Orders workload (`busy.py`) that pushes profiles to Pyroscope 1.9.2, wired together in `compose.yaml`.

## Goal

Show continuous profiling as a signal alongside traces: an app sends CPU profiles to a server, which you can query and browse by application name.

## Run it

```bash
./verify.sh
```

`verify.sh` starts Pyroscope and the app (the container installs `pyroscope-io==0.8.8` with pip on startup), then polls Pyroscope's label-values API for up to about 200 s. It runs `docker compose down -v` on exit. The UI is at http://localhost:4040 while it runs.
Expected last line: `OK: Pyroscope has profiles for orders.busy (UI: http://localhost:4040)`.

Not run end to end in this pass: it needs Docker, image pulls and pip downloads.

## What it proves

- `pyroscope.configure` in `busy.py` registers the application as `orders.busy` with tag `env=lab`, using the server address from `PYROSCOPE_SERVER`.
- The `checkout` loop calling `price_order(200_000)` produces a CPU hot spot you can find in the flame graph.
- The profiles are queryable through the API, not only visible in the UI.

## Trade-offs

- The profiler samples the running process, which costs a little CPU.
- Profiles are not linked to traces here; connecting them needs span-profile integration that this folder does not set up.
- Installing the client at container start makes the run depend on network access and is slow.

## When not to use it

- For short scripts that finish quickly; a one-off profiler run is simpler.
- When you only need request latency, which traces already give you.
