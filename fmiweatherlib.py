# coding=utf-8
import requests, urllib, datetime
import xml.dom.minidom

# Docs:
# https://en.ilmatieteenlaitos.fi/open-data-manual-fmi-wfs-services

# Available queries:
# http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=describeStoredQueries

class fmiweather():
    FMI_BASE_URL = "http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::weather::simple&"

    def __init__(self, debug=False):
        self.debugMode = debug

    def getCurrentWeather(self, location, historyMinutes=20, timestep=10):

        d = datetime.datetime.utcnow()
        d_start = d-datetime.timedelta(minutes=historyMinutes)

        params = {}
        params['place']      = location
        params['starttime']  = d_start.strftime("%Y-%m-%dT%H:%M:00Z")
        params['parameters'] = 't2m'   # comma separated list of measured items to query, 't2m' is observed temperature
        params['timestep']   = timestep      # granularity of data

        URL = self.FMI_BASE_URL + urllib.urlencode(params)

        if self.debugMode: print "URL: " + URL

        response = requests.get(URL)

        if self.debugMode: print "status: " + str(response.status_code)
        if self.debugMode: print response.headers

        if self.debugMode: print response.text

        DOMTree = xml.dom.minidom.parseString(response.text)

        collection = DOMTree.documentElement
        members = collection.getElementsByTagName("wfs:member")
        currentTemp = None
        measTime    = None

        # Result of this loop is that the latest found value is stored in currentTemp, in practise that is the latest by time.
        for member in members:
            name = member.getElementsByTagName('BsWfs:ParameterName')[0]
            namevalue = name.childNodes[0].data

            if namevalue == "t2m":
                value = member.getElementsByTagName('BsWfs:ParameterValue')[0]

                # Sometimes "NaN" is returned for very fresh data
                if value.childNodes[0].data != 'NaN':
                  currentTemp = value.childNodes[0].data

                  timeElem = member.getElementsByTagName('BsWfs:Time')[0]
                  measTime = timeElem.childNodes[0].data

                  if self.debugMode: print measTime + " : " + currentTemp

        return measTime, currentTemp
