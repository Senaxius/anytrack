#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class test_node(Node):
    def __init__(self):
        pass
        super().__init__("py_test")
        self.get_logger().info("Hello ROS2")


def main(args=None):
    rclpy.init(args=args)
    node = test_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
