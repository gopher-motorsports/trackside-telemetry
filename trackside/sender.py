#!/usr/bin/env python


## DEMONSTRATION PURPOSES ONLY  - SIMULATE CAR IN MOTION
## XBEE MUST BE CONNECTED TO SERIAL PORT:
port = 9600



from DLMSimulator import DLM 
import serial
import datetime
import time

ser = serial.Serial('/dev/tty',port)

for i in range( (3600//5) * 2 ): #1 hour, 2Hz

    try:
        sim = DLM()
        sim.run()
        packet = sim.data
        packet = packet.encode('utf-8')
        ser.write(packet)

        print( ('\33[0m' + "Logged point at: " + '\33[33m') + datetime.datetime.now().strftime("%H:%M:%S") + "\n")

        time.sleep(0.5)

    except KeyboardInterrupt:

        break

ser.close()