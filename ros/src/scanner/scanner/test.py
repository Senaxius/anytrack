#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import time
import math
import numpy as np

from visualization_msgs.msg import Marker 

def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q

class test(Node): 
    def __init__(self):
        super().__init__("test") 

        self.publisher_ = self.create_publisher(msg_type=Marker, topic="marker", qos_profile=10)
        self.get_logger().info("Starting publisher...")

        while (1):
            self.get_logger().info("Sending...")
            self.publish_topic()
            time.sleep(1)


    def publish_topic(self):
        msg = Marker()
        # msg.header.frame_id = "test"

        msg.id = 0
        msg.type = Marker.ARROW
        msg.action = Marker.ADD

        q = quaternion_from_euler(0, 0, 90)
        
        msg.pose.position.x = 0.
        msg.pose.position.y = 0.
        msg.pose.position.z = 0.
        msg.pose.orientation.x = q[0]
        msg.pose.orientation.y = q[1]
        msg.pose.orientation.z = q[2]
        msg.pose.orientation.w = q[3]
        msg.scale.x = 0.1
        msg.scale.y = 0.005
        msg.scale.z = 0.005
        msg.color.a = 1.
        msg.color.r = 0.8
        msg.color.g = 0.5
        msg.color.b = 0.3

        self.publisher_.publish(msg)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = test() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
