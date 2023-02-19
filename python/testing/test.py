# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import time


print(cv2.getBuildInformation())
# vs = cv2.VideoCapture("gst-launch-1.0 -v videotestsrc ! video/x-raw,width=1920,heigh=1080 ! videoconvert ! video/x-raw ! appsink", cv2.CAP_GSTREAMER)

# time.sleep(1)

# _, frame = vs.read()
# cv2.imshow("test", frame)

# while (1):
#     pass