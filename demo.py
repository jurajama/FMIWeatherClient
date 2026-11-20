# coding=utf-8
import argparse
import sys

import requests
from fmiweatherlib import fmiweather


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

    if measTime is not None:
        print ("result: " + measTime + " : " + str(temperature))
    else:
        print ("No results found")
