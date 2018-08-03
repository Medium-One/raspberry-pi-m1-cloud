# This workflow publishes data requests to the RPi according to the custom scheduler.
# It starts only after the 'Initialized':'True' message has been published by the client.

import MQTT
import Store

in1_triggered = IONode.is_trigger('in1')  # raw:Initialized tag published by client RPi
if (in1_triggered):
    Store.set_global_data("initialized", "True")

is_initialized = Store.get_global("initialized")
is_initialized_string = is_initialized.encode("latin-1")
if (is_initialized_string == "True"):
    MQTT.publish_event_to_client('Rasp_Pi', '{"Data Request":"True"}', encoding='utf-8')