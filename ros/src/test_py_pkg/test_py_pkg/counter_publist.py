#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.msg import String 

class Listener(Node): 
    def __init__(self):
        super().__init__("test_listener") 

        self.subscriber_ = self.create_subscription(msg_type=String, topic="number_publisher", callback=self.callback_test_topic, qos_profile=10)

        self.get_logger().info("Starting listener...")
    
    def callback_test_topic(self, msg):
        self.get_logger().info("Received: " + str(msg.data))
 
def main(args=None):
    rclpy.init(args=args)
    node = Listener() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
