import json

import sqlite3
import psycopg2

from os import getenv


# SQLite DB Name
DB_Name = "IoT.db"

PG_DATABASE = getenv('POSTGRES_DATABASE', 'postgres')
PG_HOSTNAME = getenv('POSTGRES_HOSTNAME')
PG_PORT = getenv('POSTGRES_PORT')
PG_USERNAME = getenv('POSTGRES_USER')
PG_PASSWORD = getenv('POSTGRES_PASSWORD')


# ===============================================================
# Database Manager Class

class DatabaseManager():
    def __init__(self):
        self.conn = psycopg2.connect(host=PG_HOSTNAME, user=PG_USERNAME, password=PG_PASSWORD, dbname=PG_DATABASE)
        self.cur = self.conn.cursor()

    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()


# ===============================================================
# Functions to push Sensor Data into Database

# Function to save Temperature to TimescaleDB
def Temp_Data_Handler(jsonData, dbg=False):
    # Parse Data
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    Temperature = json_Dict['Temperature']

    # Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record(
        "insert into DHT22_Temperature_Data (SensorID, Date_n_Time, Temperature) values (%s, %s, %s)",
        (SensorID, Data_and_Time, Temperature))
    del dbObj
    if dbg:
        print("Inserted Temperature Data into Database.\n")


# Function to save Humidity to TimescaleDB
def Humidity_Data_Handler(jsonData, dbg=False):
    # Parse Data
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    Humidity = json_Dict['Humidity']

    # Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into DHT22_Humidity_Data (SensorID, Date_n_Time, Humidity)  values (%s, %s, %s)",
                                   (SensorID, Data_and_Time, Humidity))
    del dbObj
    if dbg:
        print("Inserted Humidity Data into Database. \n")


# ===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData, dbg=False):
    if Topic == "Sensors/Temperature":
        Temp_Data_Handler(jsonData, dbg)
    elif Topic == "Sensors/Humidity":
        Humidity_Data_Handler(jsonData, dbg)