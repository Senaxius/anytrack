import rclpy
from rclpy.node import Node

import math
import numpy as np

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

class foxglove_camera(Node):  
    def __init__(self):
        super().__init__("foxglove_camera")  

        # declare Parameters
        # self.declare_parameter("device_count", 0)
        # self.declare_parameter("config_path", '/home/ALEX/anytrack/config/camera_positions.json')

        # import parameters
        # self.device_count = self.get_parameter("device_count").value
        # self.config_path = self.get_parameter("config_path").value

        self.get_logger().info("Starting foxglove_camera")

        # starting tf broadcaster
        self.position_broadcaster = TransformBroadcaster(self)

        self.x = 0
        self.y = 0
        self.z = 0
        self.ax = 0
        self.ay = 0
        self.az = 0

        # main loop
        self.loop = self.create_timer(0.01, self.loop_callback)

    def loop_callback(self):
        if self.az == 1:
            self.az = -0.001
        self.az+=0.001
        self.publish_position("world", "camera", self.x, self.y, self.z, self.ax, self.ay*(2*math.pi), self.az*(2*math.pi))

    def publish_position(self, origin, child, x, y, z, ax, ay, az):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = origin
        t.child_frame_id = child

        t.transform.translation.x = float(x)
        t.transform.translation.y = float(y)
        t.transform.translation.z = float(z)

        q = quaternion_from_euler(float(ax), float(ay), float(az))
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # Send the transformation
        self.position_broadcaster.sendTransform(t)

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
    node = foxglove_camera() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()
