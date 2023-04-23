from collections import deque
from cv_bridge import CvBridge
import numpy as np
import cv2
import time
import sys
import rclpy
from rclpy.node import Node

from scanner_interfaces.msg import Tracks
from scanner_interfaces.msg import Object
from sensor_msgs.msg import Image

sys.path.append('/home/ALEX/anytrack/python/lib')
import tracker as trk

class tracker2D(Node):  
    def __init__(self):
        super().__init__("tracker2D")  

        # declare Parameters
        self.declare_parameter("index", -1)
        self.declare_parameter("device", -1)
        self.declare_parameter("track", 1)
        self.declare_parameter("visualize", 1)
        self.declare_parameter("limit", 35)
        self.declare_parameter("debug", 0)
        self.declare_parameter("framerate", 60)
        self.declare_parameter("width", 1920)
        self.declare_parameter("height", 1080)

        # import parameters
        self.index = self.get_parameter("index").value
        self.device = self.get_parameter("device").value
        self.track = self.get_parameter("track").value
        self.visualize = self.get_parameter("visualize").value
        self.limit = self.get_parameter("limit").value
        self.debug = self.get_parameter("debug").value
        self.framerate = self.get_parameter("framerate").value
        self.width = self.get_parameter("width").value
        self.height = self.get_parameter("height").value

        # debug only
        # self.index = 0
        # self.device = 0
        # self.track = 1
        # self.visualize = 1
        # self.limit = 0
        # self.debug = 1
        # self.framerate = 60
        # self.width = 1280
        # self.height = 720

        # check if Parameters is set
        if (self.device == -1 or self.index == -1):
            self.get_logger().warning("no index was set")
            exit()

        self.get_logger().info("Starting camera tracker with index " + str(self.index) + " on device: video" + str(self.device))

        self.tracks_publisher = self.create_publisher(msg_type=Tracks, topic="tracks", qos_profile=10)

        self.image_publisher = self.create_publisher(msg_type=Image, topic="image_raw", qos_profile=10)
        # self.image_publisher_ = self.create_publisher(msg_type=Image, topic=('cam' + str(self.index) + '/image_raw'), qos_profile=10)

        # starting main camera Loop
        self.bridge = CvBridge()
        self.camera_loop()

    def add_object_to_msg(self, msg, object, x_max, y_max):
        b = Object()
        b.id = object.id
        b.x = object.x
        b.y = object.y
        b.x_max = x_max
        b.y_max = y_max
        b.radius = object.radius
        b.diff = object.diff
        msg.append(b)

    def publish_Tracks(self, msg):
        self.tracks_publisher.publish(msg)

    def publish_image(self, image):
        msg = self.bridge.cv2_to_imgmsg(np.array(image), "bgr8")
        msg.header.frame_id = ('cam' +  str(self.index) + '_position')
        self.image_publisher.publish(msg)

    def camera_loop(self):
        # camera setup
        cap = trk.VideoStream(src=self.device, resolution=(self.width, self.height), framerate=self.framerate).start()

        prev_frame_time = 0
        # use this to limit the loop speed, otherwise might use too much cpu
        limit_rate = self.limit
        # buffer for tracking line (only visualisation)
        buffer_size = 10
        line_buffer = []
        for i in range(4):
            line_buffer.append(deque(maxlen=buffer_size))
        # create TrackingObject
        green_ball = trk.ColorObject()
        green_ball.start_color = (43, 222, 116)
        green_ball.end_color = (63, 255, 255)
        
        if self.debug:
            frame = cap.read()
            # cv2.imshow("Frame", frame)
            # cv2.moveWindow("Frame", 1920, 0)

        objects = []

        # camera loop
        while (1):
            start_time = time.time()

            frame = cap.read()

            prev_objects = objects
            if self.track:
                objects = trk.ball_scanner(frame, colors=[green_ball], min_radius=10, prev_objects=prev_objects)
            if self.visualize:
                frame = trk.scanner_visulisation(frame, objects,line_buffer=line_buffer)
            
            # publish data
            msg = Tracks()
            for object in objects:
                self.add_object_to_msg(msg.tracks, object, self.width, self.height)
            self.tracks_publisher.publish(msg)
            # publish image
            self.publish_image(frame)


            if self.debug:
                # cv2.imshow("Frame", frame)
                # print fps
                new_frame_time = time.time()
                fps = 1/(new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time
                fps = int(fps)
                print(fps)
                cv2.imshow("frame", cv2.resize(frame, (960, 540)))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if self.limit != 0:
                time.sleep(max((1 / limit_rate) - (time.time() - start_time), 0))

def main(args=None):
    rclpy.init(args=args)
    node = tracker2D() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()

