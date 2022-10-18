import sys
import os
import fusee_launcher as fusee
import mock_arguments
from time import sleep

if len(sys.argv) != 2 or sys.argv[1] == "-help" or sys.argv[1] == "-h":
    print("Usage: " + sys.argv[0] + " (<payload file> | -sdmount)")
    exit()


device_found = False
usb_backend  = fusee.HaxBackend.create_appropriate_backend()

def build_mountusb_path(self):
    try:
        path = sys._MEIPASS
    except Exception:
        path = os.path.abspath('.')
    return os.path.join(path, 'memloader.bin')

def build_relocator_path(self):
    try:
        path = sys._MEIPASS
    except Exception:
        path = os.path.abspath('.')
    return os.path.join(path, 'intermezzo.bin')

print("Waiting for device...")
while not device_found:
    device = usb_backend.find_device(0x0955, 0x7321)
    device_found = bool(device)
    sleep(0.3)

args = mock_arguments.MockArguments()
if sys.argv[1] == "-sdmount":
    print("Found device, sending mountusb payload...")
    args.payload   = build_mountusb_path()
else:
    print("Found device, sending payload...")
    args.payload   = payload_path
args.relocator = build_relocator_path()
fusee.do_hax(args)

