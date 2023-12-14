import cv2
import numpy as np
from picamera2 import Picamera2, Preview
import serial
import time
from move_left import move_left 
from move_right import move_right
from move_straight import move_straight

height = 120
width = 160

ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0',9600)
time.sleep(2)

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size":(width, height)}, lores={"size": (width, height)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

def cameraTest():
    picam2.capture_file("test.jpg")


def main():
    
    while(1):
        cameraTest()
        
        frame = cv2.imread('test.jpg')
        
        #? Why flip?
        #frame = cv2.flip(frame,-1)
        cv2.imshow('before', frame)
        
        #세로: 60~120px, 가로: 0~160px
        crop_img =frame[0:90, 0:160] 
        
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        
        # 40 - 50
        ret,thresh1 = cv2.threshold(blur,40,255,cv2.THRESH_BINARY_INV)
        
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow('masked',mask)
    
        contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        #? cx 좌/우 이동 기준 설정
        # 95, 125, 39, 65 change
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            print(cx)
            
            #? 좌우 이동 속도 설정
            # 65 80 95
            if cx >= 95 and cx <= 500:              
                print("Turn Right")
                move_right(125, ser)
                #cmd_arduino(40,0)
            elif cx >= 0 and cx <= 65:
                print("Turn Left")
                move_left(125, ser)
                #cmd_arduino(0,40)
            else:
                move_straight(125, ser)
                print("go")
                #cmd_arduino(40,40)
        else:
            pass
            #print("Turn Left")
            #move_left(100,ser)
        #? 종결조건: 현재는 키보드 q입력
        
        time.sleep(0.5)
        
    cv2.destroyAllWindows()
     
if __name__ == '__main__':
    main()
