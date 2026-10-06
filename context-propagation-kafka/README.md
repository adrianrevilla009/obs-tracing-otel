# context-propagation-kafka

`propagation.py` shows W3C `traceparent` propagation across a Kafka-style record boundary in plain Python, and `compose.yaml` offers an optional Kafka 3.8.0 broker.

## Goal

Make the propagation mechanism visible: a producer writes the trace context into record headers, and a consumer reads it and continues the same trace.

## Run it

```bash
python3 propagation.py
```

Expected output:

```text
header: 00-<32 hex trace id>-<16 hex span id>-01
OK: consumer span continues the producer trace
```

This script was run in this pass and printed the lines above. It uses no Kafka and no OpenTelemetry library: records are plain dictionaries. `compose.yaml` only starts a broker (`docker compose up -d`); no code in this folder talks to it, and it has not been exercised.

## What it proves

- `inject` writes `00-<trace>-<span>-<flags>` into `headers["traceparent"]`; `extract` parses it with a strict regex.
- The consumer span has the producer's trace id and its parent id equals the producer's span id (both asserted).
- A record without the header produces a root span with no parent, so the trace restarts.

## Trade-offs

- It is a hand-written model of the mechanism; real services should use the OTel Kafka instrumentation and propagator rather than this code.
- Only `traceparent` is handled, not `tracestate` or baggage.
- No spans are exported anywhere, so there is nothing to see in a backend.

## When not to use it

- When you need working Kafka tracing; attach the OpenTelemetry Java agent to real producers and consumers instead.
- When your messaging system already propagates context for you.
