import serial
import time

class TracksideLogger:
    
    def __init__(self,port='/dev/ttyUSB1'):
        self.ser = serial.Serial(port,9600,timeout=25)
        
        white = '\33[107m'
        black = '\33[30m'
        bold = '\33[1m'
        str1 = white + black + bold + "TRACKSIDE.PI LOGGER" +'\33[0m'
        str2 = white + black + bold + "CTRL-C TO QUIT" +'\33[0m'
        str3 = white + black + bold + "WAITING FOR PACKET..." +'\33[0m'
        print("\n")
        print(str1)
        print(str2)
        print(str3)
        print("\n")
    
    def read(self):
        frame = self.ser.read() #read frame and wait
        time.sleep(0.4) # must be less than speed of input
        bytes = self.ser.in_waiting 
        frame += self.ser.read(bytes) # read package
    
        return frame # bytes object - raw

    def __del__(self):
        self.ser.close()
        
        white = '\33[107m'
        black = '\33[30m'
        bold = '\33[1m'
        str1 = white + black + bold + "GOODBYE!" +'\33[0m'
        print(str1)