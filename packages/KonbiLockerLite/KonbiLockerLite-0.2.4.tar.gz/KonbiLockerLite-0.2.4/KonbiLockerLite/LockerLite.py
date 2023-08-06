import sys
import os
from pathlib import Path
import json
import BarcodeScanner
from Locker import Locker

config_file = Path(os.path.expanduser('~') + '/lockerlite.json')
config = {}
if config_file.exists():
    config = json.loads(config_file.read_text())


def setup():

    hid_device = ''
    while(hid_device == ''):
        hids = Path('/dev').glob('hidraw*')
        selectable_hid = []
        for hid in hids:
            selectable_hid.append(str(hid.absolute()))
        selectable_hid.sort()
        index = 1
        selected = config.get('scanner', '')
        if selected != '':
            selected = '(Selected: ' + selected + ')'
        while index <= len(selectable_hid):
            print('\t ' + str(index) + ') ' + selectable_hid[index-1])
            index += 1

        selected_hid = input('Please select Barcode device '+selected+':')

        try:
            selected_hid_index = int(selected_hid)
        except ValueError:
            print('Invalid selection')
        else:

            if selected_hid_index > len(selectable_hid):
                print('Invalid selection')
            else:
                hid_device = selectable_hid[selected_hid_index-1]
        config["scanner"] = hid_device
        config_file.write_text(json.dumps(config))
    usb_device = ''
    while(usb_device == ''):
        usbs = Path('/dev').glob('ttyUSB*')
        selectable_usb = []
        for usb in usbs:
            selectable_usb.append(str(usb.absolute()))
        selectable_usb.sort()
        index = 1
        selected = config.get('locker', '')
        if selected != '':
            selected = '(Selected: ' + selected + ')'
        while index <= len(selectable_usb):
            print('\t ' + str(index) + ') ' + selectable_usb[index-1])
            index += 1

        selected_usb = input('Please select Locker Port '+selected+':')

        try:
            selected_usb_index = int(selected_usb)
        except ValueError:
            print('Invalid selection')
        else:

            if selected_usb_index > len(selectable_usb):
                print('Invalid selection')
            else:
                usb_device = selectable_usb[selected_usb_index-1]
        config["locker"] = usb_device
        config_file.write_text(json.dumps(config))
        mapping_file = Path(os.path.expanduser(
            '~') + '/lockerlite_mapping.json')
        if not mapping_file.exists():
            mapping_list = {
                '101': '01',
                '102': '02',
                '103': '03',
                '104': '04',
                '105': '05',
                '106': '06',
                '107': '07',
                '108': '08',
                '109': '09',
                '110': '010',
                '201': '11',
                '202': '12',
                '203': '13',
                '204': '14',
                '205': '15',
                '206': '16',
                '207': '17',
                '208': '18',
                '209': '19',
                '210': '110'
            }
            mapping_file.write_text(json.dumps(mapping_list))
        print(config)


def run():
    if config.get('scanner', '') != '':
        locker = Locker(config.get('locker', ''))
        print('Start locker with config: ' + str(config))
        print('^C to quit')
        try:
            BarcodeScanner.listen_scanner(config["scanner"], locker.open_slot)
        except KeyboardInterrupt:
            print(' to quit')
    else:
        print('barcode scanner is not set yet. let run lockerlite setup to config scanner & locker port')


if __name__ == "__main__":
    print(sys.argv)
    print(config_file)
    if len(sys.argv) >= 2 and sys.argv[1].lower() == 'setup':
        setup()
    else:
        run()
