 #coding=utf-8 
 #by zcy 
 #可以直接拖动进度条进行修改，也可以在checkcounter里面用预存好的counter/ground进行测试
import cv2
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
import time

import pyrealsense as pyrs
from pyrealsense.constants import rs_option
cv2.namedWindow('camera')
def nothing(x):
    pass    
cv2.createTrackbar('h1','camera',0,255,nothing)
cv2.createTrackbar('h2','camera',100,255,nothing)
cv2.createTrackbar('s1','camera',0,255,nothing)
cv2.createTrackbar('s2','camera',100,255,nothing)
cv2.createTrackbar('v1','camera',0,255,nothing)
cv2.createTrackbar('v2','camera',100,255,nothing)

color_dist = {'counter': {'Lower': np.array([40, 100, 50]), 'Upper': np.array([200, 200, 255])}, 
             'ground':{'Lower': np.array([50, 80, 40]), 'Upper': np.array([150, 180, 255])}
             }
         
def checkcounter(farme,color,erode_hsv):
    inRange_hsv = cv2.inRange(erode_hsv, color_dist[color]['Lower'], color_dist[color]['Upper'])
    cv2.imshow('11',inRange_hsv)
    contours, heirs = cv2.findContours(inRange_hsv.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            #frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)
    for item in contours:
        rect = cv2.minAreaRect(item)
        
        if(rect[1][0]>100 and rect[1][0] <400 and rect[1][1]>80 and rect[1][1]<250):   
            box = cv2.boxPoints(rect)
            cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)

def checkcounter(farme,h1,s1,v1,h2,s2,v2,erode_hsv):
    inRange_hsv = cv2.inRange(erode_hsv, np.array([h1,s1,v1]), np.array([h2,s2,v2]))
    cv2.imshow('11',inRange_hsv)
    contours, heirs = cv2.findContours(inRange_hsv.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            #frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)
    for item in contours:
        rect = cv2.minAreaRect(item)
        
        if(rect[1][0]>100 and rect[1][0] <400 and rect[1][1]>80 and rect[1][1]<250):   
            box = cv2.boxPoints(rect)
            cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)

with pyrs.Service() as serv:
    with pyrs.Service().Device() as dev:

        dev.apply_ivcam_preset(0)

        try:  # set custom gain/exposure values to obtain good depth image
            custom_options = [(rs_option.RS_OPTION_COLOR_ENABLE_AUTO_EXPOSURE,False),(rs_option.RS_OPTION_COLOR_ENABLE_AUTO_WHITE_BALANCE, False),
                              (rs_option.RS_OPTION_COLOR_EXPOSURE, 30000.0)]
            dev.set_device_options(*zip(*custom_options))
        except pyrs.RealsenseError:
            pass  # options are not available on all devices


        while True:

            h1=cv2.getTrackbarPos('h1','camera')
            h2=cv2.getTrackbarPos('h2','camera')
            s1=cv2.getTrackbarPos('h1','camera')
            s2=cv2.getTrackbarPos('h2','camera')
            v1=cv2.getTrackbarPos('h1','camera')
            v2=cv2.getTrackbarPos('h2','camera')

            dev.wait_for_frames()
            frame = dev.color
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)                     # 高斯模糊
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)                 # 转化成HSV图像
            erode_hsv = cv2.erode(hsv, None, iterations=2)                   # 腐蚀 

            checkcounter(frame,h1,s1,v1,h2,s2,v2,erode_hsv)
            cv2.imshow('camera', frame)
            cv2.waitKey(1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
