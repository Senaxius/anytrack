import cv2
import numpy as np
import imutils
import time
from collections import deque
from imutils.video import VideoStream

def ball_scanner(frame, buffer, colors = []):
    # blur it for less grain
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    # convert to HSV for color tracking
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # mask for selected color
    for color in colors:
        mask = cv2.inRange(hsv, color.start_color, color.end_color)
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=3)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        center = None
        objects = []
        # only proceed if at least one contour was found
        if len(contours) > 0:
            for contour in contours:
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                M = cv2.moments(contour)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 1:
                    objects.append(center)

        print(objects)
        #         # draw the circle and centroid on the frame,
        #         # then update the list of tracked points
        #         # cv2.circle(frame, (int(x), int(y)), int(radius),
        #         cv2.circle(frame, (int(x), int(y)), int(radius),
        #                     (0, 255, 255), 2)
        #         cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
        #     # publish on topic
        #     self.publish_coordinates(x, y, frame.shape[1], frame.shape[0], True, fps)
        # else:
        #     self.publish_coordinates(0.0, 0.0, frame.shape[1], frame.shape[0], False, fps)

        # # update the points queue
        # buffer_pts.appendleft(center)
        #     # loop over the set of tracked points
        # for i in range(1, len(buffer_pts)):
        #     # if either of the tracked points are None, ignore
        #     # them
        #     if buffer_pts[i - 1] is None or buffer_pts[i] is None:
        #         continue
        #     # otherwise, compute the thickness of the line and
        #     # draw the connecting lines
        #     thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
        #     cv2.line(frame, buffer_pts[i - 1],
        #             buffer_pts[i], (0, 0, 255), thickness)

    return frame, mask

class TrackingObject():
    def __init__(self):
        self.id = None
        self.start_color = None
        self.end_color = None

if __name__ == "__main__":
    device = 0
    # buffer for tracking line (only visualisation)
    buffer_size = 64
    buffer = deque(maxlen=buffer_size)

    # create camera capture
    # cap = VideoStream(src=device, resolution=(1920, 1080), framerate=30).start() 
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! image/jpeg,framerate=30/1,width=1920, height=1080,type=video ! jpegdec ! videoconvert ! video/x-raw ! appsink", cv2.CAP_GSTREAMER)
    # cap.set(5, 30)
    # cap.set(3, 1920)
    # cap.set(4, 1080)
    framerate = 60

    prev_frame_time = 0
    new_frame_time = 0
    fps = 0

    green_ball = TrackingObject()
    green_ball.id = 0
    green_ball.start_color = (31, 70, 50)
    green_ball.end_color = (63, 255, 255)

    # main loop
    while (cap.isOpened):
        # start time for frameratie limitting
        # start_time = time.time()
        # grab the current frame
        ret, frame = cap.read()
        # resize the frame for faster tracking
        # frame = imutils.resize(frame, width=600)

        # tracking_time = time.time()
        # frame, mask = ball_scanner(frame, buffer, colors=[green_ball])
        # print(int((time.time()-tracking_time) * 10000))

        # show frame (testing only)
        cv2.imshow("Frame", frame)
        # if ret:
        # else:
        #     print("no")
        # cv2.imshow("mask", mask)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # sleeping to maintain framerate
        # time.sleep(max((1 / framerate) - (time.time() - start_time), 0))

        # new_frame_time = time.time()
        # fps = 1/(new_frame_time-prev_frame_time)
        # prev_frame_time = new_frame_time
        # fps = int(fps)
        # print(fps)