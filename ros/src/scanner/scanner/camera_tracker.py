from collections import deque
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
import rclpy
from rclpy.node import Node

from scanner_interfaces.msg import CameraXY
from sensor_msgs.msg import Image

class Tracker(Node):  
    def __init__(self):
        super().__init__("Tracker")  

        # declare Parameters
        self.declare_parameter("index", -1)
        self.declare_parameter("track", 0)
        # check if Parameters is set
    
        self.index = self.get_parameter("index").value
        self.track = self.get_parameter("track").value

        # debug only
        # self.index = 2
        # self.track = 0

        if (self.index == -1):
            self.get_logger().warning("no device index was set")
            exit()
        else:
            # read Value of Parameter
            self.get_logger().info("Starting camera tracker on device: video" + str(self.index))

        self.coordinate_publisher_ = self.create_publisher(
            msg_type=CameraXY, topic="coordinates", qos_profile=10)
        # self.get_logger().info("done!")

        self.image_publisher_ = self.create_publisher(msg_type=Image, topic="image_raw", qos_profile=10)
        # self.image_publisher_ = self.create_publisher(msg_type=Image, topic=('cam' + str(self.index) + '/image_raw'), qos_profile=10)

        self.bridge = CvBridge()
        # self.get_logger().info("done!")

        self.camera_loop()

    def publish_coordinates(self, x, y, x_max, y_max, found, fps):
        msg = CameraXY()
        msg.x = x
        msg.y = y
        msg.x_max = x_max
        msg.y_max = y_max
        msg.found = found
        msg.fps = fps
        self.coordinate_publisher_.publish(msg)

    def publish_image(self, image):
        msg = self.bridge.cv2_to_imgmsg(np.array(image), "bgr8")
        msg.header.frame_id = ('cam' +  str(self.index) + '_position')
        self.image_publisher_.publish(msg)

    def camera_loop(self):
        # color range to track
        start_color = (31, 70, 50)
        end_color = (63, 255, 255)

        buffer_size = 64

        # create line buffer
        buffer_pts = deque(maxlen=buffer_size)
        # create camera capture
        cap = VideoStream(src=self.index).start()

        prev_frame_time = 0
        new_frame_time = 0
        fps = 0

        rate = 30

        # main loop
        while True:
            start = time.time()
            # grab the current frame
            frame = cap.read()
            # resize the frame for faster tracking
            frame = imutils.resize(frame, width=600)
            if (self.track == 1):
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
                    # x = 330.
                    # y = 225.
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    # center = (330, 225)
                    # only proceed if the radius meets a minimum size
                    if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        # cv2.circle(frame, (int(x), int(y)), int(radius),
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                                    (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    
                    # publish on topic
                    self.publish_coordinates(x, y, frame.shape[1], frame.shape[0], True, fps)
                else:
                    self.publish_coordinates(0.0, 0.0, frame.shape[1], frame.shape[0], False, fps)

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
            # cv2.imshow("Frame", frame)
            self.publish_image(frame)

            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)

            time.sleep(max((1 / rate) - (time.time() - start), 0))

            # key = cv2.waitKey(1) & 0xFF
            # # if the 'q' key is pressed, stop the loop
            # if key == ord("q"):
            #     break


        cap.release()
        cv2.destroyAllWindows()

 
def main(args=None):
    rclpy.init(args=args)
    node = Tracker() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()

