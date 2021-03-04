#!/usr/bin/env python
import time
import datetime
import psutil
from influxdb import InfluxDBClient


# influx configuration - edit these
ifuser = "trackside"
ifpass = "trackside"
ifdb = "trackside"
ifhost = "172.17.0.1"
ifport = 8086
measurement_name = "system"

def main():
    # take a timestamp for this measurement
    time = datetime.datetime.utcnow()

    # collect some stats from psutil
    disk = psutil.disk_usage('/')
    mem = psutil.virtual_memory()
    load = [0,0]
    load[0] = psutil.cpu_freq()[0]
    load[1] = psutil.cpu_percent()

    # format the data as a single measurement for influx
    body = [
        {
            "measurement": measurement_name,
            "time": time,
            "fields": {
                "cpu_frequency": load[0],
                "cpu_usage": load[1],
                "disk_percent": disk.percent,
                "disk_free": disk.free,
                "disk_used": disk.used,
                "mem_percent": mem.percent,
                "mem_free": mem.free,
                "mem_used": mem.used
            }
        }
    ]

    # connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

    # write the measurement
    ifclient.write_points(body)


white = '\33[107m'
black = '\33[30m'
bold = '\33[1m'
str1 = white + black + bold + "TRACKSIDE.PI SYSTEM PERFORMANCE MONITOR" +'\33[0m'

print(str1)



for i in range( (3600//5) * 2 ): #2 hours
    main()
    print(('\33[0m' + "Logged point at: " + '\33[33m'),datetime.datetime.now().strftime("%H:%M:%S"))
    time.sleep(5)
