import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
import os
import math
import time
import numpy as np

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

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

class position_manager(Node):
    def __init__(self):
        super().__init__("position_manager") 

        self.declare_parameter("index", -1)
        self.cams = self.get_parameter("index").value
        
        # debug only
        self.index = 2

        # check if Parameters is set
        if (self.index == -1):
            self.get_logger().warning("no device index was set!")
            exit()

        command = "v4l2-ctl -d /dev/video" + str(self.index) + " -D"
        stream = os.popen(command)
        output = stream.read()
        if "HD Web Camera" in output:
            self.config = 1
            self.get_logger().info("Found camera with known start location: cam" + str(self.config))
        elif "CameraA" in output:
            self.config = 2
            self.get_logger().info("Found camera with known start location: cam" + str(self.config))
        else:
            self.get_logger().warning("Found device but no known start location")
            exit()

        # create publisher
        self.position_broadcaster = TransformBroadcaster(self)

        while(1):
            self.publish_position("world", ('cam' + str(self.index) + '_position'), 0, 0, 0, 0, 0, 0)
            time.sleep(0.5)

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

def main(args=None):
    rclpy.init(args=args)
    node = position_manager()  
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()