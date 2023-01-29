#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
import cv2
import numpy as np

from sensor_msgs.msg import Image

class camera_publisher(Node):
    def __init__(self):
        super().__init__("camera_publisher") # MODIFY NAME

        self.get_logger().info("Initialize the camera publisher...")
        self.publisher_ = self.create_publisher(msg_type=Image, topic="camera_info/image_raw", qos_profile=10)
        self.get_logger().info("done!")

        self.bridge = CvBridge()

        self.get_logger().info("Starting the main camera loop...")
        self.camera_capture()

    def publish_topic(self, image):
        msg = self.bridge.cv2_to_imgmsg(np.array(image), "bgr8")
        msg.header.frame_id = "cam1"
        self.publisher_.publish(msg)

    def camera_capture(self):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        width = 1920
        height = 1080
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        while(1):
            _, frame = cap.read()
            cv2.imshow('frame',frame)
            self.publish_topic(frame)
            cv2.waitKey(1) 
 
 
def main(args=None):
    rclpy.init(args=args)
    node = camera_publisher() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
