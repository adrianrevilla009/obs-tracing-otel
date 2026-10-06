#!/usr/bin/env python3
"""W3C trace-context propagation across a Kafka-style message boundary, stdlib only.

Producer injects a `traceparent` header into the record headers; the consumer extracts it
and creates a child span in the SAME trace. Real clients (OTel Kafka instrumentation) do
exactly this with the TextMapPropagator; here it is spelled out so the mechanism is visible.
"""
import re
import secrets

TRACEPARENT = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


def new_span(parent=None):
    if parent:
        return dict(trace_id=parent["trace_id"], span_id=secrets.token_hex(8),
                    parent_id=parent["span_id"], flags=parent["flags"])
    return dict(trace_id=secrets.token_hex(16), span_id=secrets.token_hex(8), parent_id=None, flags="01")


def inject(span, headers):
    headers["traceparent"] = f"00-{span['trace_id']}-{span['span_id']}-{span['flags']}"


def extract(headers):
    m = TRACEPARENT.match(headers.get("traceparent", ""))
    return dict(trace_id=m[1], span_id=m[2], flags=m[3]) if m else None


def produce(topic):
    span = new_span()
    headers = {}
    inject(span, headers)
    return span, dict(topic=topic, value=b"order-42", headers=headers)


def consume(record):
    return new_span(extract(record["headers"]))


if __name__ == "__main__":
    producer_span, record = produce("orders")
    consumer_span = consume(record)
    print("header:", record["headers"]["traceparent"])
    assert consumer_span["trace_id"] == producer_span["trace_id"]
    assert consumer_span["parent_id"] == producer_span["span_id"]
    assert consume(dict(headers={}))["parent_id"] is None  # no header -> new root trace
    print("OK: consumer span continues the producer trace")
