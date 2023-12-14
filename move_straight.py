import serial
import time
    
def move_straight(left, ser):
    cmd = "S{:d}\n".format(left).encode('ascii')
    print("Debug cmd -- %s" %cmd)
    
    ser.write(cmd)
    read_serial=ser.readline()
    print(read_serial)
