#!/usr/bin/env python3
"""Send 100 fast OK traces, 5 ERROR traces and 5 slow traces (one span each). Stdlib only."""
import json
import secrets
import time
import urllib.request


def trace(kind):
    now = time.time_ns()
    dur = 800_000_000 if kind == "slow" else 5_000_000
    return dict(traceId=secrets.token_hex(16), spanId=secrets.token_hex(8), name=kind, kind=2,
                startTimeUnixNano=str(now - dur), endTimeUnixNano=str(now),
                status=dict(code=2 if kind == "error" else 1))


spans = [trace("ok") for _ in range(100)] + [trace("error") for _ in range(5)] + [trace("slow") for _ in range(5)]
svc = dict(key="service.name", value=dict(stringValue="sampling-demo"))
body = dict(resourceSpans=[dict(resource=dict(attributes=[svc]),
                                scopeSpans=[dict(scope=dict(name="demo"), spans=spans)])])
req = urllib.request.Request("http://localhost:4318/v1/traces", json.dumps(body).encode(),
                             {"Content-Type": "application/json"})
print("sent", len(spans), "spans ->", urllib.request.urlopen(req).status)
