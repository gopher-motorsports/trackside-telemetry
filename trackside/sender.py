#!/usr/bin/env python3

from DLMSimulator import DLM 
import serial
import datetime
import time


if __name__ == "__main__":
    port = '/dev/ttyUSB0'
    speed = 9600
    ser = serial.Serial(port,speed)
    sim = DLM()
    prnt = 0

    while True:
        try:
            sim.run()
            packet = sim.data
            ser.write(packet)
            if prnt == 10:
                prnt = 0
                print( ('\33[0m' + "Logged point at: " + '\33[33m') + datetime.datetime.now().strftime("%H:%M:%S") + "\n")
            else:
                prnt += 1
            time.sleep(0.1)

        except KeyboardInterrupt:
            break

    ser.close()
