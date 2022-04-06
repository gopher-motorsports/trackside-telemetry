import struct
import binascii

packet = '3fe519d040000000'


while '7d' in packet:
        index = packet.index('7d')
        result = int(packet[index + 2:index + 4], 16) ^ int('0x20', 16)
        packet = packet[0:index] + '{:x}'.format(result) + packet[index + 4:]
        
value = struct.unpack('>d', binascii.unhexlify(packet))
print(type(value[0]))