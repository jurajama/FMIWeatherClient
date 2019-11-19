# FMIWeatherClient
Python client to read weather info from FMI open data service https://en.ilmatieteenlaitos.fi/open-data-manual-fmi-wfs-services

## Installation and use

Using the demo application to print result to console does not require any other modules to be installed. Execute the tool:
``python3 demo.py --location tampella
``

Location parameter is geographical name for the place for which you want to get the data. It could be generic like "helsinki", or more specific FMI observation station like "tampella".

_weathersender.py_ is application that sends temperature data to InfluxDB database setup with https://github.com/jurajama/TempMonitor. To use that, configure your server information in _my_config.py_ and run the application like _python3 /home/pi/FMIWeatherClient/weathersender.py --location=tampella_. You may want to make that as cron task to send data periodically.
