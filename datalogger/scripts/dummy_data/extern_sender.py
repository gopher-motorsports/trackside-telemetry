#!/usr/bin/env python
import serial
import datetime
import time
from SystemMonitor import usage

ser = serial.Serial('/dev/tty',9600)

for i in range( (3600//5) * 2 ): #1 hour, 2Hz

    try:
        packet = usage()
        packet = packet.encode('utf-8')
        ser.write(packet)

        print( ('\33[0m' + "Logged point at: " + '\33[33m') + datetime.datetime.now().strftime("%H:%M:%S") + "\n")

        time.sleep(0.5)

    except KeyboardInterrupt:

        break

ser.close()
