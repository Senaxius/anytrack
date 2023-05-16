import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup,MutuallyExclusiveCallbackGroup

import math as m
import cv2
import numpy as np
from cv_bridge import CvBridge

from scanner_interfaces.msg import Tracks
from scanner_interfaces.msg import Object
from sensor_msgs.msg import Image

class optical_flow(Node): 
    def __init__(self):
        super().__init__("optical_flow") 

        self.device_count = 2
        self.width = 1280
        self.height = 720

        self.get_logger().info("Starting optical_flow visualisation...")

        loop_grp = MutuallyExclusiveCallbackGroup()
        tracks_grp = ReentrantCallbackGroup()

        # create optical_flow publisher
        self.publisher = self.create_publisher(msg_type=Image, topic="optical_flow", qos_profile=10)

        # create variables to store input for optical_flow
        self.input = dict()

        # create subscribers
        for i in range(self.device_count):
            self.create_subscription(msg_type=Tracks, topic=('/cam' + str(i) + '/tracks'), callback=self.create_tracks_callback(i), qos_profile=10, callback_group=tracks_grp)
            self.input.update({i: {
                'time': 0,
                'buffer': [],
                'objects': [],
            }})

        # checks
        self.info_check = 0
        self.date_check = 0

        # create empty picture
        self.image = np.zeros((720,1280,3), np.uint8)
        self.bridge = CvBridge()

        # main loop
        self.loop = self.create_timer(0.1, self.loop_callback, callback_group=loop_grp)


    def loop_callback(self):
        # check if every camera detected one object
        for cam in self.input:
            if len(self.input[cam]['buffer']) != 1:
                print("not every camera detected one object")
                return
        
        # add the object to the optical_flow data
        for cam in self.input:
            # undistort Points
            input = self.input[cam]
            if len(input['buffer']) != 1:
                print("ohno")
                return
            distorted_point = (input['buffer'][0].x, input['buffer'][0].y)
            input['objects'].append(distorted_point)

        # calculate position for number of cameras in relation to cam0
        for cam in range(self.device_count - 1):
            index = cam + 1

            cam0_points = np.array(self.input[0]['objects'])
            cam1_points = np.array(self.input[index]['objects'])

            x_slope = cam1_points[-1][0] - cam0_points[-1][0]
            y_slope = cam1_points[-1][1] - cam0_points[-1][1]

            start = (int(cam0_points[-1][0] - (4 * x_slope)), int(cam0_points[-1][1] - (4 * y_slope)))
            end = (int(cam1_points[-1][0] + (4 * x_slope)), int(cam1_points[-1][1] + (4 * y_slope)))

            # self.image = cv2.line(self.image, (int(cam0_points[-1][0]), int(cam0_points[-1][1])), (int(cam1_points[-1][0]), int(cam1_points[-1][1])), (0, 255, 0), 1)
            self.image = cv2.line(self.image, start, end, (0, 255, 0), 1)

            self.publish_image(self.image)

            # self.publish_optical_flow()
    
    def create_tracks_callback(self, index):
        return lambda msg:self.tracks_callback(msg, index)
    def tracks_callback(self, msg, index):
        self.input[index]['time'] = msg.header.stamp.sec * 1000000000 + msg.header.stamp.nanosec
        self.input[index]['buffer'] = []
        for object in msg.tracks:
            self.input[index]['buffer'].append(object)
    def publish_image(self, image):
        msg = self.bridge.cv2_to_imgmsg(np.array(image), "bgr8")
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)
        print("done")

def main(args=None):
    rclpy.init(args=args)
    node = optical_flow() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
