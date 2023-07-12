from collections import deque
from cv_bridge import CvBridge
import numpy as np
import cv2
import time
import sys
import os
import yaml
import rclpy
from rclpy.node import Node

from interfaces.msg import Object2dList
from interfaces.msg import Object2d
from sensor_msgs.msg import Image

sys.path.append('/home/ALEX/anytrack/python/lib')
import tracker as trk

class camera_detector(Node):  
    def __init__(self):
        super().__init__("camera_detector")  

        # declare Parameters
        self.declare_parameter("index", -1)
        self.declare_parameter("config", '')
        self.declare_parameter("visualize", 1)
        self.declare_parameter("debug", 0)
        self.declare_parameter("width", 1920)
        self.declare_parameter("height", 1080)

        # import parameters
        self.index = self.get_parameter("index").value
        self.file = self.get_parameter("config").value
        self.visualize = self.get_parameter("visualize").value
        self.debug = self.get_parameter("debug").value
        self.width = self.get_parameter("width").value
        self.height = self.get_parameter("height").value

        # debug only
        # self.index = 0
        # self.visualize = 1
        # self.debug = 1
        # self.width = 1280
        # self.height = 720

        # check if Parameters is set
        if (self.index == -1):
            self.get_logger().warning("no index was set")
            exit()

        self.get_logger().info("Starting camera detector with index " + str(self.index))
        self.data = self.read_yaml(self.file)

        self.tracks_publisher = self.create_publisher(msg_type=Object2dList, topic="/cam" + str(self.index) + "/tracks", qos_profile=10)

        self.image_publisher = self.create_publisher(msg_type=Image, topic="/cam" + str(self.index) + "/image_tracked", qos_profile=10)

        self.buffer_size = 10
        self.line_buffer = []
        for i in range(4):
            self.line_buffer.append(deque(maxlen=self.buffer_size))
        # create TrackingObject
        self.green_ball = trk.ColorObject()
        self.green_ball.start_color = np.array(self.data['color']['start'])
        self.green_ball.end_color = np.array(self.data['color']['end'])
        
        self.objects = []

        # bridge to convert between ros msg and opencv
        self.bridge = CvBridge()

        # starting main camera subcription to driver
        self.driver_subscriber = self.create_subscription(msg_type=Image, topic=("/cam" + str(self.index) + "/image_raw"), callback=self.driver_callback, qos_profile=10)

    def read_yaml(self, filename):
        with open(filename, "r") as file_handle:
            return yaml.load(file_handle, Loader=yaml.FullLoader)
    
    def driver_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg)

        prev_objects = self.objects
        self.objects = trk.ball_scanner(frame, colors=[self.green_ball], min_radius=2, prev_objects=prev_objects)
        if self.visualize:
            frame = trk.scanner_visulisation(frame, self.objects,line_buffer=self.line_buffer)
        # publish data
        msg = Object2dList()
        for object in self.objects:
            self.add_object_to_msg(msg.tracks, object, self.width, self.height)
        msg.header.stamp = self.get_clock().now().to_msg()
        self.tracks_publisher.publish(msg)

        # publish image
        self.publish_image(frame)

    def add_object_to_msg(self, msg, object, x_max, y_max):
        b = Object2d()
        b.id = object.id
        b.x = round(object.x, 1)
        b.y = round(object.y, 1)
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

def main(args=None):
    rclpy.init(args=args)
    node = camera_detector() 
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()

