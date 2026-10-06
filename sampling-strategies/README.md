# sampling-strategies

A Collector `tail_sampling` config (`otelcol.yaml`) in front of Jaeger 1.62.0, and `load.py` to send 110 single-span traces.

## Goal

Show tail sampling: decide whether to keep a trace after it is complete, so errors and slow requests are never lost while ordinary traffic is thinned.

## Run it

```bash
./verify.sh
```

`verify.sh` starts Jaeger and the Collector, runs `load.py` (100 fast OK traces, 5 ERROR traces, 5 slow traces of 800 ms), waits 12 s, then counts traces per operation in Jaeger. It runs `docker compose down -v` on exit.
Expected: a line like `kept: error=5/5 slow=5/5 ok=<fewer than 50>/100`, then `OK: tail sampling kept every error and slow trace`.

Not run end to end in this pass: it needs Docker and image pulls. The OK count is random, so it will vary between runs.

## What it proves

- The `keep-errors` policy (status code ERROR) keeps all 5 error traces.
- The `keep-slow` policy (latency over 500 ms) keeps all 5 slow traces.
- The `sample-rest` policy keeps about 10% of the other traces; the check only requires fewer than 50 of 100.

## Trade-offs

- The Collector must buffer spans for `decision_wait` (5 s here), which costs memory and delays export.
- All spans of a trace must reach the same Collector instance; scaling out needs load balancing by trace id.
- Policies are OR-ed, so a trace matching any policy is kept.

## When not to use it

- When traffic is low enough to keep everything.
- When you need a decision before the first span is sent; use head sampling in the SDK instead.
