import rclpy
from rclpy.node import Node

import json
import math
import numpy as np
import time

from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

class test(Node):  
    def __init__(self):
        super().__init__("test")  

        self.publisher = self.create_publisher(msg_type=Marker, topic="test", qos_profile=10)

        # main loop
        while(1):
            self.publish()
            print("publish")
            # for each device

            time.sleep(1)

    def publish(self):
        msg = Marker()
        msg.header.frame_id = "cam0_position"
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.type = msg.ARROW
        msg.action = msg.ADD
        # msg.pose.position.x = 0.0
        # msg.pose.position.y = 0.0
        # msg.pose.position.z = 0.0
        # msg.pose.orientation.x = 0.0
        # msg.pose.orientation.y = 0.0
        # msg.pose.orientation.z = 0.0
        # msg.pose.orientation.w = 1.0
        msg.scale.x = 0.01
        msg.scale.y = 0.0
        msg.scale.z = 0.0
        msg.color.a = 1.0
        msg.color.r = 0.0
        msg.color.g = 0.0
        msg.color.b = 0.0

        start = Point()
        start.x = 0.0
        start.y = 0.0
        start.z = 0.0
        end = Point()
        end.x = 0.0
        end.y = 0.0
        end.z = 1.0

        msg.points = [start, end]


        self.publisher.publish(msg)

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

def main(args=None):
    rclpy.init(args=args)
    node = test() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()