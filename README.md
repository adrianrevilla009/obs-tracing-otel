# obs-tracing-otel

Seven small OpenTelemetry labs that show how traces and profiles get from an Orders service to a backend you can query, from the Java agent to Collector pipelines, Jaeger, Zipkin, Tempo, Kafka propagation, tail sampling and Pyroscope.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`otel-java-agent`](./otel-java-agent) | A plain Java HTTP service traced by the OTel Java agent, exported to Jaeger | `./verify.sh` |
| [`collector-pipelines`](./collector-pipelines) | Collector filter and attribute processors dropping health spans and scrubbing an auth header | `./verify.sh` |
| [`jaeger-zipkin`](./jaeger-zipkin) | One OTLP trace fanned out to Jaeger and Zipkin by the Collector | `./verify.sh` |
| [`tempo`](./tempo) | Tempo with local storage and a provisioned Grafana datasource | `./verify.sh` |
| [`context-propagation-kafka`](./context-propagation-kafka) | W3C `traceparent` injected and extracted on Kafka-style record headers | `python3 propagation.py` |
| [`sampling-strategies`](./sampling-strategies) | Collector tail sampling that keeps every error and slow trace | `./verify.sh` |
| [`continuous-profiling`](./continuous-profiling) | A CPU-bound Python app pushing profiles to Pyroscope | `./verify.sh` |

## Prerequisites

- Docker with the Compose plugin (all folders except `context-propagation-kafka`)
- Python 3 (standard library only for the send scripts and `propagation.py`)
- curl
- Java 21 is supplied by the `eclipse-temurin` image in `otel-java-agent`; no local JDK is needed

## How to read it

Start with `otel-java-agent` to see where spans come from, then `collector-pipelines` to see what the Collector does with them. The other folders each swap one piece: backend, propagation, sampling or profiling. The example domain is a tiny Orders service.
