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

    usage = monitor.usage().split(",")

    diskfree = usage[0]
    diskpercent = usage[1]
    diskused = usage[2]
    mem1 = usage[3]
    mem2 = usage[4]
    mem3 = usage[5]
    load_0 = usage[6]
    load_1 = usage[7]

    # format the data as a single measurement for influx
    body = [
        {
            "measurement": measurement_name,
            "time": time,
            "fields": {
                "cpu_frequency": load_0,
                "cpu_usage": load_1,
                "disk_percent": diskpercent,
                "disk_free": diskfree,
                "disk_used": diskused,
                "mem_percent": mem1,
                "mem_free": mem2,
                "mem_used": mem3
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
str1 = white + black + bold + "SYSTEM PERFORMANCE MONITOR" +'\33[0m'

print(str1)



for i in range( (3600//5) * 2 ): #2 hours
    main()
    print(('\33[0m' + "Logged point at: " + '\33[33m'),datetime.datetime.now().strftime("%H:%M:%S"))
    time.sleep(0.5)
