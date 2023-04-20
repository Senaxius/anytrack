from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
import rclpy
from rclpy.node import Node

from scanner_interfaces.msg import CameraXY

class Scanner(Node):  # MODIFY NAME
    def __init__(self):
        super().__init__("Scanner")  # MODIFY NAME

        self.get_logger().info("Initialize the scanner publisher...")
        self.publisher_ = self.create_publisher(
            msg_type=CameraXY, topic="scanner_coordinates", qos_profile=10)
        self.get_logger().info("done!")

        self.get_logger().info("Starting camera loop...")
        self.camera_loop()

    def publish_topic(self, x, y, x_max, y_max, found):
        msg = CameraXY()
        msg.x = x
        msg.y = y
        msg.x_max = x_max
        msg.y_max = y_max
        msg.found = found
        self.publisher_.publish(msg)

    def camera_loop(self):
        # color range to track
        start_color = (31, 70, 50)
        end_color = (63, 255, 255)

        buffer_size = 64

        # create line buffer
        buffer_pts = deque(maxlen=buffer_size)
        # create camera capture
        cap = VideoStream(src=0).start()

        prev_frame_time = 0
        new_frame_time = 0

        # main loop
        while True:
            # grab the current frame
            frame = cap.read()

            # resize the frame for faster tracking
            frame = imutils.resize(frame, width=600)
            # blur it for less grain
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            # convert to HSV for color tracking
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # mask for selected color
            mask = cv2.inRange(hsv, start_color, end_color)
            # remove any small blobs
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,

                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                
                # publish on topic
                self.publish_topic(x, (frame.shape[0] - y), frame.shape[1], frame.shape[0], True)
            else:
                self.publish_topic(0.0, 0.0, frame.shape[1], frame.shape[0], False)

            # update the points queue
            buffer_pts.appendleft(center)
                # loop over the set of tracked points
            for i in range(1, len(buffer_pts)):
                # if either of the tracked points are None, ignore
                # them
                if buffer_pts[i - 1] is None or buffer_pts[i] is None:
                    continue
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
                cv2.line(frame, buffer_pts[i - 1],
                         buffer_pts[i], (0, 0, 255), thickness)

            # show the frame to our screen
            cv2.imshow("Frame", frame)

            # new_frame_time = time.time()
            # fps = 1/(new_frame_time-prev_frame_time)
            # prev_frame_time = new_frame_time
            # fps = int(fps)
            # print(fps)

            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

            # print(x, y, frame.width, frame.height)

        cap.release()
        cv2.destroyAllWindows()

 
def main(args=None):
    rclpy.init(args=args)
    node = Scanner() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()

