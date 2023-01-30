import rclpy
from rclpy.node import Node
import yaml
import os
import time

from sensor_msgs.msg import CameraInfo


class Camera_info(Node):
    def __init__(self):
        super().__init__("Camera_info") 

        self.declare_parameter("index", -1)
        self.index = self.get_parameter("index").value
        
        # debug only
        # self.index = 2

        # check if Parameters is set
        if (self.index == -1):
            self.get_logger().warning("no device index was set")
            exit()
        # read Value of Parameter
        # self.get_logger().info("Starting camera tracker on device: video" + str(self.index))
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
    node = Camera_info()  
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()