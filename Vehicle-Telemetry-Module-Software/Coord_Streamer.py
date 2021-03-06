import serial
import datetime
import time

ser = serial.Serial('/dev/tty.usbserial-AK05ZIWP',9600)

for i in range( (3600//5) * 2 ): #1 hour, 2Hz

    try:
        packet = "Time: $" + datetime.datetime.now().strftime("%H:%M:%S")

        ser.write(packet)

        print( ('\33[0m' + "Logged point at: " + '\33[33m') + datetime.datetime.now().strftime("%H:%M:%S") + "\n")

        time.sleep(0.5)

    except KeyboardInterrupt:

        break

ser.close()