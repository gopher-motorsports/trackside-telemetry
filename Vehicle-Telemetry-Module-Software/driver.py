import TracksideLogger as tl
import InfluxWriter as iw
import datetime
import sys

logr = tl.TracksideLogger()
wrtr = iw.InfluxWriter()

def print_formatted(string):
    white = '\33[104m'
    black = '\33[36m'
    bold = '\33[1m'
    str1 = white + black + bold + string +'\33[0m'
    print(str1)

while True:
    try:
        time = datetime.datetime.utcnow()
        frame = logr.read() # bytes object - raw
        frame = str(frame,'utf-8')
            
        usage = frame.split(",")
        
        try:
            diskpercent = float(usage[1])
            diskused = int(usage[2])
            mem1 = float(usage[3])
            mem2 = int(usage[4])
            mem3 = int(usage[5])
            load_0 = float(usage[6])
            load_1 = float(usage[7])
        
            # format the data as a single measurement for influx
            body = [
                {
                    "measurement": "system",
                    "time": time,
                    "fields": {
                        "cpu_frequency": load_0,
                        "cpu_usage": load_1,
                        "disk_percent": diskpercent,
                        "disk_used": diskused,
                        "mem_percent": mem1,
                        "mem_free": mem2,
                        "mem_used": mem3
                    }
                }
            ]
            
            wrtr.write(body)
            
            
            
            print_formatted("Wrote Data at: " + str(time))
            
            
            
        except IndexError:
            print_formatted("Attempting to sync again...")
            pass
        except ValueError:
            print_formatted("Attempting to sync again...")
            pass
        
    except KeyboardInterrupt:
        print("\n")
        print_formatted("SHUTTING DOWN INTERNALS...")
        
        del logr
        break
        
