import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

# ====================================================
# MQTT Settings 
MQTT_Broker = "127.0.0.1"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Humidity = "Sensors/Humidity"
MQTT_Topic_Temperature = "Sensors/Temperature"

DEBUG = True


# ====================================================

def on_connect(client, userdata, rc):
    if rc != 0:
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker: " + str(MQTT_Broker))


def on_publish(client, userdata, mid):
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


def publish_To_Topic(topic, message):
    mqttc.publish(topic, message)
    if DEBUG:
        print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
        print("")


toggle = 0


def publish_Fake_Sensor_Values_to_MQTT():
    threading.Timer(0.8, publish_Fake_Sensor_Values_to_MQTT).start()
    global toggle
    if toggle == 0:
        Humidity_Fake_Value = float("{0:.2f}".format(random.uniform(50, 100)))

        Humidity_Data = {}
        Humidity_Data['Sensor_ID'] = "Dummy-1"
        Humidity_Data['Date'] = (datetime.today()).strftime("%Y-%m-%d %H:%M:%S")
        Humidity_Data['Humidity'] = Humidity_Fake_Value
        humidity_json_data = json.dumps(Humidity_Data)

        if DEBUG:
            print("Publishing fake Humidity Value: " + str(Humidity_Fake_Value) + "...")
        publish_To_Topic(MQTT_Topic_Humidity, humidity_json_data)
        toggle = 1

    else:
        Temperature_Fake_Value = float("{0:.2f}".format(random.uniform(1, 30)))

        Temperature_Data = {}
        Temperature_Data['Sensor_ID'] = "Dummy-2"
        Temperature_Data['Date'] = (datetime.today()).strftime("%Y-%m-%d %H:%M:%S")
        Temperature_Data['Temperature'] = Temperature_Fake_Value
        temperature_json_data = json.dumps(Temperature_Data)

        if DEBUG:
            print("Publishing fake Temperature Value: " + str(Temperature_Fake_Value) + "...")
        publish_To_Topic(MQTT_Topic_Temperature, temperature_json_data)
        toggle = 0


publish_Fake_Sensor_Values_to_MQTT()