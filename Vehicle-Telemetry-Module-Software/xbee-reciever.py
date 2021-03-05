from xbee import XBee
import serial

ser = serial.Serial('/dev/ttyUSB0',9600)

xbee = XBee(ser)

while True:
    try:
        print(xbee.wait_read_frame())
    except KeyboardInterrupt:
        break
    
ser.close()