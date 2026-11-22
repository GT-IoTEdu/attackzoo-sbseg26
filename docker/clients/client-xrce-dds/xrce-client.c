// Benign Micro XRCE-DDS client: publishes HelloWorldTopic with the session key, topic and type of the
// PublishHelloWorld example of Micro-XRCE-DDS-Client, to a given agent or to one found by XRCE discovery.
#include "HelloWorld.h"

#include <uxr/client/client.h>
#include <ucdr/microcdr.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STREAM_HISTORY  8
#define BUFFER_SIZE     UXR_CONFIG_UDP_TRANSPORT_MTU * STREAM_HISTORY
#define CLIENT_KEY      0xAAAABBBB

static char agent_ip[16];
static char agent_port[8];

// Accept a discovered agent only if a session opens on it, as micro-ROS does.
static bool on_agent_found(
        const TransportLocator* locator,
        void* args)
{
    (void) args;
    if (agent_ip[0] != '\0')
    {
        return true;
    }

    char ip[16];
    char port_str[8];
    uint16_t port;
    uxrIpProtocol protocol;
    if (!uxr_locator_to_ip(locator, ip, sizeof(ip), &port, &protocol))
    {
        return false;
    }
    snprintf(port_str, sizeof(port_str), "%u", port);

    bool ok = false;
    uxrUDPTransport transport;
    if (uxr_init_udp_transport(&transport, protocol, ip, port_str))
    {
        uxrSession session;
        uxr_init_session(&session, &transport.comm, CLIENT_KEY);
        ok = uxr_create_session_retries(&session, 5);
        if (ok)
        {
            uxr_delete_session(&session);
        }
        uxr_close_udp_transport(&transport);
    }
    printf("discovery: agent %s:%s %s\n", ip, port_str, ok ? "accepted" : "rejected (no session)");
    if (ok)
    {
        snprintf(agent_ip, sizeof(agent_ip), "%s", ip);
        snprintf(agent_port, sizeof(agent_port), "%s", port_str);
    }
    return ok;
}

static void usage(
        const char* prog)
{
    printf("usage: %s publish <agent_ip> <agent_port> <count> <interval_ms>\n"
            "       %s discover <attempts> <period_ms> <count> <interval_ms>\n"
            "count 0 publishes until the container stops or the session is lost\n", prog, prog);
}

int main(
        int argc,
        char** argv)
{
    setvbuf(stdout, NULL, _IOLBF, 0);
    if (argc != 6)
    {
        usage(argv[0]);
        return 2;
    }
    uint32_t max_topics = (uint32_t)strtoul(argv[4], NULL, 10);
    int interval_ms = atoi(argv[5]);

    if (0 == strcmp(argv[1], "discover"))
    {
        printf("discovery: GET_INFO to 239.255.0.2:7400, attempts %s, period %s ms\n", argv[2], argv[3]);
        uxr_discovery_agents_default((uint32_t)atoi(argv[2]), atoi(argv[3]), on_agent_found, NULL);
        if (agent_ip[0] == '\0')
        {
            printf("discovery: no agent accepted\n");
            return 1;
        }
    }
    else if (0 == strcmp(argv[1], "publish"))
    {
        snprintf(agent_ip, sizeof(agent_ip), "%s", argv[2]);
        snprintf(agent_port, sizeof(agent_port), "%s", argv[3]);
    }
    else
    {
        usage(argv[0]);
        return 2;
    }

    uxrUDPTransport transport;
    if (!uxr_init_udp_transport(&transport, UXR_IPv4, agent_ip, agent_port))
    {
        printf("transport: cannot open %s:%s\n", agent_ip, agent_port);
        return 1;
    }
    uxrSession session;
    uxr_init_session(&session, &transport.comm, CLIENT_KEY);
    if (!uxr_create_session(&session))
    {
        printf("session: create on %s:%s failed\n", agent_ip, agent_port);
        return 1;
    }
    printf("session: created on %s:%s, key 0x%08X\n", agent_ip, agent_port, CLIENT_KEY);

    uint8_t output_reliable_stream_buffer[BUFFER_SIZE];
    uxrStreamId reliable_out = uxr_create_output_reliable_stream(&session, output_reliable_stream_buffer, BUFFER_SIZE,
                    STREAM_HISTORY);
    uint8_t input_reliable_stream_buffer[BUFFER_SIZE];
    uxr_create_input_reliable_stream(&session, input_reliable_stream_buffer, BUFFER_SIZE, STREAM_HISTORY);

    uxrObjectId participant_id = uxr_object_id(0x01, UXR_PARTICIPANT_ID);
    const char* participant_xml = "<dds>"
            "<participant>"
            "<rtps>"
            "<name>default_xrce_participant</name>"
            "</rtps>"
            "</participant>"
            "</dds>";
    uint16_t participant_req = uxr_buffer_create_participant_xml(&session, reliable_out, participant_id, 0,
                    participant_xml, UXR_REPLACE);

    uxrObjectId topic_id = uxr_object_id(0x01, UXR_TOPIC_ID);
    const char* topic_xml = "<dds>"
            "<topic>"
            "<name>HelloWorldTopic</name>"
            "<dataType>HelloWorld</dataType>"
            "</topic>"
            "</dds>";
    uint16_t topic_req = uxr_buffer_create_topic_xml(&session, reliable_out, topic_id, participant_id, topic_xml,
                    UXR_REPLACE);

    uxrObjectId publisher_id = uxr_object_id(0x01, UXR_PUBLISHER_ID);
    uint16_t publisher_req = uxr_buffer_create_publisher_xml(&session, reliable_out, publisher_id, participant_id,
                    "", UXR_REPLACE);

    uxrObjectId datawriter_id = uxr_object_id(0x01, UXR_DATAWRITER_ID);
    const char* datawriter_xml = "<dds>"
            "<data_writer>"
            "<topic>"
            "<kind>NO_KEY</kind>"
            "<name>HelloWorldTopic</name>"
            "<dataType>HelloWorld</dataType>"
            "</topic>"
            "</data_writer>"
            "</dds>";
    uint16_t datawriter_req = uxr_buffer_create_datawriter_xml(&session, reliable_out, datawriter_id, publisher_id,
                    datawriter_xml, UXR_REPLACE);

    uint8_t status[4];
    uint16_t requests[4] = {
        participant_req, topic_req, publisher_req, datawriter_req
    };
    if (!uxr_run_session_until_all_status(&session, 1000, requests, status, 4))
    {
        printf("entities: participant %u topic %u publisher %u datawriter %u\n", status[0], status[1], status[2],
                status[3]);
        return 1;
    }

    bool connected = true;
    uint32_t count = 0;
    while (connected && (0 == max_topics || count < max_topics))
    {
        HelloWorld topic = {
            ++count, "Hello DDS world!"
        };
        ucdrBuffer ub;
        uint32_t topic_size = HelloWorld_size_of_topic(&topic, 0);
        uxr_prepare_output_stream(&session, reliable_out, datawriter_id, &ub, topic_size);
        HelloWorld_serialize_topic(&ub, &topic);
        printf("write: id %u\n", topic.index);
        connected = uxr_run_session_time(&session, interval_ms);
    }
    if (!connected)
    {
        printf("session: lost, write id %u not acknowledged\n", count);
    }

    uxr_delete_session(&session);
    uxr_close_udp_transport(&transport);
    return connected ? 0 : 3;
}
