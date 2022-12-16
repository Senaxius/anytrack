#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial

from example_interfaces.srv import AddTwoInts

class test_client_op(Node): 
    def __init__(self):
        super().__init__("test_client_op")
        self.call_server(10, 5)
    
    def call_server(self, a, b):
        client = self.create_client(AddTwoInts, "add_two_ints")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Wating for Server to start...")

        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        
        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_done_server, a=a, b=b))
    
    def callback_done_server(self, future, a, b):
        try:
            response = future.result()
            self.get_logger().info("Result: " + str(response.sum))
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))

def main(args=None):
    rclpy.init(args=args)
    node = test_client_op() 
    node.call_server(20,4)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
