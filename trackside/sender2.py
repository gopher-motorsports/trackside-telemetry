import serial
import time

port = serial.Serial("/dev/ttyUSB0", 9600, timeout=None)
while True:
    packet = bytes.fromhex('7e 01234567 0001 01233455')
    
    port.write(packet)
    
    time.sleep(0.08)