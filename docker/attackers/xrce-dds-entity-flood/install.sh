#!/usr/bin/env bash
set -e
DEBIAN_FRONTEND=noninteractive
cd /opt/
git clone https://github.com/eProsima/Micro-CDR.git
cd Micro-CDR
mkdir -p build
cd build
cmake ..
make -j$(nproc)
make install
ldconfig

cd /opt/
rm -rf Micro-XRCE-DDS-Client
git clone https://github.com/eProsima/Micro-XRCE-DDS-Client.git
cp /opt/attack_entity_flood.c Micro-XRCE-DDS-Client/
cd Micro-XRCE-DDS-Client
mkdir -p build && cd build
cmake .. -DUCLIENT_BUILD_EXAMPLES=OFF
make -j$(nproc)
make install
ldconfig