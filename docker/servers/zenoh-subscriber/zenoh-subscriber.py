"""Zenoh client that subscribes to a key expression on a router and prints one line per received sample."""
import json
import signal
import sys
import threading
import time

import zenoh

if len(sys.argv) < 2 or len(sys.argv) > 4:
    print("usage: zenoh-subscriber.py <router_ip> [port (7447)] [key_expr (attackzoo/**)]")
    sys.exit(2)
endpoint = f"tcp/{sys.argv[1]}:{sys.argv[2] if len(sys.argv) > 2 else 7447}"
key_expr = sys.argv[3] if len(sys.argv) > 3 else "attackzoo/**"

conf = zenoh.Config()
conf.insert_json5("mode", '"client"')
conf.insert_json5("connect/endpoints", json.dumps([endpoint]))
conf.insert_json5("scouting/multicast/enabled", "false")

lock = threading.Lock()
received = 0


def on_sample(sample):
    global received
    ts = sample.timestamp
    with lock:
        received += 1
        # receive order, receive time, kind, key, sample timestamp as NTP64 and as RFC 3339/id, payload bytes
        print(received, f"{time.time():.6f}", sample.kind, sample.key_expr,
              ts.get_time_as_ntp64() if ts else "-", ts.to_string_rfc3339_lossy() if ts else "-",
              len(sample.payload.to_bytes()))


stop = threading.Event()
signal.signal(signal.SIGTERM, lambda *_: stop.set())
signal.signal(signal.SIGINT, lambda *_: stop.set())

session = zenoh.open(conf)
subscriber = session.declare_subscriber(key_expr, on_sample)
print(f"subscribed to {key_expr} via {endpoint}")
while not stop.wait(1):
    pass
session.close()
with lock:
    print(f"stopped, {received} samples received")
