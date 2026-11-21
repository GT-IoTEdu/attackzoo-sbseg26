FROM docker.io/vulnerables/web-dvwa:latest@sha256:dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7
# Without this the DVWA database has no tables: every login is redirected to setup.php
COPY servers/http-server/init-db.php /tmp/init-db.php
RUN chown -R mysql:mysql /var/lib/mysql /var/run/mysqld && \
    service mysql start && service apache2 start && \
    php /tmp/init-db.php && \
    service apache2 stop && service mysql stop && rm /tmp/init-db.php
EXPOSE 80
