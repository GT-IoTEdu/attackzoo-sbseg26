#!/usr/bin/env bash
# Small pool (10 addresses) served on eth0 only, inside the container's own subnet.
NET="$(hostname -I | awk '{print $1}' | cut -d. -f1-3)"
POOL_START="${POOL_START:-${NET}.240}"
POOL_END="${POOL_END:-${NET}.249}"
cat > /etc/udhcpd.conf <<CONF
start ${POOL_START}
end ${POOL_END}
interface eth0
max_leases 10
lease_file /tmp/udhcpd.leases
CONF
touch /tmp/udhcpd.leases
exec udhcpd -f /etc/udhcpd.conf
