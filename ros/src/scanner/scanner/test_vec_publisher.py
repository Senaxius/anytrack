#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.msg import String 
from geometry_msgs.msg import Vector3

class test_vec_publisher(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("test_vec_publisher") # MODIFY NAME

        self.publisher_ = self.create_publisher(msg_type=Vector3, topic="test_vec_topic", qos_profile=10)
        self.time_ = self.create_timer(0.5, self.publish_topic)

        self.get_logger().info("Started test_vec_publisher")

    def publish_topic(self):
        msg = Vector3()
        msg.x = 43.0
        msg.y = 32.0
        msg.z = 50.0
        self.publisher_.publish(msg)
        self.get_logger().info("published test vektor...")
 
 
def main(args=None):
    rclpy.init(args=args)
    node = test_vec_publisher() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
