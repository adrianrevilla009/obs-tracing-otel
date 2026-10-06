"""CPU-bound Orders workload that pushes CPU profiles to Pyroscope."""
import os

import pyroscope

pyroscope.configure(application_name="orders.busy", server_address=os.environ["PYROSCOPE_SERVER"],
                    tags=dict(env="lab"))


def price_order(n):
    return sum(i * i % 7 for i in range(n))


def checkout():
    while True:
        price_order(200_000)


if __name__ == "__main__":
    print("profiling started", flush=True)
    checkout()
