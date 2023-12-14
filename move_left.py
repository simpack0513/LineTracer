import serial
import time
    
def move_left(right, ser):
    ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0',9600)

    cmd = "R{:d}\n".format(right).encode('ascii')
    print("Debug cmd -- %s" %cmd)
    
    ser.write(cmd)
    read_serial=ser.readline()
    print(read_serial)


