#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.srv import AddTwoInts


class test_server(Node):
    def __init__(self):
        super().__init__("test_server")
        self.server_ = self.create_service(
            AddTwoInts, "add_two_ints", self.callback_test_server)

        self.get_logger().info("Started server...")

    def callback_test_server(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(str(response.sum))
        return response


def main(args=None):
    rclpy.init(args=args)
    node = test_server()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
