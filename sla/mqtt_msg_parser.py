import paho.mqtt.client as mqtt
from data_saver import sensor_Data_Handler

# MQTT Settings
MQTT_Broker = "mosquitto"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "#"
QOS = 1
DEBUG = False

#Subscribe to all Sensors at Base Topic
def on_connect(mosq, obj, rc):
    print(mqttc.subscribe(MQTT_Topic, 0))

#Save Data into DB Table
def on_message(mosq, obj, msg):
    # This is the Master Call for saving MQTT Data into DB
    # For details of "sensor_Data_Handler" function please refer "data_saver.py"
    if DEBUG:
        print("MQTT Data Received...")
        print("MQTT Topic: " + msg.topic)
        print("Data: " + msg.payload.decode())
    sensor_Data_Handler(msg.topic, msg.payload.decode(), DEBUG)

def on_subscribe(client, userdata, mid, granted_qos):
    if DEBUG:
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
mqttc.subscribe(MQTT_Topic, QOS)

# Continue the network loop
mqttc.loop_forever()


