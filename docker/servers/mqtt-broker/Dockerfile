FROM eclipse-mosquitto:2
COPY servers/mqtt-broker/mosquitto.conf /mosquitto/config/mosquitto.conf
# Usuario benigno para a campanha benigna (B8). password_file deve pertencer ao
# usuario mosquitto e nao ser legivel por outros, senao o broker recusa iniciar.
RUN mosquitto_passwd -b -c /mosquitto/config/passwd benign benignpass \
    && chown mosquitto:mosquitto /mosquitto/config/passwd \
    && chmod 0700 /mosquitto/config/passwd
EXPOSE 1883 9001
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
