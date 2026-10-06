#!/usr/bin/env python3
"""Send two hand-built OTLP/JSON spans (one /health, one /orders) to the Collector. Stdlib only."""
import json, time, urllib.request


def attr(k, v):
    return {"key": k, "value": {"stringValue": v}}


def span(name, route, trace_id, span_id):
    now = time.time_ns()
    return dict(traceId=trace_id, spanId=span_id, name=name, kind=2,
                startTimeUnixNano=str(now - 10_000_000), endTimeUnixNano=str(now),
                attributes=[attr("http.route", route), attr("http.request.header.authorization", "Bearer x")])


spans = [span("GET /health", "/health", "0af7651916cd43dd8448eb211c80319c", "b7ad6b7169203331"),
         span("GET /orders", "/orders", "1af7651916cd43dd8448eb211c80319d", "c7ad6b7169203332")]
body = dict(resourceSpans=[dict(resource=dict(attributes=[attr("service.name", "pipeline-demo")]),
                                scopeSpans=[dict(scope=dict(name="demo"), spans=spans)])])
req = urllib.request.Request("http://localhost:4318/v1/traces", json.dumps(body).encode(),
                             {"Content-Type": "application/json"})
print("collector replied", urllib.request.urlopen(req).status)
