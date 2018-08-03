# This workflow is triggered when the Raspberry Pi client successfully connects to the Medium One cloud via MQTT.
# As soon as this happens, the Medium One MQTT broker publishes an "Initialize Request" message which initializes
# the RPi.

import MQTT

MQTT.publish_event_to_client('Rasp_Pi', '{"Initialize Request":"True"}', encoding='utf-8')