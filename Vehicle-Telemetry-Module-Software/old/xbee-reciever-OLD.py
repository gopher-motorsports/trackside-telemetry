import serial
import time

ser = serial.Serial('/dev/ttyUSB1',9600,timeout=25)

white = '\33[107m'
black = '\33[30m'
bold = '\33[1m'
str1 = white + black + bold + "XBEE-RECIEVER PI-SIDE" +'\33[0m'

print(str1)

while True:
    try:
        #xbee.wait_read_frame()
        #frame = xbee.wait_read_frame()['rf_data']
        frame = ser.read()
        time.sleep(0.4)
        bytes = ser.in_waiting
        frame += ser.read(bytes)
        
        print(frame)
        print("\n")
        print(" type: ")
        print(type(frame))
        print("\n")
        
    except KeyboardInterrupt:
        break
    
ser.close()