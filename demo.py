# coding=utf-8
from optparse import OptionParser
from fmiweatherlib import fmiweather


if __name__ == '__main__':
    parser = OptionParser('usage: %prog [options]')

    parser.add_option("-l", "--location", type="string", dest="location", help="Location for which weather data is searched")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debug mode")

    (options, args) = parser.parse_args()

    required="location".split()

    for r in required:
        if options.__dict__[r] is None:
            parser.error("parameter %s required"%r)


    w = fmiweather(debug=options.debug)

    measTime, temperature = w.getCurrentWeather(location=options.location, historyMinutes=30)

    print "result: " + measTime + " : " + str(temperature)
