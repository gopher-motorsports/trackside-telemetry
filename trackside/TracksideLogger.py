#!/usr/bin/env python3

import serial
import time

class TracksideLogger:
    '''
        Class TracksideLogger
        Sets up serial port communications between the xbee/usb port and python
            Parameters:
                    self (self): self
                    port (string): USB port folder to use as COM
    '''
    def __init__(self,port='/dev/ttyUSB0'):
        self.ser = serial.Serial(port,9600,timeout=120)
    
    '''
        Reads bytes from XBees

            Parameters:
                    self (self): self
                    packet (dictionary): A dictionary of the sensors.yaml file

            Returns:
                    packet: bytes object of the packet read
    '''
    def read(self):
        packet = self.ser.read_until(expected=bytes.fromhex("7e"))
        time.sleep(0.08)
        return packet

    
    def __del__(self):
        try:
            self.ser.close()
        except:
            pass
