# coding=utf-8
import argparse
import datetime
import sys

import requests
from fmiweatherlib import fmiweather

import my_config as conf

# This application pulls data from FMI API and sends to InfluxDB database

# Example:
# python weathersender.py --location=tampella

def _escape(value):
    """Escape characters special in line protocol measurement names and field keys."""
    return str(value).replace('\\', '\\\\').replace(',', '\\,').replace('=', '\\=').replace(' ', '\\ ')


def make_line(measurement, fields, timestamp_ns):
    """Build one InfluxDB line protocol line (numeric fields only)."""
    field_str = ','.join('%s=%s' % (_escape(k), repr(float(v))) for k, v in fields.items())
    return '%s %s %d' % (_escape(measurement), field_str, timestamp_ns)


def write_lines(lines, host, port, user, password, database, timeout=5):
    """Write line protocol lines to an InfluxDB 1.x database using the HTTP /write API."""
    response = requests.post(
        'http://%s:%s/write' % (host, port),
        params={'db': database, 'precision': 'ns'},
        auth=(user, password) if user else None,
        data='\n'.join(lines).encode('utf-8'),
        timeout=timeout)
    response.raise_for_status()  # InfluxDB answers 204 No Content on success


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

    if measTime is not None and temperature is not None:
        ts = datetime.datetime.strptime(measTime, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        timestamp_ns = int(ts.timestamp()) * 10**9
        line = make_line("weather", {"OutTemperature": temperature}, timestamp_ns)
        try:
            write_lines([line], conf.INFLUXDB_HOST, conf.INFLUXDB_PORT, conf.INFLUXDB_USER,
                        conf.INFLUXDB_PWD, conf.INFLUXDB_DATABASE)
        except requests.RequestException as e:
            sys.exit("Failed to write to InfluxDB: %s" % e)
