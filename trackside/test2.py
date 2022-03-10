"""Receive packets via Xbee module

This script uses an Xbee module connected via USB to wirelessly receive data sent from another Xbee module.
Run with "python -u xbee-demo.py" to prevent output buffering
"""

import serial
from utils import *

def decodePacket(packet):
    # remove start delimiter from byte string
    byteStr = packet.rstrip(bytes.fromhex("7e"))
    pkt = []
    # escape & append bytes
    escNext = False
    for byte in byteStr:
        if escNext:
            pkt.append(byte ^ 0x20)
            escNext = False
        elif (byte == int("7d", base=16)):
            escNext = True
        else:
            pkt.append(byte)
            escNext = False
    # convert to hex strings
    pkt = [hex(byte) for byte in pkt]
    print(pkt)

print("Listening...")
port = serial.Serial("/dev/ttyUSB0", 9600, timeout=None)
while True:
    # start = bytes.fromhex("7e")
    # print(type(bytes.fromhex("7e")))
    # print(port.read_until(expected=start))
    # packet = port.read_until(expected=bytes.fromhex("7e"))
    # decodePacket(packet)
    # packet = port.read(1)
    # print(packet)

    packet = port.read_until(expected=bytes.fromhex("7e"))
    print(packet)
    print(parse_packet(packet))