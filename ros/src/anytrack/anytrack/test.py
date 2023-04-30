import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.node import Node

from scanner_interfaces.msg import CameraLocations
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
from sensor_msgs.msg import PointField
from std_msgs.msg import Header

import numpy as np

class test(Node):  
    def __init__(self):
        super().__init__("test")  
        
        listener_group = MutuallyExclusiveCallbackGroup() 

        self.points = []

        self.listener = self.create_subscription(msg_type=CameraLocations, topic=('/calibration'), callback=self.points_callback, qos_profile=10, callback_group=listener_group)

        self.publisher = self.create_publisher(msg_type=PointCloud2, topic="/simulation_points", qos_profile=10)

    def points_callback(self, msg):
        x = msg.locations[1].x
        y = msg.locations[1].y
        z = msg.locations[1].z

        header = Header()
        header.frame_id='world'

        self.points.append((x, y, z))

        msg = point_cloud2.create_cloud_xyz32(header=header, points=self.points)
        self.publisher.publish(msg)
        print("hello")

def main(args=None):
    rclpy.init(args=args)
    node = test() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()