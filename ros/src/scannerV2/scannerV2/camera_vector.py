import rclpy
from rclpy.node import Node

import os
import yaml

from scanner_interfaces.msg import Tracks
from scanner_interfaces.msg import Object
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Point

class camera_vector(Node):  
    def __init__(self):
        super().__init__("camera_vector")  

        # declare Parameters
        self.declare_parameter("index", -1)
        self.declare_parameter("device", -1)
        self.declare_parameter("multiplier", -1)
        self.declare_parameter("width", -1)
        self.declare_parameter("height", -1)

        # import parameters
        self.index = self.get_parameter("index").value
        self.device = self.get_parameter("device").value
        self.multiplier = self.get_parameter("multiplier").value
        self.width = self.get_parameter("width").value
        self.height = self.get_parameter("height").value

        # debug only
        # self.index = 0
        # self.device = 0
        # self.multiplier = 2
        # self.width = 1280
        # self.height = 720

        # check if Parameters is set
        if (self.device == -1 or self.index == -1):
            self.get_logger().warning("no index was set")
            exit()

        self.get_logger().info("Starting camera vector with index " + str(self.index))

        command = "v4l2-ctl -d /dev/video" + str(self.device) + " -D"
        stream = os.popen(command)
        output = stream.read()
        if "HD Web Camera" in output:
            self.config = 0
            self.get_logger().info("Detected camera with know device type: HD Web Camera")
            self.file = "/home/ALEX/3dev/config/HD_WEB_Camera.yaml"
        elif "CameraA" in output:
            self.config = 1
            self.get_logger().info("Detected camera with know device type: CameraA")
            self.file = "/home/ALEX/3dev/config/CameraA.yaml"
        elif "WEB CAMERA M9 Pro" in output:
            self.config = 2
            self.get_logger().info("Detected camera with know device type: WEB CAMERA M9 Pro")
            self.file = "/home/ALEX/3dev/config/M9_Pro.yaml"
        else:
            self.get_logger().warning("Found device but no known configuration")
            exit()
        
        # create msg from .yaml file
        self.data = self.read_yaml(self.file)

        self.fx = (self.data["projection_matrix"]["data"][0] * (self.width / self.data["image_width"]))
        self.fy = (self.data["projection_matrix"]["data"][5] * (self.height / self.data["image_height"]))
        self.cx = (self.data["projection_matrix"]["data"][2] * (self.width / self.data["image_width"]))
        self.cy = (self.data["projection_matrix"]["data"][6] * (self.height / self.data["image_height"]))

        color_1 = (237, 255, 0)
        color_2 = (0, 255, 255)
        color_3 = (255, 0, 255)
        color_4 = (0, 255, 0)
        self.colors = [color_1, color_2, color_3, color_4]

        self.subscriber = self.create_subscription(msg_type=Tracks, topic=('/cam' + str(self.index) + '/tracks'), callback=self.tracks_callback, qos_profile=10)
        self.publisher = self.create_publisher(msg_type=MarkerArray, topic="vector", qos_profile=10)

    def read_yaml(self, filename):
        with open(filename, "r") as file_handle:
            return yaml.load(file_handle, Loader=yaml.FullLoader)

    def tracks_callback(self, msg):
        markerarray = MarkerArray()
        for object in msg.tracks:
            marker = self.create_marker(object.x, object.y, object.id)
            markerarray.markers.append(marker)
        self.publisher.publish(markerarray)
    
    def create_marker(self, x, y, id):
        x = (float(x) - self.cx) / self.fx
        y = (float(y) - self.cy) / self.fy
        marker = Marker()
        marker.header.frame_id = ('cam' + str(self.index) + '_position')
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.id = id
        marker.ns = ('cam' + str(self.index) + '/markers')
        marker.action = marker.ADD
        marker.lifetime.sec = 0
        marker.lifetime.nanosec = 100000000
        
        marker.scale.x = 0.01
        marker.scale.y = 0.0
        marker.scale.z = 0.0

        marker.color.a = 1.0
        if id < 4:
            marker.color.r = float(self.colors[id][2])
            marker.color.g = float(self.colors[id][1])
            marker.color.b = float(self.colors[id][0])
        start = Point()
        start.x = 0.0
        start.y = 0.0
        start.z = 0.0
        end = Point()
        end.x = x    * self.multiplier
        end.y = y  * self.multiplier
        end.z = 1.0  * self.multiplier
        marker.points = [start, end]
        return marker



def main(args=None):
    rclpy.init(args=args)
    node = camera_vector() 
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()