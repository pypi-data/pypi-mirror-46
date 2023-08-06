import os
from pathlib import Path
import json
import serial
import time
from crccheck.crc import Crc16


class Locker:
    def __init__(self, port):
        self.port = port
        self.location_mapping = {}
        mapping_file = Path(os.path.expanduser(
            '~') + '/lockerlite_mapping.json')
        if mapping_file.exists():
            self.location_mapping = json.loads(mapping_file.read_text())

    def get_location(self, location):
        cabinet = 0
        slot = 0
        code = self.location_mapping.get(str(location), '')
        if len(code) < 2:
            raise ValueError('location: ' + str(location) +
                             ' code: ' + code + ' - is invalid')

        cabinet = int(code[0:1])
        slot = int(code[1:])
        return (cabinet, slot)

    def calcCrc(self, barray):
        num = 0
        for idx, value in enumerate(list(barray)):
            num ^= value << 8
            for idx2 in range(8):
                if (num & 32768) != 0:
                    num = num << 1 ^ 4129
                else:
                    num <<= 1

    def open(self, cabinet, slots):

        open_success = False

        with serial.Serial() as ser:
            ser.port = self.port
            ser.open()

            # PCToDrivingBoard
            bytes = bytearray.fromhex('C7')
            # number of slots
            if len(slots) > 0:
                bytes.append(6+len(slots))
            else:
                bytes.append(7)
            # cabinet
            bytes.append(cabinet)
            # RequestToOpen
            bytearray.extend(bytes, bytearray.fromhex('52'))
            # cabinet
            bytes.append(cabinet)
            bytes.append(0)

            bytearray.extend(bytes, bytearray(slots))

            # calculate crc
            crc = Crc16.calc(bytes)

            bytearray.extend(bytes, bytearray(
                crc.to_bytes(2, byteorder='big')))

            print('write to Serial Port', "".join("%02x " % b for b in bytes))
            ser.write(bytes)
            open_success = ser.is_open

        return open_success

    def open_slot(self, barcode):
        locations = json.loads(barcode)
        print(locations)
        for location in locations:
            cabinet, slot = self.get_location(location)
            result = self.open(cabinet, [slot])
            if result:
                print('open success', 'cabinet: ' +
                      str(cabinet), 'slot: ' + str(slot))
            else:
                print('fail to open', 'cabinet: ' +
                      str(cabinet), 'slot: ' + str(slot))
