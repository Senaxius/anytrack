import cv2
import time
from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
from imutils.video import FPS

vs = VideoStream(src=0).start()
# cam_capture = cv2.VideoCapture(0)  # create camera object outside while-loop

# vs.stream.set(3, 640)
# vs.stream.set(4, 480)

prev_frame_time = 0
new_frame_time = 0
fps = 0

while(True):
    frame = vs.read()
    cv2.imshow('frame', frame)

    # frame = vs.read()
    # # the 'q' button is set as the
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # new_frame_time = time.time()
    # fps = 1/(new_frame_time-prev_frame_time)
    # prev_frame_time = new_frame_time
    # fps = int(fps)

    # print(fps)
cv2.destroyAllWindows()
vs.stop()
