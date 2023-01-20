<<<<<<< HEAD
from utils import *
import time

here = str(pathlib.Path(__file__).absolute())
filepath = here[:-10] + os.path.join("\\data","sensors.yaml")
#global variable
file_descriptor = open(filepath, "r")  
variable = yaml.load(file_descriptor, yaml.FullLoader)

# f = open("dlm_data_20210413_004735.gdat", "rb")
with open("dlm_data_20210413_004735.gdat", "rb") as f:
    packet = b''
    start = False
    while (byte := f.read(1)):
        if(byte.hex() == '7e'):
            print(parse_packet(packet, variable))
            time.sleep(0.1)
            packet = b''
            start = True
        elif start:
            packet += byte
    
        # Do stuff with byte.
=======
from utils import *
import time
# import csv
import InfluxWriter as iw

here = str(pathlib.Path(__file__).absolute())
filepath = here[:-10] + os.path.join("\\data","sensors.yaml")
#global variable
file_descriptor = open(filepath, "r")  
variable = yaml.load(file_descriptor, yaml.FullLoader)

# f = open("dlm_data_20210413_004735.gdat", "rb")
with open("dlm_data_20210413_004735.gdat", "rb") as f:
    packet = b''
    start = False
    while (byte := f.read(1)):
        if(byte.hex() == '7e'):
            # print(parse_packet(packet, variable))
            wrtr = iw.InfluxWriter()
            wrtr.write([parse_packet(packet, variable)])
            time.sleep(0.1)
            packet = b''
            start = True
        elif start:
            packet += byte
    
        # Do stuff with byte.
>>>>>>> f5b83cdacdde3fcb99e6c4f3d965fcbf85af9c7e
# print(parse_packet(f.read(6), variable))