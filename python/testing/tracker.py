import cv2
from threading import Thread
import time
from collections import deque
import imutils
import numpy as np


class VideoStream:
    def __init__(self, src=0, resolution=(640, 480), framerate=30, name="WebcamVideoStream"):
        # initialize the video camera stream and read the first frame
        self.stream = cv2.VideoCapture(src)

        # setting the right codex to use
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.stream.set(cv2.CAP_PROP_FOURCC, fourcc)

        self.stream.set(cv2.CAP_PROP_FPS, framerate)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


class ColorObject():
    def __init__(self):
        self.start_color = None
        self.end_color = None


class TrackedObject():
    def __init__(self):
        self.id = None
        self.center = None
        self.radius = None
        self.diff = -1
        self.x = None
        self.y = None


def ball_scanner(frame, colors=[], min_radius=10, prev_objects=[]):
    # blur it for less grain
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    # convert to HSV for color tracking
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # mask for selected color
    for color in colors:
        mask = cv2.inRange(hsv, color.start_color, color.end_color)
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=3)
        # cv2.imshow("mask", mask)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        contours = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        center = None
        objects = []
        # only proceed if at least one contour was found
        count = 0
        if len(contours) > 0:
            for contour in contours:
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                M = cv2.moments(contour)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > min_radius:
                    object = TrackedObject()
                    object.x = x
                    object.y = y
                    object.radius = radius
                    object.center = center
                    # find nearest previous object
                    diffs = []
                    if prev_objects == []:
                        object.id = count
                        count += 1
                        object.diff = 0
                    elif len(prev_objects) == 1 and len(contours) == 1:
                        object.id = prev_objects[0].id
                        object.diff = abs(prev_objects[0].center[0] - object.center[0]) + abs(prev_objects[0].center[1] - object.center[1])
                    else:
                        for prev_object in prev_objects:
                            diff = abs(prev_object.center[0] - object.center[0]) + abs(prev_object.center[1] - object.center[1])
                            diffs.append(diff)
                        min_diff_id = diffs.index(min(diffs))
                        object.id = prev_objects[min_diff_id].id
                        object.diff = diffs[min_diff_id]
                    objects.append(object)
        # remove duplicate ids
        used = []
        for object in objects:
            used.append(object.id)
        ids = []
        for object in objects:
            if object.id in ids:
                id = 0 
                if object.diff > objects[ids.index(object.id)].diff:
                    while(1):
                        if id not in used:
                            break
                        id += 1
                    object.id = id
                else:
                    while(1):
                        if id not in used:
                            break
                        id += 1
                    objects[ids.index(object.id)].id = id
            else:
                ids.append(object.id)
    return objects



def scanner_visulisation(frame, objects, line_buffer):
    color_1 = (237, 255, 0)
    color_2 = (0, 255, 255)
    color_3 = (255, 0, 255)
    color_4 = (0, 255, 0)
    colors = [color_1, color_2, color_3, color_4]
    for object in objects:
        if object.id < 4:
            cv2.circle(frame, (int(object.x), int(object.y)), int(object.radius), colors[object.id], 2)
            cv2.circle(frame, object.center, 5, colors[object.id], -1)

            # update the points queue
            buffer = line_buffer[object.id]
            buffer.appendleft(object.center)
            for i in range(1, len(buffer)):
                # if either of the tracked points are None, ignore them
                if buffer[i - 1] is None or buffer[i] is None:
                    continue
                # otherwise, compute the thickness of the line and draw the connecting lines
                thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
                cv2.line(frame, buffer[i - 1],
                        buffer[i], colors[object.id], thickness)
        else:
            cv2.circle(frame, (int(object.x), int(object.y)), int(object.radius), (255, 255, 255), 2)
            cv2.circle(frame, object.center, 5, (255,255,255), -1)


    return frame

if __name__ == "__main__":
    device = 0
    cap = VideoStream(src=device, resolution=(
        1920, 1080), framerate=60).start()

    prev_frame_time = 0

    # use this to limit the loop speed, otherwise might use too much cpu
    limit_rate = 60
    # buffer for tracking line (only visualisation)
    buffer_size = 10
    line_buffer = []
    for i in range(4):
        line_buffer.append(deque(maxlen=buffer_size))
    # create TrackingObject
    green_ball = ColorObject()
    green_ball.start_color = (56, 184, 127)
    green_ball.end_color = (65, 255, 255)

    frame = cap.read()
    cv2.imshow("Frame", frame)
    cv2.moveWindow("Frame", 1920, 0)

    objects = []

    while True:
        start_time = time.time()

        frame = cap.read()
        # tracking_time = time.time()
        prev_objects = objects
        objects = ball_scanner(frame, colors=[green_ball], min_radius=10, prev_objects=prev_objects)
        # objects = identify_objects(previous_objects, objects)
        tracked_frame = scanner_visulisation(frame, objects, line_buffer=line_buffer)

        cv2.imshow("Frame", tracked_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # print fps
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        print(fps)

        time.sleep(max((1 / limit_rate) - (time.time() - start_time), 0))
