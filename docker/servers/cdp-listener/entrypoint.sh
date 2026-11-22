#!/usr/bin/env bash
# lldpd keeping a CDP neighbor table for eth0; receive-only, so it sends no LLDP/CDP frames.
mkdir -p /run/lldpd
exec lldpd -d -r -c -I eth0
