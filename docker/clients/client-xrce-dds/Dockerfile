FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install build-essential cmake git -y && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone --depth 1 --branch v3.0.2 https://github.com/eProsima/Micro-XRCE-DDS-Client.git \
    && cmake -S Micro-XRCE-DDS-Client -B Micro-XRCE-DDS-Client/build -DUCLIENT_BUILD_EXAMPLES=OFF \
    && make -C Micro-XRCE-DDS-Client/build -j"$(nproc)" \
    && make -C Micro-XRCE-DDS-Client/build install \
    && ldconfig

COPY clients/client-xrce-dds/xrce-client.c /opt/xrce-client.c
RUN gcc -Wall -Wextra -O2 /opt/xrce-client.c /opt/Micro-XRCE-DDS-Client/examples/PublishHelloWorld/HelloWorld.c \
    -I/opt/Micro-XRCE-DDS-Client/examples/PublishHelloWorld -I/usr/local/include \
    -L/usr/local/lib -lmicroxrcedds_client -lmicrocdr -lpthread \
    -o /usr/local/bin/xrce-client

ENTRYPOINT ["/usr/local/bin/xrce-client"]
