import serial
import time
    
def move_right(left, ser):
    cmd = "L{:d}\n".format(left).encode('ascii')
    print("Debug cmd -- %s" %cmd)
    
    ser.write(cmd)
    read_serial=ser.readline()
    print(read_serial)