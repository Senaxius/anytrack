import rclpy
from rclpy.node import Node

import json
import math
import numpy as np
import time

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

class position_manager(Node):  
    def __init__(self):
        super().__init__("position_manager")  

        # declare Parameters
        self.declare_parameter("device_count", 0)
        self.declare_parameter("config_path", '/home/ALEX/3dev/config/camera_positions.json')

        # import parameters
        self.device_count = self.get_parameter("device_count").value
        self.config_path = self.get_parameter("config_path").value

        # debug only
        self.device_count = 4
        self.config_path = '/home/ALEX/3dev/config/camera_positions.json'
        self.debug = 0

        # check if Parameters are set
        if (self.device_count == 0):
            self.get_logger().warning("no parameters were supplied!")
            exit()

        self.get_logger().info("Starting position_manager with device count: " + str(self.device_count) + " and config path: " + str(self.config_path))

        # starting tf broadcaster
        self.position_broadcaster = TransformBroadcaster(self)

        # reading config file
        file = open(self.config_path)
        print("hello")
        config = json.load(file)

        # main loop
        while(1):
            # for each device
            for i in range(self.device_count):
                if (self.debug == 1):
                    print(i)
                    print(config[str(i)])
                # publish camera_position
                data = config[str(i)]
                x = data["x"]
                y = data["y"]
                z = data["z"]
                ax = data["ax"] / 180 * math.pi
                ay = data["ay"] / 180 * math.pi
                az = data["az"] / 180 * math.pi

                self.publish_position("world", ("cam" + str(i) + "_position"), x, y, z, ax, ay, az)

            time.sleep(2)

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
    node = position_manager() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()