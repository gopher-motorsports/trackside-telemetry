#!/usr/bin/env python3

import yaml
import datetime
import os
import pathlib
import struct


here = str(pathlib.Path(__file__).absolute())
filepath = here[:-8] + os.path.join("data","dyno-can-config.yaml")
#global variable
file_descriptor = open(filepath, "r")  
data = yaml.load(file_descriptor, yaml.FullLoader)

'''
        Parses a single packet from the car (DLM) 
        and returns it as a python dictionary with
        the key as the sensor name, and the value
        as the sensors reading

            Parameters:
                    packet (bytes): A bytes object that represents the data from the car
                    data (dictionary): A dictionary of the sensors.yaml file

            Returns:
                    dictionary: dictionary with keys as name, data, and time
    '''
def parse_packet(packet, data):
    #packet = packet.rstrip(bytes.fromhex("7e"))
    packet = packet.hex()
    # if startBit == b'7e':
    #Account for escape bytes
    while '7d' in packet:
        index = packet.index('7d')
        result = int(packet[index + 2:index + 4], 16) ^ int('0x20', 16)
        packet = packet[0:index] + '{:x}'.format(result) + packet[index + 4:]
    
    if packet != b'' and len(packet) - 2 >= 14:
        time = int(packet[0:8], 16)
        name = int(packet[8:12], 16)
        dic = data['parameters']
        
        for info in dic.values():
            if info['id'] == name:
                try:
                    value_type = info['type']
                    nobytes = 0 
                    if(value_type == "UNSIGNED8"):
                        nobytes = 1
                        structFormat = '>B'
                    elif(value_type == "FLOATING"):
                        nobytes = 4
                        structFormat = '>f'
                    elif(value_type == "UNSIGNED32"):
                        nobytes = 4
                        structFormat = '>I'
                    elif(value_type == "UNSIGNED16"):
                        nobytes = 2
                        structFormat = '>H'
                    end = 12 + nobytes * 2
                    value = packet[12:end]
                    value = struct.unpack(structFormat, bytes.fromhex(value))[0]
                    return {"name": info['motec_name'], "data": value, "time": time}
                   
                except ValueError as ve:
                    return {"name": 'Error bytes', "data": packet, "time": time, "Message":ve}
                except struct.error as error:
                    print(error)
                    return {"name": 'Error bytes', "data": packet, "time": time, "Message":error}
    else:
        return {"name": 'Error bytes', "data": packet, "time": datetime.datetime.utcnow()}

def parse_packet_checksum(packet, data):
    #packet = packet.rstrip(bytes.fromhex("7e"))
    packet = packet.hex()
    # print(packet)
    # if startBit == b'7e':
    #Account for escape bytes
    while '7d' in packet:
        index = packet.index('7d')
        result = int(packet[index + 2:index + 4], 16) ^ int('0x20', 16)
        packet = packet[0:index] + '{:x}'.format(result) + packet[index + 4:]
    
        
    if packet != b'' and len(packet) - 2 >= 15:
        time = int(packet[0:8], 16)
        name = int(packet[8:12], 16)
        dic = data['parameters']
        
        for info in dic.values():
            if info['id'] == name:
                try:
                    value_type = info['type']
                    nobytes = 0 
                    if(value_type == "UNSIGNED8"):
                        nobytes = 1
                        structFormat = '>B'
                    elif(value_type == "FLOATING"):
                        nobytes = 4
                        structFormat = '>f'
                    elif(value_type == "UNSIGNED32"):
                        nobytes = 4
                        structFormat = '>I'
                    elif(value_type == "UNSIGNED16"):
                        nobytes = 2
                        structFormat = '>H'
                    end = 12 + nobytes * 2
                    value = packet[12:end]
                    value = struct.unpack(structFormat, bytes.fromhex(value))[0]

                    # Check the single byte checksum that is the sum of each byte in the message, including the start byte
                    checksum = packet[end:end + 2]
                    checksum = int(str(checksum), 16)
                    num_bytes = 0
                    total = 0
                    hex = ""
                    escape = False
                    for byte in packet:
                        hex += str(byte)
                        num_bytes += 1
                        if num_bytes == 2:
                            # if (hex == "7d"):  # Throw away the 0x7D byte
                            #     hex = ""
                            #     num_bytes = 0
                            #     escape = True
                            # elif escape:  # XOR the escaped byte with 0x20
                            #     total += (int(hex, 16) ^ int("20", 16))
                            #     num_bytes = 0
                            #     hex = ""
                            #     escape = False
                            # else:
                            #     total += int(hex, 16)
                            #     num_bytes = 0
                            #     hex = ""
                            total += int(hex, 16)
                            num_bytes = 0
                            hex = ""
                    total += 126  # Accounts for the decimal value of the start byte (7E -> 126)
                    new_checksum = total % 256
                    if new_checksum != checksum:
                        # print("Checksum failed")
                        # print("Expected: " + total)
                        # print("Acutal: " + checksum)
                        return {"name": 'Error bytes', "data": packet, "time": time, "Message":'Checksum failed'}

                    return {"name": info['motec_name'], "data": value, "time": time}
    
                except ValueError as ve:
                    return {"name": 'Error bytes', "data": packet, "time": time, "Message":ve}
                except struct.error as error:
                    print(error)
                    return {"name": 'Error bytes', "data": packet, "time": time, "Message":error}
    else:
        return {"name": 'Error bytes', "data": packet, "time": datetime.datetime.utcnow()}