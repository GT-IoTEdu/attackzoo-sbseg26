FROM ubuntu:24.04
RUN apt update
RUN apt install lldpd -y
COPY servers/cdp-listener/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
