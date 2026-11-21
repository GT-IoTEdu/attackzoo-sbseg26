FROM docker.io/hahwul/dalfox:latest@sha256:91d5cebda9114fb7c2bfc7ad179ac5d605705c0bf4632a68f572f7a2f1d8a6dc
USER root
COPY attackers/xss-scanner/XSS-payloadbox.txt /app/XSS-payloadbox.txt
COPY --chmod=0777 attackers/xss-scanner/entrypoint.sh /app/runstart.sh
RUN chmod +x /app/dalfox && apk add --no-cache curl
ENTRYPOINT ["/app/runstart.sh"]
