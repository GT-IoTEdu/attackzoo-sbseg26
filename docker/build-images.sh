#!/usr/bin/env bash
PROFILE="${1:-full}"

case "${PROFILE}" in
    full)
        ;;
    redux)
        if [ $( docker ps -a | grep -Ec '(server|attack)' ) -gt 0 ]; then
            while read -r CONTAINER; do
                docker rm -f "${CONTAINER}"
            done < <( docker ps -a | grep -E '(server|attack)' | awk '{print $1}' )
        fi
        LOCAL_IP=$( ip route get 9.9.9.9 | awk '{print $7; exit}' )

        docker build --no-cache -t server-http-server -f servers/http-server/Dockerfile .
        docker run -d --rm --name server-http-server -p 8080:80 server-http-server:latest
        wait
        docker build -t server-ssh-server -f servers/ssh-server/Dockerfile .
        docker run -d --rm --name server-ssh-server -p 2222:22 server-ssh-server:latest
        wait
        docker build -t server-mqtt-broker -f servers/mqtt-broker/Dockerfile .
        docker run -d --rm --name server-mqtt-broker -p 1883:1883 -p 9001:9001 server-mqtt-broker:latest
        wait

        docker build --no-cache -t attack-arp-scan -f attackers/arp-scan/Dockerfile .
        docker build --no-cache -t attack-arp-spoof -f attackers/arp-spoof/Dockerfile .
        docker build -t attack-web-simple-scanner -f attackers/web-simple-scanner/Dockerfile .
        docker build -t attack-ssh-bruteforce -f attackers/ssh-bruteforce/Dockerfile .
        docker build -t attack-icmp-tunnel -f attackers/icmp-tunnel/Dockerfile .
        docker build -t attack-dos-http-simple -f attackers/dos-http-simple/Dockerfile .
        docker build -t attack-mqtt-publisher -f attackers/mqtt-publisher-flood/Dockerfile .

        echo "Web server: $( docker container inspect server-http-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' )"
        echo "SSH server: $( docker container inspect server-ssh-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' )"
        echo "MQTT Broker: $( docker container inspect server-mqtt-broker --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' )"
        echo "This machine: ${LOCAL_IP}"
        echo "Reduced lab images created. Benign client images were not built."
        exit 0
        ;;
    *)
        echo "Usage: $0 [full|redux]"
        exit 1
        ;;
esac

if [ $( docker ps -a | grep -Ec '(server|attack)' ) -gt 0 ]; then
    while read -r CONTAINER; do
        docker rm -f "${CONTAINER}"
    done < <( docker ps -a | grep -E '(server|attack)' | awk '{print $1}' )
