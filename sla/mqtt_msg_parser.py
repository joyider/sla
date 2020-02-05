import paho.mqtt.client as mqtt
from data_saver import sensor_Data_Handler

# MQTT Settings
MQTT_Broker = "mosquitto"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "#"
QOS = 1

#Subscribe to all Sensors at Base Topic
def on_connect(mosq, obj, rc):
    print(mqttc.subscribe(MQTT_Topic, 0))

#Save Data into DB Table
def on_message(mosq, obj, msg):
    # This is the Master Call for saving MQTT Data into DB
    # For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
    print("MQTT Data Received...")
    print("MQTT Topic: " + msg.topic)
    print("Data: " + msg.payload.decode())
    sensor_Data_Handler(msg.topic, msg.payload.decode())

def on_subscribe(client, userdata, mid, granted_qos):
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



# import paho.mqtt.client as paho

# def on_subscribe(client, userdata, mid, granted_qos):
#    print("Subscribed: "+str(mid)+" "+str(granted_qos))

# def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

# client = paho.Client()
# client.on_subscribe = on_subscribe
# client.on_message = on_message
# client.connect("127.0.0.1", 1883)
# client.subscribe("#", qos=1)

# client.loop_forever()