FROM ubuntu:24.04
RUN apt update
RUN apt install udhcpd -y
COPY servers/dhcp-server/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 67/udp
ENTRYPOINT ["/entrypoint.sh"]
