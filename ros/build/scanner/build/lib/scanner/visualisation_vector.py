import math
import os
from geometry_msgs.msg import TransformStamped
import numpy as np
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose
import time
import yaml

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

def read_yaml(filename):
    with open(filename, "r") as file_handle:
        return yaml.load(file_handle, Loader=yaml.FullLoader)

class visualisation_vector(Node):
    def __init__(self):
        super().__init__('visualisation_vector')

        # declare Parameters
        self.declare_parameter("index", -1)
        self.declare_parameter("device", -1)

        # import parameters
        self.index = self.get_parameter("index").value
        self.device = self.get_parameter("device").value

        # debug only
        # self.index = 2
        # self.device = 2

        # check if Parameters is set
        if (self.device == -1 or self.index == -1):
            self.get_logger().warning("no index was set")
            exit()

        self.get_logger().info("Starting visualisation vector with index " + str(self.index) + " on device: video" + str(self.device))

        command = "v4l2-ctl -d /dev/video" + str(self.device) + " -D"
        stream = os.popen(command)
        output = stream.read()
        if "HD Web Camera" in output:
            self.config = 0
            # self.get_logger().info("Detected camera with know device type: HD Web Camera")
            self.file = "/home/ALEX/3dev/config/HD_WEB_Camera.yaml"
        elif "CameraA" in output:
            self.config = 1
            # self.get_logger().info("Detected camera with know device type: CameraA")
            self.file = "/home/ALEX/3dev/config/CameraA.yaml"
        elif "WEB CAMERA M9 Pro" in output:
            self.config = 2
            # self.get_logger().info("Detected camera with know device type: WEB CAMERA M9 Pro")
            self.file = "/home/ALEX/3dev/config/M9_Pro.yaml"
        else:
            self.get_logger().warning("Found device but no known configuration")
            exit()
        
        # read camera matrix from config file
        self.data = read_yaml(self.file)

        self.fx = self.data["projection_matrix"]["data"][0]
        self.fy = self.data["projection_matrix"]["data"][5]
        self.cx = self.data["projection_matrix"]["data"][2]
        self.cy = self.data["projection_matrix"]["data"][6]

        self.origin = ('cam' + str(self.index) + '_position')
        self.child = ('vec' + str(self.index))


        # self.get_logger().info(str(self.fx))
        # self.get_logger().info(str(self.fy))
        # self.get_logger().info(str(self.cx))
        # self.get_logger().info(str(self.cy))

        # Initialize the transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # self.get_logger().info("Initialize the scanner listener...")
        self.subscriber_ = self.create_subscription(msg_type=CameraXY, topic=('/cam' +  str(self.index) + '/coordinates'), callback=self.scanner_coordinates_callback, qos_profile=10)
        self.get_logger().info('cam' +  str(self.index) + '/coordinates')
    
    def scanner_coordinates_callback(self, msg):
        if (msg.found == False):
            z = 0.0
            x = 0.0
            y = 0.0
        else:
            z = 1.0
            x = (float(msg.x) - self.cx) / self.fx
            y = (float(msg.y) - self.cy) / self.fy
        
        multiplier = 3
        x *= multiplier
        y *= multiplier
        z *= multiplier

        self.broadcaster(self.origin, self.child, x, y, z)

    def broadcaster(self, origin, child, x, y, z):
        t = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = origin
        t.child_frame_id = child

        # Turtle only exists in 2D, thus we get x and y translation
        # coordinates from the message and set the z coordinate to 0
        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = z

        # For the same reason, turtle can only rotate around one axis
        # and this why we set rotation in x and y to 0 and obtain
        # rotation in z axis from the message
        q = quaternion_from_euler(0, 0, 0)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # Send the transformation
        self.tf_broadcaster.sendTransform(t)

def main():
    rclpy.init()
    node = visualisation_vector()
    rclpy.spin(node)
    rclpy.shutdown()
