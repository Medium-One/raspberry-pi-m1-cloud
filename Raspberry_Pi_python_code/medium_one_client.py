# This code connects the Raspberry Pi (RPi) to Medium One (M1) cloud.
# Here, RPi first publishes the connected event to the M1 cloud after a successful MQTT connection is established.
# Then RPi subscribes to the messages from the M1 cloud.
# After getting the initialized request as the subscribed message from M1 cloud,
# RPi then publish the initialized event, which in turn gets the data request from M1 cloud.
# The RPi then start sending the data at customize interval of time.

import paho.mqtt.client as mqtt
import ssl
import json

# Medium One Credentials from Medium One Sandbox.
# All Medium One Credentials need to be updated as individual specific Medium One Sandbox account.
m1_user = "device"                                                          # User_name.
m1_password = "Device1@"                                                    # User_password.
m1_apikey = "FEBTXN77HHV2PJPKJRC52PZQG5SGGMRSGM2TEOBYGQ4DAMBQ"              # API_Key.
m1_project_mqtt_id = "7T3kxm_Rdf4"                                          # Project_MQTT_ID.
m1_user_mqtt_id = "y9s1ZTasZs8"                                             # User_MQTT_ID.
m1_client_id = "Rasp_Pi"                       # Can be anything. Needs to match publish requests from Medium One cloud.

# Medium One specification for user credential.
MQTT_username = m1_project_mqtt_id + "/" + m1_user_mqtt_id
# Medium One specification for password credential.
MQTT_password = m1_apikey + "/" + m1_password

# MQTT publish topic.
m1_topic_publish = "0/" + m1_project_mqtt_id + "/" + m1_user_mqtt_id + "/" + m1_client_id
# MQTT subscribe topic.
m1_topic_subscribe = "1/" + m1_project_mqtt_id + "/" + m1_user_mqtt_id + "/" + m1_client_id + "/event"

data_connected = {"event_data": {"Connected": "True"}}                      # Payload to transmit when connected.
m1_connect_payload = json.dumps(data_connected)                             # Medium One MQTT accepts JSON format.

init_data = {"event_data": {"Initialized": "True"}}                         # Payload to transmit when initialized.
m1_init_payload = json.dumps(init_data)                                     # Medium One MQTT accepts JSON format.

test_data = {"event_data": {"Test_Data": "True"}}                           # Payload to transmit test data.
m1_data_payload = json.dumps(test_data)                                     # Medium One MQTT accepts JSON format.


# 'on_connect' handles the initial connection as well as the case where the RPi must reconnect due to a network problem.
def on_connect(m1_client, obj, flags, rc):
    print("Publishing Result Code: " + str(rc))

    # Publish "Connected:True" event to Medium One broker
    m1_client.publish(topic=m1_topic_publish, payload=m1_connect_payload, qos=0, retain=False)

    # Subscribe to Medium One topic in order to receive requests for information from Raspberry Pi.
    m1_client.subscribe(topic=m1_topic_subscribe, qos=0)


# Incoming requests are handled by the 'on_message' function.
def on_message(m1_client, obj, msg):
    payload_string = msg.payload.decode("utf-8", "strict")                 # Convert from bytes to str
    payload_dict = json.JSONDecoder().decode(payload_string)               # Create a Python dict object from the string
    if "Initialize Request" in payload_dict:
        print("Initialize Request Message: " + payload_string)

        # Send initialized message to M1 cloud.
        m1_client.publish(topic=m1_topic_publish, payload=m1_init_payload, qos=0, retain=False)
    elif "Data Request" in payload_dict:
        print("Data Request Message: " + payload_string)

        # Send test data to M1 cloud.
        m1_client.publish(topic=m1_topic_publish, payload=m1_data_payload, qos=0, retain=False)
    else:
        print("Invalid Message Received: " + payload_string)


def on_publish(m1_client, obj, mid):
    print("Publish Request Message ID: " + str(mid))


def on_subscribe(m1_client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    print("Subscription Result: " + str(obj))


def on_log(m1_client, obj, level, string):
    print(string)


m1_client = mqtt.Client(client_id=m1_client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311,
                        transport="tcp")

m1_client.on_message = on_message
m1_client.on_connect = on_connect
m1_client.on_publish = on_publish
m1_client.on_subscribe = on_subscribe
m1_client.on_log = on_log

m1_client.username_pw_set(username=MQTT_username, password=MQTT_password)
m1_client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)

# Certificates aren't currently used, but this is how you might point to them in the future.
# m1_client.tls_set(ca_certs="/etc/ca-certificates/ca-certs.pem", tls_version=ssl.PROTOCOL_TLSv1_2)

# Establish connection with Medium One broker
m1_client.connect(host="mqtt.mediumone.com", port=61620, keepalive=300)

# The mi_client.loop_forever() call creates a raspberry-pi-m1-cloud thread which handles MQTT communication.
# It automatically handles reconnecting.
# This is a blocking form of the network loop and will not return until the client calls disconnect().
m1_client.loop_forever()
