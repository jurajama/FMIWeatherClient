# coding=utf-8
import os

# Connection details of InfluxDB database.
# Edit the defaults below, or override them with environment variables
# (e.g. INFLUXDB_HOST=localhost) to avoid keeping secrets in the file.
INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST", "influxhost.xxx.com")
INFLUXDB_PORT = int(os.environ.get("INFLUXDB_PORT", 8086))
INFLUXDB_USER = os.environ.get("INFLUXDB_USER", "raspi")
INFLUXDB_PWD  = os.environ.get("INFLUXDB_PWD", "secret")
INFLUXDB_DATABASE = os.environ.get("INFLUXDB_DATABASE", "raspidata")
