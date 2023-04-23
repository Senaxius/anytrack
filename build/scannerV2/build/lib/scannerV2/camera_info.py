import rclpy
from rclpy.node import Node
import yaml
import os
import time

from sensor_msgs.msg import CameraInfo

class camera_info(Node):
    def __init__(self):
        super().__init__("camera_info") 

        # declare Parameters
        self.declare_parameter("index", -1)
        self.declare_parameter("device", -1)

        # import parameters
        self.index = self.get_parameter("index").value
        self.device = self.get_parameter("device").value

        # debug only
        # self.index = 0
        # self.device = 0

        # check if Parameters is set
        if (self.device == -1 or self.index == -1):
            self.get_logger().warning("no index was set")
            exit()

        self.get_logger().info("Starting camera_info publisher with index " + str(self.index) + " on device: video" + str(self.device))

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
        self.msg = self.convert_yaml_to_msg(self.data)

        # create publisher
        self.camera_info_publisher_ = self.create_publisher(msg_type=CameraInfo, topic="camera_info", qos_profile=10)

        while(1):
            self.camera_info_publisher_.publish(self.msg)
            time.sleep(0.5)


    def read_yaml(self, filename):
        with open(filename, "r") as file_handle:
            return yaml.load(file_handle, Loader=yaml.FullLoader)

    def convert_yaml_to_msg(self, data):
        msg = CameraInfo()
        msg.width = data["image_width"]
        msg.height = data["image_height"]
        # msg.k = data["camera_matrix"]["data"]
        # msg.d = data["distortion_coefficients"]["data"]
        msg.r = data["rectification_matrix"]["data"]
        msg.p = data["projection_matrix"]["data"]
        # msg.distortion_model = data["distortion_model"]
        ################ TODO: adaptive frame id
        msg.header.frame_id = ('cam' +  str(self.index) + '_position')
        return msg

def main(args=None):
    rclpy.init(args=args)
    node = camera_info()  
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()