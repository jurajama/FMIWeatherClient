# coding=utf-8
import argparse
import sys

import requests
from fmiweatherlib import fmiweather

from influxdb import InfluxDBClient

import my_config as conf

# This application pulls data from FMI API and sends to InfluxDB database

# Example:
# python weathersender.py --location=tampella

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--location", required=True, help="Location for which weather data is searched")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    options = parser.parse_args()

    w = fmiweather(debug=options.debug)

    try:
        measTime, temperature = w.getCurrentWeather(location=options.location, historyMinutes=30)
    except requests.RequestException as e:
        sys.exit("Failed to fetch weather data: %s" % e)

    json_temp = [
        {
            "measurement": "weather",
            "time": measTime,
            "fields": {
               "OutTemperature": temperature
            }
        }
    ]

    if measTime is not None and temperature is not None:
        client = InfluxDBClient(conf.INFLUXDB_HOST, conf.INFLUXDB_PORT, conf.INFLUXDB_USER, conf.INFLUXDB_PWD, conf.INFLUXDB_DATABASE, timeout=5)
        client.write_points(json_temp)
