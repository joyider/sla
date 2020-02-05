import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists DHT22_Temperature_Data ;
create table DHT22_Temperature_Data (
  SensorID text,
  Date_n_Time TIMESTAMPTZ not null,
  Temperature DOUBLE PRECISION
);
drop table if exists DHT22_Humidity_Data ;
create table DHT22_Humidity_Data (
  SensorID text,
  Date_n_Time TIMESTAMPTZ not null,
  Humidity DOUBLE PRECISION
);
"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()tz