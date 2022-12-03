#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.msg import String 

class Publisher(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("test_publisher") # MODIFY NAME

        self.publisher_ = self.create_publisher(msg_type=String, topic="test_topic", qos_profile=10)
        self.time_ = self.create_timer(0.5, self.publish_topic)

        self.get_logger().info("Starting publisher...")

    def publish_topic(self):
        msg = String()
        msg.data = "Test"
        self.publisher_.publish(msg)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = Publisher() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
