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

        self.t_points = []
        self.r_points = []

        self.listener = self.create_subscription(msg_type=CameraLocations, topic=('/calibration'), callback=self.points_callback, qos_profile=10, callback_group=listener_group)

        self.t_publisher = self.create_publisher(msg_type=PointCloud2, topic="/translation_points", qos_profile=10)
        self.r_publisher = self.create_publisher(msg_type=PointCloud2, topic="/rotation_points", qos_profile=10)

        self.counter = 0
        self.min = 80

    def points_callback(self, msg):
        if self.counter <= self.min:
            print("not yet enough data to reach min")
            self.counter += 1
            return
        x = msg.locations[1].x 
        y = msg.locations[1].y 
        z = msg.locations[1].z 
        ax = msg.locations[1].ax * 1
        ay = msg.locations[1].ay * 1
        az = msg.locations[1].az * 1

        header = Header()
        header.frame_id='world'
        header.stamp = self.get_clock().now().to_msg()

        self.t_points.append((x, y, z))
        self.r_points.append((ax, ay, az))

        t_msg = point_cloud2.create_cloud_xyz32(header=header, points=self.t_points)
        r_msg = point_cloud2.create_cloud_xyz32(header=header, points=self.r_points)
        self.t_publisher.publish(t_msg)
        self.r_publisher.publish(r_msg)
        print(len(self.t_points))

def main(args=None):
    rclpy.init(args=args)
    node = test() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()
