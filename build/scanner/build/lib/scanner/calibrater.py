#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
import math
import numpy as np

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

class calibrater(Node): 
    def __init__(self):
        super().__init__("calibrater") 

        # self.publisher = self.create_publisher(msg_type=Marker, topic="marker", qos_profile=10)
        self.get_logger().info("Starting calibrater...")

        while (1):
            self.get_logger().info("Sending...")
            # self.publish_topic()
            time.sleep(1)


    def publish_topic(self):
        pass
 
 
def main(args=None):
    rclpy.init(args=args)
    node = calibrater() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
