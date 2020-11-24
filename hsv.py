import logging
logging.basicConfig(level=logging.INFO)

import time
import numpy as np
import cv2
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
def getposHsv(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print("HSV is",HSV[y,x])

def getposBgr(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print("Bgr is",c[y,x])
with pyrs.Service() as serv:
    with pyrs.Service().Device() as dev:

        dev.apply_ivcam_preset(0)

        try:  # set custom gain/exposure values to obtain good depth image
            custom_options = [(rs_option.RS_OPTION_COLOR_ENABLE_AUTO_EXPOSURE,False),
                              (rs_option.RS_OPTION_COLOR_ENABLE_AUTO_WHITE_BALANCE, False),
                              (rs_option.RS_OPTION_COLOR_EXPOSURE, 20000.0)]
        except pyrs.RealsenseError:
            pass  # options are not available on all devices


        while True:

            dev.wait_for_frames()
            c = dev.color
            c = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)
            HSV=cv2.cvtColor(c,cv2.COLOR_BGR2HSV)
            cv2.imshow("imageHSV",c)
            cv2.imshow('image',c)

            cv2.setMouseCallback("imageHSV",getposHsv)
            cv2.setMouseCallback("image",getposBgr)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                        

