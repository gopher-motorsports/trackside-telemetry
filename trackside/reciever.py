#!/usr/bin/env python3

import yaml
import logging
import pathlib
import argparse
import datetime
from utils import *
import InfluxWriter as iw
import TracksideLogger as tl
import time as tm

'''
    Applies a format to provided string

            Parameters:
                    string (string): A string to be formatted

            Returns:
                    strl (string): formatted string with white text and blue background
    '''
def formatted(string):
    white = '\33[104m'
    black = '\33[36m'
    bold = '\33[1m'
    str1 = white + black + bold + string + "\33[0m"
    return str1

'''
    Receives hex packets from XBees, parses packets according to telemetry standard protocol and writes packet information to InfluxDB
'''
def reciever():
    #Parsing command line arguments which includes debug mode and folder for location of usb port Xbee is plugged into
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

    #checking if correct usb port is provided
    nousb = True
    try:
        logr = tl.TracksideLogger()
        nousb = False
    except Exception as e:
        nousb = True
        print("No/Wrong USB port provided.")
        print(e)

    wrtr = iw.InfluxWriter()
    
    times = [0,0,0,0,0,0]
    prnt = 0
    logging.debug("\n" * 6)

    here = str(pathlib.Path(__file__).absolute())
    filepath = here[:-11] + os.path.join("data","sensors.yaml")
    #global variable
    file_descriptor = open(filepath, "r")  
    variable = yaml.load(file_descriptor, yaml.FullLoader)
    start_time = round(tm.time() * 1000)
    
    while (True and not nousb):
        try:
            #read packet from XBee
            frame = logr.read()
            data = parse_packet_checksum(frame, variable)
            
            ## skip over each error packet until none present
            while data["name"] == 'Error bytes':
                frame = logr.read()
                data = parse_packet_checksum(frame, variable)
            ## extract data from dict
            name = data['name']
            data = data["data"]
            #time = data["time"] + start_time
            time = data["time"]
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
                tm.sleep(0.05)
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
        except TypeError:
            pass

if __name__ == "__main__":
    reciever()
