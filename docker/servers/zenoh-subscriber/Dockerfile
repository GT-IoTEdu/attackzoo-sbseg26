FROM python:3.11-slim
RUN pip install --no-cache-dir eclipse-zenoh==1.7.2
COPY servers/zenoh-subscriber/zenoh-subscriber.py /opt/zenoh-subscriber.py
ENTRYPOINT ["python3", "-u", "/opt/zenoh-subscriber.py"]
