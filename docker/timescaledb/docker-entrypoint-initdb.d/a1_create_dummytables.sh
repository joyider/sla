#!/usr/bin/env bash

psql -U "${POSTGRES_USER}" postgres -c "create table DHT22_Temperature_Data (
  SensorID text,
  Date_n_Time TIMESTAMPTZ not null,
  Temperature DOUBLE PRECISION
);"

psql -U "${POSTGRES_USER}" postgres -c "create table DHT22_Humidity_Data (
  SensorID text,
  Date_n_Time TIMESTAMPTZ not null,
  Humidity DOUBLE PRECISION
);"

psql -U "${POSTGRES_USER}" postgres -c "select create_hypertable('dht22_humidity_data','date_n_time');"
psql -U "${POSTGRES_USER}" postgres -c "select create_hypertable('dht22_temperature_data','date_n_time');"