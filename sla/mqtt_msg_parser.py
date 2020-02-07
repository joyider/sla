import paho.mqtt.client as mqtt
import psycopg2

import sys
from os import getenv

PG_DATABASE = getenv('POSTGRES_DATABASE', 'mqtt')
PG_HOSTNAME = getenv('POSTGRES_HOSTNAME', 'localhost')
PG_PORT = getenv('POSTGRES_PORT', '5432')
PG_USERNAME = getenv('POSTGRES_USER', 'postgres')
PG_PASSWORD = getenv('POSTGRES_PASSWORD', 'k4km0nster')

# MQTT Settings
MQTT_Broker = "10.28.29.177"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "#"
QOS = 1
DEBUG = True


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class DatabaseManager():

    def __init__(self):
        self.conn = psycopg2.connect(host=PG_HOSTNAME, user=PG_USERNAME, password=PG_PASSWORD, dbname=PG_DATABASE)
        self.cur = self.conn.cursor()
        self.cur.execute("SET application_name TO 'MQTT to Postgres Gateway'");

    def add_del_update_db_record(self, sql_query, args=()):

        # If the SQL statement fails for some reason, do a rollback. Otherwise we will hang with "idle in transaction(aborted)" which is bad, bad, bad. Patrik.
        if sys.version_info[:3] < (3, 0):
            try:
                self.cur.execute(sql_query, args)
            except Exception, e:
                self.conn.rollback()
            else:
                self.conn.commit()
            return
        else:
            try:
                self.cur.execute(sql_query, args)
            except Exception as e:
                self.conn.rollback()
            else:
                self.conn.commit()
            return

    def __del__(self):
        self.cur.close()
        self.conn.close()


def Data_Handler(payload, dbg=False):
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into mqtt_interface (jsondata) values ('%s')" % (payload))


# Subscribe to all Sensors at Base Topic
def on_connect(mosq, obj, rc):
    print(mqttc.subscribe(MQTT_Topic, 0))


# Save Data into DB Table
def on_message(mosq, obj, msg):
    Data_Handler(str(msg.payload.decode()), DEBUG)


def on_subscribe(client, userdata, mid, granted_qos):
    if DEBUG:
        print("Subscribed: " + str(mid) + " " + str(granted_qos))


mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect to MQTT
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
mqttc.subscribe(MQTT_Topic, QOS)

# Continue the network loop
mqttc.loop_forever()