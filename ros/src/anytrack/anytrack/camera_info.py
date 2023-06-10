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
        self.declare_parameter("config", '')
        self.declare_parameter("width", 1280)
        self.declare_parameter("height", 720)

        # import parameters
        self.index = self.get_parameter("index").value
        self.device = self.get_parameter("device").value
        self.file = self.get_parameter("config").value
        self.width = self.get_parameter("width").value
        self.height = self.get_parameter("height").value

        # debug only
        # self.index = 0
        # self.device = 0

        # check if Parameters is set
        if (self.device == -1 or self.index == -1):
            self.get_logger().warning("no index was set")
            exit()

        self.get_logger().info("Starting camera_info publisher with index " + str(self.index) + " on device: video" + str(self.device))

        # create msg from .yaml file
        self.data = self.read_yaml(self.file)
        self.msg = self.convert_yaml_to_msg(self.data)

        # create publisher
        self.camera_info_publisher_ = self.create_publisher(msg_type=CameraInfo, topic="/cam" + str(self.index) + "/camera_info", qos_profile=10)

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
        msg.k = data["camera_matrix"]["data"]
        msg.d = data["distortion_coefficients"]["data"]
        msg.r = data["rectification_matrix"]["data"]
        msg.p = data["projection_matrix"]["data"]
        # Convert for change in resolution
        msg.k[0] *= (self.width / msg.width)
        msg.k[2] *= (self.width / msg.width)
        msg.k[4] *= (self.height / msg.height)
        msg.k[5] *= (self.height / msg.height)

        msg.p[0] *= (self.width / msg.width)
        msg.p[2] *= (self.width / msg.width)
        msg.p[5] *= (self.height / msg.height)
        msg.p[6] *= (self.height / msg.height)

        msg.width = self.width
        msg.height = self.height
        # for index, param in enumerate(msg.k):
        #     msg.k[index] = param * (self.width / msg.width)
        # for index, param in enumerate(msg.p):
        #     msg.p[index] = param * (self.width / msg.width)

        msg.distortion_model = data["distortion_model"]
        msg.header.frame_id = ('cam' +  str(self.index) + '_position')
        return msg

def main(args=None):
    rclpy.init(args=args)
    node = camera_info()  
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
