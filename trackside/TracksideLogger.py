#!/usr/bin/env python3

import serial
import time

class TracksideLogger:
    """
    Class TracksideLogger
    Params:
    self: self
    port: USB Port to use as com
    Purpose: 
    To set up serial port communications between the xbee/usb port and python
    """
    
    def __init__(self,port='/dev/ttyUSB1'):
        self.ser = serial.Serial(port,9600,timeout=120)
    
    def read(self):
        frame = self.ser.read() #read 1 byte from xbee
        time.sleep(0.08) # idk why but this must be here, and must be less than speed of input
        # 1000x a second time.sleep(0.0008) # must be less than speed of input
        bytes = self.ser.in_waiting # returns # of bytes in xbee buffer
        frame += self.ser.read(bytes) # read package
        return frame # bytes object - raw

    def __del__(self):
        try:
            self.ser.close()
        except:
            pass
