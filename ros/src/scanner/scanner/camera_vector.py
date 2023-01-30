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

# def convert_yaml_to_msg(self, data):
#     msg = CameraInfo()
#     msg.width = data["image_width"]
#     msg.height = data["image_height"]
#     # msg.k = data["camera_matrix"]["data"]
#     # msg.d = data["distortion_coefficients"]["data"]
#     msg.r = data["rectification_matrix"]["data"]
#     msg.p = data["projection_matrix"]["data"]
#     # msg.distortion_model = data["distortion_model"]
#     ################ TODO: adaptive frame id
#     msg.header.frame_id = ('cam' +  str(self.index) + '_position')
#     return msg

class FramePublisher(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')

        # declare Parameters
        self.declare_parameter("index", -1)
    
        self.index = self.get_parameter("index").value

        # debug only
        # self.index = 2

        if (self.index == -1):
            self.get_logger().warning("no device index was set")
            exit()
        command = "v4l2-ctl -d /dev/video" + str(self.index) + " -D"
        stream = os.popen(command)
        output = stream.read()
        if "HD Web Camera" in output:
            self.config = 1
            self.get_logger().info("Found camera with known configuration-index: " + str(self.config))
            self.file = "/home/ALEX/3dev/config/cam1.yaml"
        elif "CameraA" in output:
            self.config = 2
            self.get_logger().info("Found camera with known configuration-index: " + str(self.config))
            self.file = "/home/ALEX/3dev/config/cam2.yaml"
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
        self.get_logger().info("Starting the vector visualisation on device: video" + str(self.index))
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
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