fi
LOCAL_IP=$( ip route get 9.9.9.9 | awk '{print $7; exit}' )
docker build --no-cache -t server-http-server -f servers/http-server/Dockerfile .
docker run -d --rm --name server-http-server -p 8080:80 server-http-server:latest
wait
docker build -t server-ssh-server -f servers/ssh-server/Dockerfile .
docker run -d --rm --name server-ssh-server -p 2222:22 server-ssh-server:latest
wait
docker build --no-cache -t server-smb-server -f servers/smb-server/Dockerfile .
docker run -it -d --rm --name server-smb-server -p 139:139 -p 445:445 -p 137:137/udp -p 138:138/udp server-smb-server:latest  -g "log level = 3" -s "public;/share" -u "example2;badpass"
wait
docker build -t server-mqtt-broker -f servers/mqtt-broker/Dockerfile .
docker run -it -d --rm --name server-mqtt-broker -p 1883:1883 -p 9001:9001 server-mqtt-broker:latest
wait
docker build -t server-coap-server -f servers/coap-server/Dockerfile .
docker run -d --restart on-failure --name server-coap-server -p 5683:5683 -p 5683:5683/udp server-coap-server:latest
wait
chmod +x servers/xrce-dds-agent/agent-source-install.sh
servers/xrce-dds-agent/agent-source-install.sh
docker run -d --rm -p 8888:8888/udp --name server-xrce-dds-agent server-xrce-dds-agent:latest "udp4" "-p" "8888"
docker build --no-cache -t server-zenoh-router -f servers/zenoh-router/Dockerfile .
docker run -d --rm --name server-zenoh-router -p 7447:7447 server-zenoh-router:latest
wait
docker build -t server-telnet-server -f servers/telnet-server/Dockerfile .
docker run -d --rm --name server-telnet-server -p 2323:23 server-telnet-server:latest
wait
docker build --no-cache -t server-ssl-heartbleed -f servers/ssl-heartbleed/Dockerfile .
docker run -d --rm --name server-ssl-heartbleed -p 8443:443 server-ssl-heartbleed:latest
wait
docker build -t server-dhcp-server -f servers/dhcp-server/Dockerfile .
docker run -d --rm --name server-dhcp-server server-dhcp-server:latest
wait
docker build --no-cache -t attack-arp-scan -f attackers/arp-scan/Dockerfile .
docker build --no-cache -t attack-arp-spoof -f attackers/arp-spoof/Dockerfile .
docker build -t attack-cdp-table-flood -f attackers/cdp-table-flood/Dockerfile .
docker build -t attack-coap-get-flood -f attackers/coap-get-flood/Dockerfile .
docker build -t attack-coap-response-fuzz -f attackers/coap-response-fuzz/Dockerfile .
docker build -t attack-coap-resource-exhaustion -f attackers/coap-resource-exhaustion/Dockerfile .
docker build -t attack-coap-token-collision -f attackers/coap-token-collision/Dockerfile .
docker build -t attack-dhcp-starvation -f attackers/dhcp-starvation/Dockerfile .
docker build -t attack-dns-tunneling -f attackers/dns-tunneling/Dockerfile .
docker build -t attack-dos-http-simple -f attackers/dos-http-simple/Dockerfile .
docker build -t attack-dos-http-slowloris -f attackers/dos-http-slowloris/Dockerfile .
docker build -t attack-fin-flood -f attackers/fin-flood/Dockerfile .
docker build -t attack-icmp-flood -f attackers/icmp-flood/Dockerfile .
docker build -t attack-icmp-tunnel -f attackers/icmp-tunnel/Dockerfile .
docker build -t attack-idor-path-traversal -f attackers/idor-path-traversal/Dockerfile .
docker build -t attack-idor-url-parameter -f attackers/idor-url-parameter/Dockerfile .
docker build -t attack-ipv6-mld-flood -f attackers/ipv6-mld-flood/Dockerfile .
docker build -t attack-ipv6-ns-flood -f attackers/ipv6-ns-flood/Dockerfile .
docker build -t attack-ipv6-ra-flood -f attackers/ipv6-ra-flood/Dockerfile .
docker build -t attack-mqtt-bruteforce -f attackers/mqtt-bruteforce/Dockerfile .
docker build -t attack-mqtt-lwt-abuse -f attackers/mqtt-lwt-abuse/Dockerfile .
docker build -t attack-mqtt-publisher -f attackers/mqtt-publisher-flood/Dockerfile .
docker build -t attack-mqtt-qos-amplification -f attackers/mqtt-qos-amplification/Dockerfile .
docker build -t attack-php-lfi-enumeration -f attackers/php-lfi-enumeration/Dockerfile .
docker build -t attack-ping-sweep -f attackers/ping-sweep/Dockerfile .
docker build -t attack-port-scanner-aggressive -f attackers/port-scanner-aggressive/Dockerfile .
docker build -t attack-port-scanner-os -f attackers/port-scanner-os/Dockerfile .
docker build -t attack-port-scanner-tcp -f attackers/port-scanner-tcp/Dockerfile .
docker build -t attack-port-scanner-udp -f attackers/port-scanner-udp/Dockerfile .
docker build -t attack-port-scanner-vulnerabilities -f attackers/port-scanner-vulnerabilities/Dockerfile .
docker build -t attack-psh-flood -f attackers/psh-flood/Dockerfile .
docker build -t attack-rst-flood -f attackers/rst-flood/Dockerfile .
docker build -t attack-smb-enumerating -f attackers/smb-enumerating/Dockerfile .
docker build -t attack-snmp-scanner -f attackers/snmp-scanner/Dockerfile .
docker build --no-cache -t attack-sql-injection -f attackers/sql-injection/Dockerfile .
docker build -t attack-ssh-bruteforce -f attackers/ssh-bruteforce/Dockerfile .
docker build -t attack-stp-conf-flood -f attackers/stp-conf-flood/Dockerfile .
docker build -t attack-stp-tcn-flood -f attackers/stp-tcn-flood/Dockerfile .
docker build -t attack-syn-flood -f attackers/syn-flood/Dockerfile .
docker build -t attack-telnet-bruteforce -f attackers/telnet-bruteforce/Dockerfile .
docker build -t attack-udp-flood -f attackers/udp-flood/Dockerfile .
docker build -t attack-web-dir-enumeration -f attackers/web-dir-enumeration/Dockerfile .
docker build -t attack-web-https-heartbleed -f attackers/web-https-heartbleed/Dockerfile .
docker build -t attack-web-post-bruteforce -f attackers/web-post-bruteforce/Dockerfile .
docker build -t attack-web-simple-scanner -f attackers/web-simple-scanner/Dockerfile .
docker build -t attack-web-wide-scanner -f attackers/web-wide-scanner/Dockerfile .
docker build -t attack-xrce-dds-discovery-poison -f attackers/xrce-dds-discovery-poison/Dockerfile .
docker build -t attack-xrce-dds-entity-flood -f attackers/xrce-dds-entity-flood/Dockerfile .
docker build -t attack-xrce-dds-fragment-abuse -f attackers/xrce-dds-fragment-abuse/Dockerfile .
docker build -t attack-xrce-dds-malformed-inject -f attackers/xrce-dds-malformed-inject/Dockerfile .
docker build -t attack-xrce-dds-session-hijack -f attackers/xrce-dds-session-hijack/Dockerfile .
docker build -t attack-xrce-dds-time-desync -f attackers/xrce-dds-time-desync/Dockerfile .
docker build -t attack-xrce-dds-udp-dos -f attackers/xrce-dds-udp-dos/Dockerfile .
docker build --no-cache -t attack-xss-scanner -f attackers/xss-scanner/Dockerfile .
docker build -t attack-zenoh-pico-fragments-reassembly -f attackers/zenoh-pico-fragments-reassembly/Dockerfile .
docker build -t attack-zenoh-pico-keepalive-flood -f attackers/zenoh-pico-keepalive-flood/Dockerfile .
docker build -t attack-zenoh-pico-memory-exhaustion -f attackers/zenoh-pico-memory-exhaustion/Dockerfile .
docker build -t attack-zenoh-pico-proto-fuzzer -f attackers/zenoh-pico-proto-fuzzer/Dockerfile .
docker build -t attack-zenoh-pico-sequence-exhaustion -f attackers/zenoh-pico-sequence-exhaustion/Dockerfile .
docker build -t attack-zenoh-pico-timestamp-mess -f attackers/zenoh-pico-timestamp-mess/Dockerfile .
docker build --no-cache -t client-random -f clients/client-random/Dockerfile .
docker build --no-cache -t client-super -f clients/client-super/Dockerfile .
if [ $( docker ps -a | grep -Ec '(dozzle)' ) -eq 0 ]; then
    docker run -d -v /var/run/docker.sock:/var/run/docker.sock -v dozzle_data:/data --restart unless-stopped --name suporte-dozzle -p 11080:8080 docker.io/amir20/dozzle:latest@sha256:6f4644814cce31e11fe80f2610515df6a5a2e40120b4087c298a72df8d65866b
fi
echo "Web server: $( docker container inspect $( docker ps -a | grep 'server-http-server' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "SSH server: $( docker container inspect $( docker ps -a | grep 'server-ssh-server' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "SMB Server: $( docker container inspect $( docker ps -a | grep 'server-smb-server' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "MQTT Broker: $( docker container inspect $( docker ps -a | grep 'server-mqtt-broker' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "CoAP Server: $( docker container inspect $( docker ps -a | grep 'server-coap-server' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "XRCE-DDS Agent: $( docker container inspect $( docker ps -a | grep 'server-xrce-dds-agent' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "Zenoh Router: $( docker container inspect $( docker ps -a | grep 'server-zenoh-router' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "Telnet Server: $( docker container inspect $( docker ps -a | grep 'server-telnet-server' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "SSL Heartbleed: $( docker container inspect $( docker ps -a | grep 'server-ssl-heartbleed' | awk '{print $NF}' ) | grep 'IPAddress' | tail -n1 | awk -F'"' '{print $4}' )"
echo "This machine: ${LOCAL_IP}"
echo -e "To monitor target server logs, open: \e[32mhttp://${LOCAL_IP}:11080/\e[0m"
