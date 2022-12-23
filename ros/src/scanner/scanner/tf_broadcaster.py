import math
from geometry_msgs.msg import TransformStamped
import numpy as np
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose
import time

from scanner_interfaces.msg import CameraXY

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

class FramePublisher(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        # Initialize the transform broadcaster
        self.get_logger().info("Initialize the transform broadcaster...")
        self.tf_broadcaster = TransformBroadcaster(self)
        self.get_logger().info("done!")
        # self.broadcaster(10.0, -5.0, 5.0, 0.0)

        self.get_logger().info("Initialize the scanner listener...")
        self.subscriber_ = self.create_subscription(msg_type=CameraXY, topic="scanner_coordinates", callback=self.scanner_coordinates_callback, qos_profile=10)
        self.get_logger().info("done!")
    
    def scanner_coordinates_callback(self, msg):
        # self.get_logger().info("Received: x: " + str(msg.x) + " y: " + str(msg.y) + " x_max: " + str(msg.x_max) + " y_max: " + str(msg.y_max) + " found: " + str(msg.found))
        # self.broadcaster(-10.0, 32.0, 10.0)
        if (msg.found == False):
            depth = 0.0
            x = 0.0
            y = 0.0
        else:
            depth = 10.0
            x = msg.x - (msg.x_max / 2)
            x /= 50
            x *= -1 

            y = msg.y - (msg.y_max / 2)
            y /= 50

        self.broadcaster(depth, x, y, 0.0)


    def broadcaster(self, x, y, z, a):
        t = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'test'

        # Turtle only exists in 2D, thus we get x and y translation
        # coordinates from the message and set the z coordinate to 0
        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = z

        # For the same reason, turtle can only rotate around one axis
        # and this why we set rotation in x and y to 0 and obtain
        # rotation in z axis from the message
        q = quaternion_from_euler(0, 0, a)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # Send the transformation
        self.tf_broadcaster.sendTransform(t)

def main():
    rclpy.init()
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
