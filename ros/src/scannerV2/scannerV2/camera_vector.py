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

        # import parameters
        self.index = self.get_parameter("index").value
        self.device = self.get_parameter("device").value

        # debug only
        self.index = 0
        self.device = 0

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

        self.fx = self.data["projection_matrix"]["data"][0]
        self.fy = self.data["projection_matrix"]["data"][5]
        self.cx = self.data["projection_matrix"]["data"][2]
        self.cy = self.data["projection_matrix"]["data"][6]

        self.subscriber = self.create_subscription(msg_type=Tracks, topic=('cam' + str(self.index) + '/tracks'), callback=self.tracks_callback, qos_profile=10)
        self.publisher = self.create_publisher(msg_type=MarkerArray, topic="vector", qos_profile=10)

        self.create_marker(('cam' + str(self.index) + "/markers"), 4)

        # main loop
        # while(1):
        #     # self.publish()
        #     # for each device

        #     time.sleep(1)
    
    def read_yaml(self, filename):
        with open(filename, "r") as file_handle:
            return yaml.load(file_handle, Loader=yaml.FullLoader)

    def create_marker(self, ns, number):
        markerarray = MarkerArray()
        for i in range(number):
            marker = Marker()
            marker.ns = ns
            marker.id = i
            marker.type = marker.ARROW
            marker.action = marker.ADD
            marker.scale.x = 0.01
            marker.scale.y = 0.0
            marker.scale.z = 0.0
            start = Point()
            start.x = 0.0
            start.y = 0.0
            start.z = 0.0
            end = Point()
            end.x = 0.0
            end.y = 0.0
            end.z = 0.0
            marker.points = [start, end]
            markerarray.markers.append(marker)
        self.publisher.publish(markerarray)
    
    def tracks_callback(self, msg):
        markerarray = MarkerArray()
        for object in msg.tracks:
            z = 1.0
            # x = (float(object.x) - self.cx) / self.fx
            # y = (float(object.y) - self.cy) / self.fy
            # x = (float(object.x) - self.cx) 
            # y = (float(object.y) - self.cy) 
            marker = Marker()
            marker.header.frame_id = ('cam' + str(self.index) + '_position')
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.id = object.id
            marker.ns = ('cam' + str(self.index) + '/markers')
            marker.action = marker.ADD
            marker.scale.x = 0.01
            marker.scale.y = 0.0
            marker.scale.z = 0.0
            marker.color.a = 1.0
            marker.color.r = 255.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            start = Point()
            start.x = 0.0
            start.y = 0.0
            start.z = 0.0
            end = Point()
            end.x = 1.0
            end.y = 1.0
            end.z = z
            marker.points = [start, end]
            markerarray.markers.append(marker)
        self.publisher.publish(markerarray)


def main(args=None):
    rclpy.init(args=args)
    node = camera_vector() 
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()