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
        frame = self.ser.read() #read frame and wait
        time.sleep(0.08) # must be less than speed of input
        bytes = self.ser.in_waiting 
        frame += self.ser.read(bytes) # read package
        return frame # bytes object - raw

    def __del__(self):
        self.ser.close()