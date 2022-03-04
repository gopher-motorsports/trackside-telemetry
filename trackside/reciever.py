#!/usr/bin/env python3

import yaml
import logging
import pathlib
import argparse
import datetime
from utils import *
import InfluxWriter as iw
import TracksideLogger as tl


def formatted(string):
    white = '\33[104m'
    black = '\33[36m'
    bold = '\33[1m'
    str1 = white + black + bold + string + "\33[0m"
    return str1

def reciever():
    parser = argparse.ArgumentParser(description='trackside')
    parser.add_argument('--debug', dest='debug', action='store',
                        default=False,
                        help='disable logging.debuging')
    parser.add_argument('--usb', dest='com_port', action='store',
                    default='/dev/ttyUSB0',
                    help='provide usb port')
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level)
    logging.debug("Debug logging enabled.")

    print(formatted("Trackside Telemetry"))
    print(formatted("Press ctrl-C to quit"))

    nousb = True
    try:
        logr = tl.TracksideLogger(port=args.com_port)
        nousb = False
    except:
        nousb = True
        print("No/Wrong USB port provided.")

    wrtr = iw.InfluxWriter()
    
    times = [0,0,0,0,0,0]
    prnt = 0
    logging.debug("\n" * 6)

    here = str(pathlib.Path(__file__).absolute())
    filepath = here[:-11] + os.path.join("data","go4-22c.yaml")
    #global variable
    file_descriptor = open(filepath, "r")  
    data = yaml.load(file_descriptor, yaml.FullLoader)

    while (True and not nousb):
        try:
            time = datetime.datetime.utcnow()
            frame = logr.read()
            data = parse_packet(frame)
            
            ## skip over each error packet until none present
            while data["name"] == 'Error bytes':
                time = datetime.datetime.utcnow()
                frame = logr.read()
                data = parse_packet(frame)
            ## extract data from dict
            name = data['name']
            data = data["data"]
            
            try:
                # format the data as a single measurement for influx
                body = [
                    {
                        "measurement": "system",
                        "time": time,
                        "fields": {
                            name: data,
                        }
                    }
                ]
                wrtr.write(body)
                times.pop(0)
                times.append(time)
                
                if prnt == 10:
                    prnt = 0
                    line = ""
                    for i in range(6):
                        line += str(times[i]) + "\n"
                    logging.debug( " \033[6B"+"\033[1000D"  + " \033[8A"+ "   "+ formatted("Wrote Data at: " + "\n"+ line) )
                    logging.debug(f"Packet:{data}")
                else:
                    prnt += 1

            except IndexError:
                logging.debug(formatted(" \033[3B"+"\033[1000D"  + " \033[2A"+">IndexError: syncing"))
                pass

            except ValueError:
                logging.debug(formatted(" \033[3B"+"\033[1000D"  + " \033[2A"+">ValueError: syncing"))
                pass


        except KeyboardInterrupt:
            logging.debug("\n")
            logging.debug(formatted("SHUTTING DOWN INTERNALS..."))

            del logr
            break

if __name__ == "__main__":
    reciever()
